import asyncio
import logging
from typing import Any, Dict, List, Optional, Union, Callable
from llama_index.core.workflow import (
    Workflow,
    StartEvent,
    StopEvent,
    Event,
    Context,
    step
)
from llama_index.utils.workflow import draw_all_possible_flows, draw_most_recent_execution
from llama_index.core.workflow.retry_policy import RetryPolicy, ConstantDelayRetryPolicy
from llama_deploy import (
    deploy_core,
    deploy_workflow,
    ControlPlaneConfig,
    SimpleMessageQueueConfig,
    WorkflowServiceConfig,
    LlamaDeployClient
)
from llama_agents import (
    AgentService,
    ControlPlaneServer,
    SimpleMessageQueue,
    AgentOrchestrator,
    PipelineOrchestrator,
    ServiceComponent,
    LocalLauncher,
    ServerLauncher,
    CallableMessageConsumer
)
from llama_index.core.agent import FunctionCallingAgentWorker, FnAgentWorker
from llama_index.core.tools import FunctionTool
from llama_index.core import VectorStoreIndex, Document, PromptTemplate
from llama_index.core.query_pipeline import QueryPipeline
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.llms.openai import OpenAI

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkflowUtil:
    @staticmethod
    def create_event(event_type: type, **kwargs) -> Event:
        """Create a custom event with the given type and attributes."""
        return event_type(**kwargs)

    @staticmethod
    async def run_workflow(workflow: Workflow, timeout: int = 60, verbose: bool = False, **kwargs) -> Any:
        """Run a workflow with the given input parameters."""
        return await workflow.run(timeout=timeout, verbose=verbose, **kwargs)

    @staticmethod
    def visualize_workflow(workflow: Union[Workflow, type], filename: str, recent_execution: bool = False) -> None:
        """Visualize a workflow, either all possible flows or the most recent execution."""
        if recent_execution:
            if not isinstance(workflow, Workflow):
                raise ValueError("Recent execution visualization requires a Workflow instance, not a class.")
            draw_most_recent_execution(workflow, filename=filename)
        else:
            draw_all_possible_flows(workflow, filename=filename)

    @staticmethod
    def create_step(retry_policy: Optional[RetryPolicy] = None, num_workers: int = 1) -> Callable:
        """Decorator to create a step in a workflow, optionally with a retry policy and number of workers."""
        return step(retry_policy=retry_policy, num_workers=num_workers)

    @staticmethod
    async def get_context_value(ctx: Context, key: str, default: Any = None) -> Any:
        """Get a value from the workflow context."""
        return await ctx.get(key, default)

    @staticmethod
    async def set_context_value(ctx: Context, key: str, value: Any) -> None:
        """Set a value in the workflow context."""
        await ctx.set(key, value)

    @staticmethod
    def collect_events(ctx: Context, current_event: Event, expected_events: List[type]) -> Optional[List[Event]]:
        """Collect multiple events in a workflow step."""
        return ctx.collect_events(current_event, expected_events)

    @staticmethod
    def send_event(ctx: Context, event: Event) -> None:
        """Send an event in a workflow step."""
        ctx.send_event(event)

    @staticmethod
    def write_to_stream(ctx: Context, event: Event) -> None:
        """Write an event to the workflow's event stream."""
        ctx.write_event_to_stream(event)

    @staticmethod
    async def stream_workflow_events(workflow: Workflow, **kwargs) -> Any:
        """Stream events from a workflow execution and return the final result."""
        handler = workflow.run(**kwargs)
        async for event in handler.stream_events():
            yield event
        result = await handler
        return result

    @staticmethod
    def add_nested_workflow(parent_workflow: Workflow, nested_workflow: Workflow, name: str) -> None:
        """Add a nested workflow to a parent workflow."""
        parent_workflow.add_workflows(**{name: nested_workflow})

    @staticmethod
    def create_workflow_with_retry(workflow: Workflow, retry_policy: RetryPolicy) -> Workflow:
        """Create a workflow with a retry policy for all steps."""
        for step_name, step_func in workflow.__class__.__dict__.items():
            if hasattr(step_func, '__workflow_step__'):
                setattr(workflow.__class__, step_name, step(retry_policy=retry_policy)(step_func))
        return workflow

    @staticmethod
    async def run_workflow_stepwise(workflow: Workflow, **kwargs) -> Any:
        """Run a workflow step by step, allowing for inspection between steps."""
        handler = workflow.run(**kwargs)
        while not handler.is_done():
            ev = await handler.run_step()
            yield ev
            handler.ctx.send_event(ev)
        return handler.result()

    @staticmethod
    async def human_in_the_loop_workflow(workflow: Workflow, input_handler: Callable[[str], str], **kwargs) -> Any:
        """Run a workflow with human-in-the-loop interaction."""
        handler = workflow.run(**kwargs)
        async for event in handler.stream_events():
            if isinstance(event, Event) and hasattr(event, 'prefix'):
                response = input_handler(event.prefix)
                handler.ctx.send_event(Event(response=response))
            else:
                yield event
        return await handler

# Custom Events
class EvenEvent(Event):
    value: int

class OddEvent(Event):
    value: int

class InputRequiredEvent(Event):
    prefix: str

class HumanResponseEvent(Event):
    response: str

# Example Workflows
class SimpleWorkflow(Workflow):
    @WorkflowUtil.create_step()
    async def start(self, ctx: Context, ev: StartEvent) -> StopEvent:
        await WorkflowUtil.set_context_value(ctx, "key", "value")
        return StopEvent(result="Simple workflow completed")

class BranchingWorkflow(Workflow):
    @WorkflowUtil.create_step()
    async def start(self, ctx: Context, ev: StartEvent) -> Union[EvenEvent, OddEvent]:
        if ev.input % 2 == 0:
            return WorkflowUtil.create_event(EvenEvent, value=ev.input)
        else:
            return WorkflowUtil.create_event(OddEvent, value=ev.input)

    @WorkflowUtil.create_step()
    async def handle_even(self, ctx: Context, ev: EvenEvent) -> StopEvent:
        return StopEvent(result=f"Even number: {ev.value}")

    @WorkflowUtil.create_step()
    async def handle_odd(self, ctx: Context, ev: OddEvent) -> StopEvent:
        return StopEvent(result=f"Odd number: {ev.value}")

class HumanInTheLoopWorkflow(Workflow):
    @WorkflowUtil.create_step()
    async def start(self, ctx: Context, ev: StartEvent) -> InputRequiredEvent:
        return InputRequiredEvent(prefix="Enter a number: ")

    @WorkflowUtil.create_step()
    async def process_input(self, ctx: Context, ev: HumanResponseEvent) -> StopEvent:
        try:
            number = int(ev.response)
            return StopEvent(result=f"You entered: {number}")
        except ValueError:
            return StopEvent(result="Invalid input. Please enter a number.")

class ConcurrentWorkflow(Workflow):
    @WorkflowUtil.create_step()
    async def start(self, ctx: Context, ev: StartEvent) -> Union[EvenEvent, OddEvent]:
        WorkflowUtil.send_event(ctx, EvenEvent(value=2))
        WorkflowUtil.send_event(ctx, OddEvent(value=3))
        return StopEvent(result="Concurrent events sent")

    @WorkflowUtil.create_step(num_workers=2)
    async def process_events(self, ctx: Context, ev: Union[EvenEvent, OddEvent]) -> Event:
        await asyncio.sleep(1)  # Simulate some work
        return Event(result=f"Processed {ev.__class__.__name__}")

    @WorkflowUtil.create_step()
    async def collect_results(self, ctx: Context, ev: Event) -> StopEvent:
        results = WorkflowUtil.collect_events(ctx, ev, [Event, Event])
        if results is None:
            return None
        return StopEvent(result=f"Collected results: {[r.result for r in results]}")

class StatefulWorkflow(Workflow):
    @WorkflowUtil.create_step()
    async def increment_counter(self, ctx: Context, ev: StartEvent) -> StopEvent:
        counter = await WorkflowUtil.get_context_value(ctx, "counter", 0)
        counter += 1
        await WorkflowUtil.set_context_value(ctx, "counter", counter)
        return StopEvent(result=f"Counter: {counter}")

class ErrorHandlingWorkflow(Workflow):
    @WorkflowUtil.create_step()
    async def risky_step(self, ctx: Context, ev: StartEvent) -> StopEvent:
        if ev.input == "error":
            raise ValueError("Simulated error")
        return StopEvent(result="Success")

class LoopingWorkflow(Workflow):
    @WorkflowUtil.create_step()
    async def start(self, ctx: Context, ev: StartEvent) -> Union[Event, StopEvent]:
        count = await WorkflowUtil.get_context_value(ctx, "count", 0)
        if count < 3:
            await WorkflowUtil.set_context_value(ctx, "count", count + 1)
            return Event(message=f"Iteration {count + 1}")
        return StopEvent(result="Looping completed")

    @WorkflowUtil.create_step()
    async def process(self, ctx: Context, ev: Event) -> Union[Event, StopEvent]:
        print(ev.message)
        return await self.start(ctx, StartEvent())

class DefaultNestedWorkflow(Workflow):
    @WorkflowUtil.create_step()
    async def default_step(self, ctx: Context, ev: StartEvent) -> StopEvent:
        return StopEvent(result="Default nested workflow")

class OuterWorkflow(Workflow):
    def __init__(self):
        super().__init__()
        self.add_workflows(nested=DefaultNestedWorkflow())

    @WorkflowUtil.create_step()
    async def start(self, ctx: Context, ev: StartEvent, nested: Workflow) -> StopEvent:
        result = await nested.run()
        return StopEvent(result=f"Outer workflow with nested result: {result}")

class StreamingWorkflow(Workflow):
    @WorkflowUtil.create_step()
    async def start(self, ctx: Context, ev: StartEvent) -> StopEvent:
        for i in range(5):
            WorkflowUtil.write_to_stream(ctx, Event(message=f"Progress: {i*20}%"))
            await asyncio.sleep(0.5)  # Simulate some work
        return StopEvent(result="Streaming completed")

class DeployableWorkflow(Workflow):
    @step
    async def start(self, ctx: Context, ev: StartEvent) -> StopEvent:
        # Simulate some work
        await asyncio.sleep(1)
        return StopEvent(result="Deployable workflow completed")

class CustomOrchestrator:
    async def process_event(self, workflow: Workflow, event: Event) -> Event:
        # Custom logic for event processing
        logger.info(f"Custom orchestrator processing: {event}")
        return await workflow.process_event(event)

def setup_llama_agents():
    logging.getLogger("llama_agents").setLevel(logging.INFO)

    # Set up the message queue and control plane
    message_queue = SimpleMessageQueue()
    control_plane = ControlPlaneServer(
        message_queue=message_queue,
        orchestrator=AgentOrchestrator(llm=OpenAI()),
    )

    # Create a tool
    def get_the_secret_fact() -> str:
        """Returns the secret fact."""
        return "The secret fact is: A baby llama is called a 'Cria'."

    tool = FunctionTool.from_defaults(fn=get_the_secret_fact)

    # Define agents
    worker1 = FunctionCallingAgentWorker.from_tools([tool], llm=OpenAI())
    worker2 = FunctionCallingAgentWorker.from_tools([], llm=OpenAI())
    agent1 = worker1.as_agent()
    agent2 = worker2.as_agent()

    # Create agent services
    agent_service1 = AgentService(
        agent=agent1,
        message_queue=message_queue,
        description="Useful for getting the secret fact.",
        service_name="secret_fact_agent",
        host="localhost",
        port=8003
    )
    agent_service2 = AgentService(
        agent=agent2,
        message_queue=message_queue,
        description="Useful for getting random dumb facts.",
        service_name="dumb_fact_agent",
        host="localhost",
        port=8004
    )

    return control_plane, message_queue, agent_service1, agent_service2

def setup_query_rewriting_rag():
    # Load and index your document
    docs = [Document(text="The rabbit is a small mammal with long ears and a fluffy tail. His name is Peter.")]
    index = VectorStoreIndex.from_documents(docs)

    # Define a query rewrite agent
    HYDE_PROMPT_STR = (
        "Please rewrite the following query to include more detail:\n{query_str}\n"
    )
    HYDE_PROMPT_TMPL = PromptTemplate(HYDE_PROMPT_STR)

    def run_hyde_fn(state):
        prompt_tmpl, llm, input_str = (
            state["prompt_tmpl"],
            state["llm"],
            state["__task__"].input,
        )
        qp = QueryPipeline(chain=[prompt_tmpl, llm])
        output = qp.run(query_str=input_str)
        state["__output__"] = str(output)
        return state, True

    hyde_agent = FnAgentWorker(
        fn=run_hyde_fn,
        initial_state={"prompt_tmpl": HYDE_PROMPT_TMPL, "llm": OpenAI()}
    ).as_agent()

    # Define a RAG agent
    def run_rag_fn(state):
        retriever, llm, input_str = (
            state["retriever"],
            state["llm"],
            state["__task__"].input,
        )
        query_engine = RetrieverQueryEngine.from_args(retriever, llm=llm)
        response = query_engine.query(input_str)
        state["__output__"] = str(response)
        return state, True

    rag_agent = FnAgentWorker(
        fn=run_rag_fn,
        initial_state={"retriever": index.as_retriever(), "llm": OpenAI()}
    ).as_agent()

    message_queue = SimpleMessageQueue()

    query_rewrite_service = AgentService(
        agent=hyde_agent,
        message_queue=message_queue,
        description="Query rewriting service",
        service_name="query_rewrite",
    )

    rag_service = AgentService(
        agent=rag_agent,
        message_queue=message_queue,
        description="RAG service",
        service_name="rag",
    )

    # Create the pipeline
    pipeline = QueryPipeline(chain=[
        ServiceComponent.from_service_definition(query_rewrite_service),
        ServiceComponent.from_service_definition(rag_service),
    ])
    orchestrator = PipelineOrchestrator(pipeline)

    control_plane = ControlPlaneServer(
        message_queue=message_queue,
        orchestrator=orchestrator,
    )

    return control_plane, message_queue, query_rewrite_service, rag_service

async def deploy_example():
    # Deploy core services
    await deploy_core(
        control_plane_config=ControlPlaneConfig(),
        message_queue_config=SimpleMessageQueueConfig(),
    )

    # Deploy the workflow
    await deploy_workflow(
        workflow=DeployableWorkflow(),
        workflow_config=WorkflowServiceConfig(
            host="127.0.0.1", port=8002, service_name="deployable_workflow"
        ),
        control_plane_config=ControlPlaneConfig(),
    )

    # Interact with the deployed workflow
    client = LlamaDeployClient(ControlPlaneConfig())
    session = client.create_session()
    result = session.run("deployable_workflow")
    logger.info(f"Deployed workflow result: {result}")

    # Stream results from the deployed workflow
    task_id = session.run_nowait("deployable_workflow")
    for event in session.get_task_result_stream(task_id):
        logger.info(f"Streamed event: {event}")
    
    final_result = session.get_task_result(task_id)
    logger.info(f"Final result: {final_result}")

async def main():
    # 1. Simple workflow execution
    simple_workflow = SimpleWorkflow()
    result = await WorkflowUtil.run_workflow(simple_workflow)
    logger.info(f"Simple workflow result: {result}")

    # 2. Branching workflow execution
    branching_workflow = BranchingWorkflow()
    even_result = await WorkflowUtil.run_workflow(branching_workflow, input=2)
    odd_result = await WorkflowUtil.run_workflow(branching_workflow, input=3)
    logger.info(f"Branching workflow (even) result: {even_result}")
    logger.info(f"Branching workflow (odd) result: {odd_result}")

    # 3. Workflow visualization
    WorkflowUtil.visualize_workflow(BranchingWorkflow, "branching_workflow.html")
    WorkflowUtil.visualize_workflow(branching_workflow, "branching_workflow_recent.html", recent_execution=True)

    # 4. Streaming workflow events
    async for event in WorkflowUtil.stream_workflow_events(simple_workflow):
        logger.info(f"Streamed event: {event}")

    # 5. Stepwise workflow execution
    async for step_event in WorkflowUtil.run_workflow_stepwise(branching_workflow, input=4):
        logger.info(f"Step completed: {step_event}")

    # 6. Workflow with retry policy
    retry_policy = ConstantDelayRetryPolicy(delay=1, maximum_attempts=3)
    workflow_with_retry = WorkflowUtil.create_workflow_with_retry(SimpleWorkflow(), retry_policy)
    retry_result = await WorkflowUtil.run_workflow(workflow_with_retry)
    logger.info(f"Workflow with retry result: {retry_result}")

    # 7. Human-in-the-loop workflow
    def input_handler(prompt: str) -> str:
        return input(prompt)

    human_workflow = HumanInTheLoopWorkflow()
    human_result = await WorkflowUtil.human_in_the_loop_workflow(human_workflow, input_handler)
    logger.info(f"Human-in-the-loop workflow result: {human_result}")

    # 8. Nested workflows
    outer_workflow = OuterWorkflow()
    nested_result = await WorkflowUtil.run_workflow(outer_workflow)
    logger.info(f"Nested workflow result: {nested_result}")

    # 9. Concurrent workflow execution
    concurrent_workflow = ConcurrentWorkflow()
    concurrent_result = await WorkflowUtil.run_workflow(concurrent_workflow)
    logger.info(f"Concurrent workflow result: {concurrent_result}")

    # 10. Stateful workflow across multiple runs
    stateful_workflow = StatefulWorkflow()
    context = Context()
    for _ in range(3):
        result = await WorkflowUtil.run_workflow(stateful_workflow, ctx=context)
        logger.info(f"Stateful workflow result: {result}")

    # 11. Error handling workflow
    error_workflow = ErrorHandlingWorkflow()
    try:
        await WorkflowUtil.run_workflow(error_workflow, input="error")
    except ValueError as e:
        logger.error(f"Caught error: {str(e)}")

    # 12. Custom orchestrator
    custom_orchestrator = CustomOrchestrator()
    workflow = SimpleWorkflow()
    event = StartEvent()
    result = await custom_orchestrator.process_event(workflow, event)
    logger.info(f"Custom orchestrator result: {result}")

    # 13. Looping workflow
    looping_workflow = LoopingWorkflow()
    looping_result = await WorkflowUtil.run_workflow(looping_workflow)
    logger.info(f"Looping workflow result: {looping_result}")

    # 14. Streaming workflow
    streaming_workflow = StreamingWorkflow()
    streaming_result = await WorkflowUtil.run_workflow(streaming_workflow)
    logger.info(f"Streaming workflow result: {streaming_result}")

    # 15. llama-agents example
    logger.info("Running llama-agents example...")
    control_plane, message_queue, agent_service1, agent_service2 = setup_llama_agents()
    
    # Local testing
    local_launcher = LocalLauncher(
        [agent_service1, agent_service2],
        control_plane,
        message_queue,
    )
    result = local_launcher.launch_single("What's the secret fact?")
    logger.info(f"Local llama-agents result: {result}")

    # Server deployment simulation
    def handle_result(message) -> None:
        logger.info(f"Got result: {message.data}")

    human_consumer = CallableMessageConsumer(
        handler=handle_result, message_type="human"
    )

    server_launcher = ServerLauncher(
        [agent_service1, agent_service2],
        control_plane,
        message_queue,
        additional_consumers=[human_consumer]
    )

    logger.info("Server deployment setup complete. In a real scenario, you would keep this running.")

    # 16. Query Rewriting RAG example
    logger.info("Running Query Rewriting RAG example...")
    rag_control_plane, rag_message_queue, query_rewrite_service, rag_service = setup_query_rewriting_rag()
    
    rag_launcher = LocalLauncher(
        [query_rewrite_service, rag_service],
        rag_control_plane,
        rag_message_queue,
    )

    rag_result = rag_launcher.launch_single("Tell me about rabbits")
    logger.info(f"Query Rewriting RAG result: {rag_result}")

    # 17. llama_deploy example
    logger.info("Running llama_deploy example...")
    await deploy_example()

if __name__ == '__main__':
    asyncio.run(main())
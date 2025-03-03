import packages

from context.utils import typer as t

from toolkit.utils import utils
from toolkit.utils.utils import rp_print

from context.infra import clients
import context.instances as inst
import context.consts as const
import context.settings.main as settings_main

from toolkit.llm.langchain.core import integration, utils as utils_lc
from toolkit.llm.langchain.data.persistence import retrievers
from toolkit.llm.langchain.data.indexing import (
  documents, document_loaders, text_splitters,
)
from toolkit.llm.langchain.execution import (
  runnables, graphs, tools as tools_lc, agents
)
from toolkit.llm.langchain.models import (
	prompts as prompts_lc, llms, messages as msgs_lc
)
from typing import Literal, List, Dict, Any, Optional, TypeVar, Generic
from typing_extensions import Literal, TypedDict
from dataclasses import dataclass
from enum import Enum
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from langchain_core.messages import (
    HumanMessage, 
    AIMessage,
    SystemMessage,
    ToolMessage,
    BaseMessage
)
from langchain_core.tools import tool
from langgraph.graph import MessagesState, StateGraph, START, END
from langgraph.types import Command

# Initialize rich console
console = Console()

# Use the provided model
model = inst.llm_main

# ============= Core Types =============
class AgentRole(str, Enum):
    WORKER = "worker"
    SUPERVISOR = "supervisor"

@dataclass
class AgentConfig:
    agent_id: str
    role: AgentRole
    system_prompt: str
    allowed_tools: List[Any]
    allowed_handoffs: List[str]

class State(MessagesState):
    """Base state class with context tracking"""
    context: Dict[str, Any]

T = TypeVar('T', bound=State)

# ============= Calculator Tools =============
@tool
def add(a: float, b: float) -> float:
    """Adds two numbers."""
    result = a + b
    console.print(Panel(
        f"add({a}, {b}) = {result}",
        title="[#4B9EF0]Tool Execution[/#4B9EF0]",
        border_style="#4B9EF0"
    ))
    return result

@tool
def multiply(a: float, b: float) -> float:
    """Multiplies two numbers."""
    result = a * b
    console.print(Panel(
        f"multiply({a}, {b}) = {result}",
        title="[#4B9EF0]Tool Execution[/#4B9EF0]",
        border_style="#4B9EF0"
    ))
    return result

@tool
def transfer_to_multiplication_expert():
    """Transfer to multiplication expert."""
    console.print(Panel(
        "Transferring to multiplication expert",
        title="[#F0A732]Transfer[/#F0A732]",
        border_style="#F0A732"
    ))
    return

@tool
def transfer_to_addition_expert():
    """Transfer to addition expert."""
    console.print(Panel(
        "Transferring to addition expert",
        title="[#F0A732]Transfer[/#F0A732]",
        border_style="#F0A732"
    ))
    return

# ============= Base Classes =============
class BaseAgent:
    """Base class for all agents"""
    def __init__(self, config: AgentConfig):
        self.config = config

    def process_tools(self, response: AIMessage, state: State) -> tuple[State, Optional[str]]:
        """Process tool usage and determine next agent"""
        updated_state = state.copy()
        updated_state["messages"] = state["messages"] + [response]
        next_agent = None

        if hasattr(response, 'tool_calls') and response.tool_calls:
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                
                # Handle transfers
                if tool_name.startswith("transfer_to_"):
                    target_agent = tool_name.replace("transfer_to_", "")
                    if target_agent in self.config.allowed_handoffs:
                        next_agent = target_agent
                        return updated_state, next_agent

                # Handle regular tools
                for tool in self.config.allowed_tools:
                    if tool.name == tool_name:
                        try:
                            result = tool.invoke(tool_call)
                            tool_msg = ToolMessage(
                                content=str(result),
                                tool_call_id=tool_call["id"],
                                name=tool_name
                            )
                            updated_state["messages"].append(tool_msg)
                        except Exception as e:
                            tool_msg = ToolMessage(
                                content=f"Error: {str(e)}",
                                tool_call_id=tool_call["id"]
                            )
                            updated_state["messages"].append(tool_msg)
                            console.print(f"[#FF6B6B]Tool Error:[/#FF6B6B] {str(e)}")

        return updated_state, next_agent

    def __call__(self, state: State) -> Command[Dict[str, Any]]:
        """Process state and determine next action"""
        try:
            messages = [
                SystemMessage(content=self.config.system_prompt)
            ] + state["messages"]

            response = model.bind_tools(
                self.config.allowed_tools
            ).invoke(messages)
            
            console.print(Panel(
                response.content,
                title=f"[#4CAF50]{self.config.agent_id}[/#4CAF50]",
                border_style="#4CAF50"
            ))

            updated_state, next_agent = self.process_tools(response, state)
            
            if next_agent:
                return Command(goto=next_agent, update=updated_state)
            
            if "FINAL ANSWER:" in response.content:
                return Command(goto="__end__", update=updated_state)
            
            return Command(goto="supervisor", update=updated_state)

        except Exception as e:
            console.print(f"[#FF6B6B]Agent Error:[/#FF6B6B] {str(e)}")
            error_state = state.copy()
            error_state["messages"] = state["messages"] + [
                AIMessage(content=f"Error: {str(e)}")
            ]
            return Command(goto="__end__", update=error_state)

class BaseTeam(Generic[T]):
    """Base class for all agent teams"""
    def __init__(
        self,
        team_id: str,
        agents: List[BaseAgent],
        supervisor_prompt: str,
        state_class: type[T] = State
    ):
        self.team_id = team_id
        self.agents = {agent.config.agent_id: agent for agent in agents}
        self.supervisor_prompt = supervisor_prompt
        self.state_class = state_class
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Build the agent interaction graph"""
        builder = StateGraph(self.state_class)
        for agent_id, agent in self.agents.items():
            builder.add_node(agent_id, agent)
        builder.add_node("supervisor", self._create_supervisor())
        builder.add_edge(START, "supervisor")
        return builder.compile()

    def _create_supervisor(self):
        """Create supervisor node"""
        def supervisor_node(state: T) -> Command[Dict[str, Any]]:
            system_msg = SystemMessage(content=self.supervisor_prompt)
            messages = [system_msg] + state["messages"]
            
            response = model.invoke(messages)
            console.print(Panel(
                response.content,
                title="[#E040FB]Supervisor Decision[/#E040FB]",
                border_style="#E040FB"
            ))
            
            next_agent = self._determine_next_agent(response)
            if next_agent == "__end__":
                return Command(goto="__end__", update={
                    "messages": state["messages"] + [response]
                })
                
            return Command(goto=next_agent, update={
                "messages": state["messages"] + [response]
            })
        
        return supervisor_node

    def _determine_next_agent(self, response: AIMessage) -> str:
        """Determine next agent - override in subclasses"""
        raise NotImplementedError("Subclasses must implement _determine_next_agent")

    def process(self, input_data: str) -> Dict[str, Any]:
        """Process input through the team"""
        console.print(Panel(
            input_data,
            title=f"[#00BCD4]{self.team_id} Input[/#00BCD4]",
            border_style="#00BCD4"
        ))
        state = self.state_class(
            messages=[HumanMessage(content=input_data)],
            context={}
        )
        return self.graph.invoke(state)

# ============= Calculator Implementation =============
class CalculatorTeam(BaseTeam[State]):
    """Team of calculator agents"""
    def _determine_next_agent(self, response: AIMessage) -> str:
        """Route based on operation needed"""
        content = response.content.lower()
        
        if "FINAL ANSWER:" in response.content:
            return "__end__"
            
        if any(phrase in content for phrase in [
            "need to multiply",
            "multiplication needed",
            "multiply these",
            "*", "times"
        ]):
            return "multiplication_expert"
            
        if any(phrase in content for phrase in [
            "need to add",
            "addition needed",
            "add these",
            "+"
        ]):
            return "addition_expert"
            
        return "__end__"

def create_calculator_team() -> CalculatorTeam:
    """Create calculator team instance"""
    add_agent = BaseAgent(
        config=AgentConfig(
            agent_id="addition_expert",
            role=AgentRole.WORKER,
            system_prompt=(
                "You are an addition expert. Your job is to:\n"
                "1. Look for numbers that need to be added\n"
                "2. Use the add tool to perform addition\n"
                "3. If multiplication is needed, transfer to multiplication_expert\n"
                "4. Show all work and intermediate steps\n"
                "5. When the final result is ready, say 'FINAL ANSWER: [result]'\n\n"
                "Remember: Only handle addition. Always transfer multiplication tasks."
            ),
            allowed_tools=[add, transfer_to_multiplication_expert],
            allowed_handoffs=["multiplication_expert"]
        )
    )

    mult_agent = BaseAgent(
        config=AgentConfig(
            agent_id="multiplication_expert",
            role=AgentRole.WORKER,
            system_prompt=(
                "You are a multiplication expert. Your job is to:\n"
                "1. Look for numbers that need to be multiplied\n"
                "2. Use the multiply tool to perform multiplication\n"
                "3. If addition is needed, transfer to addition_expert\n"
                "4. Show all work and intermediate steps\n"
                "5. When the final result is ready, say 'FINAL ANSWER: [result]'\n\n"
                "Remember: Only handle multiplication. Always transfer addition tasks."
            ),
            allowed_tools=[multiply, transfer_to_addition_expert],
            allowed_handoffs=["addition_expert"]
        )
    )

    return CalculatorTeam(
        team_id="calculator",
        agents=[add_agent, mult_agent],
        supervisor_prompt=(
            "You are a math supervisor. Your job is to:\n"
            "1. Analyze the expression and identify needed operations\n"
            "2. Route addition tasks to addition_expert\n"
            "3. Route multiplication tasks to multiplication_expert\n"
            "4. For complex expressions, follow order of operations\n"
            "5. Only identify the next operation - do NOT calculate\n\n"
            "Remember: Your job is to ROUTE tasks, not solve them."
        )
    )

def main():
    calculator = create_calculator_team()
    expression = "What is (17 + 23) * (14 + 16)?"
    
    try:
        result = calculator.process(expression)
        final_msg = result["messages"][-1].content
        if "FINAL ANSWER:" in final_msg:
            answer = final_msg.split("FINAL ANSWER:")[-1].strip()
            console.print(Panel(
                f"[#4CAF50]{answer}[/#4CAF50]",
                title="[#4CAF50]Final Answer[/#4CAF50]",
                border_style="#4CAF50"
            ))
        else:
            console.print("[#FF6B6B]No final answer found in response[/#FF6B6B]")
            
    except Exception as e:
        console.print(f"[#FF6B6B]Error:[/#FF6B6B] {str(e)}")

if __name__ == "__main__":
    main()
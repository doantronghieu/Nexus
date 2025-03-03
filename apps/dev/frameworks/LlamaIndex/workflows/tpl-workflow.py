import packages
# from configs import settings
import asyncio, os, time, yaml, json, datetime, copy
from toolkit.llm.llama_index import (
  cores, workflows as wfs, deploys as dpls
)

from use_cases.dev.frameworks.LlamaIndex.deploys.core import control_plane_config

class EventProgress(wfs.Event):
  progress: str

class WorkflowEcho(wfs.Workflow):
  """A dummy workflow with only one step sending back the input given."""
  
  @wfs.step()
  async def run_step(
    self, ctx: wfs.Context, ev: wfs.StartEvent,
  ) -> wfs.StopEvent:
    message = str(ev.get("message", ""))
    
    ctx.write_event_to_stream(
      EventProgress(progress="I am doing something!")
    )
    
    return wfs.StopEvent(result=f"Message received: {message}")

class WorkflowInner(wfs.Workflow):
  @wfs.step()
  async def run_step(
    self, ctx: wfs.Context, ev: wfs.StartEvent,
  ) -> wfs.StopEvent:
    message = str(ev.get("message", ""))
    
    ctx.write_event_to_stream(
      EventProgress(progress="I am doing something!")
    )
    return wfs.StopEvent(result=f"Message received: {message}")
    
class WorkflowOuter(wfs.Workflow):
  @wfs.step()
  async def run_step(
    self, ctx: wfs.Context, ev: wfs.StartEvent, wf_inner: wfs.Workflow,
  ) -> wfs.StopEvent:
    message = str(ev.get("message", ""))
    
    result_inner = await wf_inner.run(message=message)
    
    return wfs.StopEvent(result=f"{result_inner} - completed!")

wf_inner = WorkflowInner()
wf_outer = WorkflowOuter()
wf_outer.add_workflows(wf_inner=WorkflowInner())

async def main():
  task_inner = asyncio.create_task(
    dpls.deploy_workflow(
      workflow=wf_inner,
      workflow_config = dpls.WorkflowServiceConfig(
        host="127.0.0.1",
        port=os.getenv("PORT_LLAMA_DEPLOY_SVC_TEST"), # type: ignore
        service_name="my_workflow_inner",
      ),
      control_plane_config=control_plane_config
    )
  )
  
  task_outer = asyncio.create_task(
    dpls.deploy_workflow(
      workflow=wf_outer,
      workflow_config = dpls.WorkflowServiceConfig(
        host="127.0.0.1",
        port=os.getenv("PORT_LLAMA_DEPLOY_SVC_TEST") + 1, # type: ignore
        service_name="my_workflow_outer",
      ),
      control_plane_config=control_plane_config
    )
  )
  
  await asyncio.gather(task_inner, task_outer)


# Make this script runnable from the shell so we can test the workflow execution
if __name__ == "__main__":
  asyncio.run(main())

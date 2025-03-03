from toolkit.utils.llm import main as utils_llm
import packages
from configs import settings, const, components
from configs.settings import logger
import asyncio, os, time, yaml, json, datetime, copy, random
from typing import Any, AsyncGenerator, Generator, Callable, Literal, Optional, TypeAlias, Union
from tqdm import tqdm
from pprint import pprint

from toolkit.llm.llama_index import (
	agents, cores, deploys as dpls, evaluation, messages, models, 
	observability, types, utils as utils_llama_index, workflows as wfs
)
from toolkit.llm.llama_index.data import loading, querying, storing

from features.agents.car.tools import VehicleDB

from toolkit.utils import utils, typer as t
from toolkit.utils.llm import measure_performance
from toolkit.utils.utils import rp_print

#*------------------------------------------------------------------------------

from features.rag import apis as apis_rag
from features.agents.car import apis as apis_car

#*==============================================================================
prompts_agent_car = settings.prompts_agent_car

class EvUserQueryCategorized(wfs.Event):
	user_query_category: t.UserQueryCategory
#*------------------------------------------------------------------------------
class EvFlowStartedRag(wfs.Event):
	pass

class EvFlowDoneRag(wfs.Event):
	pass

#*------------------------------------------------------------------------------
class EvFlowStartedControl(wfs.Event):
	pass

# class EvFlCtrlProcessTaskStarted(wfs.Event):
# 	task: str
# 	id: str

# class EvFlCtrlProcessTaskDone(wfs.Event):
# 	result: str
# 	id: str

class EvFlowDoneControl(wfs.Event):
	pass

#*------------------------------------------------------------------------------
class EvFlowDone(wfs.Event):
	pass

#*------------------------------------------------------------------------------
class EvHumanFeedbackDone(wfs.Event):
  human_feedback: dict[str, Any]

class EvHumanSatisfied(wfs.Event):
	pass

#*------------------------------------------------------------------------------
class MyWorkflow(wfs.Workflow):
	@wfs.step()
	async def categorize_user_query(
		self, ctx: wfs.Context, ev: wfs.StartEvent,
	) -> EvUserQueryCategorized:
		user_query = ev.get("user_query", "")

		user_query_category = await apis_car.categorize_user_query(user_query)
		rp_print(user_query_category)
		
		await ctx.set("user_query", user_query)
		await ctx.set("user_query_category", user_query_category)
 
		return EvUserQueryCategorized(user_query_category=user_query_category)
	
	@wfs.step()
	async def start_flow(
		self, ctx: wfs.Context, ev: EvUserQueryCategorized
	) -> EvFlowStartedRag | EvFlowStartedControl:
		user_query_category: t.UserQueryCategory = await ctx.get("user_query_category")
		
		flow_mapping = {
			"car_manual": ("rag", EvFlowStartedRag),
			"car_control": ("control", EvFlowStartedControl)
		}

		if user_query_category in flow_mapping:
			task, event_class = flow_mapping[user_query_category]
			
			flow_info = {
				"activated": True,
				"task": task
			}
			await ctx.set("flow_info", flow_info)
			return event_class()
	
	@wfs.step()
	async def run_flow_rag(
		self, ctx: wfs.Context, ev: EvFlowStartedRag,
	) -> EvFlowDoneRag:
		flow_info = await ctx.get("flow_info")
		user_query = await ctx.get("user_query")

		result = await apis_rag.do_querying(user_query=user_query, mode="achat")

		if flow_info:
			flow_info["completed"] = True
			flow_info["result"] = result
   
		await ctx.set("flow_info", flow_info)

		return EvFlowDoneRag()

	@wfs.step()
	async def run_flow_control(
		self, ctx: wfs.Context, ev: EvFlowStartedControl,
	) -> EvFlowDoneControl:
		flow_info = await ctx.get("flow_info")
		user_query = await ctx.get("user_query")

		# Get tasks
		tasks = await apis_car.separate_tasks(user_query=user_query)
		rp_print(tasks)

		if not tasks:
			if flow_info:
				flow_info["tasks"] = {}
				flow_info["n_tasks"] = 0
				flow_info["result"] = "No tasks were identified in your request."
				await ctx.set("flow_info", flow_info)
			return EvFlowDoneControl()

		# Initialize tasks map with IDs
		task_map = {}
		for task in tasks:
			task_id = str(utils.uuid_utils.generate_uuid4())
			task_map[task_id] = {
				"task": task,
				"result": None
			}

		flow_info["tasks"] = task_map
		flow_info["n_tasks"] = len(tasks)
		await ctx.set("flow_info", flow_info)

		# Process all tasks concurrently
		async def process_task(task_id: str, task: str) -> tuple[str, str]:
			try:
				result = await apis_car.do_controlling(user_query=task, mode="achat")
				return task_id, result
			except Exception as e:
				logger.error(f"Error processing task {task_id}: {str(e)}")
				return task_id, f"Error: {str(e)}"

		# Create and gather all task coroutines
		coroutines = [
			process_task(task_id, task_info["task"]) 
			for task_id, task_info in task_map.items()
		]
		
		# Execute all tasks concurrently
		results = await asyncio.gather(*coroutines)

		# Update flow info with results
		for task_id, result in results:
			flow_info["tasks"][task_id]["result"] = result

		# Combine all results
		result_texts = [
			task_info["result"] 
			for task_info in flow_info["tasks"].values() 
			if task_info["result"]
		]
		
		flow_info["result"] = "\n".join(result_texts)
		await ctx.set("flow_info", flow_info)

		return EvFlowDoneControl()
			
	@wfs.step()
	async def complete_flow(
		self, ctx: wfs.Context, ev: EvFlowDoneRag | EvFlowDoneControl
	) -> EvFlowDone:
		flow_info = await ctx.get("flow_info")

		if flow_info:
			flow_info["confirmed"] = True
		await ctx.set("flow_info", flow_info)
  
		return EvFlowDone()

	@wfs.step()
	async def human_feedback(
		self, ctx: wfs.Context, ev: EvFlowDone,
	) -> EvHumanFeedbackDone:
		human_feedback = {
			"feedback": "OK!",
			"retry": False,
		}

		await ctx.set("human_feedback", human_feedback)
		return EvHumanFeedbackDone(human_feedback=human_feedback)
	
	@wfs.step()
	async def retry(
		self, ctx: wfs.Context, ev: EvHumanFeedbackDone
	) -> EvHumanSatisfied | EvUserQueryCategorized:
		human_feedback = await ctx.get("human_feedback")
  
		if human_feedback["retry"] == True:
			return EvUserQueryCategorized(
				user_query_category=await ctx.get("user_query_category")
			)
		else:
			return EvHumanSatisfied()
 
	@wfs.step()
	async def stop(
		self, ctx: wfs.Context, ev: EvHumanSatisfied,
	) -> wfs.StopEvent:
		
		rp_print(ctx.data)
  
		flow_info: dict = await ctx.get("flow_info")
		
		if flow_info:
			result = flow_info["result"]
		
		return wfs.StopEvent(result=result)

#*==============================================================================

async def run_workflow(user_query: str) -> t.Union[str, t.Any]:
	workflow = MyWorkflow(timeout=60, verbose=True)

	result = await workflow.run(user_query=user_query)

	return result
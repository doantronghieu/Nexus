from toolkit.utils.llm import main as utils_llm
import packages
from configs import settings, const, components
from configs.settings import logger
import asyncio, os, time, yaml, json, datetime, copy
from typing import Any, AsyncGenerator, Generator, Callable, Literal, Optional, TypeAlias, Union
from tqdm import tqdm
from pprint import pprint
from rich import print as rprint

from toolkit.llm.llama_index import (
	agents, cores, deploys as dpls, evaluation, messages, models, 
	observability, types, utils as utils_llama_index, workflows as wfs
)
from toolkit.llm.llama_index.data import loading, querying, storing

from toolkit.utils import utils, typer as t
from toolkit.utils.llm import measure_performance

#*------------------------------------------------------------------------------
from services.weather import (
	main as tool_weather,
)
from features.agents.car.tools import VehicleDB
#*------------------------------------------------------------------------------

async def categorize_user_query(user_query: str):
	prompt_categorize_query = settings.prompts_agent_car["CategorizeQuestion"]["dev"]

	examples = await components.retriever_user_query_category.aretrieve(user_query)
	examples = str(await utils_llama_index.extract_retriever_results(examples))

	user_query_category: t.UserQueryCategory = await utils_llama_index.interact_model(
		prompt=prompt_categorize_query, mode="achat", user_query=user_query,
		examples=examples,
	)
	user_query_category = await utils_llm.post_process_llm_output(
		user_query_category, mode=["remove_quotes", "remove_brackets", "remove_tokens"],
	)

	return user_query_category

async def separate_tasks(user_query: str):
	prompt_separate_tasks = settings.prompts_agent_car["control"]["SeparateTasks"]["dev"]

	tasks = await utils_llama_index.interact_model(
		prompt=prompt_separate_tasks, mode="achat", user_query=user_query,
	)
	tasks = await utils_llm.post_process_llm_output(tasks, mode=["remove_tokens"])
	tasks = await utils_llm.parse_json(tasks)
 
	return tasks

#*==============================================================================

tools_control = agents.add_tools(
	[agents.FunctionTool.from_defaults(async_fn=VehicleDB.db_mongo_vehicle.process_user_query)],
)

agent_control = agents.MyAgent(
	llm=settings.llm_control,
	use_local_model=settings.use_local_model,
	tools=tools_control,
	system_prompt=settings.prompts_agent_car["control"]["System_VehicleDB"]["dev"],
	verbose=True,
	name="Control Agent",
).agent

settings.error_handler_silent.execute(
  lambda: logger.info(f'[Agent] {agent_control.__repr__().split(" ")[0].split(".")[-1]}'),
	error_msg="Error extracting agent name",
)

#*------------------------------------------------------------------------------

async def do_controlling(
  user_query: str, mode: const.TYPE_AGENT_INTERACT="achat",
):
	return await utils_llama_index.interact_agent(
		agent=agent_control,
		user_query=user_query,
		mode=mode,
	)
    
"""
response = agent.stream_chat("What is current fan speed")

for token in response.response_gen:
  print(token, end="", flush=True)

#-------------------------------------------------------------------------------
# Example usage
for token in do_controlling("What is current fan speed"):
    print(token, end="", flush=True)
"""

#*==============================================================================

tools_general = agents.add_tools(
	[agents.FunctionTool.from_defaults(fn=tool_weather.process_weather_query)],
)

agent_general = agents.MyAgent(
	llm=settings.llm_general,
	use_local_model=settings.use_local_model,
	tools=tools_general,
	system_prompt=settings.prompts_agent_car["general"]["System_General"]["dev"],
	verbose=True,
	name="General Agent",
).agent

settings.error_handler_silent.execute(
  lambda: logger.info(f'[Agent] {agent_general.__repr__().split(" ")[0].split(".")[-1]}'),
	error_msg="Error extracting agent name",
)

#*------------------------------------------------------------------------------

async def do_general(
  user_query: str, mode: const.TYPE_AGENT_INTERACT="achat",
):
	return await utils_llama_index.interact_agent(
		agent=agent_general,
		user_query=user_query,
		mode=mode,
	)
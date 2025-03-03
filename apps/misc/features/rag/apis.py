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
from features.agents.tools import map

from toolkit.utils import utils, typer as t
from toolkit.utils.llm import measure_performance
from toolkit.utils.utils import rp_print

#*==============================================================================

prompts_rag = settings.prompts_rag

#*==============================================================================

async def do_querying(
  user_query: str, mode: const.TYPE_MODEL_INTERACT="achat",
) -> Union[Generator, str]:
	retrieved_data = await components.retriever_car_manual.aretrieve(user_query)

	retrieved_data_texts = await utils_llama_index.extract_text(retrieved_data)

	response = await utils_llama_index.interact_model(
		prompt=prompts_rag["generate_result"], system_prompt=prompts_rag["system"]["car_manual"],
		mode=mode, 
		user_question=user_query, retrieved_data=retrieved_data_texts,
	)
	
	# if mode == "chat":
	# 	response = await utils_llm.post_process_llm_output(
  #   	response, mode=["remove_special_characters"],
	# 	)

	return response
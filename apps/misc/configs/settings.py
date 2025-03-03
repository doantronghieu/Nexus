import os, yaml
from loguru import logger
import packages
from configs import const
from toolkit.utils import utils

if not os.environ.get("IN_PROD", None):
  import nest_asyncio # To connect to the same event-loop,
  nest_asyncio.apply() # allows async events to run on notebook
  logger.warning(f"Running in DEVELOPMENT mode")
else:
  logger.warning(f"Running in PRODUCTION mode")

from toolkit.llm.llama_index import cores, models, agents
from toolkit.llm.llama_index.data import loading, storing

# from features.agents.car.tools import VehicleDB

#*==============================================================================

error_handler = utils.LocationAwareErrorHandler()
error_handler_silent = utils.LocationAwareErrorHandler(
    utils.CFGS_LOCATION_AWARE_ERROR_HANDLER["silent"]
)

#*==============================================================================
# Models

cores.Settings.transformations = [
	loading.SentenceSplitter(
		chunk_size=1024, chunk_overlap=100
	)
]

use_local_model = False # <-- True, False
embed_batch_size = 1

chosen_mode = "local" if use_local_model else "api"

chosen = {
	"local": {
		"model": const.Model.Ollama.LLAMA_3_2_3B,
		"embed_model": const.EmbedModel.Ollama.MXBAI_EMBED_LARGE,
		"model_infer_server": const.ModelInferServer.OLLAMA,
		"embed_model_infer_server": const.EmbedModelInferServer.OLLAMA,
		"qdrant_collections": {
			"car_manual": const.QdrantCollection.CAR_MANUAL_HF,
			"user_query_category": const.QdrantCollection.USER_QUERY_CATEGORY_HF,
			"car_info_field_paths": const.QdrantCollection.CAR_INFO_FIELD_PATHS_HF,
		},
	},
	"api": {
		"model": const.Model.OpenAI.GPT_3_5_TURBO,
		"embed_model": const.EmbedModel.OpenAI.TEXT_EMBED_3_SMALL,
		"model_infer_server": const.ModelInferServer.OPENAI,
		"embed_model_infer_server": const.EmbedModelInferServer.OPENAI,
		"qdrant_collections": {
			"car_manual": const.QdrantCollection.CAR_MANUAL_OPENAI,
			"user_query_category": const.QdrantCollection.USER_QUERY_CATEGORY_OPENAI,
			"car_info_field_paths": const.QdrantCollection.CAR_INFO_FIELD_PATHS_OPENAI,
		},
	},
}

chosen_model = chosen[chosen_mode]["model"]
chosen_embed_model = chosen[chosen_mode]["embed_model"]
chosen_model_infer_server = chosen[chosen_mode]["model_infer_server"]
chosen_embed_model_infer_server = chosen[chosen_mode]["embed_model_infer_server"]

chosen_qdrant_collections = chosen[chosen_mode]["qdrant_collections"]

llm_factory = models.MyModel(
	use_local_model=use_local_model,
	model_name=chosen_model,
	model_infer_server=chosen_model_infer_server,
)

embed_model_factory = models.MyEmbedModel(
	use_local_model=use_local_model,
	model_name=chosen_embed_model,
	embed_model_infer_server=chosen_embed_model_infer_server,
	embed_batch_size=embed_batch_size,
)

cores.Settings.llm = llm_factory.get_model()
cores.Settings.embed_model = embed_model_factory.get_embed_model()

llm_control = llm_factory.get_model()
llm_general = llm_factory.get_model()
llm_map = llm_factory.get_model()

llm_json = error_handler_silent.execute(
  lambda: llm_factory.get_model(json_mode=True),
	error_msg="Error creating `llm_json`",
)

mode_debug = False
if mode_debug:
	import logging
	import sys
	logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
	logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

#*------------------------------------------------------------------------------
llm_vllm = error_handler_silent.execute(
  lambda: models.OpenLLM(
		api_base=f'http://localhost:{os.getenv("PORT_SVC_LLM_VLLM")}/v1',
		model="meta-llama/Llama-3.2-1B-Instruct",
		max_tokens=512,
		temperature=0.0,
		additional_kwargs={
			"frequency_penalty": 0.5,
		},
		is_chat_model=True,
		is_function_calling_model=True,
		strict=True,
	),
	error_msg="Error creating `LLM vLLM`",
)
if llm_vllm: logger.info(f"`LLM vLLM` created")
  
#*==============================================================================
with open(f"{packages.APP_PATH}/features/agents/car/prompts.yaml", 'r') as file:
  prompts_agent_car = yaml.safe_load(file)

with open(f"{packages.APP_PATH}/features/rag/prompts.yaml", 'r') as file:
  prompts_rag = yaml.safe_load(file)
#*==============================================================================
# Data

qdrant_client = storing.QdrantClient(
  host=os.getenv("HOST_QDRANT"),
	port=os.getenv("PORT_QDRANT"),
	grpc_port=os.getenv("PORT_QDRANT") + 1,
	timeout=15
)
qdrant_aclient = storing.AsyncQdrantClient(
  host=os.getenv("HOST_QDRANT"),
	port=os.getenv("PORT_QDRANT"),
	grpc_port=os.getenv("PORT_QDRANT") + 1,
	# prefer_grpc=True,
	# force_disable_check_same_thread=True,
)

#*==============================================================================

REDIS_KEY_PREFIX_DIRECTIONS = "directions:"
REDIS_TTL_DIRECTIONS = 3600  # 1 hour
REDIS_KEY_PREFIX_PLACES = "places:"
REDIS_TTL_PLACES = 3600
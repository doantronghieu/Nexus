import packages
import os
from loguru import logger
from toolkit.utils import typer as t
from toolkit.utils import utils
from toolkit.llm.langchain.data.persistence import (
  vector_stores as vector_stores_lc, 
  retrievers as retrievers_lc
)
from toolkit.llm.langchain.models import llms as llms_lc
from toolkit.llm.langchain.models import embeddings as embeddings_lc

#*==============================================================================

cfgs = {}
app_dir = f"{packages.APP_PATH}/context/app"
for file_name in os.listdir(app_dir):
    if file_name.endswith(".yaml"):
        base_name = os.path.splitext(file_name)[0]
        with open(f"{app_dir}/{file_name}") as f:
            cfgs[base_name] = utils.yaml.safe_load(f)

#*==============================================================================

if not os.environ.get("IN_PROD", None):
  import nest_asyncio # To connect to the same event-loop,
  nest_asyncio.apply() # allows async events to run on notebook
  logger.warning(f"Running in DEVELOPMENT mode")
else:
  logger.warning(f"Running in PRODUCTION mode")

#*==============================================================================

class FRAMEWORK_LLM(t.EnumCustom):
  LANGCHAIN = t.auto()
  LLAMAINDEX = t.auto()

class VEC_STR_COLLS(t.EnumCustom):
  """Vector Store Collections"""
  DEV = t.auto()
  VEHICLE = t.auto()
  USER_QUERY_CATEGORY = t.auto()
  VEHICLE_PROPERTIES_FIELD_PATHS = t.auto()

#*==============================================================================

CHOSEN = {
  "framework_llm": FRAMEWORK_LLM.LANGCHAIN,
  "langchain": {
    "llm": {
      "provider": llms_lc.ProviderLLM.OpenAI.name,
      "model": llms_lc.ProviderLLM.OpenAI.GPT_4O_MINI,
      # "provider": llms_lc.ProviderLLM.Ollama.name,
      # "model": llms_lc.ProviderLLM.Ollama.LLAMA_3DOT2_1B,
    },
    "embedding": {
      "provider": embeddings_lc.ProviderEmbedding.OpenAI.name,
      "model": embeddings_lc.ProviderEmbedding.OpenAI.TEXT_EMBEDDING_3_SMALL,
      "size": embeddings_lc.EMBEDDING_SIZE_MAP[embeddings_lc.ProviderEmbedding.OpenAI.TEXT_EMBEDDING_3_SMALL],
    },
    "vector_stores": [
      vector_stores_lc.ProviderVectorStore.IN_MEMORY,
      vector_stores_lc.ProviderVectorStore.QDRANT,
    ],
  },
  "qdrant": {
      "collections": list(set([
          *[collection for cfg_name in cfgs if "qdrant" in cfgs[cfg_name] 
            for collection in cfgs[cfg_name]["qdrant"]["collections"].keys()]
      ])),
      "params": {
        "mode_retrieval": vector_stores_lc.ModeRetrieval.HYBRID,
        "search_type": retrievers_lc.ModeRetriever.MMR,
      }
    },
}


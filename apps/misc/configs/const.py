import packages
from toolkit.utils import typer as t

from enum import Enum
from typing import TypeAlias, Literal

# from typing import TypeAlias, Literal

# MODEL: TypeAlias = Literal[

# ]

#*------------------------ Color codes for printing ------------------------*#

class Color(Enum):
  RED = "\033[91m"
  GREEN = "\033[92m"
  YELLOW = "\033[93m"
  BLUE = "\033[94m"
  MAGENTA = "\033[95m"
  CYAN = "\033[96m"
  WHITE = "\033[97m"
  RESET = "\033[0m"
  BLACK = "\033[30m"
  BRIGHT_RED = "\033[91m"
  BRIGHT_GREEN = "\033[92m"
  BRIGHT_YELLOW = "\033[93m"
  BRIGHT_BLUE = "\033[94m"
  BRIGHT_MAGENTA = "\033[95m"
  BRIGHT_CYAN = "\033[96m"
  BRIGHT_WHITE = "\033[97m"
  BOLD = "\033[1m"
  UNDERLINE = "\033[4m"
  BLINK = "\033[5m"
  REVERSE = "\033[7m"
  HIDDEN = "\033[8m"
  
#*--------------------------------- Models ---------------------------------*#
class Model:
    class Ollama(t.EnumCustom):
        LLAMA_3_1_8B = "llama3.1:8b" 
        LLAMA_3_2_1B = "llama3.2:1b"
        LLAMA_3_2_1B_INST_Q4KM = "llama3.2:1b-instruct-q4_K_M"
        LLAMA_3_2_3B = "llama3.2:3b"
        LLAMA_3_2_3B_INST_Q2K = "llama3.2:3b-instruct-q2_K"
        LLAMA_3_2_3B_INST_Q4KM = "llama3.2:3b-instruct-q4_K_M"
        LLAMA_3_2_1B_INSTRUCT_Q5_K_M = "Llama-3.2-1B-Instruct-Q5_K_M:latest"
        QWEN_2_5_0_5B = "qwen2.5:0.5b"
        QWEN_2_5_1_5B = "qwen2.5:1.5b"
        QWEN_2_5_3B = "qwen2.5:3b"
        QWEN_2_5_7B = "qwen2.5:7b"
        NEMOTRON_MINI = "nemotron-mini"
        MISTRAL = "mistral"
        MISTRAL_NEMO = "mistral-nemo"
        HERMES_3_8B = "hermes3:8b"

    class Vllm(t.EnumCustom):
        LLAMA_3_2_1B_INST = "meta-llama/Llama-3.2-1B-Instruct"

    class Mlc(t.EnumCustom):
        # Add MLC-specific models here
        pass

    class OpenAI(t.EnumCustom):
        GPT_3_5_TURBO = "gpt-3.5-turbo"
    
    class HuggingFace(t.EnumCustom):
        # Add HuggingFace-specific models here
        pass
    
class ModelInferServer(t.EnumCustom):
  OPENAI = t.auto()
  OLLAMA = t.auto()
  VLLM = t.auto()
  HUGGING_FACE = t.auto()
  MLC = t.auto()
  
#*---------------------------------- Embed ----------------------------------*#
# Open-sourced Embed models leaderboard: https://huggingface.co/spaces/mteb/leaderboard
class EmbedModel:
  class Ollama(t.EnumCustom):
    MXBAI_EMBED_LARGE = "mxbai-embed-large:latest"
  
  class OpenAI(t.EnumCustom):
    TEXT_EMBED_ADA_002 = "text-embedding-ada-002"
    TEXT_EMBED_3_LARGE = "text-embedding-3-large"
    TEXT_EMBED_3_SMALL = "text-embedding-3-small"

  class HuggingFace(t.EnumCustom):
    BGE_SMALL_EN = "BAAI/bge-small-en"
    BGE_BASE_EN_V1_5 = "BAAI/bge-base-en-v1.5"
    SELLA_EN_400M_V5 = "dunzhang/stella_en_400M_v5"
    STELLA_EN_1_5B_V5 = "dunzhang/stella_en_1.5B_v5"

class EmbedModelInferServer(t.EnumCustom):
  OPENAI = t.auto()
  OLLAMA = t.auto()
  HUGGING_FACE = t.auto()
  
#*--------------------------------------------------------------------------*#

TYPE_MODEL_INTERACT: TypeAlias = Literal[
  "chat", "achat", "stream", "astream", "astream_chat",
  "structured_predict", "astructured_predict"
]

TYPE_AGENT_INTERACT: TypeAlias = Literal[
  "chat", "achat", "stream_chat", "astream_chat", "chat_repl", "query",
]

#*---------------------------------- Data ----------------------------------*#

class QdrantCollection(t.EnumCustom):
  CAR_MANUAL_HF = "car_manual_HF"
  USER_QUERY_CATEGORY_HF = "user_query_category_HF"
  CAR_INFO_FIELD_PATHS_HF = "car_info_field_paths_HF"

  CAR_MANUAL_OPENAI = "car_manual_OpenAI"
  USER_QUERY_CATEGORY_OPENAI = "user_query_category_OpenAI"
  CAR_INFO_FIELD_PATHS_OPENAI = "car_info_field_paths_OpenAI"
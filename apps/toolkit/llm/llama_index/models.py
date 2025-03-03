"""
This module provides comprehensive coverage of `LLMs`, `Embeddings`, `Multi Modal` within LlamaIndex.

Refs:
- https://docs.llamaindex.ai/en/stable/module_guides/models/

TODO: Do survey: https://llamahub.ai/?tab=llms; https://llamahub.ai/?tab=embeddings
- https://llamahub.ai/l/llms/llama-index-llms-vllm?from=llms
- https://llamahub.ai/l/llms/llama-index-llms-xinference?from=llms
- https://llamahub.ai/l/llms/llama-index-llms-yi?from=llms
- https://llamahub.ai/l/llms/llama-index-llms-ipex-llm?from=llms
"""

# MODEL: TypeAlias = Literal[

# ]

from loguru import logger
from llama_index.core.llms import LLM
from llama_index.core.llms.function_calling import FunctionCallingLLM

from llama_index.llms.openai import OpenAI
from llama_index.llms.ollama import Ollama
import ollama
from llama_index.llms.openllm import OpenLLM
from llama_index.llms.vllm import Vllm, VllmServer

from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.embeddings.ollama import OllamaEmbedding

"""
response = OpenAI().complete("Paul Graham is ")
"""

class MyModel:
  def __init__(
    self,
    use_local_model: bool = False,
    model_name: str = "qwen2.5:0.5b",
    model_infer_server: str = "ollama",
    json_mode: bool = False,
  ):
    self.use_local_model = use_local_model
    self.model_name = model_name
    self.model_infer_server = model_infer_server
    self.model = self.get_model(json_mode)
    
    logger.info(f"LLM: {self.model_name}")
    logger.info(f"LLM inference server: {self.model_infer_server}")
    
  def get_model(self, json_mode: bool = False) -> LLM:
    if self.use_local_model:
      if self.model_infer_server == "ollama":
        models = [model["model"] for model in ollama.list()["models"]]

        if self.model_name not in models:
          logger.info(f"Pulling model: {self.model_name}")
          ollama.pull(self.model_name)

        model_specs = ollama.show(self.model_name)
        model_info = model_specs["modelinfo"]
        # model_context_length = modelinfo["llama.context_length"]
        
        return Ollama(
          model=self.model_name, request_timeout=360.0, 
          temperature=0.0,
          # context_window=model_context_length, 
          json_mode=json_mode,
          # keep_alive="30m",
        )
      else:
        raise ValueError(f"Invalid LLM inference server: {self.model_infer_server}")
    else:
      if self.model_infer_server == "openai":
        return OpenAI(model=self.model_name, temperature=0.0)
      else:
        raise ValueError(f"Invalid LLM inference server: {self.model_infer_server}")

class MyEmbedModel:
  def __init__(
    self,
    use_local_model: bool = False,
    model_name: str = "BAAI/bge-small-en-v1.5",
    embed_model_infer_server: str = "ollama",
    embed_batch_size: int = 1,
  ):
    self.use_local_model = use_local_model
    self.model_name = model_name
    self.embed_model_infer_server = embed_model_infer_server
    self.embed_batch_size = embed_batch_size
    self.embed_model = self.get_embed_model()
    
    logger.info(f"Embed model: {self.model_name}")
    logger.info(f"Embed model inference server: {self.embed_model_infer_server}")
    
  def get_embed_model(self):
    if self.use_local_model:
      if self.embed_model_infer_server == "ollama":
        models = [model["model"] for model in ollama.list()["models"]]

        if self.model_name not in models:
          logger.info(f"Pulling model: {self.model_name}")
          ollama.pull(self.model_name)
          
        return OllamaEmbedding(model_name=self.model_name, embed_batch_size=self.embed_batch_size)
      elif self.embed_model_infer_server == "huggingface":
        return HuggingFaceEmbedding(
          model_name=self.model_name, embed_batch_size=self.embed_batch_size,
          trust_remote_code=True,
        )
      else:
        raise ValueError(f"Invalid model inference server: {self.embed_model_infer_server}")
    else:
      if self.embed_model_infer_server == "openai":
        return OpenAIEmbedding(model=self.model_name, embed_batch_size=self.embed_batch_size)
      else:
        raise ValueError(f"Invalid model inference server: {self.embed_model_infer_server}")
  
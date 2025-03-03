import packages
from context.utils import typer as t
from context.utils import consts as c
from context.infra.clients import logger

from langchain_core.embeddings.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

#*======================================

class ProviderEmbedding:
  @t.parent_enum
  class OpenAI(t.EnumCustom):
    TEXT_EMBEDDING_3_SMALL = "text-embedding-3-small"
    TEXT_EMBEDDING_3_LARGE = "text-embedding-3-large"
  
  @t.parent_enum
  class Ollama(t.EnumCustom):
    # https://ollama.com/search?c=embedding
    LLAMA_3 = "llama3"
    NOMIC_EMBED_TEXT = "nomic-embed-text"


EMBEDDING_SIZE_MAP = {
  ProviderEmbedding.OpenAI.TEXT_EMBEDDING_3_SMALL: 1536,
  ProviderEmbedding.OpenAI.TEXT_EMBEDDING_3_LARGE: 3072,
}
#*======================================

def create_embedding(
  provider: str, model: str,
  **kwargs
):
  if provider == ProviderEmbedding.OpenAI.name:
    result = OpenAIEmbeddings(
      model=model,
    )
  elif provider == ProviderEmbedding.Ollama.name:
    result = None

  logger.info(f"{c.EMOJI.INIT} {c.CLR_TERM.ORANGE}Embedding{c.CLR_TERM.RESET} "
              F"{c.CLR_TERM.PURPLE}{provider}{c.CLR_TERM.RESET} "
              f"{c.CLR_TERM.GREEN}{model}{c.CLR_TERM.RESET}")
  return result
    
import packages

from context.utils import typer as t
from context import settings
from context.infra import clients

from context.settings import main as settings_main
from context.settings.main import CHOSEN

from toolkit.llm.langchain.data.persistence import (
  vector_stores as vector_stores_lc, retrievers as retrievers_lc
)
from toolkit.llm.langchain.models import embeddings as embeddings_lc

from context.instances.llms import embedding_main

#*======================================

fw = CHOSEN["framework_llm"]

if fw == settings_main.FRAMEWORK_LLM.LANGCHAIN:
  if vector_stores_lc.ProviderVectorStore.IN_MEMORY in CHOSEN[fw]["vector_stores"]:
    vector_store_in_memory: vector_stores_lc.VectorStore = clients.error_handler_silent.execute(
      lambda: vector_stores_lc.create_vector_store(
        provider=vector_stores_lc.ProviderVectorStore.IN_MEMORY,
        embeddings=embedding_main,
        collection_name=None,
      ),
      error_msg="Error creating Vector store (In Memory)",
    )
  if vector_stores_lc.ProviderVectorStore.QDRANT in CHOSEN[fw]["vector_stores"]:
    vector_stores_qdrant: dict[str, vector_stores_lc.VectorStore] = {}
    retrievers_qdrant: dict[str, retrievers_lc.BaseRetriever] = {}
    
    for collection in CHOSEN["qdrant"]["collections"]:
      vector_stores_qdrant[collection] = clients.error_handler_silent.execute(
        lambda: vector_stores_lc.create_vector_store(
          provider=vector_stores_lc.ProviderVectorStore.QDRANT,
          embeddings=embedding_main,
          embedding_size=embeddings_lc.EMBEDDING_SIZE_MAP[CHOSEN[fw]["embedding"]["model"]],
          collection_name=collection,
          mode_retrieval=CHOSEN["qdrant"]["params"]["mode_retrieval"],
        ),
        error_msg=f"Error creating Vector store (Qdrant, Collection: {collection})",
      )
      
      retrievers_qdrant[collection] = vector_stores_qdrant[collection].as_retriever(
        search_kwargs={'k': 10,}
      )
      
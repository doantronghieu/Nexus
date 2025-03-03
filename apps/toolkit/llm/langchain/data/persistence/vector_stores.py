import packages
from toolkit.utils import typer as t

from context.infra import clients
from context.infra.clients import logger
from context.utils import consts as c

from langchain_core.vectorstores.base import VectorStore, VectorStoreRetriever
from langchain_core.embeddings.embeddings import Embeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_qdrant import QdrantVectorStore, FastEmbedSparse, RetrievalMode
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import Distance, VectorParams

from langchain_core.vectorstores.utils import maximal_marginal_relevance

from langchain.agents.agent_toolkits.vectorstore.toolkit import (
  VectorStoreInfo, VectorStoreRouterToolkit, VectorStoreToolkit,
)

#*======================================

class ProviderVectorStore(t.EnumCustom):
  QDRANT = t.auto()
  IN_MEMORY = t.auto()

class ModeRetrieval(t.EnumCustom):
    DENSE = t.auto()
    SPARSE = t.auto()
    HYBRID = t.auto()

#*======================================

def create_vector_store(
  provider: str,
  embeddings: Embeddings,
  collection_name: t.Optional[str]=None,
  embedding_size: t.Optional[int]=None,
  mode_retrieval: t.Optional[str]=None,
) -> VectorStore:
  vector_store = None
  
  if provider == ProviderVectorStore.IN_MEMORY:
    vector_store = InMemoryVectorStore(embeddings) 
    logger.info(f"{c.EMOJI.INIT} {c.CLR_TERM.ORANGE}VectorStore{c.CLR_TERM.RESET} "
                f"{c.CLR_TERM.PURPLE}InMemory{c.CLR_TERM.RESET}")

  if provider == ProviderVectorStore.QDRANT:
    if not clients.client_qdrant.collection_exists(collection_name):
      # https://qdrant.tech/documentation/concepts/collections/
      clients.client_qdrant.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
          size=embedding_size, 
          distance=Distance.COSINE
        ),
        sparse_vectors_config={
          "text": models.SparseVectorParams(),
        }
      )
      logger.info(f"{c.EMOJI.INIT} {c.CLR_TERM.ORANGE}VectorStore{c.CLR_TERM.RESET} "
                f"{c.CLR_TERM.PURPLE}Qdrant{c.CLR_TERM.RESET} "
                f"Collection {c.CLR_TERM.GREEN}{collection_name}{c.CLR_TERM.RESET}")

    vector_store = QdrantVectorStore(
      client=clients.client_qdrant,
      embedding=embeddings,
      sparse_embedding=FastEmbedSparse(model_name="Qdrant/bm25"),
      collection_name=collection_name,
      retrieval_mode=mode_retrieval,
      sparse_vector_name="text",
    )
    logger.info(f"{c.EMOJI.CONNECTED} {c.CLR_TERM.ORANGE}VectorStore{c.CLR_TERM.RESET} "
                f"{c.CLR_TERM.PURPLE}Qdrant{c.CLR_TERM.RESET} "
                f"Collection {c.CLR_TERM.GREEN}{collection_name}{c.CLR_TERM.RESET}")

  return vector_store
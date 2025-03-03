"""
This module provides comprehensive coverage of `Indexing`, `Storing` within LlamaIndex.

Refs:
- https://docs.llamaindex.ai/en/stable/module_guides/storing/
- https://docs.llamaindex.ai/en/stable/module_guides/indexing/
"""

from llama_index.core import (
  VectorStoreIndex, SummaryIndex, StorageContext, 
  load_index_from_storage, load_indices_from_storage, load_graph_from_storage,
)
from llama_index.core.objects import ObjectIndex
from llama_index.core.storage.docstore import SimpleDocumentStore
try: 
    from llama_index.storage.docstore.mongodb import MongoDocumentStore
    from llama_index.storage.index_store.mongodb import MongoIndexStore
except: pass

from llama_index.core.vector_stores import SimpleVectorStore
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient, AsyncQdrantClient

from llama_index.core.indices import PropertyGraphIndex
from llama_index.core.graph_stores import (
  SimplePropertyGraphStore, EntityNode, Relation,
)
from llama_index.core.graph_stores.types import (
  KG_NODES_KEY, KG_RELATIONS_KEY
)
from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore

from llama_index.indices.managed.llama_cloud import (
  LlamaCloudIndex, LlamaCloudRetriever,
)

from llama_index.core.indices.property_graph import (
  SimpleLLMPathExtractor, ImplicitPathExtractor, DynamicLLMPathExtractor,
  SchemaLLMPathExtractor, 
)

from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.storage.chat_store.redis import RedisChatStore
from llama_index.core.memory import ChatMemoryBuffer

#*------------------------------------------------------------------------------
import packages
import asyncio
from toolkit.utils import typer as t
from configs.settings import logger
#*------------------------------------------------------------------------------
from llama_index.core.vector_stores.types import BasePydanticVectorStore
from contextlib import contextmanager

#*==============================================================================
@contextmanager
def get_or_create_eventloop():
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        yield loop
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        yield loop
        
def get_vector_store(
  client: t.Optional[t.Union[t.Any, QdrantClient]] = None,
  aclient: t.Optional[t.Union[t.Any, AsyncQdrantClient]] = None,
  url: t.Optional[str] = None,
  api_key: t.Optional[str] = None,
  collection_name: t.Optional[str] = None,
  type_store: t.Literal["qdrant"] = None,
  **kwargs
) -> BasePydanticVectorStore:
  vector_store = None
  
  # Validate that exactly one client type is provided
  if (client is not None and aclient is not None) or (client is None and aclient is None):
    raise ValueError("Exactly one of 'client' or 'aclient' must be provided")
  
  # Determine which client to use
  active_client = client if aclient is None else aclient
  is_async = aclient is not None

  vector_store = None
  if type_store == "qdrant":
    vector_store = QdrantVectorStore(
      client=active_client if not is_async else None,
      aclient=active_client if is_async else None,
      collection_name=collection_name,
    )
  
  logger.info(f"Using Vector store `{type_store}`")
  return vector_store

async def get_index_async(
    storage_context: t.Optional[StorageContext] = None,
    vector_store: t.Optional[BasePydanticVectorStore] = None,
    type_index: t.Literal["qdrant"] = None,
    client: t.Optional[t.Union[t.Any, QdrantClient]] = None,
    aclient: t.Optional[t.Union[t.Any, AsyncQdrantClient]] = None,
    collection_name: t.Optional[str] = None,
    **kwargs
) -> t.Union[VectorStoreIndex, None]:
    index = None
    
    # Validate that exactly one client type is provided
    if (client is not None and aclient is not None) or (client is None and aclient is None):
        raise ValueError("Exactly one of 'client' or 'aclient' must be provided")
    
    # Determine which client to use
    active_client = client if aclient is None else aclient
    is_async = aclient is not None
    
    logger.info(f"Client: {active_client}")
    
    if storage_context is None:
        vector_store = get_vector_store(
            client=active_client if not is_async else None,
            aclient=active_client if is_async else None,
            collection_name=collection_name,
            type_store=type_index,
        )
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        logger.info(f"Storage context for collection '{collection_name}' created")
    
    if vector_store is None:
        _vector_store = storage_context.vector_store
    else:
        _vector_store = vector_store
    
    # Handle collection existence check based on client type
    try:
        # Check collection existence based on client type
        if not is_async:
            collection_exists = active_client.collection_exists(collection_name=collection_name)
        else:
            collection_exists = await active_client.collection_exists(collection_name=collection_name)
        
        if collection_exists:
            index = VectorStoreIndex.from_vector_store(
                vector_store=_vector_store,
                storage_context=storage_context,
            )
            logger.info(f"Vector store index from collection '{collection_name}' created")
        else:
            logger.warning(f"Collection '{collection_name}' not found in database")
            index = None
            
        return index
    except Exception as e:
        logger.error(f"Error creating index for collection '{collection_name}': {str(e)}")
        return None

def get_index(
    storage_context: t.Optional[StorageContext] = None,
    vector_store: t.Optional[BasePydanticVectorStore] = None,
    type_index: t.Literal["qdrant"] = None,
    client: t.Optional[t.Union[t.Any, QdrantClient]] = None,
    aclient: t.Optional[t.Union[t.Any, AsyncQdrantClient]] = None,
    collection_name: t.Optional[str] = None,
    **kwargs
) -> t.Union[VectorStoreIndex, None]:
    """
    Synchronous version of get_index function.
    """
    # Validate that exactly one client type is provided
    if (client is not None and aclient is not None) or (client is None and aclient is None):
        raise ValueError("Exactly one of 'client' or 'aclient' must be provided")
    
    # Determine which client to use and whether it's async
    active_client = client if aclient is None else aclient
    is_async = aclient is not None

    if not is_async:
        # For synchronous client, run synchronously
        try:
            vector_store = get_vector_store(
                client=active_client,
                aclient=None,
                collection_name=collection_name,
                type_store=type_index,
            )
            
            if storage_context is None:
                storage_context = StorageContext.from_defaults(vector_store=vector_store)
                logger.info(f"Storage context for collection '{collection_name}' created")
            
            _vector_store = vector_store if vector_store is not None else storage_context.vector_store
            
            if active_client.collection_exists(collection_name=collection_name):
                index = VectorStoreIndex.from_vector_store(
                    vector_store=_vector_store,
                    storage_context=storage_context,
                )
                logger.info(f"Vector store index from collection '{collection_name}' created")
                return index
            else:
                logger.warning(f"Collection '{collection_name}' not found in database")
                return None
                
        except Exception as e:
            logger.error(f"Error in get_index: {str(e)}")
            return None
    else:
        # For async client, use event loop
        with get_or_create_eventloop() as loop:
            try:
                return loop.run_until_complete(get_index_async(
                    storage_context=storage_context,
                    vector_store=vector_store,
                    type_index=type_index,
                    aclient=active_client,
                    collection_name=collection_name,
                    **kwargs
                ))
            except Exception as e:
                logger.error(f"Error in get_index: {str(e)}")
                return None
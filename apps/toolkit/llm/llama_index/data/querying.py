"""
This module provides comprehensive coverage of `Querying` within LlamaIndex.

Refs:
- https://docs.llamaindex.ai/en/stable/module_guides/querying/
"""

from llama_index.core import QueryBundle, get_response_synthesizer
from llama_index.core.response_synthesizers import (
  BaseSynthesizer, ResponseMode, TreeSummarize
)

from llama_index.core.retrievers import (
  VectorIndexRetriever, BaseRetriever, SummaryIndexLLMRetriever, RouterRetriever
)

from llama_index.core.indices.property_graph import (
  PGRetriever, CustomPGRetriever, VectorContextRetriever, LLMSynonymRetriever, TextToCypherRetriever, CypherTemplateRetriever,
  CUSTOM_RETRIEVE_TYPE,
)

from llama_index.core.query_engine import (
  BaseQueryEngine, RetrieverQueryEngine, CustomQueryEngine, RouterQueryEngine
)
from llama_index.core.chat_engine import CondenseQuestionChatEngine

from llama_index.core.selectors import (
  LLMSingleSelector, LLMMultiSelector,
  PydanticSingleSelector, PydanticMultiSelector
)

from llama_index.core.postprocessor import (
  SimilarityPostprocessor, TimeWeightedPostprocessor, KeywordNodePostprocessor,
  MetadataReplacementPostProcessor, LongContextReorder, 
  SentenceEmbeddingOptimizer, SentenceTransformerRerank, 
  FixedRecencyPostprocessor, EmbeddingRecencyPostprocessor, 
  PIINodePostprocessor, NERPIINodePostprocessor,
)
from llama_index.core.postprocessor.types import BaseNodePostprocessor
from llama_index.core.postprocessor.llm_rerank import LLMRerank
try:
  from llama_index.postprocessor.cohere_rerank import CohereRerank
except: pass
#*------------------------------------------------------------------------------
import packages
from toolkit.utils import typer as t
from configs import settings
from configs.settings import logger
#*------------------------------------------------------------------------------
from toolkit.llm.llama_index import agents
from toolkit.llm.llama_index.data import storing
#*==============================================================================

class QueryToolkit(t.TypedDict):
  retriever: VectorIndexRetriever
  query_engine: RetrieverQueryEngine
  query_engine_tool: agents.QueryEngineTool
  query_plan_tool: agents.QueryPlanTool
  
def get_query_toolkit_from_vector_store_index(
  vector_store_index: storing.VectorStoreIndex,
  similarity_top_k: int = 10,
  similarity_cutoff: int = 0.4,
  
  res_synth_response_mode: ResponseMode = ResponseMode.COMPACT,
  res_synth_streaming: bool = True,
  
  tool_name_query_engine: str = "Query Engine", # Can be sql_agent, gmail_agent
  tool_desc_query_engine: str = (
    "Provides information about {{INFO}}. "
    "Use a detailed plain text question as input to the tool."
    # Agent that can execute SQL queries.
    # Tool that can send emails on Gmail.
  ),
  tool_return_direct_query_engine: bool = False,
):
  
  query_toolkit: QueryToolkit = {}
  
  retriever: VectorIndexRetriever = settings.error_handler_silent.execute(
    lambda: VectorIndexRetriever(
      index=vector_store_index, similarity_top_k=similarity_top_k,
    ),
    error_msg="Vector Store not found.",
  )
  if retriever is None:
    return
  
  query_toolkit["retriever"] = retriever
  
  node_postprocessors = [
    SimilarityPostprocessor(similarity_cutoff=similarity_cutoff),
  ]
  
  response_synthesizer = get_response_synthesizer(
    response_mode=res_synth_response_mode, streaming=res_synth_streaming
  )
  query_engine = RetrieverQueryEngine(
    retriever=retriever,
    node_postprocessors=node_postprocessors,
    response_synthesizer=response_synthesizer,
  )
  logger.info("Query engine created.")
  query_toolkit["query_engine"] = query_engine

  query_engine_tool = agents.QueryEngineTool(
    query_engine=query_engine,  # Can use other agents as tools
    metadata=agents.ToolMetadata(
      name=tool_name_query_engine, 
      description=tool_desc_query_engine,
      # Returned directly without being interpreted and rewritten by the agent
      return_direct=tool_return_direct_query_engine, 
    )
  )
  query_toolkit["query_engine_tool"] = query_engine_tool
  
  query_plan_tool = agents.QueryPlanTool.from_defaults(
    query_engine_tools=[query_engine_tool],
    response_synthesizer=get_response_synthesizer(),
  )
  # query_plan_tool = agents.convert_query_plan_tool(query_plan_tool, "openai")
  query_toolkit["query_plan_tool"] = query_plan_tool

  return query_toolkit
import packages
from toolkit.utils import typer as t

from langchain_core.retrievers import BaseRetriever

from langchain.retrievers.ensemble import EnsembleRetriever, unique_by_key
from langchain.retrievers.merger_retriever import MergerRetriever

from langchain.retrievers.multi_query import MultiQueryRetriever, LineListOutputParser
from langchain.retrievers.re_phraser import RePhraseQueryRetriever
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.retrievers.multi_vector import MultiVectorRetriever, SearchType
from langchain.retrievers.parent_document_retriever import ParentDocumentRetriever

from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain.retrievers.document_compressors.base import DocumentCompressorPipeline
from langchain.retrievers.document_compressors.chain_extract import (
    LLMChainExtractor, NoOutputParser, default_get_input
)
from langchain.retrievers.document_compressors.chain_filter import (
    LLMChainFilter, default_get_input
)
from langchain.retrievers.document_compressors.cross_encoder import BaseCrossEncoder
from langchain.retrievers.document_compressors.cross_encoder_rerank import CrossEncoderReranker
from langchain.retrievers.document_compressors.embeddings_filter import EmbeddingsFilter
from langchain.retrievers.document_compressors.listwise_rerank import LLMListwiseRerank

from langchain.retrievers.time_weighted_retriever import TimeWeightedVectorStoreRetriever

from langchain_community.retrievers import (
    QdrantSparseVectorRetriever,
)

#*==
from langchain_core.documents import Document
#*==

class TypeRetriever(t.EnumCustom):
    ENSEMBLE = t.auto()
    MERGER = t.auto()
    MULTI_QUERY = t.auto()
    RE_PHRASER = t.auto()
    SELF_QUERY = t.auto()
    MULTI_VECTOR = t.auto()
    PARENT_DOCUMENT = t.auto()
    CONTEXTUAL_COMPRESSION = t.auto()
    DOCUMENT_COMPRESSORS = t.auto()

    QDRANT = t.auto()

class ModeRetriever(t.EnumCustom):
    SIMILARITY = t.auto()
    MMR = t.auto()
    SIMILARITY_SCRORE_THRESHOLD = t.auto()

#*==

async def extract_retriever_results(documents: list[Document]) -> list:
	contents = []
	
	for doc in documents:
		content = doc.page_content
		contents.append(content)
					
	return contents
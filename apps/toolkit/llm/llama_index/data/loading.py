"""
This module provides comprehensive coverage of `Loading` within LlamaIndex.

Refs:
- https://docs.llamaindex.ai/en/stable/module_guides/loading/
"""

from pathlib import Path
from loguru import logger

from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader
from llama_index.core.readers.base import BaseReader
from llama_index.readers.file import (
  PyMuPDFReader, FlatReader, PDFReader, MarkdownReader, PptxReader,
  PandasCSVReader, PandasExcelReader, UnstructuredReader, CSVReader,
)
from llama_index.readers.web import (
  AsyncWebPageReader, BeautifulSoupWebReader, BrowserbaseWebReader,
  KnowledgeBaseWebReader, SimpleWebPageReader, UnstructuredURLLoader,
)
from llama_index.readers.json import JSONReader
from llama_index.readers.database import DatabaseReader

from llama_index.core import (
  Document, download_loader, PropertyGraphIndex
)
from llama_index.core.schema import (
  BaseNode, TextNode, IndexNode, NodeWithScore, MetadataMode, NodeRelationship, RelatedNodeInfo, TransformComponent,
)
from llama_index.core.data_structs import Node

from llama_index.core.node_parser import (
  SentenceSplitter, TokenTextSplitter, HTMLNodeParser, JSONNodeParser, 
  MarkdownNodeParser, CodeSplitter, LangchainNodeParser, 
  SentenceWindowNodeParser, SemanticSplitterNodeParser, HierarchicalNodeParser
)
from langchain.text_splitter import RecursiveCharacterTextSplitter, RecursiveJsonSplitter

from llama_index.core.extractors import (
  BaseExtractor, TitleExtractor, QuestionsAnsweredExtractor, 
  SummaryExtractor, KeywordExtractor,
)

from llama_index.core.ingestion import IngestionPipeline, IngestionCache

class MyReader:
  def __init__(self, file_path: str, **kwargs):
    self.file_path = file_path
    self.reader = self.get_reader(**kwargs)
    
  def get_reader(self, **kwargs) -> BaseReader: 
    # Get the file extension
    file_extension = Path(self.file_path).suffix
    # Choose the appropriate reader based on the file extension
    if file_extension == ".pdf":
      logger.info("Using PyMuPDFReader for PDF file")
      return PyMuPDFReader(**kwargs)
    elif file_extension == ".json":
      logger.info("Using JSONReader for JSON file")
      return JSONReader(**kwargs)
  
  def load_data(self) -> list[Document]:
    data = self.reader.load_data(self.file_path)
    logger.info("Data has been loaded successfully.")
    return data
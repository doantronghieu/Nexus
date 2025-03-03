import packages
from toolkit.utils import typer as t

from langchain_community.document_loaders.base import BaseLoader

import bs4

from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders import (
  BSHTMLLoader, JSONLoader, DirectoryLoader, TextLoader, PythonLoader,
  Docx2txtLoader
)

from bs4 import BeautifulSoup
from langchain_community.document_loaders import (
  WebBaseLoader, RecursiveUrlLoader, AsyncHtmlLoader,
)
from langchain_community.document_loaders.sitemap import SitemapLoader

from langchain_community.document_loaders.blob_loaders.youtube_audio import (
    YoutubeAudioLoader,
)
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import (
    OpenAIWhisperParser,
)
from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders.youtube import TranscriptFormat

from langchain_unstructured import UnstructuredLoader
from unstructured.cleaners.core import clean_extra_whitespace
from unstructured_client import UnstructuredClient
from unstructured_client.utils import BackoffStrategy, RetryConfig

from langchain_community.document_loaders.image import UnstructuredImageLoader
from langchain_community.document_loaders import (
  UnstructuredExcelLoader, UnstructuredPowerPointLoader, UnstructuredMarkdownLoader,
  UnstructuredWordDocumentLoader, UnstructuredRSTLoader, UnstructuredPDFLoader,
)

from langchain_community.document_loaders import (
  PyPDFLoader, PyMuPDFLoader
)

from langchain_community.document_loaders.discord import DiscordChatLoader
from langchain_community.document_loaders import (
    TelegramChatApiLoader, TelegramChatFileLoader,
)

from langchain_community.document_loaders.mongodb import MongodbLoader
from langchain_community.document_loaders import SnowflakeLoader

from langchain_community.document_loaders import NewsURLLoader

#*===

class TYPE_DCM_LOADER(t.EnumCustom):
  TXT = t.auto()
  CSV = t.auto()
  HTML = t.auto()
  JSON = t.auto()
  DIR = t.auto()
  PYTHON = t.auto()
  SITEMAP = t.auto()
  YOUTUBE = t.auto()
  EXCEL = t.auto()
  POWER_POINT = t.auto()
  MARKDOWN = t.auto()
  WORD = t.auto()
  PDF = t.auto()
  RST = t.auto()

#*===

def create_document_loader():
  pass
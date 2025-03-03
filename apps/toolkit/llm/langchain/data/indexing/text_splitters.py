import packages
from toolkit.utils import typer as t

from langchain_text_splitters.base import (
  TextSplitter, TokenTextSplitter
)
from langchain_text_splitters.character import RecursiveCharacterTextSplitter
from langchain_text_splitters.html import (
  HTMLHeaderTextSplitter, HTMLSectionSplitter
)
from langchain_text_splitters.json import RecursiveJsonSplitter
from langchain_text_splitters.latex import LatexTextSplitter
from langchain_text_splitters.markdown import (
  MarkdownHeaderTextSplitter, MarkdownTextSplitter
)
from langchain_text_splitters.nltk import NLTKTextSplitter
from langchain_text_splitters.python import PythonCodeTextSplitter

from langchain_experimental.text_splitter import SemanticChunker

#*===

class TYPE_TEXT_SPLITTER(t.EnumCustom):
  TEXT = t.auto()
  TOKEN_TEXT = t.auto()
  CHARACTER = t.auto()
  RECURSIVE_CHARACTER = t.auto()
  HTML_HEADER = t.auto()
  HTML_SECTION = t.auto()
  JSON = t.auto()
  LATEXT = t.auto()
  MARKDOWN_HEADER = t.auto()
  MARKDOWN = t.auto()
  NLTK = t.auto()
  PYTHON = t.auto()

#*===

def create_text_splitter():
  pass
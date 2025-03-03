import packages
from context.utils import typer as t

from toolkit.llm.langchain.data.indexing import documents
from toolkit.llm.langchain.models import messages

#*======================================

def extract_content(
    content_items: list[t.Union[documents.Document, messages.BaseMessage]]
) -> str:
    attr = "page_content" if hasattr(content_items[0], "page_content") else "content"
    return "\n\n".join(getattr(item, attr) for item in content_items)
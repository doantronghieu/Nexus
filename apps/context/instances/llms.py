import packages

from context.utils import typer as t
from context import settings
from context.infra import clients

from context.settings import main as settings_main

from toolkit.llm.langchain.models import llms as llms_lc
from toolkit.llm.langchain.models import embeddings as embeddings_lc

#*======================================

fw = settings_main.CHOSEN["framework_llm"]

if fw == settings_main.FRAMEWORK_LLM.LANGCHAIN:
  llm_main: llms_lc.BaseChatModel = clients.error_handler_silent.execute(
    lambda: llms_lc.create_llm(
      provider=settings_main.CHOSEN[fw]["llm"]["provider"], 
      model=settings_main.CHOSEN[fw]["llm"]["model"],
    ),
    error_msg="Error creating LLM Main",
  )
  
  llm_google: llms_lc.BaseChatModel = clients.error_handler_silent.execute(
    lambda: llms_lc.create_llm(
      provider=llms_lc.ProviderLLM.Google.name, 
      model=llms_lc.ProviderLLM.Google.GEMINI_2_0_FLASH_EXP,
    ),
    error_msg="Error creating LLM Google",
  )
  
  embedding_main: embeddings_lc.Embeddings = clients.error_handler_silent.execute(
    lambda: embeddings_lc.create_embedding(
      provider=settings_main.CHOSEN[fw]["embedding"]["provider"], 
      model=settings_main.CHOSEN[fw]["embedding"]["model"],
    ),
    error_msg="Error creating Embedding",
  )


import packages
from context.utils import typer as t
from context.utils import consts as c
from context.infra.clients import logger

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_ollama import ChatOllama
from langchain_community.llms.openllm import OpenLLM
from langchain_huggingface import HuggingFaceEndpoint

import ollama


from toolkit.llm.langchain.execution import runnables, tools
#*======================================

class ProviderLLM:
  @t.parent_enum
  class OpenAI(t.EnumCustom):
    # https://python.langchain.com/api_ reference/openai/index.html
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_4O_MINI = "gpt-4o-mini"
    
  @t.parent_enum
  class Anthropic(t.EnumCustom):
    pass

  @t.parent_enum
  class Google(t.EnumCustom):
    GEMINI_2_0_FLASH_EXP = "gemini-2.0-flash-exp"

  @t.parent_enum
  class Ollama(t.EnumCustom):
    # https://python.langchain.com/docs/integrations/providers/ollama/
    # https://python.langchain.com/api_reference/ollama/index.html
    # https://ollama.com/search
    LLAMA_3DOT2_1B = "llama3.2:1b"
    LLAMA_3DOT2_3B = "llama3.2:3b"
    DEEPSEEK_R1_1DOT5B = "deepseek-r1:1.5b"

#*======================================

def create_llm(provider: str, model: str, temperature: float = 0.0, **kwargs) -> BaseChatModel:
    if provider == ProviderLLM.Ollama.name:
      models = [model["model"] for model in ollama.list()["models"]]

      if model not in models:
        logger.info(f"{c.EMOJI.PACKAGE} {c.CLR_TERM.ORANGE}LLM{c.CLR_TERM.RESET} "
                    f"{c.CLR_TERM.PURPLE}{provider}{c.CLR_TERM.RESET} "
                    f"{c.CLR_TERM.GREEN}{model}{c.CLR_TERM.RESET}")
        ollama.pull(model)

    providers: t.Dict[str, t.Callable[..., BaseChatModel]] = {
        ProviderLLM.OpenAI.name: lambda model, temperature, **kwargs: ChatOpenAI(
            model=model, 
            temperature=temperature, 
            **kwargs
        ),
        ProviderLLM.Ollama.name: lambda model, temperature, **kwargs: ChatOllama(
            model=model, 
            temperature=temperature, 
            cache=False,
            **kwargs
        ),
        ProviderLLM.Google.name: lambda model, temperature, **kwargs: ChatGoogleGenerativeAI(
            model=model, 
            temperature=temperature, 
            **kwargs
        ),
    }
    
    model_factory = providers.get(provider)
    
    logger.info(f"{c.EMOJI.INIT} {c.CLR_TERM.ORANGE}LLM{c.CLR_TERM.RESET} "
                f"{c.CLR_TERM.PURPLE}{provider}{c.CLR_TERM.RESET} "
                f"{c.CLR_TERM.GREEN}{model}{c.CLR_TERM.RESET}")
    
    return model_factory(model, temperature, **kwargs)

def create_structured_llm(
  llm: BaseChatModel,
  schema: t.Type[t.TypedDictSchema]
) -> runnables.Runnable:
  return llm.with_structured_output(schema)
  
def create_tooled_llm(
  llm: BaseChatModel,
  tools: list[tools.BaseTool],
) -> runnables.Runnable:
  llm = llm.model_copy()
  return llm.bind_tools(tools)
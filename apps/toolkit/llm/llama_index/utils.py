from toolkit.utils.llm import main as utils_llm
import packages
from configs import settings, const

import asyncio, os, time, yaml, json, datetime, copy
from typing import Any, AsyncGenerator, Generator, Callable, Literal, Optional, TypeAlias, Union
from tqdm import tqdm
from loguru import logger
from pprint import pprint
from rich import print as rprint

from toolkit.llm.llama_index import (
	agents, cores, deploys as dpls, evaluation, messages, models, 
	observability, types, utils as utils_llama_index, workflows as wfs
)
from toolkit.llm.llama_index.data import loading, querying, storing

from toolkit.utils import utils, typer as t
from toolkit.utils.llm import measure_performance

#*-----------------------------------------------------------------------

from functools import wraps

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.theme import Theme
from rich.color import ANSI_COLOR_NAMES # For reference
#*=======================================================================

# Custom theme with colors visible on both light and dark backgrounds
custom_theme = Theme({
    "title": "bright_cyan",
    "header": "bright_magenta",
    "metric": "bright_red",
    "value": "bright_green",
    "border": "bright_blue"
})

console = Console(theme=custom_theme)

async def extract_text(nodes: list[loading.NodeWithScore]):
	texts = ""
	for node in nodes:
		texts += node.dict()["node"]["text"]
	return texts

async def extract_retriever_results(results: list, include_score: bool = False):
   """
   Extract text (and optionally score) values from retriever results.
   
   Args:
       results (list): List of retriever results
       include_score (bool, optional): Whether to include scores in output. Defaults to False.
       
   Returns:
       If include_score is True:
           list: List of dictionaries containing text and score for each result
       If include_score is False:
           list: List of text strings
   """
   if include_score:
       extracted_data = []
       for result in results:
           result_dict = dict(result)
           score = result_dict["score"]
           node_dict = dict(result_dict["node"])
           text = node_dict["text"]
           
           extracted_data.append({
               "text": text,
               "score": score
           })
       return extracted_data
   else:
       texts = []
       for result in results:
           result_dict = dict(result)
           node_dict = dict(result_dict["node"])
           text = node_dict["text"]
           texts.append(text)
       return texts

def measure_llm_performance(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs):
        measure = kwargs.get('measure_performance', True)
        mode = kwargs.get('mode', 'chat')
        
        if mode in ['stream', 'astream'] and measure:
            start_time = time.time()
            result = await func(*args, **kwargs)
            
            if mode == 'stream':
                def token_generator():
                    nonlocal start_time
                    token_count = 0
                    time_to_first_token = None
                    
                    for i, token in enumerate(result):
                        if i == 0:
                            time_to_first_token = time.time() - start_time
                        token_count += 1
                        yield token
                    
                    print_metrics(start_time, time_to_first_token, token_count)
                
                return token_generator()
            else:  # astream
                async def async_token_generator():
                    nonlocal start_time
                    token_count = 0
                    time_to_first_token = None
                    
                    async for i, token in aenumerate(result):
                        if i == 0:
                            time_to_first_token = time.time() - start_time
                        token_count += 1
                        yield token
                    
                    print_metrics(start_time, time_to_first_token, token_count)
                
                return async_token_generator()
        else:
            return await func(*args, **kwargs)

    def print_metrics(start_time, time_to_first_token, token_count):
        end_time = time.time()
        total_time = end_time - start_time
        tokens_per_second = token_count / total_time
        
        table = Table(title="LLM Performance Metrics", show_header=True, header_style="header")
        table.add_column("Metric", style="metric", no_wrap=True)
        table.add_column("Value", style="value")
        
        table.add_row("Time to first token", f"{time_to_first_token:.2f} seconds")
        table.add_row("Total tokens", str(token_count))
        table.add_row("Total time", f"{total_time:.2f} seconds")
        table.add_row("Tokens per second", f"{tokens_per_second:.2f}")
        
        console.print(Panel(table, expand=False, border_style="border", title="LLM Performance", title_align="left"))

    async def aenumerate(agen):
        i = 0
        async for item in agen:
            yield i, item
            i += 1

    return wrapper

@measure_llm_performance
async def interact_model(
    llm: models.LLM=cores.Settings.llm,
    prompt: str="{user_query}", system_prompt: t.Optional[str]=None,
    user_query: t.Optional[str]=None, 
    mode: const.TYPE_MODEL_INTERACT="chat",
    output_cls: t.Optional[type[t.BaseModel]]=None, 
    measure_performance: bool = not os.getenv("IN_PROD"),
    **kwargs
) -> Union[messages.ChatResponse, t.Generator, t.BaseModel]:  # Updated return type
    result = None
    
    prompt = messages.PromptTemplate(prompt)

    msg = []
    
    original_system_prompt = llm.system_prompt  # Store the original system prompt
    
    try:
        if system_prompt is not None:
            msg.append(messages.ChatMessage(
                role=messages.MessageRole.SYSTEM, content=system_prompt
            ))
            llm.system_prompt = system_prompt

        # For chat and stream modes, we need to format the message
        if mode in ["chat", "achat", "stream", "astream", "astream_chat"]:
            msg.append(
                messages.ChatMessage(
                    role=messages.MessageRole.USER, 
                    content=prompt.format(user_query=user_query, **kwargs)
                ),
            )

        if mode == "chat" or mode == "achat":
            interact_method = llm.achat if mode == "achat" else llm.chat
            result = await interact_method(msg) if mode == "achat" else interact_method(msg)
            return result.message.content
        
        elif mode == "stream" or mode == "astream" or mode == "astream_chat":
            kwargs.update({
                "prompt": prompt, "user_query": user_query
            })

            if mode == "astream":
                interact_method = llm.astream
                return await interact_method(**kwargs)
            elif mode == "stream":
                interact_method = llm.stream
                return interact_method(**kwargs)
            elif mode == "astream_chat":
                interact_method = llm.astream_chat
                return await interact_method(msg)

        elif mode == "structured_predict" or mode == "astructured_predict":
            if output_cls is None:
                raise ValueError("output_cls must be provided for structured_predict mode")
            
            interact_method = llm.astructured_predict if mode == "astructured_predict" \
                else llm.structured_predict

            kwargs.update({
                "output_cls": output_cls, "prompt": prompt, "user_query": user_query
            })

            return await interact_method(**kwargs) if mode == "astructured_predict" \
                else interact_method(**kwargs)
        
        else:
            raise ValueError(f"Unknown mode: {mode}")
    
    finally:
        # This block will always execute, even if there's an exception
        cores.Settings.llm.system_prompt = original_system_prompt
        llm.system_prompt = original_system_prompt

async def interact_agent(
    agent: agents.BaseAgent,
    user_query: Optional[str]=None, 
    mode: const.TYPE_AGENT_INTERACT="achat",
    **kwargs
) -> Union[str, AsyncGenerator[str, None], None]:
    """
    Interact with an agent using various chat modes and return the result.

    Returns:
        - For non-streaming modes: The result as a string.
        - For streaming modes: An AsyncGenerator yielding tokens.
        - For chat_repl mode: None.
    """
    if mode == "chat_repl":
        agent.chat_repl()
        return None

    if mode == "chat":
        response = agent.chat(user_query)
    elif mode == "achat":
        response = await agent.achat(user_query)
    elif mode == "stream_chat":
        response = agent.stream_chat(user_query)
    elif mode == "astream_chat":
        response = await agent.astream_chat(user_query)
    elif mode == "query":
        response = agent.query(user_query)
    else:
        raise ValueError(f"Invalid mode: {mode}")

    if mode in ("chat", "achat", "query"):
        return str(response)
    elif mode in ("stream_chat", "astream_chat"):
        async def token_generator():
            if mode == "astream_chat":
                async for token in response.async_response_gen():
                    yield token
            else:
                for token in response.response_gen:
                    yield token
        return token_generator()

async def handle_agent_response(
    result: Union[str, AsyncGenerator[str, None], None]
) -> str:
    """
    Handle different types of responses from interact_agent.
    """
    if result is None:
        return "No result (chat_repl mode)"
    elif isinstance(result, str):
        return result
    elif asyncio.iscoroutine(result):
        return await result
    else:  # AsyncGenerator
        tokens = []
        async for token in result:
            print(token, end="", flush=True)  # Print tokens as they come
            tokens.append(token)
        print()  # Newline after streaming
        return "".join(tokens)

...
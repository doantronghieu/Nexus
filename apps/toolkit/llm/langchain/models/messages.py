import packages
from context.utils import typer as t

from langchain_core.messages.base import (
  BaseMessage, BaseMessageChunk,
  message_to_dict, messages_to_dict
)
from langchain_core.messages import AnyMessage

from langchain_core.messages.system import SystemMessage, SystemMessageChunk
from langchain_core.messages.ai import (
  AIMessage, AIMessageChunk, add_ai_message_chunks
)
from langchain_core.messages.chat import ChatMessage, ChatMessageChunk
from langchain_core.messages.function import FunctionMessage, FunctionMessageChunk
from langchain_core.messages.human import HumanMessage, HumanMessageChunk
from langchain_core.messages.modifier import RemoveMessage
from langchain_core.messages.tool import (
  ToolCall, ToolCallChunk, InvalidToolCall, ToolMessage, ToolMessageChunk,
  ToolOutputMixin, 
  default_tool_parser, default_tool_chunk_parser, 
)
from langchain_core.messages.utils import (
  convert_to_messages, convert_to_openai_messages, filter_messages,
  message_chunk_to_message, messages_from_dict
)

#*======================================

class TypeMsg(t.EnumCustom):
    HUMAN = t.auto()
    HUMAN_MESSAGE_CHUNK = t.auto()
    SYSTEM = t.auto()
    SYSTEM_MESSAGE_CHUNK = t.auto()
    AI = t.auto()
    AI_MESSAGE_CHUNK = t.auto()
    CHAT = t.auto()
    CHAT_MESSAGE_CHUNK = t.auto()
    TOOL = t.auto()
    TOOL_MESSAGE_CHUNK = t.auto()
    FUNCTION = t.auto()
    FUNCTION_MESSAGE_CHUNK = t.auto()
    
    USER = t.auto()

#*======================================

def is_tool_calling(message: AIMessage):
  return len(message.tool_calls) > 0

def respond_tool_calling(response: str, message_ai: AIMessage):
  return ToolMessage(
    content=response,
    tool_call_id=message_ai.tool_calls[0]["id"],
  )
from __future__ import annotations
import packages

from context.utils import typer as t
from context.utils import consts as c
from context.infra.clients import logger

from abc import ABC, abstractmethod

from langchain_core.agents import (
  AgentAction, AgentActionMessageLog, AgentFinish, AgentStep
)
from langchain.agents.agent import (
  AgentExecutor, AgentOutputParser,
  BaseMultiActionAgent, BaseSingleActionAgent,
  MultiActionAgentOutputParser,
  RunnableAgent, RunnableMultiActionAgent,
  ExceptionTool
)
from langchain.agents.agent_iterator import AgentExecutorIterator

from langchain.agents.chat.output_parser import ChatOutputParser
from langchain.agents.structured_chat.output_parser import (
  StructuredChatOutputParser, StructuredChatOutputParserWithRetries
)
from langchain.agents.conversational.output_parser import ConvoOutputParser
from langchain.agents.output_parsers.json import JSONAgentOutputParser
from langchain.agents.output_parsers.xml import XMLAgentOutputParser
from langchain.agents.output_parsers.react_json_single_input import ReActJsonSingleInputOutputParser
from langchain.agents.output_parsers.react_single_input import ReActSingleInputOutputParser
from langchain.agents.react.output_parser import ReActOutputParser
from langchain.agents.output_parsers.self_ask import SelfAskOutputParser
from langchain.agents.output_parsers.tools import (
  ToolAgentAction, ToolsAgentOutputParser, parse_ai_message_to_tool_action
)

# from langchain.agents.conversational_chat.output_parser import ConvoOutputParser

from langchain.agents.schema import AgentScratchPadChatPromptTemplate
from langchain.agents.format_scratchpad.log import format_log_to_str
from langchain.agents.format_scratchpad.tools import format_to_tool_messages
from langchain.agents.format_scratchpad.xml import format_xml
from langchain.agents.format_scratchpad.log_to_messages import format_log_to_messages
from langchain.agents.format_scratchpad.openai_functions import (
  format_to_openai_function_messages, format_to_openai_functions
)

from langchain.agents.tools import InvalidTool

from langchain.agents import AgentType, initialize_agent
from langchain_community.agent_toolkits.load_tools import load_tools
# from langgraph.prebuilt import create_react_agent
from langchain.agents.self_ask_with_search.base import create_self_ask_with_search_agent
from langchain.agents.structured_chat.base import create_structured_chat_agent
from langchain.agents.tool_calling_agent.base import create_tool_calling_agent
from langchain.agents.xml.base import create_xml_agent
from langchain.agents.json_chat.base import create_json_chat_agent
from langchain.agents.agent_toolkits.conversational_retrieval.openai_functions import create_conversational_retrieval_agent


from langchain.agents.mrkl.base import ChainConfig
from langchain.agents.mrkl.output_parser import MRKLOutputParser

from langchain.agents.openai_assistant.base import (
  OpenAIAssistantAction, OpenAIAssistantFinish, OpenAIAssistantRunnable
)
from langchain.agents.output_parsers.openai_functions import OpenAIFunctionsAgentOutputParser
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser

from langchain.agents.openai_functions_agent.agent_token_buffer_memory import AgentTokenBufferMemory

from langchain.agents.openai_functions_agent.base import create_openai_functions_agent
from langchain.agents.openai_tools.base import create_openai_tools_agent
from langchain.agents.output_parsers.openai_tools import parse_ai_message_to_openai_tool_action

from langchain.agents.utils import validate_tools_single_input

#*==============================================================================
from toolkit.llm.langchain.models import messages as msgs_lc
from toolkit.llm.langchain.execution import graphs
from toolkit.llm.langchain.models import llms
#*==============================================================================

class TYPE_AGENT(t.EnumCustom):
  REACT = t.auto()
  SELF_ASK = t.auto()
  STRUCTURED_CHAT = t.auto()
  TOOL_CALLING = t.auto()
  XML = t.auto()
  JSON_CHAT = t.auto()

#*==============================================================================

def create_agent(
  type_agent: str
):
  pass

#*==============================================================================

class AgentBase(ABC):
  class State(t.TypedDict):
    # Inherit from parent State: class State(AgentBase.State, TypedDict):
    messages: t.Annotated[list[msgs_lc.AnyMessage], graphs.add_messages]
    user_query: str
    user_query_org: str
    user_query_category: t.Optional[str]
    result: t.Any
    data: t.Optional[t.Any]
    latest_agent: t.Optional[str]
    
  def __init__(
    self, 
    llm: llms.BaseChatModel=None,
    name: str="Agent", 
    memory=graphs.MemorySaver(),
    config=None,
    prompt_system=None,
    registry_agents: t.Dict[str, AgentBase]=None,
  ):
      self.name = name
      self.builder = graphs.StateGraph(AgentBase.State)
      self.core: graphs.CompiledStateGraph = None
      self.memory = memory
      self.config = {"configurable": {"thread_id": self.name}}
      self.llm = llm
      self.REGISTRY_AGENTS = registry_agents

      # Check if NODE is defined either as class attribute or instance attribute
      if not hasattr(self, 'node') and not hasattr(self.__class__, 'NODE'):
          raise TypeError(f"{self.__class__.__name__} must define either 'node' instance attribute or 'NODE' class attribute")

      # If node is not set as instance attribute but NODE exists as class attribute, use it
      if not hasattr(self, 'node') and hasattr(self.__class__, 'NODE'):
          self.node = self.__class__.NODE
      
      # self.build()
      
      pass

  class NODE(t.EnumCustom):
      CORE = t.auto()
      CLEAR_MSGS = t.auto()

  @staticmethod
  def static_method():
    pass
  
  def node_method(self, state: State) -> State:
    pass
  
  @abstractmethod
  def node_core(self):
    pass
  
  @abstractmethod
  def architect(self) -> graphs.CompiledStateGraph:
    # self.builder.compile(checkpointer=self.memory,)
    pass
  
  def build(self):
    logger.info(f"{c.EMOJI.COMPILE} 🤖 {c.CLR_TERM.GREEN}{self.name}{c.CLR_TERM.RESET} building")
    self.core = self.architect()
    logger.info(f"{c.EMOJI.DEPLOY} 🤖 {c.CLR_TERM.GREEN}{self.name}{c.CLR_TERM.RESET} built")
    pass
  
  async def get_user_msg(
    self, position: t.Literal["original", "latest"]="original"
  ):
    result = None
    
    state: graphs.StateSnapshot = self.core.get_state(config=self.config)
    msgs: list[msgs_lc.AnyMessage] = state.values["messages"]
    
    if position == "original":
      result = msgs[0].content
    elif position == "latest":
      print("hi")
      for m in reversed(msgs):
        if isinstance(m, msgs_lc.HumanMessage):
          result = m.content
          break
    
    print(result)
    return result
    
  async def get_agent_result(self):
    result = None
    
    try:
      state = self.core.get_state(self.config)
      
      result = state.values["result"]

      if isinstance(result, msgs_lc.AIMessage):
        result =  result.content
    except:
      pass
    
    return result
  
  async def format_agent_result(self):
    agent_result = await self.get_agent_result()
    # msgs_lc.AIMessage(str(f"Agent result: {agent_result}"))
    # return f"Agent {self.name}'s result: {agent_result}"
    return msgs_lc.AIMessage(f"Agent {self.name}'s result:\n{agent_result}")
  
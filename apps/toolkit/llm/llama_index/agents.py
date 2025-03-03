"""
This module provides comprehensive coverage of `Agents` within LlamaIndex.

Refs:
- https://docs.llamaindex.ai/en/stable/module_guides/deploying/agents/
- https://llamahub.ai/?tab=tools
"""
from typing import Literal

from llama_index.core.tools import (
	QueryEngineTool, RetrieverTool, ToolMetadata, QueryPlanTool, FunctionTool, BaseTool, 
 	ToolSelection, ToolOutput
)
from llama_index.core.program import (
	FunctionCallingProgram, LLMTextCompletionProgram,
)
from llama_index.core.tools.ondemand_loader_tool import OnDemandLoaderTool
from llama_index.core.tools.tool_spec.load_and_search import (
	LoadAndSearchToolSpec
)
from llama_index.core.agent import (
	ReActAgent, AgentRunner, StructuredPlannerAgent, FunctionCallingAgent,
	FnAgentWorker, FunctionCallingAgentWorker, 
	CustomSimpleAgentWorker, Task, AgentChatResponse
)
from llama_index.core.agent.types import (
	BaseAgent, BaseAgentWorker, Task, TaskStep, TaskStepOutput,
)

from llama_index.agent.openai import (
	OpenAIAgentWorker, OpenAIAgent, OpenAIAssistantAgent
)

from llama_index.core.agent.react.formatter import ReActChatFormatter
from llama_index.core.agent.react.output_parser import ReActOutputParser

from pydantic import Field
from loguru import logger

#*==============================================================================

def convert_query_plan_tool(
	query_plan_tool: QueryPlanTool,
	destination: Literal["langchain", "langchain_structured", "openai"],
):
	if destination == "openai":
		query_plan_tool = query_plan_tool.metadata.to_openai_tool()
	elif destination == "langchain":
		query_plan_tool = query_plan_tool.to_langchain_tool()
	elif destination == "langchain_structured":
		query_plan_tool = query_plan_tool.to_langchain_structured_tool()
	else:
		raise ValueError(f"Invalid destination: {destination}")
	return query_plan_tool

def add_tools(*args, **kwargs) -> list[FunctionTool]:
	"""
	Add tools to a list of tools.
	
	Args:
	*args: Variable length argument list. Each arg can be:
				- A single FunctionTool
				- A list of FunctionTools
				- A function to be converted to a FunctionTool
	**kwargs: Arbitrary keyword arguments. Each kwarg will be treated as:
						key: name for the tool
						value: function to be converted to a FunctionTool
	
	Returns:
	list: A list of FunctionTool objects
	"""
	tools = []
	
	for arg in args:
		if isinstance(arg, FunctionTool):
			tools.append(arg)
		elif isinstance(arg, list):
			tools.extend([item for item in arg if isinstance(item, FunctionTool)])
		elif callable(arg):
			tools.append(FunctionTool.from_defaults(fn=arg, name=arg.__name__))
	
	for name, func in kwargs.items():
		if callable(func):
			tools.append(FunctionTool.from_defaults(fn=func, name=name))
	
	return tools

#*------------------------------------------------------------------------------

from typing import List, Optional
from llama_index.core.llms.function_calling import FunctionCallingLLM
from llama_index.core.tools import BaseTool
from llama_index.core.agent import AgentRunner
from llama_index.agent.openai import OpenAIAgent

class MyAgent:
	def __init__(
		self,
		llm: FunctionCallingLLM,
		use_local_model: bool = False,
		tools: Optional[List[BaseTool]] = None,
		system_prompt: Optional[str] = None,
		verbose: bool = True,
		name: str = None,
	):
		"""
		Initialize MyAgent with configuration for either local or OpenAI agent.
		
		Args:
			llm (FunctionCallingLLM): The language model to use
			use_local_model (bool): Whether to use local model or OpenAI
			tools (List[BaseTool], optional): List of tools available to the agent
			system_prompt (str, optional): System prompt for the agent
			verbose (bool): Whether to enable verbose output
		"""
		self.llm = llm
		llm.system_prompt = system_prompt
		self.use_local_model = use_local_model
		self.tools = tools or []
		self.system_prompt = system_prompt
		self.verbose = verbose
  
		self.type = 'Local' if use_local_model else 'OpenAI'
		self.name = name

		self.agent = self.get_agent()

	def get_agent(self):
		"""
		Create and return either a local AgentRunner or OpenAIAgent based on configuration.
		
		Returns:
				Union[AgentRunner, OpenAIAgent]: The configured agent
		"""
		if self.use_local_model:
			agent = AgentRunner.from_llm(
				llm=self.llm,
				tools=self.tools,
				verbose=self.verbose,
				context=self.system_prompt,
			) 
		else:
			agent = OpenAIAgent.from_tools(
				tools=self.tools,
				verbose=self.verbose,
				system_prompt=self.system_prompt,
			)
		
		logger.info(f"Agent [{self.type}] {self.name} initialized")
		return agent

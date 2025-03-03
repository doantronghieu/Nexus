from __future__ import annotations
import packages

from context.utils import typer as t
from context.infra import clients
from context.utils.handlers import print_hldr
from context.infra.clients import logger, manager_mongodb

from toolkit.utils import utils
from toolkit.utils.utils import rp_print
from toolkit.utils.llm import main as utils_llm

import context.instances as inst
import context.consts as const
import context.settings.main as settings_main

from toolkit.llm.langchain.core import integration, utils as utils_lc
from toolkit.llm.langchain.data.indexing import (
    documents, document_loaders, text_splitters,
)
from toolkit.llm.langchain.data.persistence import retrievers
from toolkit.llm.langchain.execution import (
    runnables, graphs, tools, agents, tools as tools_lc
)
from toolkit.llm.langchain.models import (
    prompts as prompts_lc, llms, messages as msgs_lc,
)
#*==============================================================================
from services.llm.agents.vehicle.context import prompts_agent_control
from services.llm.agents.vehicle.tools.control import tool_vehicle_control

class NODE_CTRL(t.EnumCustom):
  SEPARATE_TASKS = t.auto()
  
class DATA_CTRL(t.EnumCustom):
  TASKS = t.auto()

class AgentControl(agents.AgentBase):
	def __init__(
		self, 
		name: str,
		node=NODE_CTRL,
	):
		super().__init__(name=name, llm=inst.llm_main)
		self.node = node
		self.build()
					
	@staticmethod
	def separate_tasks(parsed_query: str) -> list[str]:
		pass

	def node_separate_tasks(
		self,
		state: agents.AgentBase.State,
	) -> agents.AgentBase.State:
		pass

	@utils.print_async_function_name
	async def node_core(
		self, state: agents.AgentBase.State
	) -> agents.AgentBase.State:
		user_query = state['messages'][-1].content
		result = await tool_vehicle_control.execute(user_query)

		return {
			"result": result,
			"messages": [msgs_lc.AIMessage(str(result))],
		}

	def architect(self):
		self.builder.add_node(self.NODE.CORE, self.node_core)

		self.builder.add_edge(graphs.START, self.NODE.CORE)
		self.builder.add_edge(self.NODE.CORE, graphs.END)

		return self.builder.compile(checkpointer=self.memory)

agent_control = AgentControl(name="Control")
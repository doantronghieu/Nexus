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
from services.llm.agents.vehicle.context import prompts_agent_music
from services.llm.agents.vehicle.tools.music import tool_music

class NODE_MUSIC(t.EnumCustom):
	pass
  
class DATA_MUSIC(t.EnumCustom):
	pass

class AgentMusic(agents.AgentBase):
	def __init__(
    	self, 
     	name: str,
		node=NODE_MUSIC,
    ):
		super().__init__(name=name, llm=inst.llm_main)
		self.node = node
		self.build()
					
	@utils.print_async_function_name
	async def node_core(
    	self, state: agents.AgentBase.State
    ) -> agents.AgentBase.State:
		user_query = state['messages'][-1].content
		result = await tool_music.execute(user_query)

		return {
			"result": result,
			"messages": [msgs_lc.AIMessage(str(result))],
		}

	def architect(self):
		self.builder.add_node(self.NODE.CORE, self.node_core)

		self.builder.add_edge(graphs.START, self.NODE.CORE)
		self.builder.add_edge(self.NODE.CORE, graphs.END)

		return self.builder.compile(checkpointer=self.memory)

agent_music = AgentMusic(name="Music")
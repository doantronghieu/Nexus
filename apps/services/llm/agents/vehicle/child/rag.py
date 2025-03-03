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
from services.llm.agents.vehicle.context import prompts_agents_rag

class NODE_RAG(t.EnumCustom):
	RETRIEVE = t.auto()

class DATA_RAG(t.EnumCustom):
	RETRIEVED_DATA = t.auto()

class AgentRAG(agents.AgentBase):
	def __init__(
		self, 
		name: str,
		node=NODE_RAG,
		retriever = inst.retrievers_qdrant["vehicle"]
	):
		super().__init__(name=name, llm=inst.llm_main)

		self.node = node
		self.retriever = retriever
		self.build()
					
	@utils.print_async_function_name
	async def node_retrieve(
		self, state: agents.AgentBase.State
	) -> agents.AgentBase.State:
		user_query = state['messages'][-1].content
		
		retrieved_data = await self.retriever.ainvoke(user_query)
		retrieved_data = await retrievers.extract_retriever_results(retrieved_data)
		
		return {
			"data": {
				DATA_RAG.RETRIEVED_DATA: retrieved_data,
			},
		}

	@utils.print_async_function_name
	async def node_core(
		self, state: agents.AgentBase.State
	) -> agents.AgentBase.State:
		user_query = state['messages'][-1].content
		
		prompt_tpl = prompts_lc.ChatPromptTemplate([
			("system", prompts_agents_rag["system"]),
			("human", prompts_agents_rag["generate"]),
		])

		prompt = await prompt_tpl.ainvoke({
			"user_query": user_query,
			"retrieved_data": state["data"][DATA_RAG.RETRIEVED_DATA],
		})

		result = await inst.llm_main.ainvoke(prompt)
		
		return {
			"result": result,
			"messages": msgs_lc.AIMessage(str(result)),
		}

	async def node_delete_all_messages(
		self, state: agents.AgentBase.State
	) -> agents.AgentBase.State:
		messages: list[msgs_lc.AnyMessage] = state["messages"]
		return {"messages": [msgs_lc.RemoveMessage(id=m.id) for m in messages]}
							
	def architect(self):
		self.builder.add_node(self.node.RETRIEVE, self.node_retrieve)
		self.builder.add_node(self.NODE.CORE, self.node_core)

		self.builder.add_edge(graphs.START, self.node.RETRIEVE)
		self.builder.add_edge(self.node.RETRIEVE, self.NODE.CORE)

		# self.builder.add_edge(self.NODE.CORE, graphs.END)
		self.builder.add_node(self.NODE.CLEAR_MSGS, self.node_delete_all_messages)
		self.builder.add_edge(self.NODE.CORE, self.NODE.CLEAR_MSGS)
		self.builder.add_edge(self.NODE.CLEAR_MSGS, graphs.END)

		return self.builder.compile(checkpointer=self.memory)

agent_rag = AgentRAG(name="RAG")
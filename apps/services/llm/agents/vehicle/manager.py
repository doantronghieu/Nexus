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
from services.llm.agents.vehicle.child.control import agent_control
from services.llm.agents.vehicle.child.music import agent_music
from services.llm.agents.vehicle.child.navigation import agent_navigation
from services.llm.agents.vehicle.child.rag import agent_rag
#*==============================================================================
from services.llm.agents.vehicle.context import prompts_agents_main,  prompts_agents_vehicle

class NODE_MAIN(t.EnumCustom):
	CATEGORIZE_QUERY = t.auto()
	AGENT_RAG = t.auto()
	AGENT_CONTROL = t.auto()
	AGENT_NAVIGATION = t.auto()
	AGENT_MUSIC = t.auto()

class DATA_MAIN(t.EnumCustom):
	RESULT_AGENT_RAG = t.auto()
	RESULT_AGENT_CONTROL = t.auto()
	RESULT_AGENT_NAVIGATION = t.auto()
	RESULT_AGENT_MUSIC = t.auto()

REGISTRY_AGENTS_MAIN: t.Dict[str, agents.AgentBase] = {}
REGISTRY_AGENTS_MAIN[NODE_MAIN.AGENT_RAG] = agent_rag
REGISTRY_AGENTS_MAIN[NODE_MAIN.AGENT_CONTROL] = agent_control
REGISTRY_AGENTS_MAIN[NODE_MAIN.AGENT_NAVIGATION] = agent_navigation
REGISTRY_AGENTS_MAIN[NODE_MAIN.AGENT_MUSIC] = agent_music

T_USER_QUERY_CATEGORY: t.TypeAlias = t.Literal[
  "car_manual", "car_control", "navigation", "general", "music"
]

CATEGORY_2_AGENT: t.Dict[str, str] = {
	"car_manual": NODE_MAIN.AGENT_RAG,
	"car_control": NODE_MAIN.AGENT_CONTROL,
	"navigation": NODE_MAIN.AGENT_NAVIGATION,
	"music": NODE_MAIN.AGENT_MUSIC,
}

class AgentMain(agents.AgentBase):
	def __init__(
		self, 
		name: str,
		node=NODE_MAIN,
	):
		super().__init__(
			name=name, llm=inst.llm_main, registry_agents=REGISTRY_AGENTS_MAIN
		)
		self.node = node
		self.build()
		
	@staticmethod
	@utils.print_async_function_name
	async def categorize_query(user_query: str) -> T_USER_QUERY_CATEGORY:
		result = None
		
		examples = await inst.retrievers_qdrant["user_query_category"].ainvoke(user_query)
		examples = await retrievers.extract_retriever_results(examples)

		prompt = prompts_lc.PromptTemplate.from_template(prompts_agents_vehicle["categorize_query"])
		prompt = await prompt.ainvoke({
			"user_query": user_query,
			"examples": examples,
		})
	
		result = await inst.llm_main.ainvoke(prompt)
		result = result.content

		return result

	@utils.print_async_function_name
	async def node_core(
		self, state: agents.AgentBase.State
	) -> graphs.Command[
			t.Literal[
				NODE_MAIN.AGENT_RAG, NODE_MAIN.AGENT_CONTROL, 
				NODE_MAIN.AGENT_NAVIGATION, NODE_MAIN.AGENT_MUSIC,
				graphs.END,
			]
		]:

		result: agents.AgentBase.State = {}
		
		user_query = state["messages"][-1].content

		latest_agent = state.get("latest_agent", None)

		if latest_agent is None:
			user_query_category = await AgentMain.categorize_query(user_query)
			agent_name = CATEGORY_2_AGENT[user_query_category]

			await clients.namespace_redis_llm.set_value(
				"agent", { "current": agent_name }
			)

			return graphs.Command(
				goto=agent_name,
				update={
					"user_query": user_query,
					"messages": [msgs_lc.AIMessage(str(f"User query category: {user_query_category}"))],
					"latest_agent": agent_name,
				}
			)
		else:
			agent_name = state['latest_agent']
			
			await clients.namespace_redis_llm.set_value(
				"agent", { "current": "manager" }
			)

			child_agent_result = await self.REGISTRY_AGENTS[agent_name].get_agent_result()
			child_agent_msg = await self.REGISTRY_AGENTS[agent_name].format_agent_result()

			prompt_tpl = prompts_lc.PromptTemplate.from_template(prompts_agents_main["system"])
			
			prompt = await prompt_tpl.ainvoke({
				"user_input": user_query,
				"child_agent_result": child_agent_result,
			})

			result: msgs_lc.AIMessage = await self.llm.ainvoke(prompt)
			
			final_msg = result
   
			# final_msg = msgs_lc.AIMessage(f"Final result:\n{child_agent_msg.content}")
   
		return graphs.Command(
				goto=graphs.END,
				update={
					"result": final_msg.content,
					"messages": [final_msg],
					"latest_agent": None,
					"user_query": None,
					"user_query_org": None,
					"user_query_category": None,
				}
			)
	
	def architect(self):
		
		self.builder.add_node(self.NODE.CORE, self.node_core)
		self.builder.add_node(self.node.AGENT_RAG, self.node_agent_rag)
		self.builder.add_node(self.node.AGENT_CONTROL, self.node_agent_control)
		self.builder.add_node(self.node.AGENT_NAVIGATION, self.node_agent_navigation)
		self.builder.add_node(self.node.AGENT_MUSIC, self.node_agent_music)

		self.builder.add_edge(graphs.START, self.NODE.CORE)

		return self.builder.compile(checkpointer=self.memory)
	
	@utils.print_async_function_name
	async def node_agent_rag(
		self,
		state: agents.AgentBase.State,
	) -> graphs.Command[t.Literal[AgentMain.NODE.CORE]]:

		result = await agent_rag.core.ainvoke(
			input={"messages": [("user", state["user_query"])]}, config=agent_rag.config,
		)
		result = await agent_rag.get_agent_result()
		msg = await agent_rag.format_agent_result()
	
		return graphs.Command(
			goto=AgentMain.NODE.CORE,
			update={
				"data": {
					DATA_MAIN.RESULT_AGENT_RAG: result,
				},
				"messages": [msg],
			}
		)

	@utils.print_async_function_name
	async def node_agent_control(
		self,
		state: agents.AgentBase.State,
	) -> graphs.Command[t.Literal[AgentMain.NODE.CORE]]:

		result = await agent_control.core.ainvoke(
			input={"messages": [("user", state["user_query"])]}, config=agent_control.config
		)
		result = await agent_control.get_agent_result()
		msg = await agent_control.format_agent_result()

		return graphs.Command(
			goto=AgentMain.NODE.CORE,
			update={
				"data": {
					DATA_MAIN.RESULT_AGENT_CONTROL: result,
				},
				"messages": [msg],
			}
		)

	@utils.print_async_function_name
	async def node_agent_navigation(
		self,
		state: agents.AgentBase.State,
	) -> graphs.Command[t.Literal[AgentMain.NODE.CORE]]:

		result = await agent_navigation.core.ainvoke(
			input={"messages": [("user", state["user_query"])]}, config=agent_navigation.config
		)
		result = await agent_navigation.get_agent_result()
		msg = await agent_navigation.format_agent_result()

		return graphs.Command(
			goto=AgentMain.NODE.CORE,
			update={
				"data": {
					DATA_MAIN.RESULT_AGENT_NAVIGATION: result,
				},
				"messages": [msg],
			}
		)

	@utils.print_async_function_name
	async def node_agent_music(
		self,
		state: agents.AgentBase.State,
	) -> graphs.Command[t.Literal[AgentMain.NODE.CORE]]:

		result = await agent_music.core.ainvoke(
			input={"messages": [("user", state["user_query"])]}, config=agent_music.config
		)
		result = await agent_music.get_agent_result()
		msg = await agent_music.format_agent_result()

		return graphs.Command(
			goto=AgentMain.NODE.CORE,
			update={
				"data": {
					DATA_MAIN.RESULT_AGENT_MUSIC: result,
				},
				"messages": [msg],
			}
		)

agent_main = AgentMain(name="Main")
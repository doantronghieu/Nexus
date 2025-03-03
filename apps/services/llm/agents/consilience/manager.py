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
# from services.llm.agents.consilience.child
#*==============================================================================
from services.llm.agents.consilience.context import (
	prompts_agents_consilience, prompts_agent_main
)

class NODE_MAIN(t.EnumCustom):
	CATEGORIZE_QUERY = t.auto()
	AGENT_RAG = t.auto()

class DATA_MAIN(t.EnumCustom):
	RESULT_AGENT_RAG = t.auto()

REGISTRY_AGENTS_MAIN: t.Dict[str, agents.AgentBase] = {}
# REGISTRY_AGENTS_MAIN[NODE_MAIN.AGENT_RAG] = agent_rag

T_USER_QUERY_CATEGORY: t.TypeAlias = t.Literal[
  "rag",
]

CATEGORY_2_AGENT: t.Dict[str, str] = {
	"rag": NODE_MAIN.AGENT_RAG,
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

		prompt = prompts_lc.PromptTemplate.from_template(prompts_agents_consilience["categorize_query"])
		prompt = await prompt.ainvoke({
			"user_query": user_query,
			"examples": examples,
		})
	
		result = await inst.llm_main.ainvoke(prompt)
		result = result.content

		return result

	# @utils.print_async_function_name
	# async def node_core(
	# 	self, state: agents.AgentBase.State
	# ) -> graphs.Command[
	# 		t.Literal[
	# 			NODE_MAIN.AGENT_RAG,
	# 			graphs.END,
	# 		]
	# 	]:

	# 	result: agents.AgentBase.State = {}
		
	# 	user_query = state["messages"][-1].content

	# 	latest_agent = state.get("latest_agent", None)

	# 	if latest_agent is None:
	# 		user_query_category = await AgentMain.categorize_query(user_query)
	# 		agent_name = CATEGORY_2_AGENT[user_query_category]

	# 		await clients.namespace_redis_llm.set_value(
	# 			"agent", { "current": agent_name }
	# 		)

	# 		return graphs.Command(
	# 			goto=agent_name,
	# 			update={
	# 				"user_query": user_query,
	# 				"messages": [msgs_lc.AIMessage(str(f"User query category: {user_query_category}"))],
	# 				"latest_agent": agent_name,
	# 			}
	# 		)
	# 	else:
	# 		agent_name = state['latest_agent']
			
	# 		await clients.namespace_redis_llm.set_value(
	# 			"agent", { "current": "manager" }
	# 		)

	# 		child_agent_result = await self.REGISTRY_AGENTS[agent_name].get_agent_result()
	# 		child_agent_msg = await self.REGISTRY_AGENTS[agent_name].format_agent_result()

	# 		prompt_tpl = prompts_lc.PromptTemplate.from_template(prompts_agents_consilience["system"])
			
	# 		prompt = await prompt_tpl.ainvoke({
	# 			"user_input": user_query,
	# 			"child_agent_result": child_agent_result,
	# 		})

	# 		result: msgs_lc.AIMessage = await self.llm.ainvoke(prompt)
			
	# 		final_msg = result
   
	# 		# final_msg = msgs_lc.AIMessage(f"Final result:\n{child_agent_msg.content}")
   
	# 	return graphs.Command(
	# 			goto=graphs.END,
	# 			update={
	# 				"result": final_msg.content,
	# 				"messages": [final_msg],
	# 				"latest_agent": None,
	# 				"user_query": None,
	# 				"user_query_org": None,
	# 				"user_query_category": None,
	# 			}
	# 		)

	@utils.print_async_function_name
	async def node_core(
		self, state: agents.AgentBase.State
	) -> graphs.Command[
			t.Literal[
				graphs.END,
			]
		]:

		result: agents.AgentBase.State = {}
		
		user_query = state["messages"][-1].content

		prompt_tpl = prompts_lc.ChatPromptTemplate([
			("human", prompts_agent_main["system_tesla"]),
		])

		prompt = await prompt_tpl.ainvoke({
			"user_query": user_query,
		})

		result: msgs_lc.AIMessage = await inst.llm_main.ainvoke(prompt)
		final_msg = result

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
		# self.builder.add_node(self.node.AGENT_RAG, self.node_agent_rag)

		self.builder.add_edge(graphs.START, self.NODE.CORE)

		return self.builder.compile(checkpointer=self.memory)
	
agent_main = AgentMain(name="Main")

"""
tests = [
	"Hello",
]

user_input = tests[0]
	
async for event in agent_main.core.astream(
    input={"messages": [("user", user_input)]},
    config=agent_main.config, 
    stream_mode="updates",
    subgraphs=True
):
    graphs.print_graph_event(event)

result = await agent_main.core.ainvoke(
  input={"messages": [("user", user_input)]}, config=agent_main.config, 
)
result = await agent_main.get_agent_result()
"""
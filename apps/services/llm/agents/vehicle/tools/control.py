import packages

from context.utils import typer as t
from context.infra.clients import logger, manager_mongodb

from toolkit.utils import utils
from toolkit.utils.utils import rp_print
from toolkit.utils.llm import main as utils_llm

import context.instances as inst

from toolkit.llm.langchain.data.persistence import retrievers

from toolkit.llm.langchain.models import prompts as prompts_lc
from services.llm.agents.vehicle.context import prompts_agent_control
#*==============================================================================
collection = manager_mongodb.get_collection("vehicles")
vehicle_id = "v123"

class ToolVehicleControl:
	def __init__(self):
		self.collection = manager_mongodb.get_collection("vehicles")
		self.vehicle_id = "v123"
  
	@utils.print_async_function_name
	async def parse_user_query(
		self, 
		user_query: str = t.Field(description="User input into the tool")
	) -> t.Dict[str, t.Any]:
		"""Parse user input to determine the intended action and extract relevant information."""
		logger.info(f"Parsing user query: {user_query}")

		field_paths = await inst.retrievers_qdrant["vehicle_properties_field_paths"].ainvoke(user_query)
		field_paths = await retrievers.extract_retriever_results(field_paths)

		fields_and_values = await self.collection.get_multiple_fields(
			doc_id=self.vehicle_id, field_paths=field_paths
		)
		fields_and_values = fields_and_values["fields"]
	
		prompt_tpl = prompts_lc.PromptTemplate.from_template(prompts_agent_control["parse_query"]["prompt"])

		prompt_examples = await utils_llm.convert_examples_to_string(
    	prompts_agent_control["parse_query"]["examples"]
  	)
		
		prompt = await prompt_tpl.aformat(
			examples = prompt_examples,
			user_query = user_query,
			fields_and_values = fields_and_values
		)

		result = await inst.llm_main.ainvoke(prompt)
		result = result.content
		result = await utils_llm.parse_json(result)

		logger.info(f"Parsed user query result: {result}")

		return result
	
	@utils.print_async_function_name
	async def execute(self, user_query: str):
		"""Execute the appropriate database operation based on the parsed user input."""
  
		logger.info(f"Processing user query: {user_query}")
		result = None

		query_parsed = await self.parse_user_query(user_query)

		action = query_parsed.get("action", "")
		field_path = query_parsed.get("field_path", "")
		new_value = query_parsed.get("new_value", None)

		if action == "get":
			op_result = await self.collection.get_field(self.vehicle_id, field_path)
		elif action == "update":
			op_result = await self.collection.update_field(self.vehicle_id, field_path, new_value)
		else:
			logger.warning(f"Unsupported action: {action}")
			return {'success': False, 'message': f"Unsupported action: {action}"}
		
		logger.info(f"User query processed successfully")
		result = {
			"query": user_query,
			"success": op_result["success"],
			"operation": query_parsed,
		}
  
		if op_result.get("value", None) is not None:
			result["result"] = op_result["value"]
		
		return result
#*==============================================================================
tool_vehicle_control = ToolVehicleControl()
#*==============================================================================
# tests = [
# 	"What's the current fan speed?",
# 	"Set the driver's temperature to 23 degrees",
# ]
# result = await tool_vehicle_control.execute(tests[0])
# rp_print(result)
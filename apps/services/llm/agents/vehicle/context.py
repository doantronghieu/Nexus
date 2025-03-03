import packages
from context.utils import typer as t
from toolkit.utils import utils

with open(f"{packages.APP_PATH}/services/llm/agents/vehicle/prompts.yaml", 'r') as file:
  prompts_agents_vehicle: t.Prompts = utils.yaml.safe_load(file)

prompts_agents_main = prompts_agents_vehicle["main"]
prompts_agents_rag = prompts_agents_vehicle["rag"]
prompts_agent_control = prompts_agents_vehicle["control"]
prompts_agent_general = prompts_agents_vehicle["general"]
prompts_agent_navigation = prompts_agents_vehicle["navigation"]
prompts_agent_music = prompts_agents_vehicle["music"]
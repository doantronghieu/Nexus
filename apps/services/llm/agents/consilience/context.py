import packages
from context.utils import typer as t
from toolkit.utils import utils

with open(f"{packages.APP_PATH}/services/llm/agents/Consilience/prompts.yaml", 'r') as file:
  prompts_agents_consilience: t.Prompts = utils.yaml.safe_load(file)

prompts_agents_main = prompts_agents_consilience["main"]
prompts_agents_rag = prompts_agents_consilience["rag"]
prompts_agent_action = prompts_agents_consilience["action"]
prompts_agent_query = prompts_agents_consilience["query"]
prompts_agent_data = prompts_agents_consilience["data"]

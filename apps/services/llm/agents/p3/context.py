import packages
from context.utils import typer as t
from toolkit.utils import utils

with open(f"{packages.APP_PATH}/services/llm/agents/p3/prompts.yaml", 'r') as file:
  prompts_agents_p3: t.Prompts = utils.yaml.safe_load(file)

prompts_agent_main = prompts_agents_p3["main"]

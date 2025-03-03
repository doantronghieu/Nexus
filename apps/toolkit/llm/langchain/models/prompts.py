import packages
import yaml

from context.utils import typer as t

from langchain_core.prompt_values import (
  PromptValue, ChatPromptValue, ChatPromptValueConcrete, StringPromptValue,
  ImagePromptValue, ImageURL,
)

from langchain_core.prompts import (
  ChatPromptTemplate, PromptTemplate, MessagesPlaceholder
)

from langchain_core.prompts.base import BasePromptTemplate
from langchain_core.prompts.chat import (
  BaseMessagePromptTemplate, BaseStringMessagePromptTemplate, 
  ChatMessagePromptTemplate, BaseChatPromptTemplate, MessagesPlaceholder,
  AIMessagePromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, 
)

from langchain_core.prompts.few_shot import (
  FewShotPromptTemplate, FewShotChatMessagePromptTemplate
)
from langchain_core.prompts.few_shot_with_templates import FewShotPromptWithTemplates

from langchain_core.prompts.image import ImagePromptTemplate
from langchain_core.prompts.string import (
  StringPromptTemplate, check_valid_template, get_template_variables, 
  jinja2_formatter, validate_jinja2,
  mustache_formatter, mustache_schema, mustache_template_vars
)

from langchain_core.prompts.loading import load_prompt, load_prompt_from_config

from langchain_core.example_selectors.base import BaseExampleSelector
from langchain_core.example_selectors.semantic_similarity import SemanticSimilarityExampleSelector
#*======================================

YAMLValue: t.TypeAlias = t.Union[str, t.Dict[str, 'YAMLValue']]

with open(f"{packages.APP_PATH}/toolkit/llm/langchain/models/prompts.yaml", 'r') as file:
  prompts: t.Dict[str, YAMLValue] = yaml.safe_load(file)

# with open(f"{packages.APP_PATH}/toolkit/llm/langchain/models/prompts.yaml", 'r') as file:
#   prompts = yaml.safe_load(file)
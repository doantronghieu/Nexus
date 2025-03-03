import packages
from context.utils import typer as t

from langchain_core.runnables.base import (
  Runnable, RunnableSerializable,
  RunnableBindingBase, RunnableBinding,
  RunnableEachBase, RunnableEach,
  RunnableGenerator, RunnableLambda, 
  RunnableParallel, RunnableSequence,
  chain, coerce_to_runnable,
)
from langchain_core.runnables import RunnablePassthrough, RunnableConfig, chain
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain_core.runnables.config import (
  RunnableConfig, ContextThreadPoolExecutor,
  acall_func_with_variable_args, ensure_config, get_async_callback_manager_for_config,
  get_config_list, get_executor_for_config, run_in_executor,
  merge_configs, patch_config,
)
from langchain_core.runnables.configurable import (
  DynamicRunnable, RunnableConfigurableAlternatives, RunnableConfigurableFields,
  make_options_spec, prefix_config_spec,
)
from langchain_core.runnables.fallbacks import RunnableWithFallbacks
from langchain_core.runnables.passthrough import (
  RunnableAssign, RunnablePassthrough, RunnablePick,
  aidentity,
)

from langchain_core.runnables.retry import RunnableRetry
from langchain_core.runnables.router import RouterRunnable

from langchain_core.runnables.schema import (
  BaseStreamEvent, CustomStreamEvent, EventData, StandardStreamEvent
)

from langchain_core.runnables.utils import (
  AddableDict, ConfigurableField, ConfigurableFieldSpec, 
  ConfigurableFieldMultiOption, ConfigurableFieldSingleOption,
  FunctionNonLocals, GetLambdaSource,
  IsFunctionArgDict, IsLocalDict, get_function_first_arg_dict_keys,
  aadd, 
  accepts_config, accepts_run_manager,
  gated_coro, gather_with_concurrency,
)

from langchain.runnables.hub import HubRunnable

#*======================================

from toolkit.llm.langchain.models import messages

#*======================================

class TypeRunnable(t.EnumCustom):
  LLM = t.auto()
  AGENT = t.auto()
  GRAPH = t.auto()

class TypeInteract(t.EnumCustom):
  INVOKE = t.auto()
  STREAM = t.auto()
  
async def interact_runnable(
  runnable: t.Union[Runnable, RunnableSerializable], 
  type_runnable: str, type_interact: str,
  prompt: t.Optional[str]="{user_query}", system_prompt: t.Optional[str]=None,
  user_query: t.Optional[str]=None,
  **kwargs,
) -> t.Union[t.Any, messages.BaseMessage, t.Iterator[messages.BaseMessageChunk]]:
  pass

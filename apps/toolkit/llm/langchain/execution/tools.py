import packages

from context.utils import typer as t

# https://python.langchain.com/docs/integrations/tools/
from langchain_core.tools.base import (
    BaseTool, BaseToolkit,
    InjectedToolArg, InjectedToolCallId,
    SchemaAnnotationError, ToolException,
    create_schema_from_function, get_all_basemodel_annotations,
)
from langchain_core.tools import Tool
from langchain_core.tools.structured import StructuredTool

from langchain_core.tools.convert import tool, convert_runnable_to_tool
from langchain_core.tools.render import render_text_description_and_args

from langchain_core.tools.retriever import RetrieverInput, create_retriever_tool

from langchain_community.tools import ShellTool
from langchain_experimental.utilities import PythonREPL
from langchain_community.agent_toolkits import FileManagementToolkit

from langchain_community.tools import BraveSearch
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools import TavilySearchResults
from langchain_community.utilities import SerpAPIWrapper
from langchain_community.tools import YouTubeSearchTool

from langchain_community.agent_toolkits import JsonToolkit, create_json_agent
from langchain_community.tools.json.tool import JsonSpec

from langchain_community.utilities import OpenWeatherMapAPIWrapper

from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import (
    create_async_playwright_browser,  # A synchronous browser is available, though it isn't compatible with jupyter.\n",	  },
)

from langchain_community.agent_toolkits.openapi.toolkit import RequestsToolkit
from langchain_community.utilities.requests import TextRequestsWrapper

from langchain_community.agent_toolkits import SparkSQLToolkit, create_spark_sql_agent
from langchain_community.utilities.spark_sql import SparkSQL
# from pyspark.sql import SparkSession

import sqlite3
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from sqlalchemy import create_engine as create_sql_engine
from sqlalchemy.pool import StaticPool as SqlStaticPool
from langchain_community.tools.sql_database.tool import (
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
    QuerySQLCheckerTool,
    QuerySQLDatabaseTool,
)

from tempfile import TemporaryDirectory

#*======================================

tool_search_tavily = TavilySearchResults(max_results=2)

#*--------------------------------------

@tool
def tool_python_repl(
    code: t.Annotated[str, "The python code to execute to generate your chart."],
):
    """Use this to execute python code. If you want to see the output of a value,
    you should print it out with `print(...)`. This is visible to the user."""
    repl = PythonREPL()
    
    try:
        result = repl.run(code)
    except BaseException as e:
        return f"Failed to execute. Error: {repr(e)}"
    result_str = f"Successfully executed:\n\`\`\`python\n{code}\n\`\`\`\nStdout: {result}"
    return (
        result_str + "\n\nIf you have completed all tasks, respond with FINAL ANSWER."
    )
import packages
from context.utils import typer as t

import operator

from toolkit.llm.langchain.models import messages as msgs_lc

from langchain_core.runnables.graph import (
  Branch, Node, Edge, Graph,
  LabelsDict, NodeStyles, CurveStyle, MermaidDrawMethod,
  is_uuid, node_data_json, node_data_str,
)
from langgraph.graph import (
  StateGraph, START, END, MessagesState
)
from langgraph.graph.graph import CompiledGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.graph.message import add_messages
# from langgraph.prebuilt import (
#   ToolNode, ToolExecutor, ToolInvocation, tools_condition,
#   ValidationNode,  InjectedState
# )
from langgraph.config import get_stream_writer
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.memory import MemorySaver
# from langgraph.checkpoint.postgres import PostgresSaver
# from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from langgraph.types import StateSnapshot, Command, interrupt

from langchain_core.runnables.graph_ascii import (
  AsciiCanvas, VertexViewer, draw_ascii,
)
from langchain_core.runnables.graph_mermaid import draw_mermaid, draw_mermaid_png
from langchain_core.runnables.graph_png import PngDrawer

from IPython.display import Image, display

#*======================================

#*======================================

def display_graph(graph: CompiledGraph):
  display(Image(graph.get_graph().draw_mermaid_png()))

def get_lastest_message(state: MessagesState):
  result = state["messages"][-1]
  return result

def manipulate_message(
  message: msgs_lc.AnyMessage,
  type_msg: str=msgs_lc.TypeMsg.HUMAN,
  name: str=None,
) -> msgs_lc.AnyMessage:
  message_class = None
  
  if type_msg == msgs_lc.TypeMsg.HUMAN:
    message_class = msgs_lc.HumanMessage
  
  message_new = message_class(
    content=message.content, name=name,
  )
  
  return message_new

def get_snapshot(graph: CompiledGraph, config: dict):
  return graph.get_state(config)

def get_next_snapshot(snapshot: StateSnapshot):
  return snapshot.next

def update_last_tool_calling(graph: CompiledGraph, config: dict, input_new: str):
  snapshot = get_snapshot(graph, config)
  message_current: msgs_lc.AIMessage = snapshot.values["messages"][-1]

  tool_call_new = message_current.tool_calls[0].copy()
  tool_call_new["args"]["query"] = input_new

  message_new = msgs_lc.AIMessage(
    content=message_current.content,
    tool_calls=[tool_call_new],
    id=message_current.id,
  )
  
  graph.update_state(config, {"messages": [message_new]})

  return graph

def get_available_next_agents(all_agents: list[str], current_agent: str) -> list[str]:
  """
  Returns a list of available agent names for next state transition, 
  excluding the current agent.
  
  Args:
      all_agents (list[str]): List of all agent names
      current_agent (str): Name of the current agent
      
  Returns:
      list[str]: List of agent names available for next transition
      
  Example:
      >>> get_available_next_agents(['agent_1', 'agent_2', 'agent_3'], 'agent_1')
      ['agent_2', 'agent_3']
  """
  return [agent for agent in all_agents if agent != current_agent]

#*==============================================================================
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.theme import Theme

def print_graph_event(event):
    """
    Print event information using rich formatting.
    Displays node name as title and message content in panel with message type indication.
    
    Args:
        event (tuple): Event tuple containing args and kwargs
    """
    custom_theme = Theme({
        "info": "light_slate_blue",
        "title": "dark_orange",
    })
    
    console = Console(theme=custom_theme)
    _, kwargs = event
    
    for node_name, data in kwargs.items():
        # Extract latest message if available
        if 'messages' in data and data['messages']:
            message = data['messages'][-1]
            
            # Determine message type
            is_human = 'Human' in message.__class__.__name__
            inner_panel_style = "cyan" if is_human else "yellow"
            msg_type = "Human Message" if is_human else "AI Message"
            
            # Create inner panel for message
            inner_panel = Panel(
                Text(message.content, style="info"),
                title=msg_type,
                title_align="left",
                border_style=inner_panel_style,
                padding=(0, 1)
            )
            
            # Create outer panel with node name
            outer_panel = Panel(
                inner_panel,
                title=f"[title]{node_name}[/title]",
                padding=(1, 1)
            )
            
            console.print(outer_panel)

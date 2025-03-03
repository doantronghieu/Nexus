from typing import List, Dict, Optional
from llama_index.core.llms.function_calling import FunctionCallingLLM
from llama_index.core import Settings
from llama_index.core.tools import BaseTool, FunctionTool
from llama_index.core.agent.types import BaseAgent
from llama_index.agent.openai import OpenAIAgent
from llama_index.core import ChatPromptTemplate
from llama_index.core.llms import ChatMessage
from llama_index.core.embeddings import BaseEmbedding
from llama_index.core.retrievers import BaseRetriever
import json
import os

class AgentBuilder:
    """
    A class for building and managing a single AI agent with customizable tools and prompts.
    """

    def __init__(self, llm: FunctionCallingLLM, embed_model: BaseEmbedding, tool_retriever: BaseRetriever):
        """
        Initialize the AgentBuilder.

        Args:
            llm (FunctionCallingLLM): The language model to use for generating responses.
            embed_model (BaseEmbedding): The embedding model for text representations.
            tool_retriever (BaseRetriever): The retriever for finding relevant tools.
        """
        self.llm = llm
        Settings.llm = self.llm
        Settings.embed_model = embed_model
        
        self.tool_retriever = tool_retriever
        self.tool_dict: Dict[str, BaseTool] = {}
        
        self._setup_prompts()
        self.agent: BaseAgent = self._create_or_update_agent()

    def _setup_prompts(self) -> None:
        """Set up the prompts for generating system prompts."""
        self.gen_sys_prompt_str = """
        You are an expert in crafting effective system prompts for AI language models. Your task is to create a comprehensive system prompt for an AI-powered bot that will be used to solve the following task:

        {task}

        Please generate a system prompt that includes:

        1. A clear definition of the bot's role and purpose
        2. Any necessary background information or context
        3. Specific instructions on how to approach the task
        4. Guidelines for tone, style, and format of responses
        5. Any constraints or limitations the bot should adhere to
        6. Examples of good responses, if applicable

        The system prompt should be detailed enough to guide the AI in producing high-quality, relevant responses while being concise and avoiding unnecessary information. After generating the prompt, please provide a brief explanation of your choices and how they relate to the given task.
        """

    def _create_or_update_agent(self, system_prompt: Optional[str] = None) -> BaseAgent:
        """
        Create a new agent or update the existing one with the given system prompt and tools.

        Args:
            system_prompt (Optional[str]): The system prompt for the agent. If None, a default prompt is used.

        Returns:
            BaseAgent: The created or updated agent.
        """
        if system_prompt is None:
            system_prompt = """
            You are an AI assistant specializing in the construction and operation of task-specific AI agents. Your capabilities include:

            1. Creating System Prompts: You can generate comprehensive system prompts that define an agent's role, capabilities, and behavioral guidelines.
            2. Identifying Necessary Tools: You can analyze tasks and determine the most suitable set of tools for an agent to accomplish its goals effectively.
            3. Assembling and Updating Agents: You can integrate system prompts and selected tools to construct or update fully functional agents.
            4. Executing Tasks: You can perform various tasks using the tools at your disposal.

            When given a task, follow these steps:
            1. Analyze the task requirements.
            2. If needed, create or update the system prompt to better suit the task.
            3. Identify and acquire any necessary tools for the task.
            4. Execute the task using your capabilities and available tools.
            5. Provide a clear and concise response or summary of actions taken.

            Always strive to provide accurate, helpful, and ethical responses. If you encounter any ambiguities or need more information, ask for clarification before proceeding.
            """
        
        tools = list(self.tool_dict.values()) + [
            FunctionTool.from_defaults(fn=self.create_system_prompt),
            FunctionTool.from_defaults(fn=self.get_tools),
            FunctionTool.from_defaults(fn=self.add_tool),
        ]
        
        return OpenAIAgent.from_tools(tools, llm=self.llm, system_prompt=system_prompt, verbose=True)

    def add_tool(self, name: str, tool: BaseTool) -> str:
        """
        Add a new tool to the tool dictionary and update the agent.

        Args:
            name (str): The name of the tool.
            tool (BaseTool): The tool to be added.

        Returns:
            str: A message indicating success or failure of tool addition.
        """
        try:
            self.tool_dict[name] = tool
            self.agent = self._create_or_update_agent(self.agent.system_prompt)
            return f"Tool '{name}' added successfully and agent updated."
        except Exception as e:
            return f"An error occurred when adding the tool: {repr(e)}"

    def create_system_prompt(self, task: str) -> str:
        """
        Create a system prompt for a given task.

        Args:
            task (str): The task description.

        Returns:
            str: The generated system prompt.
        """
        messages = [
            ChatMessage(role="system", content="You are an expert AI assistant specializing in crafting effective system prompts for other AI bots. Your task is to help create a clear, comprehensive, and tailored system prompt that will guide another bot's behavior and responses."),
            ChatMessage(role="user", content=self.gen_sys_prompt_str.format(task=task)),
        ]
        response = self.llm.chat(messages)
        return response.message.content

    def get_tools(self, task: str) -> List[str]:
        """
        Get a list of relevant tool names for a given task.

        Args:
            task (str): The task description.

        Returns:
            List[str]: A list of relevant tool names.
        """
        subset_tools = self.tool_retriever.retrieve(task)
        return [t.metadata.name for t in subset_tools]

    def update_agent(self, system_prompt: str) -> str:
        """
        Update the agent with a new system prompt.

        Args:
            system_prompt (str): The new system prompt for the agent.

        Returns:
            str: A message indicating success or failure of agent update.
        """
        try:
            self.agent = self._create_or_update_agent(system_prompt)
            return "Agent updated successfully with new system prompt."
        except Exception as e:
            return f"An error occurred when updating the agent: {repr(e)}"

    def query(self, task: str) -> str:
        """
        Query the agent with a task.

        Args:
            task (str): The task or query for the agent.

        Returns:
            str: The agent's response.
        """
        return self.agent.query(task)

    def save_agent(self, filename: str) -> None:
        """
        Save the current agent to a file.

        Args:
            filename (str): The name of the file to save the agent to.
        """
        agent_data = {
            "system_prompt": self.agent.system_prompt,
            "tool_names": list(self.tool_dict.keys())
        }
        
        with open(filename, 'w') as f:
            json.dump(agent_data, f)

    def load_agent(self, filename: str) -> None:
        """
        Load an agent from a file.

        Args:
            filename (str): The name of the file to load the agent from.
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File {filename} not found.")
        
        with open(filename, 'r') as f:
            agent_data = json.load(f)
        
        self.agent = self._create_or_update_agent(agent_data["system_prompt"])

# Example usage:
# from llama_index.llms.openai import OpenAI
# from llama_index.embeddings.openai import OpenAIEmbedding
# from llama_index.core import VectorStoreIndex
#
# llm = OpenAI(model="gpt-4")
# embed_model = OpenAIEmbedding(model="text-embedding-3-small")
# tool_retriever = ... # Set up your tool retriever
#
# agent_builder = AgentBuilder(llm, embed_model, tool_retriever)
#
# # Add a tool
# tool = ... # Create your tool
# agent_builder.add_tool("ExampleTool", tool)
#
# # Query the agent
# response = agent_builder.query("Tell me about the capabilities of the ExampleTool")
# print(response)
#
# # Update the agent with a new system prompt
# new_prompt = agent_builder.create_system_prompt("Analyze financial data")
# agent_builder.update_agent(new_prompt)
#
# # Save and load the agent
# agent_builder.save_agent("financial_agent.json")
# agent_builder.load_agent("financial_agent.json")
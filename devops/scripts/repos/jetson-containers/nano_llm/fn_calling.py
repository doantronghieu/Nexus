import requests
import termcolor
import sys
import json
import inspect
import typing
from typing import Optional, Dict, Union, Any, List, Callable, Type, get_origin, get_args
from dataclasses import dataclass, field
from datetime import datetime
import docstring_parser
import re
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.traceback import install
from rich.theme import Theme
from abc import ABC, abstractmethod

# Install rich traceback handler
install(show_locals=True)

class LoggerTitan:
    """Manages all logging operations for the LLMTitan system"""
    
    def __init__(self, verbose: bool = False, show_prompt: bool = False):
        self.verbose = verbose
        self.show_prompt = show_prompt
        
        self.theme = Theme({
            "debug.title": "cyan bold",
            "debug.content": "bright_blue",
            "debug.error": "red bold",
            "debug.success": "green bold",
            "debug.warning": "yellow bold",
            "debug.info": "bright_magenta"
        })
        
        self.console = Console(theme=self.theme)

    def log(self, message: str, data: Any = None, prompt: bool = False):
        """Enhanced logging with strict separation of prompt and debug output"""
        if not (self.verbose or self.show_prompt):
            return

        if prompt:
            if self.show_prompt:  # Only show prompts when -p flag is enabled
                self.console.print()
                self.console.print(Panel(
                    f"[yellow bold]PROMPT[/yellow bold]\n[yellow]{data}[/yellow]",
                    border_style="yellow",
                    expand=False
                ))
            return

        if not self.verbose:
            return

        self.console.print()
        self.console.print(Panel(
            f"[debug.title]DEBUG[/debug.title] [debug.content]{message}[/debug.content]",
            border_style="bright_blue",
            expand=False
        ))
        
        if data is not None:
            if isinstance(data, dict):
                table = Table(show_header=True, header_style="debug.title", border_style="bright_blue")
                table.add_column("Key", style="debug.info")
                table.add_column("Value", style="debug.content")
                
                for key, value in data.items():
                    table.add_row(str(key), str(value))
                self.console.print(table)
            else:
                if not (message == "Processing request:" and isinstance(data, str)):
                    self.console.print(str(data), style="debug.content")

@dataclass
class Function:
    name: str
    description: str
    parameters: Dict[str, Any]
    handler: Callable
    return_type: Dict[str, Any]

@dataclass
class FunctionCall:
    name: str
    arguments: Dict[str, Any]
    full_response: str

class FunctionManager:
    """Manages function registration, validation, and execution"""
    
    def __init__(self, logger: LoggerTitan):
        self.functions: Dict[str, Function] = {}
        self.logger = logger

    def register_functions(self, *funcs: Callable) -> None:
        """Register multiple functions at once"""
        for func in funcs:
            func_info = self._extract_function_info(func)
            self.functions[func_info["name"]] = Function(
                name=func_info["name"],
                description=func_info["description"],
                parameters=func_info["parameters"],
                handler=func,
                return_type=func_info["return"]
            )

    def get_functions_prompt(self) -> str:
        """Generate a generic prompt for function calling with strict constraints"""
        if not self.functions:
            return ""

        function_names = list(self.functions.keys())
        prompt = f"""IMPORTANT: You can ONLY use these registered functions: {', '.join(function_names)}

Respond ONLY with a function call in this exact format:
FUNCTION_CALL: function_name
ARGUMENTS: {{
    "param1": "value1",
    "param2": "value2"
}}

Available functions:

"""
        for func in self.functions.values():
            prompt += self._generate_function_description(func)

        prompt += self._generate_function_examples()
        prompt += self._generate_function_rules(function_names)
        
        return prompt

    def _generate_function_description(self, func: Function) -> str:
        """Generate description for a single function"""
        description = f"[{func.name}]\n"
        description += f"Purpose: {func.description}\n"
        
        # Required parameters
        required_params = {k: v for k, v in func.parameters.items() if v.get("required", True)}
        if required_params:
            description += "Required parameters:\n"
            for name, info in required_params.items():
                param_type = info.get("type", "string")
                description += f"- {name} ({param_type}): {info.get('description', '')}\n"
                if "enum" in info:
                    description += f"  Options: {', '.join(map(str, info['enum']))}\n"
        
        # Optional parameters
        optional_params = {k: v for k, v in func.parameters.items() if not v.get("required", True)}
        if optional_params:
            description += "Optional parameters:\n"
            for name, info in optional_params.items():
                param_type = info.get("type", "string")
                default = f", default: {info['default']}" if 'default' in info else ""
                description += f"- {name} ({param_type}{default}): {info.get('description', '')}\n"
                if "enum" in info:
                    description += f"  Options: {', '.join(map(str, info['enum']))}\n"
        
        description += "\n"
        return description

    def _generate_function_examples(self) -> str:
        """Generate examples for all registered functions"""
        examples = "Examples:\n\n"
        for func_name, func in self.functions.items():
            example_args = self._generate_example_arguments(func.parameters)
            examples += f"""Example for {func_name}:
FUNCTION_CALL: {func_name}
ARGUMENTS: {json.dumps(example_args, indent=4)}

"""
        return examples

    def _generate_example_arguments(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Generate example arguments for a function"""
        example_args = {}
        for name, info in parameters.items():
            if info.get("required", True):
                if info.get("type") == "string":
                    example_args[name] = f"example_{name}"
                elif info.get("type") == "integer":
                    example_args[name] = 1
                elif info.get("type") == "number":
                    example_args[name] = 1.0
                elif info.get("type") == "boolean":
                    example_args[name] = True
                elif "enum" in info:
                    example_args[name] = info["enum"][0]
        return example_args

    def _generate_function_rules(self, function_names: List[str]) -> str:
        """Generate rules for function usage"""
        return f"""RULES:
1. You MUST use one of these functions: {', '.join(function_names)}
2. If no suitable function exists, respond with: "No suitable function available"
3. Include ALL required parameters
4. Optional parameters can be omitted
5. Use EXACT parameter names as shown
6. Maintain the EXACT response format

User request: """

    @staticmethod
    def _type_to_json_schema(type_hint: Type) -> Dict[str, Any]:
        """Convert Python type hint to JSON Schema"""
        if type_hint == str:
            return {"type": "string"}
        elif type_hint == int:
            return {"type": "integer"}
        elif type_hint == float:
            return {"type": "number"}
        elif type_hint == bool:
            return {"type": "boolean"}
        elif type_hint == List[str]:
            return {"type": "array", "items": {"type": "string"}}
        elif type_hint == List[int]:
            return {"type": "array", "items": {"type": "integer"}}
        elif type_hint == List[float]:
            return {"type": "array", "items": {"type": "number"}}
        
        origin = get_origin(type_hint)
        if origin == Union:
            args = get_args(type_hint)
            if len(args) == 2 and args[1] == type(None):
                return {**FunctionManager._type_to_json_schema(args[0]), "required": False}
        elif origin == typing.Literal:
            args = get_args(type_hint)
            return {"type": "string", "enum": list(args)}
        elif type_hint == Dict[str, Any] or type_hint == dict:
            return {"type": "object", "additionalProperties": True}
        
        return {"type": "string"}

    @staticmethod
    def _parse_docstring(func: Callable) -> Dict[str, str]:
        """Parse function docstring for description and parameter descriptions"""
        docstring = inspect.getdoc(func) or ""
        parsed = docstring_parser.parse(docstring)
        
        result = {
            "description": parsed.short_description or func.__name__,
            "params": {}
        }
        
        for param in parsed.params:
            result["params"][param.arg_name] = param.description
            
        return result

    @staticmethod
    def _extract_function_info(func: Callable) -> Dict[str, Any]:
        """Extract function information from type hints and docstring"""
        sig = inspect.signature(func)
        doc_info = FunctionManager._parse_docstring(func)
        
        parameters = {}
        for name, param in sig.parameters.items():
            if name == 'self':
                continue
                
            param_info = {"description": doc_info["params"].get(name, f"Parameter {name}")}
            
            if param.annotation != inspect.Parameter.empty:
                param_info.update(FunctionManager._type_to_json_schema(param.annotation))
            else:
                param_info["type"] = "string"
            
            if param.default != inspect.Parameter.empty:
                param_info["default"] = param.default
                param_info["required"] = False
            else:
                param_info["required"] = True
            
            parameters[name] = param_info
        
        return_info = {}
        if sig.return_annotation != inspect.Signature.empty:
            return_info = FunctionManager._type_to_json_schema(sig.return_annotation)
        
        return {
            "name": func.__name__,
            "description": doc_info["description"],
            "parameters": parameters,
            "return": return_info
        }

    def validate_arguments(self, function_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and clean function arguments"""
        if function_name not in self.functions:
            raise ValueError(f"Unknown function: {function_name}")
            
        func = self.functions[function_name]
        cleaned_args = {}
        
        for name, param_info in func.parameters.items():
            value = arguments.get(name)
            
            if param_info.get("required", True) and value is None:
                raise ValueError(f"Missing required parameter: {name}")
            
            if value is None:
                if "default" in param_info:
                    cleaned_args[name] = param_info["default"]
                continue
                
            param_type = param_info.get("type", "string")
            try:
                if param_type == "string":
                    value = str(value)
                elif param_type == "integer":
                    value = int(value)
                elif param_type == "number":
                    value = float(value)
                elif param_type == "boolean":
                    value = bool(value)
                
                if "enum" in param_info and value not in param_info["enum"]:
                    raise ValueError(
                        f"Invalid value for {name}. Must be one of: {param_info['enum']}"
                    )
                    
                cleaned_args[name] = value
                
            except (ValueError, TypeError):
                raise ValueError(
                    f"Invalid type for {name}. Expected {param_type}, got {type(value)}"
                )
        
        return cleaned_args

    def execute_function(self, function_call: FunctionCall) -> Optional[Dict[str, Any]]:
        """Execute a function call"""
        self.logger.log(
            "[debug.title]Executing Function[/debug.title]",
            {"name": function_call.name, "arguments": function_call.arguments}
        )
        
        try:
            cleaned_args = self.validate_arguments(
                function_call.name, 
                function_call.arguments
            )
            
            self.logger.log("[debug.success]Arguments validated[/debug.success]", cleaned_args)
            
            func = self.functions[function_call.name]
            result = func.handler(**cleaned_args)
            
            self.logger.log("[debug.success]Function executed successfully[/debug.success]", result)
            return result
            
        except Exception as e:
            self.logger.log(
                "[debug.error]Error executing function[/debug.error]",
                str(e)
            )
            return None

@dataclass
class Message:
    """Represents a single message in the conversation history"""
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

class MemoryManager:
    """Manages conversation history and context for LLMTitan"""
    
    def __init__(self, max_history: int = 10):
        self.messages: List[Message] = []
        self.max_history = max_history
        self.function_calls: Dict[str, Any] = {}
        
    def add_message(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add a message to the conversation history"""
        # Clean the content by removing duplicate conversations and other artifacts
        content = self._clean_content(content)
        
        # Don't add empty messages
        if not content.strip():
            return
            
        metadata = metadata or {}
        message = Message(role=role, content=content, metadata=metadata)
        self.messages.append(message)
        
        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history:]
    
    def add_function_call(self, function_name: str, args: Dict[str, Any], result: Any) -> None:
        """
        Store function call results for context
        
        Args:
            function_name: Name of the called function
            args: Function arguments
            result: Function result
        """
        self.function_calls[function_name] = {
            'last_call': {
                'timestamp': datetime.now(),
                'arguments': args,
                'result': result
            }
        }
    
    def _clean_content(self, content: str) -> str:
        """Clean the content by removing duplicates and boilerplate text"""
        # Remove common prefixes
        content = re.sub(r'You are a helpful assistant[^\"]*?request:\s*', '', content)
        
        # Remove guidelines sections
        content = re.sub(r'Guidelines:[\s\S]*?(?=\n\n|$)', '', content)
        
        # Remove "Previous conversation:" and nested conversations
        content = re.sub(r'Previous conversation:[\s\S]*?Current request:', '', content)
        
        # Remove "Please consider the above context..." and similar suffixes
        content = re.sub(r'Please consider the above context[\s\S]*$', '', content)
        
        # Remove "Current request:" prefix
        content = re.sub(r'Current request:\s*', '', content)
        
        # Clean up any multiple newlines
        content = re.sub(r'\n\s*\n', '\n', content)
        
        # Remove any remaining nested conversation markers
        content = re.sub(r'You:|Assistant:', '', content)
        
        return content.strip()
    
    def get_context(self, include_timestamps: bool = False) -> str:
        """Generate context string from conversation history"""
        if not self.messages and not self.function_calls:
            return ""
            
        context_parts = []
        
        if self.messages:
            last_messages = self.messages[-5:]  # Only include last 5 messages for cleaner context
            context_parts.append("Previous conversation:")
            
            # Track the last message content to prevent duplicates
            last_content = set()
            
            for msg in last_messages:
                # Skip if this content has already been included
                cleaned_content = msg.content.strip()
                if cleaned_content in last_content:
                    continue
                    
                timestamp_str = f"[{msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] " if include_timestamps else ""
                prefix = "You: " if msg.role == "user" else "Assistant: "
                context_parts.append(f"{timestamp_str}{prefix}{cleaned_content}")
                
                # Add to seen content
                last_content.add(cleaned_content)
            
        if self.function_calls:
            context_parts.append("\nRecent function calls:")
            for func_name, call_info in self.function_calls.items():
                last_call = call_info['last_call']
                context_parts.append(f"{func_name}:")
                context_parts.append(f"Arguments: {json.dumps(last_call['arguments'], indent=2)}")
                context_parts.append(f"Result: {json.dumps(last_call['result'], indent=2)}")
                
        result = "\n".join(context_parts)
        return result.strip()
        
    def generate_prompt_with_memory(self, prompt: str, include_timestamps: bool = False) -> str:
        """Generate a prompt that includes conversation history"""
        context = self.get_context(include_timestamps)
        
        if context:
            return f"""{context}

Current request: {prompt}

Please consider the above context when responding. If previous interactions are relevant to the current request, incorporate that information into your response."""
        else:
            return prompt
                    
    def clear(self) -> None:
        """Clear all conversation history and function calls"""
        self.messages = []
        self.function_calls = {}
        
    def save_to_file(self, filename: str) -> None:
        """
        Save conversation history to a file
        
        Args:
            filename: Path to save the history
        """
        history = {
            'messages': [
                {
                    'role': msg.role,
                    'content': msg.content,
                    'timestamp': msg.timestamp.isoformat(),
                    'metadata': msg.metadata
                }
                for msg in self.messages
            ],
            'function_calls': self.function_calls
        }
        
        with open(filename, 'w') as f:
            json.dump(history, f, indent=2)
            
    def load_from_file(self, filename: str) -> None:
        """
        Load conversation history from a file
        
        Args:
            filename: Path to load the history from
        """
        with open(filename, 'r') as f:
            history = json.load(f)
            
        self.messages = [
            Message(
                role=msg['role'],
                content=msg['content'],
                timestamp=datetime.fromisoformat(msg['timestamp']),
                metadata=msg['metadata']
            )
            for msg in history['messages']
        ]
        
        self.function_calls = history['function_calls']

class BaseLLM(ABC):
    """Abstract base class for LLM implementations"""
    
    @abstractmethod
    def chat(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        max_tokens: Optional[int] = None,
        repetition_penalty: Optional[float] = None,
        stream: bool = True,
        print_output: bool = True
    ) -> Optional[str]:
        """Generate chat response from prompt"""
        pass

class MyBaseLLM(BaseLLM):
    """Concrete implementation of BaseLLM for specific endpoint"""
    
    def __init__(self, url: str, logger: LoggerTitan):
        self.url = url
        self.generate_endpoint = f"{url}/v1/generate"
        self.logger = logger

    def _make_request(
        self,
        prompt: str,
        stream: bool = False,
        function_call: bool = False,
        **kwargs
    ) -> requests.Response:
        """Make HTTP request to the API with proper logging"""
        # Log request metadata
        metadata_table = Table(show_header=False, box=None)
        metadata_table.add_column("Property", style="debug.info")
        metadata_table.add_column("Value", style="debug.content")
        
        metadata_table.add_row(
            "Request Type",
            "Function Call" if function_call else "Standard Generation"
        )
        metadata_table.add_row(
            "Stream Mode",
            "Enabled" if stream else "Disabled"
        )
        for key, value in kwargs.items():
            if value is not None:
                metadata_table.add_row(key, str(value))
        
        self.logger.console.print(metadata_table)
        
        # Log the prompt itself
        self.logger.log("", prompt, prompt=True)
        
        payload = {"prompt": prompt}
        payload.update({k: v for k, v in kwargs.items() if v is not None})
        
        headers = {
            'Accept': 'text/event-stream' if stream else 'application/json',
            'Content-Type': 'application/json'
        }
        
        return requests.post(
            self.generate_endpoint,
            json=payload,
            headers=headers,
            stream=stream
        )

    def chat(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        max_tokens: Optional[int] = None,
        repetition_penalty: Optional[float] = None,
        stream: bool = True,
        print_output: bool = True,
        function_call: bool = False
    ) -> Optional[str]:
        """Implementation of chat method"""
        try:
            response = self._make_request(
                prompt=prompt,
                stream=stream,
                temperature=temperature,
                top_p=top_p,
                max_new_tokens=max_tokens,
                repetition_penalty=repetition_penalty,
                function_call=function_call
            )
            
            if response.status_code != 200:
                self.logger.log(f"Error: {response.status_code}")
                return None
            
            if stream:
                full_response = ""
                first_chunk = True  # Track if this is the first chunk
                for chunk in response.iter_content(decode_unicode=True):
                    if chunk:
                        text = chunk.decode('utf-8') if isinstance(chunk, bytes) else chunk
                        full_response += text
                        if print_output and not function_call:
                            if first_chunk:
                                print("")  # Add space before first chunk
                                first_chunk = False
                            termcolor.cprint(text, 'blue', end='', flush=True)
                
                if print_output and not function_call:
                    print("\n")
                return full_response
            else:
                return response.text
                
        except Exception as e:
            self.logger.log(f"Error: {str(e)}")
            return None
          
class LLMTitan:
    """Main class that orchestrates LLM interactions, function handling, and logging"""
    
    def __init__(
        self,
        url: str = "http://localhost:8000",
        verbose: bool = False,
        show_prompt: bool = False,
        enable_memory: bool = False,
        enable_function_memory: bool = False,
        max_history: int = 10
    ):
        """
        Initialize LLMTitan with separate memory settings
        
        Args:
            url: API endpoint URL
            verbose: Enable verbose logging
            show_prompt: Show prompts in logs
            enable_memory: Enable memory for main conversation
            enable_function_memory: Enable memory for function detection
            max_history: Maximum number of messages to keep in history
        """
        self.logger = LoggerTitan(verbose, show_prompt)
        self.llm = MyBaseLLM(url, self.logger)
        self.function_manager = FunctionManager(self.logger)
        
        # Main conversation memory
        self.enable_memory = enable_memory
        self.memory = MemoryManager(max_history) if enable_memory else None
        
        # Function detection memory
        self.enable_function_memory = enable_function_memory
        self.function_memory = MemoryManager(max_history) if enable_function_memory else None

    def register_functions(self, *funcs: Callable) -> None:
        """Register functions with the function manager"""
        self.function_manager.register_functions(*funcs)

    def is_function_required(self, prompt: str) -> bool:
        """Determine if the prompt requires a function call"""
        # Base detection prompt
        detection_prompt = f"""Analyze this user request and determine if it requires calling a function.
    
Available functions:
{', '.join(self.function_manager.functions.keys())}

Function descriptions:
{self._get_function_descriptions()}

Request: "{prompt}"

Answer ONLY with "YES" if the request requires one of the available functions, or "NO" if it's a general conversation that doesn't need any function.

Guidelines for determination:
1. Function calls are needed for:
   - Requesting specific data or information
   - Searching or querying for something
   - Actions that require accessing external systems
   - Tasks that need structured data processing
2. General conversation is better for:
    - Greetings and casual chat
    - Questions about general knowledge
    - Creative or opinion-based responses
    - Jokes, stories, or explanations
"""

        # Add memory context if enabled
        if self.enable_function_memory and self.function_memory:
            detection_prompt = self.function_memory.generate_prompt_with_memory(detection_prompt)
            self.logger.log("Function detection with memory:", detection_prompt, prompt=True)

        # Get LLM's determination
        response = self.llm.chat(
            detection_prompt,
            temperature=0.0,
            stream=False,
            print_output=False
        )
        
        if response:
            cleaned_response = response.strip().upper()
            result_data = {
                "prompt": prompt,
                "decision": cleaned_response,
                "memory_enabled": self.enable_function_memory
            }
            
            self.logger.log("Function requirement detection", result_data)
            
            # Store the interaction in function memory if enabled
            if self.enable_function_memory and self.function_memory:
                self.function_memory.add_message('user', f"Request: {prompt}")
                self.function_memory.add_message('assistant', f"Decision: {cleaned_response}")
            
            return cleaned_response == "YES"
        
        return True

    def _get_function_descriptions(self) -> str:
        """Generate descriptive text for all registered functions"""
        descriptions = []
        for name, func in self.function_manager.functions.items():
            params = [f"- {k}: {v.get('description', '')}" 
                    for k, v in func.parameters.items()]
            desc = f"""
    {name}:
    Purpose: {func.description}
    Parameters:
    {chr(10).join(params)}"""
            descriptions.append(desc)
        
        return "\n".join(descriptions)

    def parse_function_call(self, response: str) -> Optional[FunctionCall]:
        """Parse function call from response"""
        self.logger.log("[debug.title]Parsing Function Call[/debug.title]", response)
        
        if "no suitable function available" in response.lower():
            self.logger.log("[debug.warning]No suitable function available for this request[/debug.warning]")
            return None
        
        try:
            func_match = re.search(r"FUNCTION_CALL:\s*([\w_]+)", response, re.IGNORECASE)
            args_match = re.search(r"ARGUMENTS:\s*({[^}]+})", response, re.DOTALL)
            
            if func_match and args_match:
                function_name = func_match.group(1)
                
                if function_name not in self.function_manager.functions:
                    self.logger.log(
                        "[debug.error]Function not found[/debug.error]",
                        f"Function '{function_name}' is not registered"
                    )
                    return None
                
                try:
                    arguments = json.loads(args_match.group(1))
                except json.JSONDecodeError:
                    self.logger.log("[debug.error]Invalid JSON in arguments[/debug.error]")
                    return None
                
                self.logger.log(
                    "[debug.success]Valid function call detected[/debug.success]",
                    {
                        "function": function_name,
                        "arguments": arguments
                    }
                )
                
                return FunctionCall(function_name, arguments, response)
                
        except Exception as e:
            self.logger.log(
                "[debug.error]Error parsing function call[/debug.error]",
                str(e)
            )
        
        self.logger.log("[debug.warning]No valid function call detected[/debug.warning]")
        return None

    def format_result_prompt(self, function_call: FunctionCall, result: Any) -> str:
        """Generate a prompt for formatting function results"""
        prompt = f"""Format these function results in a natural, informative way.
Use **bold** for important information and make it conversational.

Function details:
- Name: {function_call.name}
- Arguments: {json.dumps(function_call.arguments, indent=2)}

Result to format:
{json.dumps(result, indent=2)}

Guidelines:
1. Start with a friendly introduction
2. Present the most important information first
3. Use clear formatting and structure
4. Highlight key details using **bold**
5. End with a helpful conclusion or next steps
"""
        return prompt

    def generate_conversational_prompt(self, prompt: str) -> str:
        """Generate a prompt for conversational responses"""
        return f"""You are a helpful assistant. Please respond naturally and conversationally to this request:

{prompt}

Guidelines:
1. Be friendly and engaging
2. Provide direct and relevant responses
3. Use natural language
4. Be concise but informative
"""

    def fallback_to_conversation(
        self,
        prompt: str,
        stream: bool = True,
        print_output: bool = True
    ) -> str:
        """Fallback to conversational response when function calling fails"""
        self.logger.log("Falling back to conversational response")
        
        conv_prompt = self.generate_conversational_prompt(prompt)
        return self.llm.chat(
            conv_prompt,
            stream=stream,
            print_output=print_output,
            function_call=False
        )

    def generate_with_function_handling(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        max_tokens: Optional[int] = None,
        repetition_penalty: Optional[float] = None,
        stream: bool = True,
        print_output: bool = True
    ) -> Optional[str]:
        """Generate response with intelligent function handling"""
        try:
            self.logger.log("Processing request:", prompt)
            
            # Get memory-enhanced prompt if main memory is enabled
            if self.enable_memory and self.memory:
                enhanced_prompt = self.memory.generate_prompt_with_memory(prompt)
                if self.logger.show_prompt:
                    self.logger.log("Memory-enhanced prompt:", enhanced_prompt, prompt=True)
            else:
                enhanced_prompt = prompt
            
            needs_function = self.is_function_required(enhanced_prompt)
            
            if needs_function:
                function_prompt = self.function_manager.get_functions_prompt()
                full_prompt = f"{function_prompt}{enhanced_prompt}"
                
                function_response = self.llm.chat(
                    full_prompt,
                    temperature=0.0,
                    top_p=top_p,
                    max_tokens=max_tokens,
                    repetition_penalty=repetition_penalty,
                    stream=False,
                    print_output=False,
                    function_call=True
                )
                
                if not function_response:
                    return self.fallback_to_conversation(enhanced_prompt, stream, print_output)
                    
                function_call = self.parse_function_call(function_response)
                if not function_call:
                    return self.fallback_to_conversation(enhanced_prompt, stream, print_output)
                    
                result = self.function_manager.execute_function(function_call)
                if not result:
                    return self.fallback_to_conversation(enhanced_prompt, stream, print_output)
                    
                if self.enable_memory and self.memory:
                    self.memory.add_function_call(
                        function_call.name,
                        function_call.arguments,
                        result
                    )
                    
                prompt = self.format_result_prompt(function_call, result)
            else:
                prompt = self.generate_conversational_prompt(enhanced_prompt)
            
            if print_output:
                self.logger.console.print("")
                
            response = self.llm.chat(
                prompt,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
                repetition_penalty=repetition_penalty,
                stream=stream,
                print_output=print_output,
                function_call=False
            )
            
            if self.enable_memory and self.memory and response:
                self.memory.add_message('user', prompt)
                self.memory.add_message('assistant', response)
                
            return response
            
        except Exception as e:
            self.logger.log(f"Error in function handling: {str(e)}")
            error_msg = "I encountered an error processing your request."
            if print_output:
                print("\n" + error_msg)
            return error_msg
              
def main():
    import argparse
    parser = argparse.ArgumentParser(description='LLMTitan Chat Client')
    parser.add_argument('-v', '--verbose', action='store_true', 
                        help='Enable verbose debug output')
    parser.add_argument('-p', '--show-prompt', action='store_true', 
                        help='Show prompts being sent to model')
    parser.add_argument('-m', '--memory', action='store_true',
                        help='Enable conversation memory')
    parser.add_argument('-f', '--function-memory', action='store_true',
                        help='Enable memory for function requirement detection')
    parser.add_argument('--max-history', type=int, default=10,
                        help='Maximum number of messages to keep in history')
    args = parser.parse_args()

    client = LLMTitan(
        verbose=args.verbose,
        show_prompt=args.show_prompt,
        enable_memory=args.memory,
        enable_function_memory=args.function_memory,
        max_history=args.max_history
    )
    
    # Demo function: Weather
    def get_weather(
        location: str,
        unit: typing.Literal["celsius", "fahrenheit"] = "celsius"
    ) -> Dict[str, Any]:
        """
        Get weather information for a location
        
        Args:
            location: City and country, e.g., 'London, UK'
            unit: Temperature unit (celsius or fahrenheit)
        
        Returns:
            Dict containing weather information
        """
        return {
            "temperature": 12,
            "condition": "Partly Cloudy",
            "humidity": 60,
            "wind_speed": 15,
            "wind_direction": "West-Northwest",
            "forecast": {
                "tomorrow": {
                    "condition": "Mostly Sunny",
                    "high": 18,
                    "low": 10
                }
            }
        }

    # Demo function: Places Search
    def search_places(
        query: str,
        category: Optional[str] = None,
        max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search for places based on query and category
        
        Args:
            query: Search query string
            category: Optional category to filter results
            max_results: Maximum number of results to return
            
        Returns:
            List of places matching the search criteria
        """
        return [
            {
                "name": "Central Park",
                "location": "Manhattan",
                "type": "Urban Park",
                "size": "843 acres",
                "features": [
                    "Loeb Boathouse",
                    "Alice in Wonderland Statue",
                    "Conservatory Garden"
                ]
            },
            {
                "name": "Prospect Park",
                "location": "Brooklyn",
                "type": "Public Park",
                "size": "585 acres",
                "features": [
                    "Lake",
                    "Playgrounds",
                    "Walking Paths"
                ]
            }
        ][:max_results]

    # Register demo functions
    client.register_functions(get_weather, search_places)
    
    # Show debug configuration in welcome message
    debug_info = []
    if args.verbose:
        debug_info.append("• Verbose debug output enabled")
    if args.show_prompt:
        debug_info.append("• Prompt display enabled")
        
    welcome_message = [
        "[bold cyan]LLMTitan Chat Client[/bold cyan]\n",
        "[bright_blue]Features:[/bright_blue]",
        "• Natural conversation for general queries",
        "• Weather information lookup",
        "• Places search and discovery"
    ]
    
    debug_info = []
    if args.verbose:
        debug_info.append("• Verbose debug output enabled")
    if args.show_prompt:
        debug_info.append("• Prompt display enabled")
    if args.memory:
        debug_info.append("• Conversation memory enabled")
    if args.function_memory:
        debug_info.append("• Function detection memory enabled")
        
    if debug_info:
        welcome_message.extend([
            "\n[bright_blue]Active Settings:[/bright_blue]",
            *debug_info
        ])
        
    welcome_message.extend([
        "\n[bright_blue]Commands:[/bright_blue]",
        "  [green]/stream[/green] <prompt>   - Stream response (default)",
        "  [green]/full[/green] <prompt>     - Get full response",
        "  [green]/params[/green]           - Generate with custom parameters",
        "  [green]/functions[/green]        - List available functions",
        "  [green]/memory[/green]           - Show current memory state",
        "  [red]quit[/red]              - Exit"
    ])
    
    client.logger.console.print(Panel(
        "\n".join(welcome_message),
        border_style="bright_blue",
        expand=False
    ))
    
    while True:
        try:
            client.logger.console.print("\n[bright_blue]>>[/bright_blue] ", end='')
            user_input = input().strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
                
            elif user_input == '/functions':
                client.logger.console.print("\n[bold cyan]Available Functions:[/bold cyan]")
                for func in client.function_manager.functions.values():
                    table = Table(show_header=False, border_style="bright_blue")
                    table.add_column("Property", style="debug.info", width=15)
                    table.add_column("Value", style="debug.content")
                    
                    table.add_row("Name", func.name)
                    table.add_row("Description", func.description)
                    table.add_row(
                        "Parameters",
                        Syntax(
                            json.dumps(func.parameters, indent=2),
                            "json",
                            theme="monokai"
                        ).code
                    )
                    client.logger.console.print(table)
                    client.logger.console.print()
                
            elif user_input.startswith('/stream '):
                prompt = user_input[8:].strip()
                client.generate_with_function_handling(prompt, stream=True)
                
            elif user_input.startswith('/full '):
                prompt = user_input[6:].strip()
                response = client.generate_with_function_handling(prompt, stream=False)
                if response:
                    print("\nResponse:", response)
                    
            elif user_input.startswith('/params'):
                print("\nEnter prompt: ", end='')
                prompt = input().strip()
                
                print("Enter temperature (0.0-2.0) or press Enter for default: ", end='')
                temp = input().strip()
                temperature = float(temp) if temp else None
                
                print("Enter max tokens or press Enter for default: ", end='')
                tokens = input().strip()
                max_tokens = int(tokens) if tokens else None
                
                print("Stream response? (y/n): ", end='')
                should_stream = input().strip().lower() == 'y'
                
                response = client.generate_with_function_handling(
                    prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=should_stream
                )
                
                if response and not should_stream:
                    print("\nResponse:", response)
            
            elif user_input == '/memory':
                client.logger.console.print("\n[bold cyan]Main Conversation Memory:[/bold cyan]")
                if client.enable_memory and client.memory:
                    print(client.memory.get_context(include_timestamps=True))
                else:
                    print("Main conversation memory is disabled")
                    
                client.logger.console.print("\n[bold cyan]Function Detection Memory:[/bold cyan]")
                if client.enable_function_memory and client.function_memory:
                    print(client.function_memory.get_context(include_timestamps=True))
                else:
                    print("Function detection memory is disabled")
                         
            elif user_input:  # Default to streaming for plain prompts
                client.generate_with_function_handling(user_input)
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {str(e)}", file=sys.stderr)

if __name__ == "__main__":
    main()
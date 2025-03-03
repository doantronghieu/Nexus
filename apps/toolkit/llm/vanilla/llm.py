# llm_function_calling/
# __init__.py
from typing import List, Dict, Any, Callable, Optional, Union, TypeVar, Protocol, Awaitable
from dataclasses import dataclass
from abc import ABC, abstractmethod
import json
import re
import logging
from datetime import datetime
from enum import Enum

import packages
from configs import settings
llm_vllm = settings.llm_vllm

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Custom exceptions
class FunctionCallError(Exception):
    """Base exception for function calling errors"""
    pass

class ValidationError(FunctionCallError):
    """Raised when function arguments fail validation"""
    pass

class ExecutionError(FunctionCallError):
    """Raised when function execution fails"""
    pass

# Data models
@dataclass
class Message:
    role: str
    content: str

@dataclass
class FunctionCall:
    name: str
    arguments: Dict[str, Any]

@dataclass
class CompletionChoice:
    index: int
    message: Message
    function_call: Optional[FunctionCall] = None

@dataclass
class CompletionResponse:
    id: str
    choices: List[CompletionChoice]
    created: int
    model: str

@dataclass
class FunctionDefinition:
    name: str
    description: str
    parameters: Dict[str, Any]
    required: List[str]

class ParameterType(Enum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    ARRAY = "array"
    OBJECT = "object"

# Configuration
class ModelConfig:
    """Configuration for LLM models"""
    def __init__(
        self,
        model: str,
        max_tokens: Optional[int] = None,
        temperature: float = 1.0,
        top_p: float = 1.0,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        stop: Optional[Union[str, List[str]]] = None
    ):
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.stop = stop

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary, excluding None values"""
        return {k: v for k, v in self.__dict__.items() if v is not None}

# Parameter validation
class ParameterValidator:
    @staticmethod
    def validate(value: Any, param_type: ParameterType, constraints: Dict[str, Any]) -> bool:
        if param_type == ParameterType.STRING:
            if not isinstance(value, str):
                return False
            if "enum" in constraints and value not in constraints["enum"]:
                return False
            if "min_length" in constraints and len(value) < constraints["min_length"]:
                return False
            if "max_length" in constraints and len(value) > constraints["max_length"]:
                return False
        elif param_type == ParameterType.INTEGER:
            if not isinstance(value, int):
                return False
            if "minimum" in constraints and value < constraints["minimum"]:
                return False
            if "maximum" in constraints and value > constraints["maximum"]:
                return False
        # Add more type validations as needed
        return True

# Prompt engineering
@dataclass
class PromptTemplate:
    """Template for structuring prompts to the LLM"""
    system_message: str
    function_description_template: str
    user_message_template: str
    few_shot_examples: List[Dict[str, str]]

class PromptBuilder:
    """Builds prompts for function calling"""
    
    def __init__(self):
        self.template = PromptTemplate(
            system_message="""You are a helpful AI assistant that can call functions to help users. When a user request requires calling a function:
1. Identify the appropriate function to call
2. Respond in this exact format:
   
I'll help you with that.
<function_call>
{
    "name": "function_name",
    "arguments": {
        "param1": "value1",
        "param2": "value2"
    }
}
</function_call>

Important rules:
- Only call ONE function at a time
- Always use valid JSON inside function_call tags
- Only use functions and parameters that are available
- Always check parameter types match the schema
- If no function matches the request, just respond normally without a function call""",

            function_description_template="""Available functions:

{function_descriptions}

Parameters must match these schemas:
{parameter_schemas}""",
            
            user_message_template="User request: {user_message}",
            
            few_shot_examples=[
                {
                    "user": "What's the weather like in New York?",
                    "assistant": """I'll help you check the weather in New York.
<function_call>
{
    "name": "get_weather",
    "arguments": {
        "location": "New York",
        "unit": "celsius"
    }
}
</function_call>"""
                },
                {
                    "user": "Find me some laptops under $1000",
                    "assistant": """I'll search for laptops in that price range.
<function_call>
{
    "name": "search_products",
    "arguments": {
        "query": "laptop",
        "max_price": 1000,
        "category": "electronics"
    }
}
</function_call>"""
                },
                {
                    "user": "How are you today?",
                    "assistant": "I'm doing well, thank you for asking! How can I assist you today?"
                }
            ]
        )

    def _format_parameter_schema(self, param_schema: Dict[str, Any]) -> str:
        """Format a parameter schema into a readable string"""
        lines = []
        for param_name, details in param_schema.items():
            param_type = details.get("type", "any")
            description = details.get("description", "")
            constraints = []
            
            if "enum" in details:
                constraints.append(f"Options: {', '.join(details['enum'])}")
            if "minimum" in details:
                constraints.append(f"Min: {details['minimum']}")
            if "maximum" in details:
                constraints.append(f"Max: {details['maximum']}")
                
            constraint_str = f" ({', '.join(constraints)})" if constraints else ""
            lines.append(f"- {param_name} ({param_type}): {description}{constraint_str}")
            
        return "\n".join(lines)

    def _format_function_schema(self, function: Dict[str, Any]) -> str:
        """Format a function schema into a readable string"""
        name = function["name"]
        description = function["description"]
        parameters = self._format_parameter_schema(
            function["parameters"].get("properties", {})
        )
        required = function["parameters"].get("required", [])
        required_str = f"\nRequired parameters: {', '.join(required)}" if required else ""
        
        return f"""Function: {name}
Description: {description}
Parameters:
{parameters}{required_str}
"""

    def build_prompt(
        self,
        user_message: str,
        available_functions: List[Dict[str, Any]]
    ) -> List[Dict[str, str]]:
        """Build a complete prompt with system message, functions, and examples"""
        
        # Format function descriptions
        function_descriptions = "\n\n".join(
            self._format_function_schema(f) for f in available_functions
        )
        
        # Build the complete prompt
        messages = [
            {
                "role": "system",
                "content": self.template.system_message
            },
            {
                "role": "system",
                "content": self.template.function_description_template.format(
                    function_descriptions=function_descriptions,
                    parameter_schemas=json.dumps(
                        {f["name"]: f["parameters"] for f in available_functions},
                        indent=2
                    )
                )
            }
        ]
        
        # Add few-shot examples
        for example in self.template.few_shot_examples:
            messages.extend([
                {"role": "user", "content": example["user"]},
                {"role": "assistant", "content": example["assistant"]}
            ])
        
        # Add user message
        messages.append({
            "role": "user",
            "content": self.template.user_message_template.format(
                user_message=user_message
            )
        })
        
        return messages

# Base LLM class
class BaseLLM(ABC):
    """Abstract base class for LLM implementations"""
    
    @abstractmethod
    async def generate(
        self,
        messages: List[Message],
        functions: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 1.0,
        max_tokens: Optional[int] = None
    ) -> CompletionResponse:
        """Generate completion from the LLM"""
        pass

# Function registry
class FunctionRegistry:
    def __init__(self):
        self.functions: Dict[str, tuple[FunctionDefinition, Callable]] = {}
    
    def register(self, 
                name: str, 
                description: str, 
                parameters: Dict[str, Any],
                required: Optional[List[str]] = None) -> Callable:
        """Decorator to register functions that can be called by the LLM"""
        def decorator(func: Callable) -> Callable:
            if required is None:
                required_params = []
            else:
                required_params = required
                
            func_def = FunctionDefinition(
                name=name,
                description=description,
                parameters=parameters,
                required=required_params
            )
            self.functions[name] = (func_def, func)
            return func
        return decorator

    def get_function_schemas(self) -> List[Dict[str, Any]]:
        """Get all function schemas in the format expected by LLMs"""
        schemas = []
        for func_def, _ in self.functions.values():
            schema = {
                "name": func_def.name,
                "description": func_def.description,
                "parameters": {
                    "type": "object",
                    "properties": func_def.parameters,
                    "required": func_def.required
                }
            }
            schemas.append(schema)
        return schemas

# LLM Implementation
class MyLLM(BaseLLM):
    """Enhanced MyLLM with callable and flexible configuration"""
    
    def __init__(
        self,
        api_key: str,
        llm_callable: Callable[..., Awaitable[Any]],
        model_config: Optional[ModelConfig] = None,
        prompt_builder: Optional[PromptBuilder] = None
    ):
        self.api_key = api_key
        self.llm_callable = llm_callable
        self.model_config = model_config or ModelConfig(model="gpt-3.5-turbo")
        self.prompt_builder = prompt_builder or PromptBuilder()
        
    async def generate(
        self,
        messages: List[Message],
        functions: Optional[List[Dict[str, Any]]] = None,
        stream: bool = False,
        user: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        presence_penalty: Optional[float] = None,
        stop: Optional[Union[str, List[str]]] = None,
        **kwargs: Any
    ) -> CompletionResponse:
        """Generate completion using provided LLM callable"""
        try:
            # Extract user message and build engineered prompt
            user_message = messages[-1].content
            engineered_messages = self.prompt_builder.build_prompt(
                user_message=user_message,
                available_functions=functions or []
            )
            
            # Prepare model parameters
            model_params = self.model_config.to_dict()
            
            # Override with any provided parameters
            if temperature is not None:
                model_params['temperature'] = temperature
            if max_tokens is not None:
                model_params['max_tokens'] = max_tokens
            if top_p is not None:
                model_params['top_p'] = top_p
            if frequency_penalty is not None:
                model_params['frequency_penalty'] = frequency_penalty
            if presence_penalty is not None:
                model_params['presence_penalty'] = presence_penalty
            if stop is not None:
                model_params['stop'] = stop
            
            # Prepare request parameters
            request_params = {
                'messages': engineered_messages,
                'stream': stream,
                **model_params,
                **kwargs
            }
            
            if functions:
                request_params['functions'] = functions
            if user:
                request_params['user'] = user
                
            logger.info(f"Sending request to LLM with parameters: {request_params}")
            
            # Call the LLM using the provided callable
            raw_response = await self.llm_callable(**request_params)
            
            # Convert the response to our standard format
            return self._convert_response(raw_response)
            
        except Exception as e:
            logger.error(f"Error generating completion: {str(e)}")
            raise

    def _convert_response(self, raw_response: Any) -> CompletionResponse:
        """Convert provider-specific response to standard CompletionResponse"""
        try:
            return CompletionResponse(
                id=raw_response.get('id', f"response-{datetime.now().timestamp()}"),
                choices=[
                    CompletionChoice(
                        index=idx,
                        message=Message(
                            role=choice.get('message', {}).get('role', 'assistant'),
                            content=choice.get('message', {}).get('content', '')
                        ),
                        function_call=FunctionCall(
                            name=choice.get('function_call', {}).get('name'),
                            arguments=json.loads(
                                choice.get('function_call', {}).get('arguments', '{}')
                            )
                        ) if 'function_call' in choice else None
                    )
                    for idx, choice in enumerate(raw_response.get('choices', []))
                ],
                created=raw_response.get('created', int(datetime.now().timestamp())),
                model=raw_response.get('model', self.model_config.model)
            )
        except Exception as e:
            logger.error(f"Error converting response: {str(e)}")
            raise

# Function caller
class LLMFunctionCaller:
    def __init__(self, llm: BaseLLM, registry: FunctionRegistry):
        self.llm = llm
        self.registry = registry
    
    async def process_message(self, message: str, **kwargs) -> Any:
        """Process a message and execute any function calls"""
        messages = [Message(role="user", content=message)]
        functions = self.registry.get_function_schemas()
        
        try:
            response = await self.llm.generate(
                messages=messages,
                functions=functions,
                **kwargs
            )
            
            if not response.choices:
                return None
                
            choice = response.choices[0]
            if not choice.function_call:
                return choice.message.content
                
            return await self.execute_function_call(choice.function_call)
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            raise

    async def execute_function_call(self, function_call: FunctionCall) -> Any:
        """Execute a function call with validation"""
        if function_call.name not in self.registry.functions:
            raise ValueError(f"Unknown function: {function_call.name}")
            
        func_def, func = self.registry.functions[function_call.name]
        
        # Validate required parameters
        for required_param in func_def.required:
            if required_param not in function_call.arguments:
                raise ValidationError(f"Missing required parameter: {required_param}")
        
        # Validate parameter types and constraints
        for param_name, param_value in function_call.arguments.items():
            if param_name not in func_def.parameters:
                raise ValidationError(f"Unknown parameter: {param_name}")
            
            param_schema = func_def.parameters[param_name]
            param_type = ParameterType(param_schema["type"])
            
            if not ParameterValidator.validate(param_value, param_type, param_schema):
                raise ValidationError(f"Invalid value for parameter {param_name}")
        
        try:
            return await func(**function_call.arguments)
        except Exception as e:
            logger.error(f"Error executing function {function_call.name}: {str(e)}")
            raise ExecutionError(f"Function execution failed: {str(e)}")

# Provider-specific callables
async def openai_callable(**kwargs):
    """Example callable for OpenAI"""
    import openai
    return await openai.ChatCompletion.create(**kwargs)

async def anthropic_callable(**kwargs):
    """Example callable for Anthropic"""
    import anthropic
    
    # Convert messages to Anthropic format
    messages = kwargs.pop('messages', [])
    prompt = "\n\n".join(f"{m['role']}: {m['content']}" for m in messages)
    
    client = anthropic.Client(kwargs.pop('api_key'))
    return await client.completion(
        prompt=prompt,
        **kwargs
    )

# Example usage
async def main():
    # Configure the model
    model_config = ModelConfig(
        model="gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=150
    )
    
    # Create registry
    registry = FunctionRegistry()
    
    # Register example functions
    @registry.register(
        name="get_weather",
        description="Get the current weather for a specific location",
        parameters={
            "location": {
                "type": "string",
                "description": "City or location name",
                "min_length": 1
            },
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "Temperature unit"
            }
        },
        required=["location"]
    )
    async def get_weather(location: str, unit: str = "celsius") -> Dict[str, Any]:
        # Mock implementation
        return {
            "temperature": 22,
            "unit": unit,
            "location": location,
            "conditions": "sunny"
        }

    @registry.register(
        name="search_products",
        description="Search for products in the catalog",
        parameters={
            "query": {
                "type": "string",
                "description": "Search query",
                "min_length": 1
            },
            "max_results": {
                "type": "integer",
                "description": "Maximum number of results",
                "minimum": 1,
                "maximum": 50
            },
            "category": {
                "type": "string",
                "description": "Product category",
                "enum": ["electronics", "books", "clothing"]
            }
        },
        required=["query"]
    )
    async def search_products(
        query: str,
        max_results: int = 10,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        # Mock implementation
        return [
            {
                "name": f"Product {i}",
                "query": query,
                "category": category,
                "price": 99.99
            }
            for i in range(min(max_results, 3))
        ]

    # Create LLM instance with OpenAI callable
    llm = MyLLM(
        api_key="your-api-key",
        llm_callable=openai_callable,
        model_config=model_config
    )
    
    # Create function caller
    function_caller = LLMFunctionCaller(llm=llm, registry=registry)
    
    try:
        # Example: Get weather
        weather_result = await function_caller.process_message(
            "What's the weather like in London?",
            temperature=0.8,
            request_timeout=30
        )
        print(f"Weather result: {weather_result}")
        
        # Example: Search products
        search_result = await function_caller.process_message(
            "Find me some laptops under $1000",
            temperature=0.7,
            max_tokens=200
        )
        print(f"Search result: {search_result}")
        
    except FunctionCallError as e:
        print(f"Function call error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
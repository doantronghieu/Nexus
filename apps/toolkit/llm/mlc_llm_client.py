import requests
import json
import re
from typing import List, Dict, Optional, Union, Any, Iterator, Literal, Tuple

"""
Installation:
MacOs: python -m pip install --pre -U -f https://mlc.ai/wheels mlc-llm-nightly-cpu mlc-ai-nightly-cpu
Linux (GPU): python -m pip install --pre -U -f https://mlc.ai/wheels mlc-llm-nightly-cu121 mlc-ai-nightly-cu121

conda install -c conda-forge git-lfs
conda install -c conda-forge libgcc-ng # [Optional]

Run server: mlc_llm serve MODEL_NAME
See MODEL_NAME in `const.py`
"""

class MLCLLMError(Exception):
    """Base exception class for MLCLLMClient errors."""
    pass

class MLCLLMAPIError(MLCLLMError):
    """Exception raised for errors in the API response."""
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.status_code = status_code
        super().__init__(message)

class MLCLLMValidationError(MLCLLMError):
    """Exception raised for validation errors in the client."""
    pass

class MLCLLMClient:
    """
    A client for interacting with the MLC-LLM API.

    This class provides methods for making API calls to the MLC-LLM service,
    including model information retrieval, chat completions, and function calling.
    It includes built-in validation, error handling, and support for both
    streaming and non-streaming responses.

    Attributes:
        __version__ (str): The version of the MLCLLMClient.
        base_url (str): The base URL for the MLC-LLM API.
        headers (dict): HTTP headers to be sent with each request.
    
    Rerferences:
    - https://github.com/mlc-ai/mlc-llm
    - https://huggingface.co/mlc-ai
    - https://llm.mlc.ai/docs/index.html
    """

    __version__ = "1.0.4"

    def __init__(self, base_url: str = "http://127.0.0.1:8000", headers: Optional[Dict[str, str]] = None):
        """
        Initialize the MLCLLMClient.

        :param base_url: The base URL for the MLC-LLM API.
        :param headers: Optional custom headers to be sent with each request.
        """
        self.base_url = self._validate_url(base_url)
        self.headers = headers or {}
        self.headers.setdefault("Content-Type", "application/json")
        self._models_cache = None
        self.session = requests.Session()

    @staticmethod
    def _validate_url(url: str) -> str:
        """
        Validate the given URL.

        :param url: The URL to validate.
        :return: The validated URL.
        :raises MLCLLMValidationError: If the URL format is invalid.
        """
        if not re.match(r'https?://', url):
            raise MLCLLMValidationError("Invalid URL format. Must start with http:// or https://")
        return url

    def get_models(self) -> Dict:
        """
        Get a list of available models.

        :return: A dictionary containing the models data.
        :raises MLCLLMAPIError: If the API request fails.
        """
        url = f"{self.base_url}/v1/models"
        response = self.session.get(url, headers=self.headers, timeout=10)
        response.raise_for_status()
        return response.json()

    def list_models(self) -> List[str]:
        """
        Get a list of available model names.

        :return: A list of model names.
        """
        models_data = self.get_models()
        return [model['id'] for model in models_data.get('data', [])]

    @staticmethod
    def create_message(role: Literal["system", "user", "assistant", "tool"], content: str, name: Optional[str] = None) -> Dict[str, str]:
        """
        Create a properly structured message for the chat completion API.

        :param role: The role of the message sender (system, user, assistant, or tool).
        :param content: The content of the message.
        :param name: An optional name for the sender of the message.
        :return: A dictionary representing the message.
        """
        message = {"role": role, "content": content}
        if name:
            message["name"] = name
        return message

    @staticmethod
    def create_tool(name: str, description: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a properly structured tool definition for function calling.

        :param name: The name of the function.
        :param description: A description of what the function does.
        :param parameters: A dictionary describing the parameters of the function.
        :return: A dictionary representing the tool.
        """
        return {
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": parameters
            }
        }

    def chat_completion(
        self,
        model: Optional[str],
        messages: List[Dict[str, str]],
        stream: bool = False,
        max_tokens: Optional[int] = None,
        temperature: float = 1.0,
        top_p: float = 1.0,
        n: int = 1,
        stop: Optional[Union[str, List[str]]] = None,
        presence_penalty: float = 0.0,
        frequency_penalty: float = 0.0,
        logprobs: bool = False,
        top_logprobs: int = 0,
        logit_bias: Optional[Dict[int, float]] = None,
        seed: Optional[int] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: Optional[Union[Literal["none", "auto"], Dict[str, Any]]] = None,
        response_format: Optional[Dict[Literal["type"], Literal["text", "json_object"]]] = None,
        user: Optional[str] = None
    ) -> Union[Dict, requests.Response]:
        """
        Get a chat completion from the MLC-LLM API.
        
        :param model: The model to use for generation.
        :param messages: A list of message dictionaries.
        :param stream: Whether to stream the response.
        :param max_tokens: The maximum number of tokens to generate.
        :param temperature: Controls randomness in generation.
        :param top_p: Controls diversity via nucleus sampling.
        :param n: Number of completions to generate.
        :param stop: Sequences where the API will stop generating further tokens.
        :param presence_penalty: Penalty for token presence.
        :param frequency_penalty: Penalty for token frequency.
        :param logprobs: Whether to include log probabilities of output tokens.
        :param top_logprobs: Number of most likely tokens to return at each position.
        :param logit_bias: Adjust the probability of specific tokens appearing in the completion.
        :param seed: Seed for deterministic generation.
        :param tools: List of tools available for the model to use.
        :param tool_choice: Controls how tools are selected for use in responses.
        :param response_format: Specify the format for the model's response.
        :param user: A unique identifier for the end-user.
        :return: The API response, either as a dictionary or a streaming response.
        :raises MLCLLMAPIError: If the API request fails.
        """
        url = f"{self.base_url}/v1/chat/completions"
        payload = {
            "messages": messages,
            "stream": stream,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "n": n,
            "stop": stop,
            "presence_penalty": presence_penalty,
            "frequency_penalty": frequency_penalty,
            "logprobs": logprobs,
            "top_logprobs": top_logprobs,
            "logit_bias": logit_bias,
            "seed": seed,
            "tools": tools,
            "tool_choice": tool_choice,
            "response_format": response_format,
            "user": user
        }
        if model:
            payload["model"] = model
        payload = {k: v for k, v in payload.items() if v is not None}

        try:
            if stream:
                return self.session.post(url, json=payload, headers=self.headers, stream=True, timeout=30)
            else:
                response = self.session.post(url, json=payload, headers=self.headers, timeout=30)
                response.raise_for_status()
                return response.json()
        except requests.RequestException as e:
            if isinstance(e, requests.HTTPError):
                raise MLCLLMAPIError(f"API request failed: {str(e)}", status_code=e.response.status_code)
            else:
                raise MLCLLMAPIError(f"API request failed: {str(e)}")

    def process_streaming_response(self, response: requests.Response) -> Iterator[Tuple[str, Optional[Dict]]]:
        """
        Process a streaming response and yield content and metadata.

        :param response: The streaming response from the API.
        :return: An iterator yielding tuples of (content, metadata).
        :raises MLCLLMAPIError: If there's an error processing the streaming response.
        """
        try:
            for chunk in response.iter_content(chunk_size=None):
                chunk = chunk.decode("utf-8")
                if chunk.strip() == "data: [DONE]":
                    break
                if chunk.startswith("data: "):
                    try:
                        response_json = json.loads(chunk[6:])
                        content = response_json["choices"][0]["delta"].get("content", "")
                        metadata = {k: v for k, v in response_json.items() if k != "choices"}
                        yield content, metadata
                    except json.JSONDecodeError:
                        continue
        except requests.RequestException as e:
            raise MLCLLMAPIError(f"Error processing streaming response: {str(e)}")

    def simple_stream(self, response: requests.Response) -> Iterator[str]:
        """
        Process a streaming response and yield only the content.

        :param response: The streaming response from the API.
        :return: An iterator yielding content strings.
        """
        for chunk in response.iter_content(chunk_size=None):
            chunk = chunk.decode("utf-8")
            if "[DONE]" in chunk[6:]:
                break
            if chunk.startswith("data: "):
                try:
                    response_json = json.loads(chunk[6:])
                    content = response_json["choices"][0]["delta"].get("content", "")
                    yield content
                except json.JSONDecodeError:
                    continue

def main():
    client = MLCLLMClient("http://127.0.0.1:8000", headers={"Authorization": "Bearer your_token_here"})

    print(f"MLCLLMClient version: {MLCLLMClient.__version__}")

    # Get available models
    models = client.list_models()
    print("Available models:", models)

    # Example 1: Basic chat completion (non-streaming)
    print("\nExample 1: Basic chat completion (non-streaming)")
    messages = [
        client.create_message("user", "Write a haiku about apples.")
    ]
    response = client.chat_completion(model=None, messages=messages)
    print("Response:", response["choices"][0]["message"]["content"])

    # Example 2: Chat completion with streaming
    print("\nExample 2: Chat completion with streaming")
    messages = [
        client.create_message("user", "Tell me a joke")
    ]
    streaming_response = client.chat_completion(model=None, messages=messages, stream=True)
    print("Streaming response:")
    for content in client.simple_stream(streaming_response):
        print(content, end="", flush=True)
    print("\n")

    # Example 3: Chat completion with function calling
    print("\nExample 3: Chat completion with function calling")
    messages = [
        client.create_message("user", "What's the weather like in Pittsburgh, PA in fahrenheit?")
    ]
    weather_tool = client.create_tool(
        name="get_current_weather",
        description="Get the current weather in a given location",
        parameters={
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "The city and state, e.g. San Francisco, CA"},
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
            },
            "required": ["location"]
        }
    )
    response = client.chat_completion(
        model="HF://mlc-ai/Llama-3.2-1B-Instruct-q4f16_0-MLC",
        messages=messages,
        tools=[weather_tool],
        tool_choice="auto"
    )
    print("Function call response:", response["choices"][0]["message"]["tool_calls"][0]["function"])

    # Example 4: Chat completion with function calling and streaming
    print("\nExample 4: Chat completion with function calling and streaming")
    messages = [
        client.create_message("user", "What is the current weather in Pittsburgh, PA and Tokyo, JP in fahrenheit?")
    ]
    streaming_response = client.chat_completion(
        model="HF://mlc-ai/Llama-3.2-1B-Instruct-q4f16_0-MLC",
        messages=messages,
        tools=[weather_tool],
        tool_choice="auto",
        stream=True
    )
    print("Streaming function call response:")
    for content, metadata in client.process_streaming_response(streaming_response):
        print(content, end="", flush=True)
    print("\n")

if __name__ == "__main__":
    try:
        main()
    except MLCLLMValidationError as e:
        print(f"Validation error: {str(e)}")
    except MLCLLMAPIError as e:
        print(f"API error (Status code: {e.status_code}): {str(e)}")
    except MLCLLMError as e:
        print(f"General error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
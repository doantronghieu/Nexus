import packages
from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel, Field, ValidationError  # Add ValidationError import
from typing import List, Optional, Union, Dict, Any, Literal, AsyncGenerator
import asyncio
import time
import json
import uuid
from enum import Enum
import httpx
import os
from contextlib import asynccontextmanager

# Initialize global HTTP client with connection pooling
http_client = httpx.AsyncClient(
    timeout=httpx.Timeout(timeout=None),
    limits=httpx.Limits(max_keepalive_connections=20, max_connections=40),
    http2=True  # Enable HTTP/2 for better performance
)

# Keep LLM server URL in memory
LLM_SERVER_URL = f"http://localhost:{os.getenv('PORT_SVC_LLM_NANO')}/chat"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create global HTTP client
    yield
    # Shutdown: clean up client
    await http_client.aclose()

app = FastAPI(lifespan=lifespan)

# Response cache for frequently requested prompts
from cachetools import TTLCache
response_cache = TTLCache(maxsize=1000, ttl=3600)  # Cache for 1 hour

async def get_cached_response(cache_key: str):
    """Get cached response if available"""
    return response_cache.get(cache_key)

def cache_response(cache_key: str, response: Any):
    """Cache response for future use"""
    response_cache[cache_key] = response
    
class OpenAIError(Exception):
    def __init__(
        self,
        message: str,
        error_type: "ErrorType",
        code: int,
        param: Optional[str] = None,
    ):
        self.message = message
        self.error_type = error_type
        self.code = code
        self.param = param

class ErrorType(Enum):
    INVALID_REQUEST_ERROR = "invalid_request_error"
    AUTHENTICATION_ERROR = "authentication_error"
    PERMISSION_ERROR = "permission_error"
    RATE_LIMIT_ERROR = "rate_limit_error"
    SERVER_ERROR = "server_error"

class FunctionCall(BaseModel):
    name: str
    arguments: str

class ToolCall(BaseModel):
    id: str = Field(default_factory=lambda: f"call_{uuid.uuid4().hex}")
    type: Literal["function"] = "function"
    function: FunctionCall

class FunctionDescription(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any]

class Tool(BaseModel):
    type: Literal["function"] = "function"
    function: FunctionDescription

class ChatMessage(BaseModel):
    role: str
    content: Optional[str] = None
    function_call: Optional[FunctionCall] = None
    tool_calls: Optional[List[ToolCall]] = None
    name: Optional[str] = None

class ResponseFormat(BaseModel):
    type: Literal["text", "json_object"] = "text"

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    functions: Optional[List[FunctionDescription]] = None
    tools: Optional[List[Tool]] = None
    response_format: Optional[ResponseFormat] = None
    temperature: Optional[float] = 1.0
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False

async def format_prompt(messages: List[ChatMessage], functions: Optional[List[FunctionDescription]] = None, tools: Optional[List[Tool]] = None) -> str:
    """Format messages into a prompt for the LLM"""
    formatted_messages = []
    
    for msg in messages:
        if msg.role == "system":
            formatted_messages.append(f"System: {msg.content}")
        elif msg.role == "user":
            formatted_messages.append(f"User: {msg.content}")
        elif msg.role == "assistant":
            if msg.content:
                formatted_messages.append(f"Assistant: {msg.content}")
            if msg.function_call:
                formatted_messages.append(f"Function call: {msg.function_call.name}({msg.function_call.arguments})")
            if msg.tool_calls:
                for tool in msg.tool_calls:
                    formatted_messages.append(f"Tool call: {tool.function.name}({tool.function.arguments})")
        elif msg.role == "function":
            formatted_messages.append(f"Function response: {msg.content}")
            
    # Add available functions/tools to the prompt if present
    if functions or tools:
        formatted_messages.append("\nAvailable functions:")
        if functions:
            for func in functions:
                formatted_messages.append(f"- {func.name}: {func.description}")
        if tools:
            for tool in tools:
                formatted_messages.append(f"- {tool.function.name}: {tool.function.description}")
                
    return "\n".join(formatted_messages)

async def generate_response(
    messages: List[ChatMessage],
    model: str,
    functions: Optional[List[FunctionDescription]] = None,
    tools: Optional[List[Tool]] = None,
    response_format: Optional[ResponseFormat] = None,
    temperature: Optional[float] = None,
    stream: bool = False
) -> Union[ChatMessage, AsyncGenerator[str, None]]:
    """Generate response using the LLM client"""
    try:
        # Format prompt
        prompt = await format_prompt(messages, functions, tools)
        
        # Prepare request data
        request_data = {
            "mode": "stream" if stream else "sync",
            "messages": [{"role": "user", "content": prompt}],
            "generation_config": {
                "temperature": temperature if temperature is not None else 0.7
            }
        }

        if not stream:
            # Non-streaming request
            response = await http_client.post(
                LLM_SERVER_URL,
                json=request_data,
                timeout=None
            )
            
            if response.status_code != 200:
                raise OpenAIError(
                    f"LLM server error: {response.text}",
                    ErrorType.SERVER_ERROR,
                    status.HTTP_500_INTERNAL_SERVER_ERROR
                )
                
            result = response.json()
            return ChatMessage(role="assistant", content=result["response"])
        
        # For streaming, return an async generator
        async def response_generator():
            async with http_client.stream(
                "POST",
                LLM_SERVER_URL,
                json=request_data,
                timeout=None
            ) as response:
                async for raw_bytes in response.aiter_bytes():
                    if raw_bytes:
                        yield raw_bytes.decode('utf-8')
        
        return response_generator()

    except Exception as e:
        raise OpenAIError(
            str(e),
            ErrorType.SERVER_ERROR,
            status.HTTP_500_INTERNAL_SERVER_ERROR
        )

async def stream_chat_response(
    messages: List[ChatMessage],
    model: str,
    functions: Optional[List[FunctionDescription]] = None,
    tools: Optional[List[Tool]] = None,
    response_format: Optional[ResponseFormat] = None,
    temperature: Optional[float] = None
):
    """Stream chat responses"""
    try:
        # Format prompt
        prompt = await format_prompt(messages, functions, tools)
        
        # Prepare request data
        request_data = {
            "mode": "stream",
            "messages": [{"role": "user", "content": prompt}],
            "generation_config": {
                "temperature": temperature if temperature is not None else 0.7
            }
        }

        async with http_client.stream(
            "POST",
            LLM_SERVER_URL,
            json=request_data,
            timeout=None
        ) as response:
            if response.status_code != 200:
                raise OpenAIError(
                    f"LLM server error: {await response.text()}",
                    ErrorType.SERVER_ERROR,
                    status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            async for raw_bytes in response.aiter_bytes():
                if raw_bytes:
                    token = raw_bytes.decode('utf-8')
                    chunk = {
                        "id": f"chatcmpl-{uuid.uuid4().hex}",
                        "object": "chat.completion.chunk",
                        "created": int(time.time()),
                        "model": model,
                        "choices": [{
                            "delta": {
                                "content": token
                            },
                            "index": 0,
                            "finish_reason": None
                        }]
                    }
                    yield f"data: {json.dumps(chunk)}\n\n"
        
        # Send final chunks
        final_chunk = {
            "id": f"chatcmpl-{uuid.uuid4().hex}",
            "object": "chat.completion.chunk",
            "created": int(time.time()),
            "model": model,
            "choices": [{
                "delta": {},
                "index": 0,
                "finish_reason": "stop"
            }]
        }
        yield f"data: {json.dumps(final_chunk)}\n\n"
        yield "data: [DONE]\n\n"
        
    except Exception as e:
        raise OpenAIError(
            str(e),
            ErrorType.SERVER_ERROR,
            status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    try:
        body = await request.json()
        
        # Convert body to messages format if needed
        if "prompt" in body and "messages" not in body:
            messages = [{"role": "user", "content": body["prompt"]}]
            body["messages"] = messages
            del body["prompt"]
        
        request_data = ChatCompletionRequest(**body)
        
        if request_data.stream:
            return StreamingResponse(
                stream_chat_response(
                    request_data.messages,
                    request_data.model,
                    request_data.functions,
                    request_data.tools,
                    request_data.response_format,
                    request_data.temperature
                ),
                media_type="text/event-stream"
            )

        # Format prompt
        prompt = await format_prompt(
            request_data.messages,
            request_data.functions,
            request_data.tools
        )

        # Make request to LLM server
        response = await http_client.post(
            LLM_SERVER_URL,
            json={
                "mode": "sync",
                "messages": [{"role": "user", "content": prompt}],
                "generation_config": {
                    "temperature": request_data.temperature if request_data.temperature is not None else 0.7
                }
            }
        )

        if response.status_code != 200:
            raise OpenAIError(
                f"LLM server error: {response.text}",
                ErrorType.SERVER_ERROR,
                status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        result = response.json()
        content = result["response"]

        return {
            "id": f"chatcmpl-{uuid.uuid4().hex}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": request_data.model,
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": content
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": sum(len(msg.content.split()) if msg.content else 0 
                                  for msg in request_data.messages),
                "completion_tokens": len(content.split()),
                "total_tokens": sum(len(msg.content.split()) if msg.content else 0 
                                 for msg in request_data.messages) + len(content.split())
            }
        }
        
    except ValidationError as e:
        raise OpenAIError(
            str(e),
            ErrorType.INVALID_REQUEST_ERROR,
            status.HTTP_422_UNPROCESSABLE_ENTITY
        )
    except Exception as e:
        raise OpenAIError(
            str(e),
            ErrorType.SERVER_ERROR,
            status.HTTP_500_INTERNAL_SERVER_ERROR
        )
                
async def stream_completion_response(
    messages: List[ChatMessage],
    model: str,
    temperature: Optional[float] = None
):
    """Stream completion responses"""
    try:
        # Get streaming response
        response = await generate_response(
            messages, model, temperature=temperature, stream=True
        )
        
        async with response as streaming_response:
            async for raw_bytes in streaming_response.aiter_bytes():
                if raw_bytes:
                    token = raw_bytes.decode('utf-8')
                    chunk = {
                        "id": f"cmpl-{uuid.uuid4().hex}",
                        "object": "text_completion",
                        "created": int(time.time()),
                        "model": model,
                        "choices": [{
                            "text": token,
                            "index": 0,
                            "logprobs": None,
                            "finish_reason": None
                        }]
                    }
                    yield f"data: {json.dumps(chunk)}\n\n"
            
        # Send final chunk
        final_chunk = {
            "id": f"cmpl-{uuid.uuid4().hex}",
            "object": "text_completion",
            "created": int(time.time()),
            "model": model,
            "choices": [{
                "text": "",
                "index": 0,
                "logprobs": None,
                "finish_reason": "stop"
            }]
        }
        yield f"data: {json.dumps(final_chunk)}\n\n"
        yield "data: [DONE]\n\n"
        
    except Exception as e:
        raise OpenAIError(
            str(e),
            ErrorType.SERVER_ERROR,
            status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# Add completions endpoint for legacy support
@app.post("/v1/completions")
async def completions(request: Request):
    """Optimized completions endpoint"""
    try:
        body = await request.json()
        prompt = body.get("prompt", "")
        
        # Check cache for non-streaming requests
        if not body.get("stream", False):
            cache_key = f"completion:{prompt}:{body.get('temperature', 1.0)}"
            cached_response = await get_cached_response(cache_key)
            if cached_response:
                return cached_response
        
        # Convert to messages format
        messages = [{"role": "user", "content": prompt}]
        
        if body.get("stream", False):
            return StreamingResponse(
                stream_completion_response(messages, body.get("model", "nano-llm"), body.get("temperature")),
                media_type="text/event-stream"
            )
            
        # Get response
        response = await generate_response(
            messages=messages,
            model=body.get("model", "nano-llm"),
            temperature=body.get("temperature")
        )
        
        # Format response
        completion_response = {
            "id": f"cmpl-{uuid.uuid4().hex}",
            "object": "text_completion",
            "created": int(time.time()),
            "model": body.get("model", "nano-llm"),
            "choices": [{
                "text": response.content,
                "index": 0,
                "logprobs": None,
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": len(prompt.split()),
                "completion_tokens": len(response.content.split()) if response.content else 0,
                "total_tokens": len(prompt.split()) + (len(response.content.split()) if response.content else 0)
            }
        }
        
        # Cache the response
        cache_response(cache_key, completion_response)
        
        return completion_response
        
    except Exception as e:
        raise OpenAIError(str(e), ErrorType.SERVER_ERROR, status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.get("/v1/models")
async def list_models():
    """Return available models in OpenAI format"""
    return {
        "data": [
            {
                "id": "nano-llm",
                "object": "model",
                "created": int(time.time()),
                "owned_by": "user",
                "permission": [],
                "root": "nano-llm",
                "parent": None
            }
        ]
    }

# Error handling middleware
@app.middleware("http")
async def error_handler(request: Request, call_next):
    try:
        return await call_next(request)
    except OpenAIError as e:
        return JSONResponse(
            status_code=e.code,
            content={
                "error": {
                    "message": e.message,
                    "type": e.error_type.value,
                    "code": e.code,
                    "param": e.param
                }
            }
        )
    except ValidationError as e:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": {
                    "message": str(e),
                    "type": ErrorType.INVALID_REQUEST_ERROR.value,
                    "code": status.HTTP_422_UNPROCESSABLE_ENTITY
                }
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "message": str(e),
                    "type": ErrorType.SERVER_ERROR.value,
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR
                }
            }
        )

@app.on_event("shutdown")
async def shutdown_event():
    await http_client.aclose()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
# llm_openai.py
import nano_llm
from nano_llm import NanoLLM, ChatHistory
from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel, Field, ValidationError
from typing import AsyncGenerator, Optional, List, Union, Dict, Any, Literal
from enum import Enum
import logging
import asyncio
import time
import json
import uuid
import os
from abc import ABC, abstractmethod

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

class ChatMessage(BaseModel):
    role: str
    content: Optional[str] = None
    function_call: Optional[Dict[str, Any]] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None
    name: Optional[str] = None

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    temperature: Optional[float] = 1.0
    stream: Optional[bool] = False
    max_tokens: Optional[int] = None

class BaseLLMOpenAI(ABC):
    """Base class for OpenAI-compatible LLM implementations"""
    
    def __init__(
        self,
        default_system_prompt: str = "You are a helpful and friendly AI assistant.",
        default_max_tokens: int = 512
    ):
        self.default_system_prompt = default_system_prompt
        self.default_max_tokens = default_max_tokens

    @abstractmethod
    async def generate_completion(
        self,
        messages: List[Dict[str, str]],
        stream: bool = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> Union[str, AsyncGenerator[str, None]]:
        """Generate completion from messages"""
        pass

    @abstractmethod
    def get_model_info(self) -> Dict:
        """Get model information"""
        pass

    @abstractmethod
    async def close(self):
        """Cleanup resources"""
        pass

class NanoLLMOpenAI(BaseLLMOpenAI):
    """NanoLLM implementation of OpenAI-compatible interface"""
    
    def __init__(
        self,
        model_name: str = "meta-llama/Meta-Llama-3-8B-Instruct",
        api: str = "mlc",
        api_token: str = "HF_API_KEY",
        quantization: str = "q4f16_ft",
        default_system_prompt: str = "You are a helpful and friendly AI assistant.",
        default_max_tokens: int = 512
    ):
        super().__init__(default_system_prompt, default_max_tokens)
        self.model = NanoLLM.from_pretrained(
            model_name,
            api=api,
            api_token=api_token,
            quantization=quantization
        )
        self.model_name = model_name
        self.api = api
        self.quantization = quantization
        logging.info(f"Initialized NanoLLM with model: {model_name}")

    def create_chat_history(self, system_prompt: Optional[str] = None) -> ChatHistory:
        return ChatHistory(
            self.model, 
            system_prompt=system_prompt or self.default_system_prompt
        )

    def _process_messages(self, messages: List[Dict[str, str]]) -> ChatHistory:
        chat_history = self.create_chat_history()
        
        for msg in messages:
            if msg["role"] == "system":
                chat_history.system_prompt = msg["content"]
            else:
                chat_history.append(msg["role"], msg["content"])
                
        return chat_history

    async def generate_completion(
        self,
        messages: List[Dict[str, str]],
        stream: bool = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> Union[str, AsyncGenerator[str, None]]:
        try:
            chat_history = self._process_messages(messages)
            embedding, position = chat_history.embed_chat()

            generation_kwargs = {
                "streaming": stream,
                "kv_cache": chat_history.kv_cache,
                "stop_tokens": chat_history.template.stop,
                "max_new_tokens": max_tokens if max_tokens is not None else self.default_max_tokens
            }
            
            if temperature is not None:
                generation_kwargs["temperature"] = temperature

            if stream:
                async def token_generator():
                    response = self.model.generate(embedding, **generation_kwargs)
                    
                    for token in response:
                        if token and not response.eos:
                            yield token
                            await asyncio.sleep(0)

                    if hasattr(response, 'kv_cache'):
                        chat_history.kv_cache = response.kv_cache

                return token_generator()
            else:
                response = self.model.generate(embedding, **generation_kwargs)
                
                if hasattr(response, 'kv_cache'):
                    chat_history.kv_cache = response.kv_cache
                
                return str(response)

        except Exception as e:
            logging.error(f"Error generating completion: {str(e)}")
            raise

    def get_model_info(self) -> Dict:
        return {
            "model_name": self.model_name,
            "api": self.api,
            "quantization": self.quantization,
            "default_system_prompt": self.default_system_prompt,
            "default_max_tokens": self.default_max_tokens,
            "capabilities": {
                "streaming": True,
                "max_tokens": self.default_max_tokens,
                "temperature": True
            }
        }

    async def close(self):
        if hasattr(self.model, 'close'):
            await self.model.close()

class ServerLLMOpenAI:
    """FastAPI server implementation for OpenAI-compatible API"""
    
    def __init__(self, llm: BaseLLMOpenAI):
        self.llm = llm
        self.app = FastAPI()
        self._setup_routes()
        
    def _setup_routes(self):
        @self.app.post("/v1/chat/completions")
        async def chat_completions(request: ChatCompletionRequest):
            return await self._handle_chat_completions(request)

        @self.app.get("/v1/models")
        async def list_models():
            return await self._handle_list_models()

        @self.app.middleware("http")
        async def error_handler(request: Request, call_next):
            return await self._handle_errors(request, call_next)

    async def _stream_chat_response(
        self,
        messages: List[ChatMessage],
        model_name: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ):
        try:
            message_dicts = [msg.dict(exclude_none=True) for msg in messages]
            async for token in await self.llm.generate_completion(
                message_dicts,
                stream=True,
                temperature=temperature,
                max_tokens=max_tokens
            ):
                if token:
                    chunk = {
                        "id": f"chatcmpl-{uuid.uuid4().hex}",
                        "object": "chat.completion.chunk",
                        "created": int(time.time()),
                        "model": model_name,
                        "choices": [{
                            "delta": {
                                "content": token
                            },
                            "index": 0,
                            "finish_reason": None
                        }]
                    }
                    yield f"data: {json.dumps(chunk)}\n\n"

            final_chunk = {
                "id": f"chatcmpl-{uuid.uuid4().hex}",
                "object": "chat.completion.chunk",
                "created": int(time.time()),
                "model": model_name,
                "choices": [{
                    "delta": {},
                    "index": 0,
                    "finish_reason": "stop"
                }]
            }
            yield f"data: {json.dumps(final_chunk)}\n\n"
            yield "data: [DONE]\n\n"

        except Exception as e:
            raise OpenAIError(str(e), ErrorType.SERVER_ERROR, status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def _handle_chat_completions(self, request: ChatCompletionRequest):
        try:
            if request.stream:
                return StreamingResponse(
                    self._stream_chat_response(
                        request.messages,
                        request.model,
                        request.temperature,
                        request.max_tokens
                    ),
                    media_type="text/event-stream"
                )

            message_dicts = [msg.dict(exclude_none=True) for msg in request.messages]
            response_text = await self.llm.generate_completion(
                message_dicts,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            )
            
            return {
                "id": f"chatcmpl-{uuid.uuid4().hex}",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": request.model,
                "choices": [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response_text
                    },
                    "finish_reason": "stop"
                }],
                "usage": {
                    "prompt_tokens": sum(len(msg.content.split()) if msg.content else 0 
                                    for msg in request.messages),
                    "completion_tokens": len(response_text.split()),
                    "total_tokens": sum(len(msg.content.split()) if msg.content else 0 
                                    for msg in request.messages) + len(response_text.split())
                }
            }

        except ValidationError as e:
            raise OpenAIError(str(e), ErrorType.INVALID_REQUEST_ERROR, status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as e:
            raise OpenAIError(str(e), ErrorType.SERVER_ERROR, status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def _handle_list_models(self):
        model_info = self.llm.get_model_info()
        return {
            "data": [
                {
                    "id": "nano-llm",
                    "object": "model",
                    "created": int(time.time()),
                    "owned_by": "user",
                    "permission": [],
                    "root": "nano-llm",
                    "parent": None,
                    **model_info
                }
            ]
        }

    async def _handle_errors(self, request: Request, call_next):
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

    def run(self, host: str = "0.0.0.0", port: int = 8000):
        """Run the server"""
        import uvicorn
        uvicorn.run(self.app, host=host, port=port)

if __name__ == "__main__":
    # Initialize the LLM
    llm = NanoLLMOpenAI()
    
    # Create and run the server
    server = ServerLLMOpenAI(llm)
    server.run()
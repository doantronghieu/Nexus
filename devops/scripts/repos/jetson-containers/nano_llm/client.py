import asyncio, httpx, os, sys
from dataclasses import dataclass
from enum import Enum
from pydantic import BaseModel, Field
from termcolor import cprint
from typing import Any, AsyncGenerator, Callable, Dict, List, Optional, Union

class ChatMode(str, Enum):
    SYNC = "sync"
    ASYNC = "async"
    STREAM = "stream"
    ASTREAM = "astream"

SPECIAL_TOKENS = [
    '</s>', 
    '<|endoftext|>', 
    '<|im_end|>', 
    '<eos>', 
    '<|end_of_text|>', 
    '<|eot_id|>',
    '<s>',
]

def remove_special_tokens(text: str) -> str:
    """Remove special tokens from text response"""
    for token in SPECIAL_TOKENS:
        text = text.replace(token, '')
    return text.strip()

@dataclass
class ChatMessage:
    role: str
    content: str

    def to_dict(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}

class GenerationConfig(BaseModel):
    """Generation parameters for the model"""
    max_new_tokens: Optional[int] = Field(default=256)
    min_new_tokens: Optional[int] = Field(default=-1)
    do_sample: Optional[bool] = Field(default=True)
    repetition_penalty: Optional[float] = Field(default=1.0)
    temperature: Optional[float] = Field(default=0.0)
    top_p: Optional[float] = Field(default=0.95)
    stop_tokens: Optional[List[str]] = Field(default=None)

class ChatResponse:
    """Wrapper for chat responses"""
    def __init__(self, content: str = "", error: Optional[str] = None):
        self.content = content
        self.error = error
        self.is_error = error is not None

    @staticmethod
    def success(content: str) -> 'ChatResponse':
        return ChatResponse(content=content)

    @staticmethod
    def failure(error: str) -> 'ChatResponse':
        return ChatResponse(error=error)

class LLMClient:
    def __init__(
        self,
        base_url: str = "http://localhost:8767",
        system_prompt: str = "You are a helpful and friendly AI assistant.",
        use_history: bool = False,
        on_token: Optional[Callable[[str], None]] = None,
        on_error: Optional[Callable[[str], None]] = None,
        on_complete: Optional[Callable[[str], None]] = None
    ):
        self.base_url = base_url
        self.system_prompt = system_prompt
        self.use_history = use_history
        self.chat_history: List[ChatMessage] = []
        self.generation_config = GenerationConfig()
        
        self.on_token = on_token
        self.on_error = on_error
        self.on_complete = on_complete
        
        # Use limits and timeouts optimized for LLM responses
        self._http_client = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout=None),
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10),
            http2=True
        )

    async def close(self):
        if self._http_client:
            await self._http_client.aclose()

    def update_config(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if hasattr(self.generation_config, key):
                setattr(self.generation_config, key, value)

    def clear_history(self) -> None:
        self.chat_history.clear()

    def _build_request(self, prompt: str, mode: ChatMode) -> dict:
        current_message = ChatMessage(role="user", content=prompt)
        
        messages = (
            [msg.to_dict() for msg in ([*self.chat_history, current_message] if self.use_history else [current_message])]
        )
        
        return {
            "mode": mode,
            "messages": messages,
            "system_prompt": self.system_prompt,
            "generation_config": self.generation_config.dict(exclude_unset=True)
        }

    async def _process_stream(self, response: httpx.Response) -> str:
        current_message = []  # Use list for more efficient string building
        try:
            async for chunk in response.aiter_bytes():
                if chunk:
                    token = chunk.decode('utf-8', errors='replace')
                    current_message.append(token)
                    
                    if self.on_token:
                        self.on_token(token)
            
            final_message = "".join(current_message)
            
            if self.use_history:
                self.chat_history.append(ChatMessage(role="bot", content=final_message))
            
            if self.on_complete:
                self.on_complete(final_message)
                
            return final_message
                
        except Exception as e:
            if self.on_error:
                self.on_error(str(e))
            raise

    async def _process_sync_response(self, response_json: dict) -> ChatResponse:
        try:
            response_text = response_json["response"]
            cleaned_response = remove_special_tokens(response_text)
            
            if self.use_history:
                self.chat_history.append(ChatMessage(role="bot", content=cleaned_response))
            
            if self.on_complete:
                self.on_complete(cleaned_response)
                
            return ChatResponse.success(cleaned_response)
            
        except Exception as e:
            error_msg = f"Error processing response: {str(e)}"
            if self.on_error:
                self.on_error(error_msg)
            return ChatResponse.failure(error_msg)

    async def chat(
        self, 
        prompt: str, 
        mode: ChatMode = ChatMode.STREAM
    ) -> Union[ChatResponse, str]:
        """
        Send a chat message and get response.
        
        Args:
            prompt: User input message
            mode: Chat mode (sync/async/stream/astream), defaults to stream
            
        Returns:
            For streaming modes: Complete response string
            For sync modes: ChatResponse object with cleaned response text
        """
        request_data = self._build_request(prompt, mode)
        headers = {"Content-Type": "application/json"}

        try:
            if mode in [ChatMode.STREAM, ChatMode.ASTREAM]:
                async with self._http_client.stream(
                    "POST",
                    f"{self.base_url}/chat",
                    json=request_data,
                    headers=headers,
                    timeout=None
                ) as response:
                    return await self._process_stream(response)
            else:
                response = await self._http_client.post(
                    f"{self.base_url}/chat",
                    json=request_data,
                    headers=headers
                )
                
                if response.status_code == 200:
                    return await self._process_sync_response(response.json())
                else:
                    error_msg = f"Error: Server returned status code {response.status_code}\nResponse: {response.text}"
                    if self.on_error:
                        self.on_error(error_msg)
                    return ChatResponse.failure(error_msg)
                    
        except Exception as e:
            error_msg = f"Request error: {str(e)}"
            if self.on_error:
                self.on_error(error_msg)
            return ChatResponse.failure(error_msg)

class TerminalState:
    def __init__(self):
        self.current_mode = ChatMode.STREAM
        self.history_enabled = False

    def print_prompt(self):
        mode_color = 'green' if self.current_mode in [ChatMode.STREAM, ChatMode.ASTREAM] else 'yellow'
        history_status = "H" if self.history_enabled else "-"
        cprint(f"[{self.current_mode.value}|{history_status}] >> ", mode_color, end='', flush=True)

    def print_response(self, response: Union[str, ChatResponse]):
        if isinstance(response, ChatResponse):
            if response.is_error:
                cprint(f"\nError: {response.error}", 'red')
            else:
                cprint(response.content, 'blue')
        else:
            # Streaming response is already printed by the token callback
            pass

class TerminalApp:
    def __init__(self):
        self.terminal = TerminalState()
        self.client = LLMClient(
            use_history=self.terminal.history_enabled,
            on_token=lambda token: print(token, end='', flush=True),
            on_error=lambda error: cprint(f"\nError: {error}", 'red'),
            on_complete=lambda _: print()
        )

    def handle_command(self, command: str) -> bool:
        """Handle terminal commands. Returns True if command was handled."""
        if command.startswith('/'):
            cmd_parts = command.lower().strip().split()
            cmd = cmd_parts[0]
            
            if cmd == '/mode':
                if len(cmd_parts) == 1:
                    # Just show available modes if no mode specified
                    cprint("Available modes:", 'yellow')
                    for mode in ChatMode:
                        cprint(f"  {mode.value} {'(current)' if mode == self.terminal.current_mode else ''}", 'yellow')
                    return True
                    
                # Try to switch to the specified mode
                requested_mode = cmd_parts[1]
                try:
                    new_mode = ChatMode(requested_mode)  # This validates the mode
                    self.terminal.current_mode = new_mode
                    cprint(f"Switched to {new_mode.value} mode", 'green')
                except ValueError:
                    cprint(f"Invalid mode: {requested_mode}", 'red')
                    cprint("Available modes:", 'yellow')
                    for mode in ChatMode:
                        cprint(f"  {mode.value}", 'yellow')
                return True
                
            elif cmd == '/history':
                self.terminal.history_enabled = not self.terminal.history_enabled
                self.client.use_history = self.terminal.history_enabled
                cprint(f"History {'enabled' if self.terminal.history_enabled else 'disabled'}", 'green')
                return True
                
            elif cmd == '/clear':
                self.client.clear_history()
                cprint("Chat history cleared", 'green')
                return True
                
            elif cmd == '/temp':
                if len(cmd_parts) > 1:
                    try:
                        temp = float(cmd_parts[1])
                        self.client.update_config(temperature=temp)
                        cprint(f"Temperature set to {temp}", 'green')
                    except ValueError:
                        cprint("Invalid temperature value", 'red')
                return True
                
            elif cmd == '/config':
                config = self.client.generation_config.dict()
                cprint("\nCurrent configuration:", 'yellow')
                for key, value in config.items():
                    if value is not None:
                        cprint(f"  {key}: {value}", 'yellow')
                cprint(f"\nCurrent mode: {self.terminal.current_mode.value}", 'yellow')
                cprint(f"History: {'enabled' if self.terminal.history_enabled else 'disabled'}", 'yellow')
                return True
                
            elif cmd == '/help':
                cprint("\nAvailable commands:", 'yellow')
                cprint("  /mode          - Show current mode and available modes", 'yellow')
                cprint("  /mode <mode>   - Switch to specified mode (sync/async/stream/astream)", 'yellow')
                cprint("  /history       - Toggle chat history", 'yellow')
                cprint("  /clear         - Clear chat history", 'yellow')
                cprint("  /temp N        - Set temperature (0.0-1.0)", 'yellow')
                cprint("  /config        - Show current configuration", 'yellow')
                cprint("  /help          - Show this help", 'yellow')
                cprint("  /quit          - Exit the program", 'yellow')
                return True
                
            elif cmd == '/quit':
                raise KeyboardInterrupt()
                
            else:
                cprint(f"Unknown command: {command}", 'red')
                return True
                
        return False

    async def run(self):
        cprint("\nChat client started. Type /help for commands.", 'green')
        cprint(f"Current mode: {self.terminal.current_mode.value}", 'green')
        
        try:
            while True:
                self.terminal.print_prompt()
                prompt = input().strip()
                
                if not prompt:
                    continue
                    
                if not self.handle_command(prompt):
                    response = await self.client.chat(prompt, mode=self.terminal.current_mode)
                    self.terminal.print_response(response)
                    
        except KeyboardInterrupt:
            cprint("\nExiting...", 'yellow')
        finally:
            await self.client.close()

def main():
    app = TerminalApp()
    asyncio.run(app.run())

if __name__ == "__main__":
    main()
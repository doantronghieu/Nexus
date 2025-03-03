import asyncio
import streamlit as st
from functools import wraps
import threading
from typing import Any, Callable
from queue import Queue
import time

class AsyncWebSocket:
    """Async WebSocket support for Streamlit."""
    def __init__(self):
        self._loop = None
        self._thread = None
        self._queue = Queue()
        self._running = False
        
    def start(self):
        """Start the async event loop in a separate thread."""
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._run_event_loop)
            self._thread.daemon = True
            self._thread.start()
            
    def stop(self):
        """Stop the async event loop."""
        self._running = False
        if self._loop:
            self._loop.call_soon_threadsafe(self._loop.stop)
        if self._thread:
            self._thread.join()
            
    def _run_event_loop(self):
        """Run the async event loop."""
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()
        
    async def _run_coroutine(self, coro):
        """Run a coroutine and put its result in the queue."""
        try:
            result = await coro
            self._queue.put((result, None))
        except Exception as e:
            self._queue.put((None, e))
            
    def run(self, coro):
        """Run a coroutine and return its result."""
        if not self._running:
            self.start()
            
        asyncio.run_coroutine_threadsafe(
            self._run_coroutine(coro),
            self._loop
        )
        
        result, error = self._queue.get()
        if error:
            raise error
        return result

def async_support(f: Callable) -> Callable:
    """Decorator to add async support to Streamlit functions."""
    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if 'async_websocket' not in st.session_state:
            st.session_state.async_websocket = AsyncWebSocket()
        return st.session_state.async_websocket.run(f(*args, **kwargs))
    return wrapper
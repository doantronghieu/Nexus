import packages
from context.utils import consts as c

import re, copy, json, threading, time, traceback, os, inspect, asyncio, \
    statistic, uuid, inspect, types, yaml, statistics, httpx
from contextlib import contextmanager
from pathlib import Path
from faker import Faker

from dataclasses import dataclass, field
from enum import Enum, auto
from functools import wraps
from urllib.parse import quote

from typing import (
    Any, Callable, ContextManager, Dict, List, Literal, Optional, Tuple, Type, 
    Union, Coroutine
)

from loguru import logger
from tqdm.asyncio import tqdm
from datetime import datetime
from uuid import uuid4
from fastapi.responses import JSONResponse

from rich import print as rprint
from rich.console import Console
from rich.table import Table
from rich.theme import Theme
from rich.panel import Panel
from rich.pretty import Pretty
from rich.text import Text

#*==============================================================================

def get_name(obj):
    """
    Get the name of a variable or function passed to this function.
    
    Args:
        obj: Any variable or function whose name you want to retrieve
        
    Returns:
        str: Name of the variable/function, or None if name cannot be determined
        
    Example:
        x = 42
        def test_func(): pass
        
        name1 = get_name(x)          # Returns 'x'
        name2 = get_name(test_func)  # Returns 'test_func'
    """
    # First check if it's a function
    if isinstance(obj, types.FunctionType):
        return obj.__name__
        
    try:
        frame = inspect.currentframe()
        if frame is None:
            return None
            
        caller_frame = frame.f_back
        if caller_frame is None:
            return None
            
        result = next(
            (var_name for var_name, var_val in caller_frame.f_locals.items() 
             if var_val is obj), 
            None
        )
        
        return result
        
    except Exception:
        return None
        
    finally:
        if 'frame' in locals():
            del frame
        if 'caller_frame' in locals():
            del caller_frame
            
def read_json_file(file_path: str) -> Union[Dict[str, Any], List[Any]]:
    """
    Reads and parses a JSON file.
    
    Args:
        file_path (str): Path to the JSON file
        
    Returns:
        Union[Dict[str, Any], List[Any]]: Parsed JSON data as a dictionary or list
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
        PermissionError: If the program doesn't have read permissions for the file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {file_path} was not found")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Error decoding JSON in {file_path}: {str(e)}", e.doc, e.pos)
    except PermissionError:
        raise PermissionError(f"Permission denied accessing {file_path}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred while reading {file_path}: {str(e)}")

def save_to_json(
   data: Union[Dict, List, str, int, float, bool],
   filename: Union[str, Path],
   indent: int = 2,
   encoding: str = 'utf-8'
) -> None:
   """
   Save any JSON-serializable data to a JSON file.
   
   Args:
       data: The data to save (dict, list, string, number, bool)
       filename: The name of the file to save to (e.g., 'data.json')
       indent: Number of spaces for indentation (default: 2)
       encoding: File encoding (default: utf-8)
   
   Returns:
       None
       
   Raises:
       TypeError: If data is not JSON serializable
       IOError: If there's an error writing to the file
   """
   try:
       with open(filename, 'w', encoding=encoding) as f:
           json.dump(data, f, indent=indent, ensure_ascii=False)
       print(f"Data successfully saved to {filename}")
   except TypeError as e:
       print(f"Error: Data is not JSON serializable - {e}")
   except IOError as e:
       print(f"Error: Failed to write to file - {e}")
   except Exception as e:
       print(f"Error saving data: {e}")

def try_except_pass(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            pass
    return wrapper

def read_file_content(filename):
    """
    Usage example:
    file_content = read_file_content('filename.txt')
    if file_content is not None:
        print(file_content)
    """
    try:
        with open(filename, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return None
    except IOError:
        print(f"Error: There was an issue reading the file '{filename}'.")
        return None

def timed_api(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        execution_time = round(end_time - start_time, 2)
        
        if isinstance(result, JSONResponse):
            content = result.body
            try:
                content_dict = json.loads(content)
                content_dict["execution_time_seconds"] = execution_time
                return JSONResponse(content=content_dict)
            except json.JSONDecodeError:
                # If the content is not JSON, wrap it in a new JSONResponse
                return JSONResponse(content={
                    "result": content,
                    "execution_time_seconds": execution_time
                })
        else:
            # If the result is not a JSONResponse, wrap it in one
            return JSONResponse(content={
                "result": result,
                "execution_time_seconds": execution_time
            })
    
    return wrapper

def safe_deepcopy(obj, unpicklable_attrs=['lock'], lock_types=(threading.Lock, threading.RLock), lock_factory=threading.RLock):
    removed_attrs = {}
    for attr in unpicklable_attrs:
        if hasattr(obj, attr):
            value = getattr(obj, attr)
            if isinstance(value, lock_types):
                removed_attrs[attr] = value
                delattr(obj, attr)

    try:
        new_obj = copy.deepcopy(obj)
    finally:
        for attr, value in removed_attrs.items():
            setattr(obj, attr, value)

    for attr in removed_attrs:
        setattr(new_obj, attr, lock_factory())

    return new_obj

async def time_it(
    func_or_code: Any = None,
    name: str = None,
    n_times: Optional[int] = None,
    warmup: bool = True
) -> Union[Any, tuple[Any, Dict[str, Any]]]:
    """
    Time the execution of a function, async function, or code block, with optional multiple runs.
    
    Args:
        func_or_code: Function, async function, lambda, or code string to execute
        name: Name of the operation for display (default: "Operation")
        n_times: Number of times to run for averaging (default: None = single run)
        warmup: Whether to perform a warmup run before timing (default: True)
    """
    
    custom_theme = Theme({
        "info": "bright_blue",
        "stats": "bright_green",
        "warning": "bright_yellow",
        "time": "bright_cyan",
        "header": "bright_magenta"
    })

    console = Console(theme=custom_theme)
    
    if func_or_code is None:
        raise ValueError("func_or_code must be provided")
    if n_times is not None and n_times <= 0:
        raise ValueError("n_times must be positive")
        
    operation_name = name or "Operation"
    times = []
    last_result = None

    async def execute_once():
        result = func_or_code()
        # If the result is a coroutine, await it
        if asyncio.iscoroutine(result):
            return await result
        return result

    # Perform warmup if requested
    if warmup and callable(func_or_code):
        console.print(f"[warning]Performing warmup run for {operation_name}...[/warning]")
        await execute_once()

    # Single run case
    if n_times is None:
        start_time = time.perf_counter()
        result = await execute_once()
        execution_time = time.perf_counter() - start_time
        console.print(f"[info]{operation_name}[/info] took [time]{execution_time:.4f}[/time] seconds")
        return result

    # Multiple runs case with progress bar
    async for _ in tqdm(
        range(n_times),
        desc=f"Running {operation_name}",
        unit="run",
        colour="green",
        leave=False
    ):
        start_time = time.perf_counter()
        last_result = await execute_once()
        execution_time = time.perf_counter() - start_time
        times.append(execution_time)

    # Calculate statistics
    stats = {
        'avg_time': statistics.mean(times),
        'min_time': min(times),
        'max_time': max(times),
        'std_dev': statistics.stdev(times) if len(times) > 1 else 0,
        'all_times': times
    }

    # Create and populate table
    table = Table(
        show_header=True,
        header_style="bright_magenta",
        show_lines=True,
        title=f"{operation_name} • {n_times} runs",
        title_style="header",
        title_justify="center"
    )
    
    table.add_column("Metric", style="stats", justify="right")
    table.add_column("Time (s)", style="time", justify="center")
    
    table.add_row("Average", f"{stats['avg_time']:.4f}")
    table.add_row("Minimum", f"{stats['min_time']:.4f}")
    table.add_row("Maximum", f"{stats['max_time']:.4f}")
    table.add_row("Std Dev", f"{stats['std_dev']:.4f}")

    # Print table
    console.print(table)

    return last_result, stats

def print_dict_as_table(dictionary, table_name="Dictionary Contents"):
    table = Table(title=table_name)
    
    table.add_column("Key", style="bright_cyan", no_wrap=True)
    table.add_column("Value", style="bright_magenta")
    table.add_column("Type", style="bright_green")

    for key, value in dictionary.items():
        table.add_row(str(key), str(value), str(type(value).__name__))

    console = Console()
    console.print(table)

def rp_print(var: Any, title: str = None) -> None:
    """
    Pretty prints any Python variable using rich library with bright colors.
    If no title provided, tries to get the variable name from the calling context.
    Works with imported functions and direct usage.
    
    Args:
        var: Any Python variable (number, string, list, tuple, dict, etc.)
        title: Optional title to display above the output. If None, tries to find variable name.
    """
    theme = Theme({
        "pretty": "bright_white",
        "type": "bright_yellow",
        "title": "orange_red1",
        "none": "bright_red"
    })
    console = Console(theme=theme)
    
    # Enhanced variable name detection
    if title is None:
        try:
            # Get the calling frame and its local/global variables
            frame = inspect.currentframe().f_back
            calling_vars = {**frame.f_locals, **frame.f_globals}
            
            # Find variable name by identity comparison
            var_name = None
            for name, value in calling_vars.items():
                if value is var:  # Use identity comparison
                    var_name = name
                    break
            
            title = var_name if var_name else type(var).__name__
        except Exception:
            title = type(var).__name__
    
    # Handle special cases
    if var is None:
        pretty_var = Text("None", style="none")
    elif isinstance(var, (str, int, float, bool)):
        pretty_var = Text(repr(var), style="pretty")
    else:
        pretty_var = Pretty(var, expand_all=True)
    
    # Add length information for sequences
    type_name = type(var).__name__
    length_info = ""
    if isinstance(var, (list, tuple, dict, str, set)):
        length_info = f" [length={len(var)}]"
    
    # Construct title with type information
    panel_title = Text()
    panel_title.append(f"{title} ", style="title")
    panel_title.append(f"({type_name}{length_info})", style="type")
    
    # Create panel
    panel = Panel(
        pretty_var,
        title=panel_title,
        border_style="bright_blue",
        style="pretty",
        padding=(1, 2)
    )
    
    console.print(panel)

def print_function_name(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Get the class name if it's a method
        if args and hasattr(args[0], '__class__'):
            class_name = args[0].__class__.__name__
            logger.info(f"{c.EMOJI.FUNCTION} Calling {c.CLR_TERM.CYAN}{class_name}.{func.__name__}{c.CLR_TERM.RESET}")
        else:
            logger.info(f"{c.EMOJI.FUNCTION} Calling {c.CLR_TERM.CYAN}{func.__name__}{c.CLR_TERM.RESET}")
        
        result = func(*args, **kwargs)
        return result
    return wrapper

# For async functions
def print_async_function_name(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Get the class name if it's a method
        if args and hasattr(args[0], '__class__'):
            class_name = args[0].__class__.__name__
            logger.info(f"{c.EMOJI.FUNCTION} Calling async {c.CLR_TERM.CYAN}{class_name}.{func.__name__}{c.CLR_TERM.RESET}")
        else:
            logger.info(f"{c.EMOJI.FUNCTION} Calling async {c.CLR_TERM.CYAN}{func.__name__}{c.CLR_TERM.RESET}")
        
        result = await func(*args, **kwargs)
        return result
    return wrapper

#*------------------------------------------------------------------------------
ErrHandlerLogLevel = Literal[
    "TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"
]

class ErrorStrategy(Enum):
    RAISE = auto()      # Re-raise the exception
    RETURN = auto()     # Return default value
    RETRY = auto()      # Retry the operation
    IGNORE = auto()     # Ignore and continue

@dataclass
class ErrorConfig:
    """Configuration for error handling behavior"""
    exceptions: Union[Type[Exception], Tuple[Type[Exception], ...]] = Exception
    default_value: Any = None
    log_error: bool = True
    log_level: ErrHandlerLogLevel = "ERROR"
    retry_count: int = 0
    retry_delay: float = 0
    strategy: ErrorStrategy = ErrorStrategy.RAISE
    error_callback: Optional[Callable[[Exception], None]] = None
    log_context: dict = field(default_factory=dict)

class ErrorHandler:
    """
    A versatile error handling utility with flexible logging options.
    """
    
    def __init__(self, config: Optional[ErrorConfig] = None):
        self.config = config or ErrorConfig()
        self.logger = logger.bind(**self.config.log_context)
    
    def __call__(self, func: Optional[Callable] = None) -> Union[Callable, Any]:
        """Use as a decorator"""
        if func is None:
            return self
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            ctx = {"function": func.__name__, "args": args, "kwargs": kwargs}
            self.logger = self.logger.bind(**ctx)
            return self.execute(lambda: func(*args, **kwargs))
        return wrapper
    
    def execute(
        self,
        callable_obj: Callable[[], Any],
        error_level: Optional[ErrHandlerLogLevel] = "ERROR",
        warning_level: Optional[ErrHandlerLogLevel] = "WARNING",
        error_msg: Optional[str] = None,
        warning_msg: Optional[str] = None,
        **kwargs
    ) -> Any:
        """
        Execute a callable with error handling and flexible logging options.
        
        Args:
            callable_obj: The function or lambda to execute
            error_level: Log level for errors (overrides config)
            warning_level: Log level for warnings/retries
            error_msg: Custom error message
            warning_msg: Custom warning message for retries
            **kwargs: Additional context for logging
        """
        attempts = self.config.retry_count + 1
        last_error = None
        
        # Update logger context with any additional kwargs
        current_logger = self.logger.bind(**kwargs) if kwargs else self.logger
        
        for attempt in range(attempts):
            try:
                return callable_obj()
            except self.config.exceptions as e:
                last_error = e
                if not self._should_retry(attempt, attempts):
                    return self._handle_error(
                        e,
                        current_logger,
                        level=error_level,
                        custom_msg=error_msg
                    )
                self._handle_retry(
                    attempt,
                    e,
                    current_logger,
                    level=warning_level,
                    custom_msg=warning_msg
                )
        
        return self._handle_error(
            last_error,
            current_logger,
            level=error_level,
            custom_msg=error_msg
        ) if last_error else None

    def _handle_error(
        self,
        error: Exception,
        logger_instance: logger,
        level: Optional[ErrHandlerLogLevel] = None,
        custom_msg: Optional[str] = None
    ) -> Any:
        """Handle caught exceptions with flexible logging"""
        if self.config.log_error:
            self._log_error(
                error,
                logger_instance,
                level or self.config.log_level,
                custom_msg
            )
        
        if self.config.error_callback:
            self.config.error_callback(error)
        
        if self.config.strategy == ErrorStrategy.RAISE:
            raise error
        elif self.config.strategy == ErrorStrategy.RETURN:
            return self.config.default_value
        elif self.config.strategy == ErrorStrategy.IGNORE:
            return None
        
        return self.config.default_value
    
    def _should_retry(self, current_attempt: int, max_attempts: int) -> bool:
        """Determine if another retry attempt should be made"""
        return (self.config.strategy == ErrorStrategy.RETRY and 
                current_attempt < max_attempts - 1)
    
    def _handle_retry(
        self,
        attempt: int,
        error: Exception,
        logger_instance: logger,
        level: Optional[ErrHandlerLogLevel] = None,
        custom_msg: Optional[str] = None
    ) -> None:
        """Handle retry logic with flexible logging"""
        if self.config.log_error:
            msg = custom_msg or f"Attempt {attempt + 1} failed. Error: {str(error)}. Retrying..."
            log_func = getattr(logger_instance, (level or "WARNING").lower())
            log_func(msg)
            
        if self.config.retry_delay:
            time.sleep(self.config.retry_delay)
    
    def _log_error(
        self,
        error: Exception,
        logger_instance: logger,
        level: ErrHandlerLogLevel,
        custom_msg: Optional[str] = None
    ) -> None:
        """Log the error with custom message support"""
        msg = custom_msg or f"Error occurred: {type(error).__name__}: {str(error)}"
        log_func = getattr(logger_instance, level.lower())
        log_func(msg)
        
        # Always log traceback at TRACE level for debugging
        logger_instance.trace(f"Traceback:\n{traceback.format_exc()}")

# Common preset configurations
CFGS_ERROR_HANDLER = {
    'silent': ErrorConfig(
        log_error=True,
        strategy=ErrorStrategy.RETURN
    ),
    'strict': ErrorConfig(
        strategy=ErrorStrategy.RAISE,
        log_error=True,
        log_level="ERROR"
    ),
    'retry': ErrorConfig(
        strategy=ErrorStrategy.RETRY,
        retry_count=3,
        retry_delay=1,
        log_error=True,
        log_level="WARNING"
    ),
    'debug': ErrorConfig(
        strategy=ErrorStrategy.RETURN,
        log_error=True,
        log_level="DEBUG",
        log_context={'environment': 'development'}
    )
}

class LocationAwareErrorHandler(ErrorHandler):
    """
    Enhanced error handler that accurately tracks the original caller location.
    """
    def __init__(self, config: Optional[ErrorConfig] = None):
        super().__init__(config)
        self._last_caller_info = None
        
    def _get_caller_info(self, depth: int = 0) -> dict:
        """
        Get information about the calling function and its location.
        
        Args:
            depth: How many frames to skip to find the real caller
        """
        try:
            # Get the current stack frame
            stack = inspect.stack()
            
            # Find the first frame that's not in our error handling code
            caller_frame = None
            current_file = os.path.abspath(__file__)
            utils_dir = os.path.dirname(current_file)
            
            for frame in stack[1:]:
                frame_file = os.path.abspath(frame.filename)
                # Skip frames from error handler or utility files
                if not (frame_file.startswith(utils_dir) or
                       'error_handler' in frame_file.lower() or
                       frame.function == '<lambda>'):
                    caller_frame = frame
                    break
            
            if not caller_frame:
                return {}
                
            # Convert absolute path to relative path from project root
            abs_filename = os.path.abspath(caller_frame.filename)
            try:
                # Try to make path relative to project root (apps directory)
                apps_index = abs_filename.rindex('apps')
                rel_filename = abs_filename[apps_index:]
            except ValueError:
                # Fallback to full path if apps directory not found
                rel_filename = abs_filename
            
            # Extract location information
            function = caller_frame.function
            lineno = caller_frame.lineno
            
            # Get the source code of the line
            source_line = caller_frame.code_context[0].strip() if caller_frame.code_context else ""
            
            caller_info = {
                "file": rel_filename,
                "function": function,
                "line": lineno,
                "source": source_line
            }
            
            # Store this information for later use
            self._last_caller_info = caller_info
            return caller_info
            
        except Exception as e:
            logger.warning(f"Failed to get caller info: {e}")
            return {}

    def __call__(self, func: Optional[Callable] = None) -> Union[Callable, Any]:
        """Enhanced decorator that captures location information"""
        if func is None:
            return self
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            caller_info = self._get_caller_info()
            ctx = {
                "function": func.__name__,
                "args": args,
                "kwargs": kwargs,
                **caller_info
            }
            self.logger = self.logger.bind(**ctx)
            return self.execute(lambda: func(*args, **kwargs))
        return wrapper

    def execute(
        self,
        callable_obj: Callable[[], Any],
        error_level: Optional[ErrHandlerLogLevel] = "ERROR",
        warning_level: Optional[ErrHandlerLogLevel] = "WARNING",
        error_msg: Optional[str] = None,
        warning_msg: Optional[str] = None,
        **kwargs
    ) -> Any:
        """Enhanced execute method with accurate location tracking"""
        # Get caller information before executing the callable
        caller_info = self._get_caller_info()
        
        # Update kwargs with location information
        execution_context = {**caller_info, **kwargs}
        
        # Update logger context
        current_logger = self.logger.bind(**execution_context)
        
        attempts = self.config.retry_count + 1
        last_error = None
        
        for attempt in range(attempts):
            try:
                result = callable_obj()
                self._last_caller_info = None  # Reset after successful execution
                return result
            except self.config.exceptions as e:
                last_error = e
                if not self._should_retry(attempt, attempts):
                    return self._handle_error(
                        e,
                        current_logger,
                        level=error_level,
                        custom_msg=error_msg
                    )
                self._handle_retry(
                    attempt,
                    e,
                    current_logger,
                    level=warning_level,
                    custom_msg=warning_msg
                )
        
        if last_error:
            result = self._handle_error(
                last_error,
                current_logger,
                level=error_level,
                custom_msg=error_msg
            )
            self._last_caller_info = None  # Reset after handling
            return result
        return None

    def _log_error(
        self,
        error: Exception,
        logger_instance: logger,
        level: ErrHandlerLogLevel,
        custom_msg: Optional[str] = None
    ) -> None:
        """Enhanced error logging with accurate location information"""
        # Use stored caller info if available, otherwise try to get it again
        location_info = self._last_caller_info or self._get_caller_info()
        
        base_msg = custom_msg or f"Error occurred: {type(error).__name__}: {str(error)}"
        
        if location_info:
            # Format the location information
            location_str = f"[{location_info['file']}:{location_info['line']} in {location_info['function']}]"
            msg = f"{location_str} {base_msg}"
        else:
            msg = base_msg
        
        log_func = getattr(logger_instance, level.lower())
        log_func(msg)
        
        # Log source code context and traceback at TRACE level
        if location_info.get('source'):
            logger_instance.trace(f"Source: {location_info['source']}")
        logger_instance.trace(f"Traceback:\n{traceback.format_exc()}")

CFGS_LOCATION_AWARE_ERROR_HANDLER = {
    'silent': ErrorConfig(
        log_error=True,
        strategy=ErrorStrategy.RETURN,
        default_value=None,
        log_context={'handler_type': 'location_aware'}
    ),
    'strict': ErrorConfig(
        strategy=ErrorStrategy.RAISE,
        log_error=True,
        log_level="ERROR",
        log_context={'handler_type': 'location_aware'}
    ),
    'retry': ErrorConfig(
        strategy=ErrorStrategy.RETRY,
        retry_count=3,
        retry_delay=1,
        log_error=True,
        log_level="WARNING",
        log_context={'handler_type': 'location_aware'}
    ),
    'debug': ErrorConfig(
        strategy=ErrorStrategy.RETURN,
        log_error=True,
        log_level="DEBUG",
        log_context={'handler_type': 'location_aware', 'environment': 'development'}
    )
}
#*------------------------------------------------------------------------------

class UUIDUtils:
    @staticmethod
    def generate_uuid4() -> uuid.UUID:
        """Generate a random UUID (version 4)."""
        return uuid.uuid4()
    
    @staticmethod
    def generate_uuid1() -> uuid.UUID:
        """Generate a UUID (version 1) based on host ID and current timestamp."""
        return uuid.uuid1()
    
    @staticmethod
    def generate_namespaced_uuid(
        name: str,
        namespace: Union[uuid.UUID, str] = uuid.NAMESPACE_DNS,
        version: int = 5
    ) -> uuid.UUID:
        """
        Generate a namespaced UUID (version 3 or 5).
        
        Args:
            name: The name to use for generating the UUID
            namespace: The namespace UUID (default: NAMESPACE_DNS)
            version: UUID version to generate (3 or 5, default: 5)
            
        Returns:
            UUID object
        
        Raises:
            ValueError: If version is not 3 or 5
        """
        if version not in (3, 5):
            raise ValueError("Version must be either 3 or 5")
        
        if isinstance(namespace, str):
            namespace = uuid.UUID(namespace)
            
        if version == 3:
            return uuid.uuid3(namespace, name)
        return uuid.uuid5(namespace, name)
    
    @staticmethod
    def is_valid_uuid(uuid_string: str) -> bool:
        """
        Check if a string is a valid UUID.
        
        Args:
            uuid_string: String to validate
            
        Returns:
            bool: True if string is a valid UUID, False otherwise
        """
        try:
            uuid.UUID(str(uuid_string))
            return True
        except (ValueError, AttributeError, TypeError):
            return False
    
    @staticmethod
    def uuid_to_string(uuid_obj: uuid.UUID) -> str:
        """Convert UUID object to string."""
        return str(uuid_obj)
    
    @staticmethod
    def string_to_uuid(uuid_string: str) -> Optional[uuid.UUID]:
        """
        Convert string to UUID object.
        
        Returns:
            UUID object if valid, None if invalid
        """
        try:
            return uuid.UUID(uuid_string)
        except ValueError:
            return None
    
    @staticmethod
    def get_uuid_version(uuid_obj: Union[uuid.UUID, str]) -> Optional[int]:
        """
        Get the version of a UUID.
        
        Args:
            uuid_obj: UUID object or string
            
        Returns:
            int: UUID version if valid, None if invalid
        """
        try:
            if isinstance(uuid_obj, str):
                uuid_obj = uuid.UUID(uuid_obj)
            return uuid_obj.version
        except ValueError:
            return None
    
    @staticmethod
    def generate_timestamp_uuid() -> tuple[uuid.UUID, datetime]:
        """
        Generate a timestamp-based UUID (version 1) and return its timestamp.
        
        Returns:
            tuple: (UUID object, datetime object)
        """
        uuid_obj = uuid.uuid1()
        timestamp = datetime.fromtimestamp(uuid_obj.time / 1e7 - 12219292800)
        return uuid_obj, timestamp

uuid_utils = UUIDUtils()
#*------------------------------------------------------------------------------

def generate_readable_uuid(
    mode: Literal["full", "uuid", "name", "readable"] = "full"
) -> Union[str, Tuple[str, str, str]]:
    """
    Generate a unique readable identifier combining UUID and a fake name.
    
    Args:
        mode: Return mode determining what data to return
              "full" -> (uuid, name, readable_id)
              "uuid" -> just the UUID string
              "name" -> just the generated name
              "readable" -> the combined readable identifier
    
    Returns:
        Single string or tuple of strings based on mode
    
    Raises:
        ValueError: If an invalid mode is provided
    """
    # Create Faker instance
    fake = Faker()
    
    # Generate base values
    unique_id = str(uuid.uuid4())
    random_name = fake.name().replace(' ', '_').lower()
    readable_identifier = f"{random_name}_{unique_id[:8]}"
    
    # Return based on mode
    if mode == "uuid":
        return unique_id
    elif mode == "name":
        return random_name
    elif mode == "readable":
        return readable_identifier
    elif mode == "full":
        return unique_id, random_name, readable_identifier
    else:
        valid_modes = ["full", "uuid", "name", "readable"]
        raise ValueError(f"Invalid mode. Valid modes are: {valid_modes}")


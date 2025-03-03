import packages
import time
from datetime import datetime
import psutil
import threading
import json
import os
import platform
from functools import wraps
from typing import Callable, Any, Dict, List, Optional, Literal, Tuple
from pydantic import BaseModel
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import csv

class PerformanceData:
    def __init__(self):
        self.system_performance = {}
        self.llm_performance = {}
        self.cpu_usage = []
        self.ram_usage = []
        self.timestamps = []
        self.peak_memory = 0

    def to_dict(self):
        return {
            "system_performance": self.system_performance,
            "llm_performance": self.llm_performance,
            "cpu_usage": self.cpu_usage,
            "ram_usage": self.ram_usage,
            "peak_memory": self.peak_memory
        }

class Metadata(BaseModel):
    dataset: Optional[str]
    algorithm: Literal["basic", "advance", "agentic"]
    model: Optional[str]
    inference_server: Literal["API", "Ollama", "vLLM", "llama.cpp"]

class LlmInfo(BaseModel):
    model: Optional[str]
    params: Optional[float]
    size: Optional[int]
    context_window: Optional[int]
    input_tokens: Optional[int]
    memory: Optional[float]
    out_tokens_per_sec: Optional[float]
    source: Optional[str]

def get_system_info() -> Dict[str, Any]:
    return {
        "device_name": platform.node(),
        "os": f"{platform.system()} {platform.release()}",
        "python_version": platform.python_version(),
        "cpu": platform.processor(),
        "cpu_count": psutil.cpu_count(logical=False),
        "cpu_count_logical": psutil.cpu_count(logical=True),
        "total_ram": f"{psutil.virtual_memory().total / (1024 * 1024 * 1024):.2f} GB",
    }

def print_boxed(title: str, content: str):
    lines = content.split('\n')
    width = max(len(line) for line in lines + [title]) + 4
    box_top = '┌' + '─' * (width - 2) + '┐'
    box_bottom = '└' + '─' * (width - 2) + '┘'
    title_line = f'│ {title.center(width - 4)} │'
    
    print(box_top)
    print(title_line)
    print('├' + '─' * (width - 2) + '┤')
    for line in lines:
        print(f'│ {line:<{width - 4}} │')
    print(box_bottom)

def measure_performance(log_cpu: bool = True, log_memory: bool = True, log_time: bool = True, cpu_interval: float = 0.1):
    def decorator(func: Callable[..., Any]):
        @wraps(func)
        def wrapper(*args, perf_data: PerformanceData = None, **kwargs):
            if perf_data is None:
                perf_data = PerformanceData()
            
            process = psutil.Process()
            
            start_cpu_time = process.cpu_times() if log_cpu else None
            start_ram = process.memory_info().rss if log_memory else None
            start_time = time.perf_counter() if log_time else None
            
            peak_ram = start_ram
            
            def monitor_resources():
                nonlocal peak_ram
                while not func_finished:
                    cpu_percent = psutil.cpu_percent(interval=cpu_interval)
                    current_ram = process.memory_info().rss
                    ram_usage = current_ram / (1024 * 1024)  # Convert to MB
                    
                    peak_ram = max(peak_ram, current_ram)
                    
                    perf_data.timestamps.append(time.perf_counter() - start_time)
                    perf_data.cpu_usage.append(cpu_percent)
                    perf_data.ram_usage.append(ram_usage)
                    
                    time.sleep(cpu_interval)
            
            func_finished = False
            monitor_thread = threading.Thread(target=monitor_resources)
            monitor_thread.start()
            
            try:
                result = func(*args, perf_data=perf_data, **kwargs)
            except Exception as e:
                print(f"Error in {func.__name__}: {str(e)}")
                raise
            finally:
                func_finished = True
                monitor_thread.join()
                
                if log_time:
                    end_time = time.perf_counter()
                    execution_time = end_time - start_time
                    perf_data.system_performance["execution_time"] = f"{execution_time:.6f} seconds"
                
                if log_cpu:
                    end_cpu_time = process.cpu_times()
                    cpu_user = end_cpu_time.user - start_cpu_time.user
                    cpu_system = end_cpu_time.system - start_cpu_time.system
                    avg_cpu_percent = sum(perf_data.cpu_usage) / len(perf_data.cpu_usage) if perf_data.cpu_usage else 0
                    peak_cpu_percent = max(perf_data.cpu_usage) if perf_data.cpu_usage else 0
                    perf_data.system_performance["cpu_user"] = f"{cpu_user:.3f} seconds"
                    perf_data.system_performance["cpu_system"] = f"{cpu_system:.3f} seconds"
                    perf_data.system_performance["cpu_percent_avg"] = f"{avg_cpu_percent:.2f}%"
                    perf_data.system_performance["cpu_percent_peak"] = f"{peak_cpu_percent:.2f}%"
                
                if log_memory:
                    end_ram = process.memory_info().rss
                    ram_usage = (end_ram - start_ram) / (1024 * 1024)  # Convert to MB
                    peak_ram_mb = peak_ram / (1024 * 1024)  # Convert to MB
                    perf_data.peak_memory = peak_ram_mb
                    perf_data.system_performance["ram_usage"] = f"{ram_usage:.2f} MB"
                    perf_data.system_performance["ram_peak"] = f"{peak_ram_mb:.2f} MB"
                
                if perf_data.system_performance:
                    print_boxed(f"Performance Metrics for {func.__name__}", json.dumps(perf_data.system_performance, indent=2))
                
                display_performance_chart(perf_data, func.__name__)
            
            return result
        return wrapper
    return decorator

def display_performance_chart(perf_data: PerformanceData, func_name: str):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1,
                        subplot_titles=("CPU Usage (%)", "RAM Usage (MB)"))
    
    fig.add_trace(go.Scatter(x=perf_data.timestamps, y=perf_data.cpu_usage,
                             mode='lines', name='CPU Usage'), row=1, col=1)
    
    fig.add_trace(go.Scatter(x=perf_data.timestamps, y=perf_data.ram_usage,
                             mode='lines', name='RAM Usage'), row=2, col=1)
    
    # Add a horizontal line for peak memory
    fig.add_hline(y=perf_data.peak_memory, line_dash="dash", line_color="red",
                  annotation_text=f"Peak Memory: {perf_data.peak_memory:.2f} MB",
                  annotation_position="top right", row=2, col=1)
    
    fig.update_layout(title_text=f"Performance Metrics for {func_name}",
                      height=600, width=800)
    
    fig.update_xaxes(title_text="Time (seconds)")
    fig.update_yaxes(title_text="CPU Usage (%)", row=1, col=1)
    fig.update_yaxes(title_text="RAM Usage (MB)", row=2, col=1)
    
    # Display the chart in the terminal
    fig.show()

def measure_llm_performance(tokenizer: Callable[[str], List[str]] = str.split):
    def decorator(func: Callable[..., Any]):
        @wraps(func)
        def wrapper(*args, perf_data: PerformanceData = None, **kwargs):
            if perf_data is None:
                perf_data = PerformanceData()
            
            start_time = time.perf_counter()
            
            input_tokens = sum(len(tokenizer(str(arg))) for arg in args)
            input_tokens += sum(len(tokenizer(str(v))) for v in kwargs.values())
            
            try:
                result = func(*args, perf_data=perf_data, **kwargs)
            except Exception as e:
                print(f"Error in {func.__name__}: {str(e)}")
                raise
            
            end_time = time.perf_counter()
            
            # Unpack the result if it's a tuple containing the response and timing information
            if isinstance(result, tuple) and len(result) == 3:
                response, first_token_time, total_time = result
            else:
                response = result
                first_token_time = None
                total_time = end_time - start_time

            if isinstance(response, str):
                output_tokens = len(tokenizer(response))
            elif isinstance(response, list):
                output_tokens = sum(len(tokenizer(str(item))) for item in response)
            else:
                output_tokens = len(tokenizer(str(response)))
            
            total_tokens = input_tokens + output_tokens
            tokens_per_second = total_tokens / total_time if total_time > 0 else 0
            
            perf_data.llm_performance = {
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": total_tokens,
                "execution_time": total_time,
                "tokens_per_second": tokens_per_second,
                "first_token_time": first_token_time
            }
            
            print_boxed(f"LLM Metrics for {func.__name__}", json.dumps(perf_data.llm_performance, indent=2))
            
            return result
        return wrapper
    return decorator

def log_to_json(file_path: str):
    def decorator(func: Callable[..., Any]):
        @wraps(func)
        def wrapper(*args, metadata: Optional[Metadata] = None, **kwargs):
            perf_data = PerformanceData()
            result = func(*args, perf_data=perf_data, **kwargs)
            
            timestamp = time.time()
            formatted_time = datetime.fromtimestamp(timestamp).isoformat()
            
            log_entry = {
                "timestamp": formatted_time,
                "function_name": func.__name__,
                "system_info": get_system_info(),
                "performance_data": perf_data.to_dict()
            }
            
            if metadata:
                log_entry["metadata"] = metadata.model_dump()
            
            abs_file_path = os.path.abspath(file_path)
            os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
            
            try:
                if os.path.exists(abs_file_path):
                    with open(abs_file_path, 'r+') as f:
                        try:
                            data = json.load(f)
                            if not isinstance(data, list):
                                data = []
                        except json.JSONDecodeError:
                            data = []
                        
                        data.append(log_entry)
                        f.seek(0)
                        f.truncate()
                        json.dump(data, f, indent=2)
                else:
                    with open(abs_file_path, 'w') as f:
                        json.dump([log_entry], f, indent=2)
                
                print(f"Performance data logged to: {abs_file_path}")
            except Exception as e:
                print(f"Error writing to log file: {str(e)}")
            
            return result
        return wrapper
    return decorator

#*-- TO CSV
def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '_') -> Dict[str, Any]:
    items: List[tuple] = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def json_to_csv(json_file_path: str, csv_file_path: str):
    """
    Example usage
    json_to_csv('performance_logs.json', 'performance_logs.csv')
    """
    try:
        # Read JSON file
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

        # Ensure data is a list of dictionaries
        if not isinstance(data, list):
            data = [data]

        # Flatten nested dictionaries
        flattened_data = [flatten_dict(entry) for entry in data]

        # Get all unique keys as CSV headers
        fieldnames = set()
        for entry in flattened_data:
            fieldnames.update(entry.keys())

        # Sort fieldnames to ensure consistent column order
        fieldnames = sorted(fieldnames)

        # Write to CSV
        with open(csv_file_path, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for entry in flattened_data:
                writer.writerow(entry)

        print(f"Successfully converted {json_file_path} to {csv_file_path}")

    except json.JSONDecodeError:
        print(f"Error: {json_file_path} is not a valid JSON file.")
    except IOError as e:
        print(f"IO Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage
@log_to_json(f"{packages.APP_PATH}/data/logs/performance_logs.json")
@measure_llm_performance()
@measure_performance(cpu_interval=0.5)
def execute_query(query_engine: callable, run_query_engine: callable, query: str, perf_data: PerformanceData = None) -> Any:
    """
    Example usage
    
    ```python
    metadatjja = Metadata(
			dataset="simple",
			algorithm="basic",
			model="Llama 3.1 8b",
			inference_server="Ollama",
		)

    execute_query(query_engine, "What did the author do growing up?", metadata=metadata)
    """
    response, first_token_time, total_time = run_query_engine(query, query_engine, print_in_streaming=False)
    return response, first_token_time, total_time
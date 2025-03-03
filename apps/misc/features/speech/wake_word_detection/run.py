import subprocess
import sys
import time
from pathlib import Path

def check_redis():
    """Check if Redis is running."""
    try:
        import redis
        client = redis.Redis(host='localhost', port=6379)
        client.ping()
        return True
    except:
        return False

def main():
    # Check Redis
    if not check_redis():
        print("Please start Redis server first!")
        sys.exit(1)
    
    base_dir = Path(__file__).parent
    
    try:
        # Start Background Service
        background_process = subprocess.Popen(
            [sys.executable, str(base_dir / "background_service.py")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("Started background service...")
        time.sleep(2)  # Wait for background service to initialize
        
        # Start FastAPI Server
        fastapi_process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "fastapi_server:create_app", "--factory", "--port", "5000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("Started FastAPI server...")
        time.sleep(2)  # Wait for FastAPI server to initialize
        
        # Start Streamlit
        streamlit_process = subprocess.Popen(
            ["streamlit", "run", str(base_dir / "streamlit_app.py")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("Started Streamlit app...")
        
        # Wait for interrupt
        streamlit_process.wait()
        
    except KeyboardInterrupt:
        print("\nShutting down services...")
        background_process.terminate()
        fastapi_process.terminate()
        streamlit_process.terminate()
        
    except Exception as e:
        print(f"Error starting services: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
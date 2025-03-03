from dataclasses import dataclass
from pathlib import Path
import logging

@dataclass
class AudioConfig:
    CHUNK_SIZE: int = 1280
    SAMPLE_RATE: int = 16000
    CHANNELS: int = 1
    FORMAT: int = 16  # pyaudio.paInt16

@dataclass
class ModelConfig:
    WAKE_WORD: str = "alexa"
    CONFIDENCE_THRESHOLD: float = 0.5
    INFERENCE_FRAMEWORK: str = "onnx"

@dataclass
class RedisConfig:
    HOST: str = "localhost"
    PORT: int = 6379
    DB: int = 0
    CHANNEL: str = "wake_word"
    RETRY_ATTEMPTS: int = 3
    RETRY_DELAY: int = 1  # seconds

@dataclass
class ServerConfig:
    HOST: str = "0.0.0.0"
    STREAMLIT_PORT: int = 8501
    FASTAPI_PORT: int = 5000
    UPDATE_INTERVAL: float = 0.5  # seconds

@dataclass
class AppConfig:
    BASE_DIR: Path = Path(__file__).parent
    LOG_DIR: Path = BASE_DIR / "logs"
    LOG_LEVEL: int = logging.INFO
    LOG_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    def setup_logging(self, logger_name: str) -> logging.Logger:
        """Configure and return a logger instance."""
        self.LOG_DIR.mkdir(exist_ok=True)
        
        logger = logging.getLogger(logger_name)
        logger.setLevel(self.LOG_LEVEL)
        
        # File handler
        file_handler = logging.FileHandler(
            self.LOG_DIR / f"{logger_name.lower()}.log"
        )
        file_handler.setFormatter(logging.Formatter(self.LOG_FORMAT))
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(self.LOG_FORMAT))
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger

# Create global config instances
audio_config = AudioConfig()
model_config = ModelConfig()
redis_config = RedisConfig()
server_config = ServerConfig()
app_config = AppConfig()
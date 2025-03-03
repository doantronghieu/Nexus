from typing import Optional
import redis
import queue
import time
from redis.exceptions import ConnectionError, RedisError
from wake_word_detector import WakeWordDetector, AudioStreamError, ModelError
from config import redis_config, app_config

class RedisConnection:
    """Redis connection manager with retry logic."""
    def __init__(self):
        self.logger = app_config.setup_logging('RedisConnection')
        self.client: Optional[redis.Redis] = None
        
    def connect(self) -> bool:
        """Establish Redis connection with retry logic."""
        retry_count = 0
        while retry_count < redis_config.RETRY_ATTEMPTS:
            try:
                self.client = redis.Redis(
                    host=redis_config.HOST,
                    port=redis_config.PORT,
                    db=redis_config.DB
                )
                self.client.ping()
                self.logger.info("Successfully connected to Redis")
                return True
            except ConnectionError:
                retry_count += 1
                self.logger.warning(
                    f"Redis connection failed, retrying... "
                    f"({retry_count}/{redis_config.RETRY_ATTEMPTS})"
                )
                time.sleep(redis_config.RETRY_DELAY)
        
        self.logger.error("Failed to connect to Redis after all attempts")
        return False
        
    def publish(self, message: str) -> bool:
        """Publish message to Redis with error handling."""
        try:
            if self.client:
                self.client.publish(redis_config.CHANNEL, message)
                return True
        except RedisError as e:
            self.logger.error(f"Error publishing to Redis: {e}")
        return False
        
    def close(self) -> None:
        """Close Redis connection."""
        if self.client:
            try:
                self.client.close()
                self.logger.info("Redis connection closed")
            except Exception as e:
                self.logger.error(f"Error closing Redis connection: {e}")

class BackgroundService:
    """Main service coordinator."""
    def __init__(self):
        self.logger = app_config.setup_logging('BackgroundService')
        self.redis = RedisConnection()
        self.callback_queue = queue.Queue()
        self.detector: Optional[WakeWordDetector] = None
        self.running = False
        
    def handle_detector_error(self, error: Exception) -> None:
        """Handle errors from the wake word detector."""
        if isinstance(error, AudioStreamError):
            self.logger.error(f"Audio stream error: {error}")
        elif isinstance(error, ModelError):
            self.logger.error(f"Model error: {error}")
        else:
            self.logger.error(f"Unexpected error: {error}")
        self.stop()
        
    def process_detection_events(self) -> None:
        """Process events from the detection queue."""
        try:
            event, data = self.callback_queue.get_nowait()
            if event == "wake_word_detected":
                self.logger.info(f"Wake word detected: {data}")
                self.redis.publish('wake_up')
        except queue.Empty:
            time.sleep(0.1)
        except Exception as e:
            self.logger.error(f"Error processing detection event: {e}")
            
    def start(self) -> None:
        """Start the background service."""
        self.logger.info("Starting background service...")
        
        if not self.redis.connect():
            self.logger.error("Failed to start: Redis connection failed")
            return
            
        try:
            self.detector = WakeWordDetector(
                callback_queue=self.callback_queue,
                on_error=self.handle_detector_error
            )
            self.detector.start()
            self.running = True
            
            while self.running:
                self.process_detection_events()
                
        except KeyboardInterrupt:
            self.logger.info("Received shutdown signal")
        except Exception as e:
            self.logger.error(f"Unexpected error in background service: {e}")
        finally:
            self.stop()
            
    def stop(self) -> None:
        """Stop the background service."""
        self.logger.info("Stopping background service...")
        self.running = False
        
        if self.detector:
            self.detector.stop()
            
        self.redis.close()
        self.logger.info("Background service stopped")

if __name__ == "__main__":
    service = BackgroundService()
    service.start()
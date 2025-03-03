import redis
from dataclasses import dataclass
from typing import Optional

@dataclass
class RedisConfig:
    host: str = 'localhost'
    port: int = 6379
    db: int = 0
    password: Optional[str] = None
    socket_timeout: int = 5
    max_connections: int = 10
    retry_on_timeout: bool = True
    health_check_interval: int = 30
    max_retries: int = 3
    retry_delay: int = 1
    encoding: str = 'utf-8'

class RedisToolkit:
    def __init__(self, config: Optional[RedisConfig] = None):
        """Initialize Redis toolkit with configuration."""
        self.config = config or RedisConfig()
        
        # Initialize connection pool
        self.connection_pool = redis.ConnectionPool(
            host=self.config.host,
            port=self.config.port,
            db=self.config.db,
            password=self.config.password,
            decode_responses=True,
            socket_timeout=self.config.socket_timeout,
            max_connections=self.config.max_connections,
            retry_on_timeout=self.config.retry_on_timeout,
            encoding=self.config.encoding
        )
        
        # Initialize main Redis client
        self.redis_client = redis.Redis(
            connection_pool=self.connection_pool
        )
        
        # Initialize binary client for pickle operations
        self.binary_client = redis.Redis(
            host=self.config.host,
            port=self.config.port,
            db=self.config.db,
            password=self.config.password,
            decode_responses=False,
            socket_timeout=self.config.socket_timeout
        )

    def test_connection(self) -> bool:
      """Test Redis connection."""
      try:
          return self.redis_client.ping()
      except Exception as e:
          print(f"Connection error: {str(e)}")
          return False

# Example usage:
if __name__ == "__main__":
    config = RedisConfig(
        host='localhost',
        port=6379,
        password='mypassword',
        socket_timeout=5,
        max_connections=10
    )
    
    redis_toolkit = RedisToolkit(config)
    
    # Print the connection test result
    connection_status = redis_toolkit.test_connection()
    print(f"Redis connection status: {connection_status}")
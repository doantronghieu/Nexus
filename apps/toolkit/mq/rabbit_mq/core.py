# core.py
import pika
from loguru import logger
from pika import PlainCredentials

class Consts:
    EXCHANGE = ""
    
class Client:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 5672,
        username: str = "user",
        password: str = "password",
    ):
        # Log initialization parameters (excluding password for security)
        logger.info("Initializing RabbitMQ client - Host: {}:{} | User: {}", host, port, username)
        
        self.credentials = PlainCredentials(username, password)
        self.parameters = pika.ConnectionParameters(
            host=host,
            port=port,
            credentials=self.credentials,
        )
        
        try:
            # Establish connection
            logger.debug("Attempting to connect to RabbitMQ server...")
            self.connection = pika.BlockingConnection(self.parameters)
            logger.info("Connected to RabbitMQ server successfully")
            
            # Create channel
            self.channel = self.connection.channel()
            logger.debug("AMQP channel created")
            
        except Exception as e:
            logger.error("Connection failed: {}", e)
            raise
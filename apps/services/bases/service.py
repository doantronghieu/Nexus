from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from datetime import datetime
import uuid
from loguru import logger

class BaseService(ABC):
    """
    Abstract base class for service components in a microservices architecture.
    Implements template method pattern and provides common service lifecycle management.
    
    Attributes:
        service_id (str): Unique identifier for the service instance
        name (str): Name of the service
        created_at (datetime): Service instance creation timestamp
        config (Dict[str, Any]): Service configuration parameters
        _is_initialized (bool): Internal flag to track initialization state
    """
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the service with basic attributes.
        
        Args:
            name: Service name identifier
            config: Optional configuration dictionary
        """
        self.service_id = str(uuid.uuid4())
        self.name = name
        self.created_at = datetime.utcnow()
        self.config = config or {}
        self._is_initialized = False

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """
        Make the service callable. Ensures initialization before execution.
        Template method pattern implementation.
        
        Returns:
            Result of service execution
        
        Raises:
            RuntimeError: If service is not properly initialized
        """
        if not self._is_initialized:
            raise RuntimeError(f"Service {self.name} must be initialized before calling")
        
        try:
            self._pre_execute(*args, **kwargs)
            result = self._execute(*args, **kwargs)
            self._post_execute(result)
            return result
        except Exception as e:
            self._handle_error(e)
            raise

    def initialize(self) -> None:
        """
        Initialize the service. Template method pattern implementation.
        """
        try:
            self._validate_config()
            self._setup_resources()
            self._initialize_impl()
            self._is_initialized = True
            logger.debug(f"Service {self.name} initialized")
        except Exception as e:
            logger.error(f"Failed to initialize service {self.name}: {str(e)}")
            self._cleanup_resources()
            raise

    def shutdown(self) -> None:
        """
        Cleanup and shutdown the service properly.
        """
        try:
            logger.info(f"Shutting down service: {self.name}")
            self._cleanup_resources()
            self._shutdown_impl()
            self._is_initialized = False
            logger.debug(f"Service {self.name} shut down successfully")
        except Exception as e:
            logger.error(f"Error during shutdown of service {self.name}: {str(e)}")
            raise

    def _execute(self, *args: Any, **kwargs: Any) -> Any:
        """
        Core service execution logic. Must be implemented by concrete services.
        """
        pass

    def _validate_config(self) -> None:
        """
        Validate service configuration. Must be implemented by concrete services.
        
        Raises:
            ValueError: If configuration is invalid
        """
        pass

    def _initialize_impl(self) -> None:
        """
        Implementation-specific initialization logic.
        Can be overridden by concrete services.
        """
        pass

    def _shutdown_impl(self) -> None:
        """
        Implementation-specific shutdown logic.
        Can be overridden by concrete services.
        """
        pass

    def _setup_resources(self) -> None:
        """
        Setup service resources (e.g., database connections, cache, etc.).
        Can be overridden by concrete services.
        """
        pass

    def _cleanup_resources(self) -> None:
        """
        Cleanup service resources.
        Can be overridden by concrete services.
        """
        pass

    def _pre_execute(self, *args: Any, **kwargs: Any) -> None:
        """
        Pre-execution hook. Can be overridden by concrete services.
        """
        pass

    def _post_execute(self, result: Any) -> None:
        """
        Post-execution hook. Can be overridden by concrete services.
        """
        pass

    def _handle_error(self, error: Exception) -> None:
        """
        Handle execution errors. Can be overridden by concrete services.
        
        Args:
            error: The exception that occurred during execution
        """
        logger.error(f"Error in service {self.name}: {str(error)}")

    @property
    def is_initialized(self) -> bool:
        """
        Check if the service is initialized.
        
        Returns:
            bool: True if service is initialized, False otherwise
        """
        return self._is_initialized
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class RAGBase(ABC):
    """Abstract base class for Retrieval-Augmented Generation implementations.
    
    This class defines the interface that all RAG implementations must follow.
    Child classes should implement the abstract methods according to their specific
    retrieval and generation strategies.
    """
    
    def __init__(
        self, 
        knowledge_base: Optional[Any] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> None:
        """Initialize the RAG system.
        
        Args:
            knowledge_base: Optional knowledge base for retrieval.
                          Child classes should document their specific knowledge base requirements.
            config: Optional configuration dictionary for the RAG implementation.
                   Child classes should document their specific configuration requirements.
        """
        self.knowledge_base = knowledge_base
        self.config = config or {}
        self._validate_params()
        self._initialize_components()
    
    @abstractmethod
    def _validate_params(self) -> None:
        """Validate the configuration parameters.
        
        Raises:
            ValueError: If the configuration is invalid.
        """
        pass

    @abstractmethod
    def _initialize_components(self) -> None:
        """Initialize the necessary components for the RAG system.
        
        This method should set up any required retrievers, generators, or other
        components needed for the RAG implementation.
        
        Raises:
            RuntimeError: If component initialization fails.
        """
        pass
    
    @abstractmethod
    def __call__(self, query: str) -> str:
        """Process a query through the RAG system.
        
        Args:
            query: The user's input query string.
            
        Returns:
            str: The generated response based on the retrieved context.
            
        Raises:
            ValueError: If the query is invalid.
            RuntimeError: If processing fails.
        """
        pass
    
    def __repr__(self) -> str:
        """Return a string representation of the RAG implementation."""
        return f"{self.__class__.__name__}(knowledge_base={self.knowledge_base}, config={self.config})"
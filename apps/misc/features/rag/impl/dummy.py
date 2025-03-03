import packages
import random
from typing import Any, Dict, Optional
from features.rag.base import RAGBase

class DummyRAG(RAGBase):
    """A dummy implementation of RAG that returns random responses.
    
    This implementation is for demonstration purposes and simply returns
    random predefined responses regardless of the input query.
    """
    
    def __init__(
        self,
        knowledge_base: Optional[Any] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> None:
        # Some dummy responses to choose from
        self.dummy_responses = [
            "This is a random response from the knowledge base.",
            "Here's another possible answer I found.",
            "Based on the retrieved context, here's what I know.",
            "According to the knowledge base, this might help.",
        ]
        super().__init__(knowledge_base, config)
    
    def _validate_params(self) -> None:
        """Validate configuration and knowledge base.
        
        For this dummy implementation, we accept any input.
        """
        # Example validation - require max_length in config if provided
        if self.config and 'max_length' in self.config:
            if not isinstance(self.config['max_length'], int):
                raise ValueError("max_length must be an integer")
    
    def _initialize_components(self) -> None:
        """Initialize dummy components.
        
        For this implementation, we just set a random seed if provided.
        """
        if self.config.get('random_seed'):
            random.seed(self.config['random_seed'])
    
    def __call__(self, query: str) -> str:
        """Return a random response from the dummy knowledge base.
        
        Args:
            query: The input query (ignored in this implementation).
            
        Returns:
            str: A randomly selected response.
        """
        if not query.strip():
            raise ValueError("Query cannot be empty")
            
        response = random.choice(self.dummy_responses)
        
        # Apply max length constraint if configured
        max_length = self.config.get('max_length')
        if max_length:
            response = response[:max_length]
            
        return response

def main():
    # Basic usage
    rag = DummyRAG()
    response = rag("What is the meaning of life?")
    print(response)

    # With configuration
    config = {
        'max_length': 50,
        'random_seed': 42
    }
    rag_with_config = DummyRAG(config=config)
    response = rag_with_config("Tell me something interesting")
    print(response)
    
  if __name__ == "main":
    main()

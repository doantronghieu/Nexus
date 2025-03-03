from typing import Dict, Any, Optional, Literal
from pydantic import BaseModel, Field

import packages
from services.bases.service import BaseService

class AIModelConfig(BaseModel):
    """
    General configuration model for AI services
    """
    class Config:
        extra = 'allow'  # Allow extra fields for child classes

    name: Optional[str] = Field(None, description="Name of the model")
    version: Optional[str] = Field(None, description="Model version")
    type: Optional[Literal["text", "image", "audio", "multimodal"]] = Field(None, description="Type of the model")
    framework: Optional[Literal["pytorch", "tensorflow", "onnx", "other"]] = Field(None, description="Framework used for the model")
    device: Optional[Literal["cpu", "cuda", "mps"]] = Field(None, description="Device to run the model on")
    precision: Literal["float32", "float16", "bfloat16"] = Field(None, description="Precision for model inference")
    batch_size: Optional[int] = Field(1, ge=1, description="Batch size for inference")
    max_memory: Optional[int] = Field(None, ge=1, description="Maximum memory usage in MB")

class AIService(BaseService):
    """Base class for AI services providing common AI functionality"""
    
    def __init__(
        self,
        name: str,
        config: Optional[Dict[str, Any]] = None,
        model_config: Optional[AIModelConfig] = None
    ) -> None:
        """
        Initialize AI service
        
        Args:
            name: Service name
            config: Service configuration
            model_config: AI model specific configuration
        """
        super().__init__(name, config)
        
        # Initialize model configuration
        self.model_config = model_config or self.get_default_model_config()
        
        # Common AI service attributes
        self.model = None
        
    def get_default_model_config(self) -> AIModelConfig:
        """Get default model configuration"""
        raise NotImplementedError("Subclasses must implement get_default_model_config()")
        
    def load_model(self) -> None:
        """Load AI model and related components"""
        raise NotImplementedError("Subclasses must implement load_model()")
        
    def preprocess_input(self, input_data: Any) -> Any:
        """Preprocess input data for the model"""
        raise NotImplementedError("Subclasses must implement preprocess_input()")
        
    def postprocess_output(self, model_output: Any) -> Any:
        """Postprocess model output for the client"""
        raise NotImplementedError("Subclasses must implement postprocess_output()")
        
    def predict(self, input_data: Any) -> Any:
        """Make prediction using the loaded model"""
        raise NotImplementedError("Subclasses must implement predict()")
        
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model"""
        if not hasattr(self, 'model_config'):
            return {
                "model_name": None,
                "model_version": None,
                "model_type": None,
                "loaded": False
            }
            
        return {
            "model_name": getattr(self.model_config, 'name', None),
            "model_version": getattr(self.model_config, 'version', None),
            "model_type": getattr(self.model_config, 'type', None),
            "loaded": self.model is not None
        }
        
    def get_service_info(self) -> Dict[str, Any]:
        """Get comprehensive service information
        
        Returns:
            Dict containing service status and configuration
        """
        return {
            "name": self.name,
            "initialized": self.is_initialized,
            "model_info": self.get_model_info(),
            "config": {
                k: v for k, v in self.model_config.dict().items()
                if not k.startswith('_')
            }
        }
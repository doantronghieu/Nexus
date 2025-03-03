"""
Configuration settings for the Weather Service.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Service configuration settings."""
    
    # Service Configuration
    SERVICE_NAME: str = "weather-service"
    DEBUG: bool = False
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # API Base URLs
    WEATHER_API_URL: str = "https://api.open-meteo.com/v1"
    HISTORICAL_API_URL: str = "https://archive-api.open-meteo.com/v1"
    MARINE_API_URL: str = "https://marine-api.open-meteo.com/v1"
    AIR_QUALITY_API_URL: str = "https://air-quality-api.open-meteo.com/v1"
    GEOCODING_API_URL: str = "https://geocoding-api.open-meteo.com/v1"
    FLOOD_API_URL: str = "https://flood-api.open-meteo.com/v1"
    ENSEMBLE_API_URL: str = "https://ensemble-api.open-meteo.com/v1"
    CLIMATE_API_URL: str = "https://climate-api.open-meteo.com/v1"
    
    # API Settings
    REQUEST_TIMEOUT: int = 30
    MAX_RETRIES: int = 3
    RETRY_DELAY: int = 1
    
    # Optional API Key for commercial usage
    API_KEY: Optional[str] = None
    
    class Config:
        """Pydantic configuration."""
        case_sensitive = True
        env_prefix = "WEATHER_"


# Create global settings instance
settings = Settings()
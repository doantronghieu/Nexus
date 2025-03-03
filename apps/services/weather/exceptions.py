"""
Custom exceptions for the Weather Service.
"""
from typing import Optional, Any, Dict


class WeatherServiceError(Exception):
    """Base exception for Weather Service errors."""
    
    def __init__(self, message: str, detail: Optional[Dict[str, Any]] = None):
        self.message = message
        self.detail = detail
        super().__init__(self.message)


class APIError(WeatherServiceError):
    """Raised when an API request fails."""
    
    def __init__(self, message: str, status_code: int, detail: Optional[Dict[str, Any]] = None):
        self.status_code = status_code
        super().__init__(message, detail)


class ValidationError(WeatherServiceError):
    """Raised when input validation fails."""
    pass


class ConfigurationError(WeatherServiceError):
    """Raised when there's a configuration error."""
    pass


class ServiceUnavailableError(WeatherServiceError):
    """Raised when a required service is unavailable."""
    pass
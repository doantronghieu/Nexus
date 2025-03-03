"""
Climate data service implementation.
"""
from typing import Dict, Any, Optional, List
from ..base import BaseWeatherService
from ..config import settings
from ..models import WeatherRequest, WeatherResponse
from ..utils import clean_none_values


class ClimateService(BaseWeatherService):
    """Service for fetching climate data."""
    
    def __init__(self):
        """Initialize the climate service."""
        super().__init__(settings.CLIMATE_API_URL)
    
    async def get_climate_data(
        self,
        request: WeatherRequest,
        models: Optional[List[str]] = None,
        disable_bias_correction: bool = False
    ) -> WeatherResponse:
        """
        Get climate data.
        
        Args:
            request: Weather request parameters
            models: List of climate models to include
            disable_bias_correction: Whether to disable statistical downscaling and bias correction
            
        Returns:
            WeatherResponse: Climate data
        """
        # Verify time range is provided
        if not request.time_range or not (request.time_range.start_date and request.time_range.end_date):
            raise ValueError("Start date and end date are required for climate data")
        
        # Prepare query parameters
        params = {
            'latitude': request.coordinates.latitude,
            'longitude': request.coordinates.longitude,
            'start_date': request.time_range.start_date.date().isoformat(),
            'end_date': request.time_range.end_date.date().isoformat(),
            'timezone': request.timezone,
            'temperature_unit': request.temperature_unit,
            'wind_speed_unit': request.wind_speed_unit,
            'precipitation_unit': request.precipitation_unit,
        }
        
        # Add daily parameters if specified
        if request.daily:
            params['daily'] = ','.join(request.daily)
            
        # Add specific models if requested
        if models:
            params['models'] = ','.join(models)
            
        # Add bias correction parameter
        if disable_bias_correction:
            params['disable_bias_correction'] = 'true'
        
        # Remove None values
        params = clean_none_values(params)
        
        # Make API request
        response_data = await self.get('climate', params=params)
        
        # Convert response to WeatherResponse model
        return WeatherResponse(**response_data)
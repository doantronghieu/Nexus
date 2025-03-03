"""
Marine weather service implementation.
"""
from typing import Dict, Any, Optional
from ..base import BaseWeatherService
from ..config import settings
from ..models import WeatherRequest, WeatherResponse
from ..utils import clean_none_values


class MarineWeatherService(BaseWeatherService):
    """Service for fetching marine weather data."""
    
    def __init__(self):
        """Initialize the marine weather service."""
        super().__init__(settings.MARINE_API_URL)
    
    async def get_marine_weather(self, request: WeatherRequest) -> WeatherResponse:
        """
        Get marine weather data.
        
        Args:
            request: Weather request parameters
        
        Returns:
            WeatherResponse: Marine weather data
        """
        # Prepare query parameters
        params = {
            'latitude': request.coordinates.latitude,
            'longitude': request.coordinates.longitude,
            'timezone': request.timezone,
        }
        
        # Add time range parameters if specified
        if request.time_range:
            if request.time_range.forecast_days is not None:
                params['forecast_days'] = request.time_range.forecast_days
            if request.time_range.past_days is not None:
                params['past_days'] = request.time_range.past_days
            if request.time_range.start_date:
                params['start_date'] = request.time_range.start_date.date().isoformat()
            if request.time_range.end_date:
                params['end_date'] = request.time_range.end_date.date().isoformat()
        
        # Add hourly/daily parameters if specified
        if request.hourly:
            params['hourly'] = ','.join(request.hourly)
        if request.daily:
            params['daily'] = ','.join(request.daily)
        
        # Remove None values
        params = clean_none_values(params)
        
        # Make API request
        response_data = await self.get('marine', params=params)
        
        # Convert response to WeatherResponse model
        return WeatherResponse(**response_data)
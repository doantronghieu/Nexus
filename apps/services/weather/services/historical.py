"""
Historical weather service implementation.
"""
from typing import Dict, Any, Optional
from ..base import BaseWeatherService
from ..config import settings
from ..models import WeatherRequest, WeatherResponse
from ..utils import clean_none_values


class HistoricalWeatherService(BaseWeatherService):
    """Service for fetching historical weather data."""
    
    def __init__(self):
        """Initialize the historical weather service."""
        super().__init__(settings.HISTORICAL_API_URL)
    
    async def get_historical_weather(self, request: WeatherRequest) -> WeatherResponse:
        """
        Get historical weather data.
        
        Args:
            request: Weather request parameters
        
        Returns:
            WeatherResponse: Historical weather data
        """
        if not request.time_range or not (request.time_range.start_date and request.time_range.end_date):
            raise ValueError("Start date and end date are required for historical data")
        
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
        
        # Add hourly/daily parameters if specified
        if request.hourly:
            params['hourly'] = ','.join(request.hourly)
        if request.daily:
            params['daily'] = ','.join(request.daily)
        
        # Remove None values
        params = clean_none_values(params)
        
        # Make API request
        response_data = await self.get('archive', params=params)
        
        # Convert response to WeatherResponse model
        return WeatherResponse(**response_data)
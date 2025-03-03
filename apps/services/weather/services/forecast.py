"""
Weather forecast service implementation.
"""
from typing import Dict, Any, Optional, List
from ..base import BaseWeatherService
from ..config import settings
from ..models import WeatherRequest, WeatherResponse
from ..utils import clean_none_values


class WeatherForecastService(BaseWeatherService):
    """Service for fetching weather forecasts."""
    
    def __init__(self):
        """Initialize the forecast service."""
        super().__init__(settings.WEATHER_API_URL)
    
    async def get_forecast(self, request: WeatherRequest) -> WeatherResponse:
        """
        Get weather forecast data.
        
        Args:
            request: Weather request parameters
        
        Returns:
            WeatherResponse: Weather forecast data
        """
        # Prepare query parameters
        params = {
            'latitude': request.coordinates.latitude,
            'longitude': request.coordinates.longitude,
            'timezone': request.timezone,
            'temperature_unit': request.temperature_unit,
            'wind_speed_unit': request.wind_speed_unit,
            'precipitation_unit': request.precipitation_unit,
        }
        
        # Add optional parameters
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
        response_data = await self.get('forecast', params=params)
        
        # Convert response to WeatherResponse model
        return WeatherResponse(**response_data)
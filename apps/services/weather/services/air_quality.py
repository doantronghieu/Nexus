"""
Air quality service implementation.
"""
from typing import Dict, Any, Optional
from ..base import BaseWeatherService
from ..config import settings
from ..models import WeatherRequest, WeatherResponse
from ..utils import clean_none_values


class AirQualityService(BaseWeatherService):
    """Service for fetching air quality data."""
    
    def __init__(self):
        """Initialize the air quality service."""
        super().__init__(settings.AIR_QUALITY_API_URL)
    
    async def get_air_quality(self, request: WeatherRequest) -> WeatherResponse:
        """
        Get air quality data.
        
        Args:
            request: Weather request parameters
        
        Returns:
            WeatherResponse: Air quality data
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
            
        # Add domains parameter if available
        params['domains'] = 'auto'
        
        # Remove None values
        params = clean_none_values(params)
        
        # Make API request
        response_data = await self.get('air-quality', params=params)
        
        # Convert response to WeatherResponse model
        return WeatherResponse(**response_data)
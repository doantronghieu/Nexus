"""
Flood data service implementation.
"""
from typing import Dict, Any, Optional
from ..base import BaseWeatherService
from ..config import settings
from ..models import WeatherRequest, WeatherResponse
from ..utils import clean_none_values


class FloodService(BaseWeatherService):
    """Service for fetching flood data."""
    
    def __init__(self):
        """Initialize the flood service."""
        super().__init__(settings.FLOOD_API_URL)
    
    async def get_flood_data(
        self,
        request: WeatherRequest,
        ensemble: bool = False
    ) -> WeatherResponse:
        """
        Get flood forecast data.
        
        Args:
            request: Weather request parameters
            ensemble: Whether to return ensemble forecast data
            
        Returns:
            WeatherResponse: Flood forecast data
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
                params['forecast_days'] = min(request.time_range.forecast_days, 210)  # Max 210 days
            if request.time_range.past_days is not None:
                params['past_days'] = request.time_range.past_days
            if request.time_range.start_date:
                params['start_date'] = request.time_range.start_date.date().isoformat()
            if request.time_range.end_date:
                params['end_date'] = request.time_range.end_date.date().isoformat()
        
        # Add hourly/daily parameters if specified
        if request.daily:
            params['daily'] = ','.join(request.daily)
            
        # Add ensemble parameter if requested
        if ensemble:
            params['ensemble'] = 'true'
        
        # Remove None values
        params = clean_none_values(params)
        
        # Make API request
        response_data = await self.get('flood', params=params)
        
        # Convert response to WeatherResponse model
        return WeatherResponse(**response_data)
"""
Ensemble forecast service implementation.
"""
from typing import Dict, Any, Optional, List
from ..base import BaseWeatherService
from ..config import settings
from ..models import WeatherRequest, WeatherResponse
from ..utils import clean_none_values


class EnsembleService(BaseWeatherService):
    """Service for fetching ensemble forecast data."""
    
    def __init__(self):
        """Initialize the ensemble service."""
        super().__init__(settings.ENSEMBLE_API_URL)
    
    async def get_ensemble_forecast(
        self,
        request: WeatherRequest,
        models: Optional[List[str]] = None
    ) -> WeatherResponse:
        """
        Get ensemble forecast data.
        
        Args:
            request: Weather request parameters
            models: List of ensemble models to include
            
        Returns:
            WeatherResponse: Ensemble forecast data
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
                params['forecast_days'] = min(request.time_range.forecast_days, 35)  # Max 35 days
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
            
        # Add specific models if requested
        if models:
            params['models'] = ','.join(models)
        
        # Remove None values
        params = clean_none_values(params)
        
        # Make API request
        response_data = await self.get('ensemble', params=params)
        
        # Convert response to WeatherResponse model
        return WeatherResponse(**response_data)
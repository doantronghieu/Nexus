"""
Elevation service implementation.
"""
from typing import Dict, Any, Optional, List, Union
from pydantic import BaseModel
from ..base import BaseWeatherService
from ..config import settings
from ..utils import clean_none_values, validate_coordinates


class ElevationResponse(BaseModel):
    """Model for elevation API response."""
    elevation: List[float]
    generationtime_ms: Optional[float] = None


class ElevationService(BaseWeatherService):
    """Service for fetching elevation data."""
    
    def __init__(self):
        """Initialize the elevation service."""
        super().__init__(settings.WEATHER_API_URL)
    
    async def get_elevation(
        self,
        latitude: Union[float, List[float]],
        longitude: Union[float, List[float]]
    ) -> ElevationResponse:
        """
        Get elevation data for coordinates.
        
        Args:
            latitude: Single latitude or list of latitudes
            longitude: Single longitude or list of longitudes
        
        Returns:
            ElevationResponse: Elevation data
            
        Raises:
            ValueError: If input validation fails
        """
        # Convert single values to lists
        lat_list = [latitude] if isinstance(latitude, (int, float)) else latitude
        lon_list = [longitude] if isinstance(longitude, (int, float)) else longitude
        
        # Validate input
        if len(lat_list) != len(lon_list):
            raise ValueError("Number of latitudes and longitudes must match")
        
        if len(lat_list) > 100:
            raise ValueError("Maximum of 100 coordinate pairs allowed")
        
        # Validate each coordinate pair
        for lat, lon in zip(lat_list, lon_list):
            validate_coordinates(lat, lon)
        
        # Prepare query parameters
        params = {
            'latitude': ','.join(str(lat) for lat in lat_list),
            'longitude': ','.join(str(lon) for lon in lon_list)
        }
        
        # Make API request
        response_data = await self.get('elevation', params=params)
        
        # Convert response to ElevationResponse model
        return ElevationResponse(**response_data)
"""
Geocoding service implementation.
"""
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..base import BaseWeatherService
from ..config import settings
from ..utils import clean_none_values


class GeocodingResult(BaseModel):
    """Model for geocoding results."""
    id: int
    name: str
    latitude: float
    longitude: float
    elevation: Optional[float] = None
    feature_code: Optional[str] = None
    country_code: Optional[str] = None
    timezone: Optional[str] = None
    population: Optional[int] = None
    country: Optional[str] = None
    admin1: Optional[str] = None
    admin2: Optional[str] = None
    admin3: Optional[str] = None
    admin4: Optional[str] = None


class GeocodingResponse(BaseModel):
    """Model for geocoding API response."""
    results: List[GeocodingResult]
    generationtime_ms: Optional[float] = None


class GeocodingService(BaseWeatherService):
    """Service for geocoding locations."""
    
    def __init__(self):
        """Initialize the geocoding service."""
        super().__init__(settings.GEOCODING_API_URL)
    
    async def search_locations(
        self,
        name: str,
        count: Optional[int] = 10,
        language: Optional[str] = "en",
        format: Optional[str] = "json"
    ) -> GeocodingResponse:
        """
        Search for locations by name.
        
        Args:
            name: Location name to search for
            count: Maximum number of results to return
            language: Language for results
            format: Response format (json or protobuf)
        
        Returns:
            GeocodingResponse: Search results
        """
        # Validate input
        if not name or len(name.strip()) < 2:
            raise ValueError("Search term must be at least 2 characters long")
        
        if count < 1 or count > 100:
            raise ValueError("Count must be between 1 and 100")
        
        # Prepare query parameters
        params = {
            'name': name.strip(),
            'count': count,
            'language': language,
            'format': format
        }
        
        # Remove None values
        params = clean_none_values(params)
        
        # Make API request
        response_data = await self.get('search', params=params)
        
        # Convert response to GeocodingResponse model
        return GeocodingResponse(**response_data)
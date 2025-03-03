"""
Tests for Weather Service implementations.
"""
import pytest
from unittest.mock import patch, AsyncMock
from datetime import datetime

from ..models import WeatherRequest, WeatherResponse
from ..services import (
    WeatherForecastService,
    HistoricalWeatherService,
    MarineWeatherService,
    AirQualityService,
    GeocodingService,
    ElevationService,
    FloodService,
    EnsembleService,
    ClimateService
)
from ..exceptions import APIError, ValidationError


@pytest.fixture
def weather_request(valid_coordinates):
    """Create a test weather request."""
    return WeatherRequest(
        coordinates=valid_coordinates,
        hourly=["temperature_2m"],
        timezone="UTC"
    )


class TestWeatherForecastService:
    """Test cases for WeatherForecastService."""
    
    @pytest.fixture
    def forecast_service(self):
        """Create a test forecast service instance."""
        return WeatherForecastService()
    
    @pytest.mark.asyncio
    async def test_get_forecast(self, forecast_service, weather_request):
        """Test getting weather forecast."""
        with patch.object(forecast_service, 'get') as mock_get:
            mock_get.return_value = {
                "latitude": weather_request.coordinates.latitude,
                "longitude": weather_request.coordinates.longitude,
                "timezone": "UTC",
                "timezone_abbreviation": "UTC",
                "generationtime_ms": 50.0,
                "hourly": {
                    "time": ["2024-01-01T00:00"],
                    "temperature_2m": [10.5]
                }
            }
            
            response = await forecast_service.get_forecast(weather_request)
            
            assert isinstance(response, WeatherResponse)
            assert response.latitude == weather_request.coordinates.latitude
            assert "temperature_2m" in response.hourly
            
            mock_get.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_forecast_error_handling(self, forecast_service, weather_request):
        """Test forecast error handling."""
        with patch.object(forecast_service, 'get') as mock_get:
            mock_get.side_effect = APIError("API Error", status_code=400)
            
            with pytest.raises(APIError) as exc_info:
                await forecast_service.get_forecast(weather_request)
            
            assert exc_info.value.status_code == 400


class TestHistoricalWeatherService:
    """Test cases for HistoricalWeatherService."""
    
    @pytest.fixture
    def historical_service(self):
        """Create a test historical service instance."""
        return HistoricalWeatherService()
    
    @pytest.mark.asyncio
    async def test_get_historical_weather(self, historical_service, weather_request):
        """Test getting historical weather data."""
        weather_request.time_range = {
            "start_date": datetime(2024, 1, 1),
            "end_date": datetime(2024, 1, 7)
        }
        
        with patch.object(historical_service, 'get') as mock_get:
            mock_get.return_value = {
                "latitude": weather_request.coordinates.latitude,
                "longitude": weather_request.coordinates.longitude,
                "timezone": "UTC",
                "timezone_abbreviation": "UTC",
                "generationtime_ms": 50.0,
                "hourly": {
                    "time": ["2024-01-01T00:00"],
                    "temperature_2m": [10.5]
                }
            }
            
            response = await historical_service.get_historical_weather(weather_request)
            
            assert isinstance(response, WeatherResponse)
            assert "temperature_2m" in response.hourly
            mock_get.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_historical_missing_dates(self, historical_service, weather_request):
        """Test historical request without dates."""
        with pytest.raises(ValueError):
            await historical_service.get_historical_weather(weather_request)


class TestMarineWeatherService:
    """Test cases for MarineWeatherService."""
    
    @pytest.fixture
    def marine_service(self):
        """Create a test marine service instance."""
        return MarineWeatherService()
    
    @pytest.mark.asyncio
    async def test_get_marine_weather(self, marine_service, weather_request):
        """Test getting marine weather data."""
        weather_request.hourly = ["wave_height", "wave_direction"]
        
        with patch.object(marine_service, 'get') as mock_get:
            mock_get.return_value = {
                "latitude": weather_request.coordinates.latitude,
                "longitude": weather_request.coordinates.longitude,
                "timezone": "UTC",
                "timezone_abbreviation": "UTC",
                "generationtime_ms": 50.0,
                "hourly": {
                    "time": ["2024-01-01T00:00"],
                    "wave_height": [1.5],
                    "wave_direction": [180]
                }
            }
            
            response = await marine_service.get_marine_weather(weather_request)
            
            assert isinstance(response, WeatherResponse)
            assert "wave_height" in response.hourly
            assert "wave_direction" in response.hourly
            mock_get.assert_called_once()


class TestAirQualityService:
    """Test cases for AirQualityService."""
    
    @pytest.fixture
    def air_quality_service(self):
        """Create a test air quality service instance."""
        return AirQualityService()
    
    @pytest.mark.asyncio
    async def test_get_air_quality(self, air_quality_service, weather_request):
        """Test getting air quality data."""
        weather_request.hourly = ["pm10", "pm2_5"]
        
        with patch.object(air_quality_service, 'get') as mock_get:
            mock_get.return_value = {
                "latitude": weather_request.coordinates.latitude,
                "longitude": weather_request.coordinates.longitude,
                "timezone": "UTC",
                "timezone_abbreviation": "UTC",
                "generationtime_ms": 50.0,
                "hourly": {
                    "time": ["2024-01-01T00:00"],
                    "pm10": [15.5],
                    "pm2_5": [8.2]
                }
            }
            
            response = await air_quality_service.get_air_quality(weather_request)
            
            assert isinstance(response, WeatherResponse)
            assert "pm10" in response.hourly
            assert "pm2_5" in response.hourly
            mock_get.assert_called_once()


class TestGeocodingService:
    """Test cases for GeocodingService."""
    
    @pytest.fixture
    def geocoding_service(self):
        """Create a test geocoding service instance."""
        return GeocodingService()
    
    @pytest.mark.asyncio
    async def test_search_locations(self, geocoding_service):
        """Test searching locations."""
        with patch.object(geocoding_service, 'get') as mock_get:
            mock_get.return_value = {
                "results": [{
                    "id": 2950159,
                    "name": "Berlin",
                    "latitude": 52.52437,
                    "longitude": 13.41053,
                    "elevation": 74.0,
                    "timezone": "Europe/Berlin"
                }]
            }
            
            response = await geocoding_service.search_locations("Berlin")
            
            assert "results" in response
            assert len(response.results) == 1
            assert response.results[0].name == "Berlin"
            mock_get.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_invalid_search_term(self, geocoding_service):
        """Test search with invalid term."""
        with pytest.raises(ValueError):
            await geocoding_service.search_locations("")


class TestElevationService:
    """Test cases for ElevationService."""
    
    @pytest.fixture
    def elevation_service(self):
        """Create a test elevation service instance."""
        return ElevationService()
    
    @pytest.mark.asyncio
    async def test_get_elevation(self, elevation_service, valid_coordinates):
        """Test getting elevation data."""
        with patch.object(elevation_service, 'get') as mock_get:
            mock_get.return_value = {
                "elevation": [100.0]
            }
            
            response = await elevation_service.get_elevation(
                valid_coordinates["latitude"],
                valid_coordinates["longitude"]
            )
            
            assert "elevation" in response
            assert isinstance(response.elevation, list)
            assert len(response.elevation) == 1
            mock_get.assert_called_once()


class TestFloodService:
    """Test cases for FloodService."""
    
    @pytest.fixture
    def flood_service(self):
        """Create a test flood service instance."""
        return FloodService()
    
    @pytest.mark.asyncio
    async def test_get_flood_data(self, flood_service, weather_request):
        """Test getting flood data."""
        with patch.object(flood_service, 'get') as mock_get:
            mock_get.return_value = {
                "latitude": weather_request.coordinates.latitude,
                "longitude": weather_request.coordinates.longitude,
                "timezone": "UTC",
                "timezone_abbreviation": "UTC",
                "generationtime_ms": 50.0,
                "daily": {
                    "time": ["2024-01-01"],
                    "river_discharge": [100.5]
                }
            }
            
            response = await flood_service.get_flood_data(weather_request)
            
            assert isinstance(response, WeatherResponse)
            assert "river_discharge" in response.daily
            mock_get.assert_called_once()


class TestEnsembleService:
    """Test cases for EnsembleService."""
    
    @pytest.fixture
    def ensemble_service(self):
        """Create a test ensemble service instance."""
        return EnsembleService()
    
    @pytest.mark.asyncio
    async def test_get_ensemble_forecast(self, ensemble_service, weather_request):
        """Test getting ensemble forecast."""
        models = ["icon_seamless", "icon_global"]
        
        with patch.object(ensemble_service, 'get') as mock_get:
            mock_get.return_value = {
                "latitude": weather_request.coordinates.latitude,
                "longitude": weather_request.coordinates.longitude,
                "timezone": "UTC",
                "timezone_abbreviation": "UTC",
                "generationtime_ms": 50.0,
                "hourly": {
                    "time": ["2024-01-01T00:00"],
                    "temperature_2m": [10.5]
                }
            }
            
            response = await ensemble_service.get_ensemble_forecast(
                weather_request,
                models=models
            )
            
            assert isinstance(response, WeatherResponse)
            assert "temperature_2m" in response.hourly
            mock_get.assert_called_once()


class TestClimateService:
    """Test cases for ClimateService."""
    
    @pytest.fixture
    def climate_service(self):
        """Create a test climate service instance."""
        return ClimateService()
    
    @pytest.mark.asyncio
    async def test_get_climate_data(self, climate_service, weather_request):
        """Test getting climate data."""
        weather_request.time_range = {
            "start_date": datetime(2024, 1, 1),
            "end_date": datetime(2024, 1, 7)
        }
        
        with patch.object(climate_service, 'get') as mock_get:
            mock_get.return_value = {
                "latitude": weather_request.coordinates.latitude,
                "longitude": weather_request.coordinates.longitude,
                "timezone": "UTC",
                "timezone_abbreviation": "UTC",
                "generationtime_ms": 50.0,
                "daily": {
                    "time": ["2024-01-01"],
                    "temperature_2m_max": [15.5],
                    "temperature_2m_min": [8.2]
                }
            }
            
            response = await climate_service.get_climate_data(weather_request)
            
            assert isinstance(response, WeatherResponse)
            assert "temperature_2m_max" in response.daily
            assert "temperature_2m_min" in response.daily
            mock_get.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_climate_missing_dates(self, climate_service, weather_request):
        """Test climate request without dates."""
        with pytest.raises(ValueError):
            await climate_service.get_climate_data(weather_request)
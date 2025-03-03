"""
Tests for Weather Service API endpoints.
"""
import pytest
from datetime import datetime
from unittest.mock import patch, AsyncMock

from ..models import WeatherRequest, WeatherResponse
from ..server import app
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


class TestHealthEndpoint:
    """Test cases for health check endpoint."""
    
    def test_health_check(self, test_client):
        """Test health check endpoint."""
        response = test_client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "ok"
        assert "version" in data
        assert isinstance(data["timestamp"], str)


class TestUIEndpoint:
    """Test cases for UI endpoint."""
    
    def test_ui_page(self, test_client):
        """Test UI page rendering."""
        response = test_client.get("/ui")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


class TestWeatherForecastAPI:
    """Test cases for weather forecast API."""
    
    @pytest.fixture
    def mock_forecast_service(self):
        """Create mock forecast service."""
        with patch.object(WeatherForecastService, 'get_forecast', new_callable=AsyncMock) as mock:
            yield mock
    
    @pytest.mark.asyncio
    async def test_get_forecast(self, test_client, mock_forecast_service, valid_coordinates):
        """Test getting weather forecast."""
        request_data = {
            "coordinates": valid_coordinates,
            "hourly": ["temperature_2m", "relative_humidity_2m"],
            "timezone": "UTC"
        }
        
        response_data = {
            "latitude": valid_coordinates["latitude"],
            "longitude": valid_coordinates["longitude"],
            "timezone": "UTC",
            "timezone_abbreviation": "UTC",
            "generationtime_ms": 50.0,
            "hourly": {
                "time": ["2024-01-01T00:00", "2024-01-01T01:00"],
                "temperature_2m": [10.5, 11.0],
                "relative_humidity_2m": [75, 78]
            },
            "hourly_units": {
                "temperature_2m": "°C",
                "relative_humidity_2m": "%"
            }
        }
        
        mock_forecast_service.return_value = WeatherResponse(**response_data)
        
        response = test_client.post("/api/forecast", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["latitude"] == valid_coordinates["latitude"]
        assert "hourly" in data
        assert "temperature_2m" in data["hourly"]
        assert len(data["hourly"]["time"]) == 2
    
    @pytest.mark.asyncio
    async def test_invalid_forecast_request(self, test_client):
        """Test invalid forecast request handling."""
        # Missing coordinates
        response = test_client.post("/api/forecast", json={})
        assert response.status_code == 422
        
        # Invalid coordinates
        response = test_client.post("/api/forecast", json={
            "coordinates": {
                "latitude": 91,
                "longitude": 0
            }
        })
        assert response.status_code == 422
        
        # Invalid hourly variables
        response = test_client.post("/api/forecast", json={
            "coordinates": {
                "latitude": 52.52,
                "longitude": 13.41
            },
            "hourly": ["invalid_variable"]
        })
        assert response.status_code == 422


class TestHistoricalWeatherAPI:
    """Test cases for historical weather API."""
    
    @pytest.fixture
    def mock_historical_service(self):
        """Create mock historical service."""
        with patch.object(HistoricalWeatherService, 'get_historical_weather', new_callable=AsyncMock) as mock:
            yield mock
    
    @pytest.mark.asyncio
    async def test_get_historical_weather(
        self,
        test_client,
        mock_historical_service,
        valid_coordinates,
        valid_time_range
    ):
        """Test getting historical weather data."""
        request_data = {
            "coordinates": valid_coordinates,
            "time_range": valid_time_range,
            "hourly": ["temperature_2m"]
        }
        
        response_data = {
            "latitude": valid_coordinates["latitude"],
            "longitude": valid_coordinates["longitude"],
            "timezone": "UTC",
            "timezone_abbreviation": "UTC",
            "generationtime_ms": 50.0,
            "hourly": {
                "time": ["2024-01-01T00:00"],
                "temperature_2m": [10.5]
            }
        }
        
        mock_historical_service.return_value = WeatherResponse(**response_data)
        
        response = test_client.post("/api/historical", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["latitude"] == valid_coordinates["latitude"]
        assert "hourly" in data
        assert "temperature_2m" in data["hourly"]


class TestMarineWeatherAPI:
    """Test cases for marine weather API."""
    
    @pytest.fixture
    def mock_marine_service(self):
        """Create mock marine service."""
        with patch.object(MarineWeatherService, 'get_marine_weather', new_callable=AsyncMock) as mock:
            yield mock
    
    @pytest.mark.asyncio
    async def test_get_marine_weather(self, test_client, mock_marine_service, valid_coordinates):
        """Test getting marine weather data."""
        request_data = {
            "coordinates": valid_coordinates,
            "hourly": ["wave_height", "wave_direction"]
        }
        
        response_data = {
            "latitude": valid_coordinates["latitude"],
            "longitude": valid_coordinates["longitude"],
            "timezone": "UTC",
            "timezone_abbreviation": "UTC",
            "generationtime_ms": 50.0,
            "hourly": {
                "time": ["2024-01-01T00:00"],
                "wave_height": [1.5],
                "wave_direction": [180]
            }
        }
        
        mock_marine_service.return_value = WeatherResponse(**response_data)
        
        response = test_client.post("/api/marine", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "wave_height" in data["hourly"]
        assert "wave_direction" in data["hourly"]


class TestAirQualityAPI:
    """Test cases for air quality API."""
    
    @pytest.fixture
    def mock_air_quality_service(self):
        """Create mock air quality service."""
        with patch.object(AirQualityService, 'get_air_quality', new_callable=AsyncMock) as mock:
            yield mock
    
    @pytest.mark.asyncio
    async def test_get_air_quality(self, test_client, mock_air_quality_service, valid_coordinates):
        """Test getting air quality data."""
        request_data = {
            "coordinates": valid_coordinates,
            "hourly": ["pm10", "pm2_5"]
        }
        
        response_data = {
            "latitude": valid_coordinates["latitude"],
            "longitude": valid_coordinates["longitude"],
            "timezone": "UTC",
            "timezone_abbreviation": "UTC",
            "generationtime_ms": 50.0,
            "hourly": {
                "time": ["2024-01-01T00:00"],
                "pm10": [15.5],
                "pm2_5": [8.2]
            }
        }
        
        mock_air_quality_service.return_value = WeatherResponse(**response_data)
        
        response = test_client.post("/api/air-quality", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "pm10" in data["hourly"]
        assert "pm2_5" in data["hourly"]


class TestGeocodingAPI:
    """Test cases for geocoding API."""
    
    @pytest.fixture
    def mock_geocoding_service(self):
        """Create mock geocoding service."""
        with patch.object(GeocodingService, 'search_locations', new_callable=AsyncMock) as mock:
            yield mock
    
    @pytest.mark.asyncio
    async def test_geocode_location(self, test_client, mock_geocoding_service):
        """Test geocoding a location."""
        location_name = "Berlin"
        response_data = {
            "results": [{
                "id": 2950159,
                "name": "Berlin",
                "latitude": 52.52437,
                "longitude": 13.41053,
                "elevation": 74.0,
                "timezone": "Europe/Berlin"
            }]
        }
        
        mock_geocoding_service.return_value = response_data
        
        response = test_client.get(f"/api/geocoding/search?name={location_name}")
        
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert len(data["results"]) > 0
        assert data["results"][0]["name"] == "Berlin"


class TestElevationAPI:
    """Test cases for elevation API."""
    
    @pytest.fixture
    def mock_elevation_service(self):
        """Create mock elevation service."""
        with patch.object(ElevationService, 'get_elevation', new_callable=AsyncMock) as mock:
            yield mock
    
    @pytest.mark.asyncio
    async def test_get_elevation(self, test_client, mock_elevation_service, valid_coordinates):
        """Test getting elevation data."""
        response_data = {
            "elevation": [100.0]
        }
        
        mock_elevation_service.return_value = response_data
        
        response = test_client.get(
            f"/api/elevation?latitude={valid_coordinates['latitude']}&longitude={valid_coordinates['longitude']}"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "elevation" in data
        assert isinstance(data["elevation"], list)
        assert len(data["elevation"]) == 1


class TestErrorHandling:
    """Test cases for error handling."""
    
    def test_validation_error(self, test_client):
        """Test validation error handling."""
        response = test_client.post("/api/forecast", json={
            "coordinates": {
                "latitude": 1000,  # Invalid latitude
                "longitude": 0
            }
        })
        assert response.status_code == 422
        
    def test_not_found_error(self, test_client):
        """Test 404 error handling."""
        response = test_client.get("/invalid-endpoint")
        assert response.status_code == 404
        
    def test_method_not_allowed(self, test_client):
        """Test method not allowed error handling."""
        response = test_client.get("/api/forecast")
        assert response.status_code == 405
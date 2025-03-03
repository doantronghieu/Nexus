"""
Tests for Weather Service data models.
"""
import pytest
from datetime import datetime
from pydantic import ValidationError

from ..models import (
    Coordinates,
    TimeRange,
    WeatherRequest,
    WeatherResponse,
    ErrorResponse
)


class TestCoordinates:
    """Test cases for Coordinates model."""
    
    def test_valid_coordinates(self):
        """Test valid coordinate values."""
        coords = Coordinates(latitude=52.52, longitude=13.41)
        assert coords.latitude == 52.52
        assert coords.longitude == 13.41
    
    def test_invalid_latitude(self):
        """Test invalid latitude values."""
        with pytest.raises(ValidationError):
            Coordinates(latitude=91, longitude=13.41)
        with pytest.raises(ValidationError):
            Coordinates(latitude=-91, longitude=13.41)
    
    def test_invalid_longitude(self):
        """Test invalid longitude values."""
        with pytest.raises(ValidationError):
            Coordinates(latitude=52.52, longitude=181)
        with pytest.raises(ValidationError):
            Coordinates(latitude=52.52, longitude=-181)


class TestTimeRange:
    """Test cases for TimeRange model."""
    
    def test_valid_time_range(self):
        """Test valid time range."""
        time_range = TimeRange(
            start_date=datetime(2024, 1, 1),
            end_date=datetime(2024, 1, 7)
        )
        assert time_range.start_date.year == 2024
        assert time_range.end_date.year == 2024
    
    def test_valid_forecast_days(self):
        """Test valid forecast days."""
        time_range = TimeRange(forecast_days=7)
        assert time_range.forecast_days == 7
    
    def test_invalid_forecast_days(self):
        """Test invalid forecast days."""
        with pytest.raises(ValidationError):
            TimeRange(forecast_days=17)
        with pytest.raises(ValidationError):
            TimeRange(forecast_days=-1)
    
    def test_valid_past_days(self):
        """Test valid past days."""
        time_range = TimeRange(past_days=30)
        assert time_range.past_days == 30
    
    def test_invalid_past_days(self):
        """Test invalid past days."""
        with pytest.raises(ValidationError):
            TimeRange(past_days=93)
        with pytest.raises(ValidationError):
            TimeRange(past_days=-1)


class TestWeatherRequest:
    """Test cases for WeatherRequest model."""
    
    def test_valid_request(self, valid_coordinates, valid_time_range):
        """Test valid weather request."""
        request = WeatherRequest(
            coordinates=valid_coordinates,
            time_range=valid_time_range,
            hourly=["temperature_2m"],
            daily=["temperature_2m_max"],
            timezone="UTC"
        )
        assert request.coordinates.latitude == valid_coordinates["latitude"]
        assert request.timezone == "UTC"
    
    def test_minimal_request(self, valid_coordinates):
        """Test minimal weather request with only required fields."""
        request = WeatherRequest(coordinates=valid_coordinates)
        assert request.coordinates.latitude == valid_coordinates["latitude"]
        assert request.timezone == "UTC"  # Default value
    
    def test_invalid_request_missing_coordinates(self):
        """Test request without required coordinates."""
        with pytest.raises(ValidationError):
            WeatherRequest()


class TestWeatherResponse:
    """Test cases for WeatherResponse model."""
    
    def test_valid_response(self):
        """Test valid weather response."""
        response = WeatherResponse(
            latitude=52.52,
            longitude=13.41,
            timezone="UTC",
            timezone_abbreviation="UTC",
            elevation=100.0,
            generationtime_ms=50.0,
            hourly={
                "time": ["2024-01-01T00:00", "2024-01-01T01:00"],
                "temperature_2m": [10.5, 11.0]
            },
            hourly_units={
                "temperature_2m": "°C"
            }
        )
        assert response.latitude == 52.52
        assert len(response.hourly["time"]) == 2
    
    def test_minimal_response(self):
        """Test minimal weather response with only required fields."""
        response = WeatherResponse(
            latitude=52.52,
            longitude=13.41,
            timezone="UTC",
            timezone_abbreviation="UTC",
            generationtime_ms=50.0
        )
        assert response.latitude == 52.52
        assert response.hourly is None


class TestErrorResponse:
    """Test cases for ErrorResponse model."""
    
    def test_error_response(self):
        """Test error response creation."""
        error = ErrorResponse(
            error=True,
            reason="Test error",
            detail="Error details"
        )
        assert error.error is True
        assert error.reason == "Test error"
        assert error.detail == "Error details"
    
    def test_minimal_error_response(self):
        """Test minimal error response without optional detail."""
        error = ErrorResponse(
            error=True,
            reason="Test error"
        )
        assert error.error is True
        assert error.reason == "Test error"
        assert error.detail is None
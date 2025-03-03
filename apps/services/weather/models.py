"""
Data models for the Weather Service.
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime


class Coordinates(BaseModel):
    """Geographic coordinates model."""
    latitude: float = Field(..., ge=-90, le=90, description="Latitude in degrees")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude in degrees")
    
    @validator('latitude')
    def validate_latitude(cls, v):
        """Validate latitude is within bounds."""
        if not -90 <= v <= 90:
            raise ValueError("Latitude must be between -90 and 90 degrees")
        return v
    
    @validator('longitude')
    def validate_longitude(cls, v):
        """Validate longitude is within bounds."""
        if not -180 <= v <= 180:
            raise ValueError("Longitude must be between -180 and 180 degrees")
        return v


class TimeRange(BaseModel):
    """Time range model for historical and forecast data."""
    start_date: Optional[datetime] = Field(None, description="Start date for data retrieval")
    end_date: Optional[datetime] = Field(None, description="End date for data retrieval")
    past_days: Optional[int] = Field(None, ge=0, le=92, description="Number of past days")
    forecast_days: Optional[int] = Field(None, ge=0, le=16, description="Number of forecast days")
    
    @validator('past_days')
    def validate_past_days(cls, v):
        """Validate past_days is within bounds."""
        if v is not None and not 0 <= v <= 92:
            raise ValueError("past_days must be between 0 and 92")
        return v
    
    @validator('forecast_days')
    def validate_forecast_days(cls, v):
        """Validate forecast_days is within bounds."""
        if v is not None and not 0 <= v <= 16:
            raise ValueError("forecast_days must be between 0 and 16")
        return v


class WeatherRequest(BaseModel):
    """Base weather request model."""
    coordinates: Coordinates
    time_range: Optional[TimeRange] = None
    hourly: Optional[List[str]] = Field(None, description="Hourly weather variables")
    daily: Optional[List[str]] = Field(None, description="Daily weather variables")
    timezone: Optional[str] = Field("UTC", description="Timezone for data")
    temperature_unit: Optional[str] = Field("celsius", description="Temperature unit")
    wind_speed_unit: Optional[str] = Field("kmh", description="Wind speed unit")
    precipitation_unit: Optional[str] = Field("mm", description="Precipitation unit")


class WeatherResponse(BaseModel):
    """Base weather response model."""
    latitude: float
    longitude: float
    timezone: str
    timezone_abbreviation: str
    elevation: Optional[float]
    generationtime_ms: float
    hourly: Optional[Dict[str, List[Any]]]
    daily: Optional[Dict[str, List[Any]]]
    hourly_units: Optional[Dict[str, str]]
    daily_units: Optional[Dict[str, str]]


class ErrorResponse(BaseModel):
    """Error response model."""
    error: bool = True
    reason: str
    detail: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    version: str
    timestamp: datetime
"""
Test configuration and fixtures for the Weather Service.
"""
import asyncio
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from ..server import app
from ..config import settings


@pytest.fixture
def test_client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
async def async_client():
    """Create an async test client for the FastAPI application."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
def event_loop():
    """Create an event loop for async tests."""
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def valid_coordinates():
    """Return valid test coordinates."""
    return {
        "latitude": 52.52,
        "longitude": 13.41
    }


@pytest.fixture
def valid_time_range():
    """Return valid test time range."""
    return {
        "start_date": "2024-01-01",
        "end_date": "2024-01-07"
    }


@pytest.fixture
def weather_variables():
    """Return test weather variables."""
    return {
        "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation"],
        "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"]
    }
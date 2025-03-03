# File: /Users/thung/Documents/Me/Coding/Embedded-AI/apps/services/weather/server.py
"""
FastAPI server implementation for the Weather Service.
"""
import packages
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from services.weather import __version__
from services.weather.config import settings
from services.weather.models import (
    WeatherRequest, WeatherResponse, ErrorResponse, 
    HealthResponse, Coordinates, TimeRange
)
from services.weather.exceptions import WeatherServiceError, APIError, ValidationError
from services.weather.logger import logger
from services.weather.services import (
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

# Initialize FastAPI app
app = FastAPI(
    title="Weather Service",
    description="Weather data service using Open-Meteo APIs",
    version=__version__,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Templates configuration
templates = Jinja2Templates(directory="templates")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Service instances
forecast_service = WeatherForecastService()
historical_service = HistoricalWeatherService()
marine_service = MarineWeatherService()
air_quality_service = AirQualityService()
geocoding_service = GeocodingService()
elevation_service = ElevationService()
flood_service = FloodService()
ensemble_service = EnsembleService()
climate_service = ClimateService()

# Global exception handler
@app.exception_handler(WeatherServiceError)
async def weather_service_exception_handler(request: Request, exc: WeatherServiceError):
    """Handle WeatherServiceError exceptions."""
    status_code = 500
    if isinstance(exc, APIError):
        status_code = exc.status_code
    elif isinstance(exc, ValidationError):
        status_code = 400
        
    return JSONResponse(
        status_code=status_code,
        content=ErrorResponse(
            error=True,
            reason=str(exc),
            detail=exc.detail if hasattr(exc, 'detail') else None
        ).dict()
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=True,
            reason=exc.detail
        ).dict()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.exception("Unhandled exception occurred")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error=True,
            reason="Internal server error",
            detail=str(exc) if settings.DEBUG else None
        ).dict()
    )

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log incoming requests and their processing time."""
    start_time = datetime.utcnow()
    response = await call_next(request)
    process_time = (datetime.utcnow() - start_time).total_seconds()
    
    logger.info(
        f"Request: {request.method} {request.url.path} "
        f"Process Time: {process_time:.3f}s "
        f"Status: {response.status_code}"
    )
    
    return response

# Health check endpoint
@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Check service health."""
    return HealthResponse(
        status="ok",
        version=__version__,
        timestamp=datetime.utcnow()
    )

# UI endpoint
@app.get("/ui", tags=["UI"])
async def ui(request: Request):
    """Render the UI template."""
    return templates.TemplateResponse(
        "ui.html",
        {"request": request, "version": __version__}
    )

# Weather forecast endpoint
@app.post("/api/forecast", response_model=WeatherResponse, tags=["Weather"])
async def get_weather_forecast(request: WeatherRequest):
    """Get weather forecast data."""
    try:
        return await forecast_service.get_forecast(request)
    except Exception as e:
        logger.exception("Error getting weather forecast")
        raise WeatherServiceError(str(e))

# Historical weather endpoint
@app.post("/api/historical", response_model=WeatherResponse, tags=["Weather"])
async def get_historical_weather(request: WeatherRequest):
    """Get historical weather data."""
    try:
        return await historical_service.get_historical_weather(request)
    except Exception as e:
        logger.exception("Error getting historical weather")
        raise WeatherServiceError(str(e))

# Marine weather endpoint
@app.post("/api/marine", response_model=WeatherResponse, tags=["Weather"])
async def get_marine_weather(request: WeatherRequest):
    """Get marine weather data."""
    try:
        return await marine_service.get_marine_weather(request)
    except Exception as e:
        logger.exception("Error getting marine weather")
        raise WeatherServiceError(str(e))

# Air quality endpoint
@app.post("/api/air-quality", response_model=WeatherResponse, tags=["Weather"])
async def get_air_quality(request: WeatherRequest):
    """Get air quality data."""
    try:
        return await air_quality_service.get_air_quality(request)
    except Exception as e:
        logger.exception("Error getting air quality data")
        raise WeatherServiceError(str(e))

# Geocoding endpoint
@app.get("/api/geocoding/search", tags=["Location"])
async def geocode_location(
    name: str,
    count: Optional[int] = 10,
    language: Optional[str] = "en",
    format: Optional[str] = "json"
):
    """Geocode location by name."""
    try:
        return await geocoding_service.search_locations(
            name=name,
            count=count,
            language=language,
            format=format
        )
    except Exception as e:
        logger.exception("Error geocoding location")
        raise WeatherServiceError(str(e))

# Elevation endpoint
@app.get("/api/elevation", tags=["Location"])
async def get_elevation(
    latitude: float,
    longitude: float
):
    """Get elevation data for coordinates."""
    try:
        return await elevation_service.get_elevation(
            latitude=latitude,
            longitude=longitude
        )
    except Exception as e:
        logger.exception("Error getting elevation data")
        raise WeatherServiceError(str(e))

# Flood data endpoint
@app.post("/api/flood", response_model=WeatherResponse, tags=["Weather"])
async def get_flood_data(
    request: WeatherRequest,
    ensemble: Optional[bool] = False
):
    """Get flood forecast data."""
    try:
        return await flood_service.get_flood_data(request, ensemble=ensemble)
    except Exception as e:
        logger.exception("Error getting flood data")
        raise WeatherServiceError(str(e))

# Ensemble forecast endpoint
@app.post("/api/ensemble", response_model=WeatherResponse, tags=["Weather"])
async def get_ensemble_forecast(
    request: WeatherRequest,
    models: Optional[List[str]] = None
):
    """Get ensemble forecast data."""
    try:
        return await ensemble_service.get_ensemble_forecast(request, models=models)
    except Exception as e:
        logger.exception("Error getting ensemble forecast")
        raise WeatherServiceError(str(e))

# Climate data endpoint
@app.post("/api/climate", response_model=WeatherResponse, tags=["Weather"])
async def get_climate_data(
    request: WeatherRequest,
    models: Optional[List[str]] = None,
    disable_bias_correction: Optional[bool] = False
):
    """Get climate data."""
    try:
        return await climate_service.get_climate_data(
            request,
            models=models,
            disable_bias_correction=disable_bias_correction
        )
    except Exception as e:
        logger.exception("Error getting climate data")
        raise WeatherServiceError(str(e))

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown."""
    await forecast_service.close()
    await historical_service.close()
    await marine_service.close()
    await air_quality_service.close()
    await geocoding_service.close()
    await elevation_service.close()
    await flood_service.close()
    await ensemble_service.close()
    await climate_service.close()

def run_server():
    """Run the FastAPI server."""
    import uvicorn
    
    # Configure logging
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    uvicorn.run(
        "server:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_config=log_config,
        log_level="debug" if settings.DEBUG else "info"
    )

if __name__ == "__main__":
    run_server()
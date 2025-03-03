import packages # Must include this

from context.infra import clients
from context.infra.clients import logger
from context.utils import typer as t
from toolkit.utils import utils
from toolkit.utils.utils import Path as PathLib

from fastapi import FastAPI, Query, HTTPException, Path, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import uvicorn
#*------------------------------------------------------------------------------
from context.infra.services_info import URL_SVC_MAP

# client_redis = rediz.REDIS_CLIENT
client_redis = clients.client_redis
#*------------------------------------------------------------------------------

REDIS_KEY_PREFIX_DIRECTIONS = "directions:"
REDIS_TTL_DIRECTIONS = 36000  # 1 hour
REDIS_KEY_PREFIX_PLACES = "places:"
REDIS_TTL_PLACES = 36000

# Environment Variables
MAPBOX_API_KEY = utils.os.getenv("MAPBOX_API_KEY")
MAPBOX_TOKEN = utils.os.getenv("MAPBOX_TOKEN")  # For frontend
MAP_CENTER_LAT = float(utils.os.getenv("MAP_CENTER_LAT", "-122.662323"))
MAP_CENTER_LNG = float(utils.os.getenv("MAP_CENTER_LNG", "45.523751"))
MAP_ZOOM = int(utils.os.getenv("MAP_ZOOM", "12"))

if not MAPBOX_API_KEY:
    logger.warning("MAPBOX_API_KEY environment variable is not set")

# Default coordinates
DEFAULT_START_LNG = 106.656136
DEFAULT_START_LAT = 10.965764
DEFAULT_END_LNG = 106.658579
DEFAULT_END_LAT = 10.979173

URL_MAPBOX = "https://api.mapbox.com"
#*=============================================================================
# Setup template directory
BASE_DIR = PathLib(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Common base model
class BaseModelWithConfig(t.BaseModel):
    model_config = t.ConfigDict(extra='allow')

# Direction API Models
class CongestionLevel(str, t.Enum):
    UNKNOWN = "unknown"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    SEVERE = "severe"

class MapboxStreetInfo(BaseModelWithConfig):
    class_: t.Optional[str] = t.Field(None, alias='class')

class Location(BaseModelWithConfig):
    distance: float
    name: str
    location: t.List[float]

    @t.field_validator('location')
    def validate_coordinates(cls, v):
        if len(v) != 2:
            raise ValueError("Location must be [longitude, latitude]")
        lng, lat = v
        if not (-180 <= lng <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        if not (-90 <= lat <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        return v

class Intersection(BaseModelWithConfig):
    bearings: t.List[int]
    entry: t.List[bool]
    in_: t.Optional[int] = t.Field(None, alias='in')
    out: t.Optional[int] = None
    geometry_index: t.Optional[int] = None
    location: t.List[float]
    mapbox_streets_v8: t.Optional[MapboxStreetInfo] = None
    is_urban: t.Optional[bool] = None

class Component(BaseModelWithConfig):
    type: str
    text: str
    mapbox_shield: t.Optional[t.Dict[str, t.Any]] = None
    delimiter: t.Optional[str] = None

class Instruction(BaseModelWithConfig):
    components: t.List[Component]
    type: str
    modifier: t.Optional[str] = None
    text: str

class BannerInstruction(BaseModelWithConfig):
    primary: Instruction
    sub: t.Optional[Instruction] = None
    distanceAlongGeometry: float

class VoiceInstruction(BaseModelWithConfig):
    ssmlAnnouncement: str
    announcement: str
    distanceAlongGeometry: float

class Maneuver(BaseModelWithConfig):
    type: str
    instruction: str
    bearing_after: int
    bearing_before: int
    location: t.List[float]
    modifier: t.Optional[str] = None

class Geometry(BaseModelWithConfig):
    coordinates: t.List[t.List[float]]
    type: t.Literal["LineString"]

class Step(BaseModelWithConfig):
    bannerInstructions: t.Optional[t.List[BannerInstruction]] = None
    voiceInstructions: t.Optional[t.List[VoiceInstruction]] = None
    intersections: t.List[Intersection]
    maneuver: Maneuver
    name: str
    duration: float
    distance: float
    driving_side: str
    weight: float
    mode: str
    geometry: Geometry
    ref: t.Optional[str] = None

class Admin(BaseModelWithConfig):
    iso_3166_1: str = ""

class Annotation(BaseModelWithConfig):
    congestion: t.List[str]
    distance: t.List[float]
    duration: t.List[float]

class Leg(BaseModelWithConfig):
    via_waypoints: t.List = t.Field(default_factory=list)
    annotation: Annotation
    admins: t.List[Admin]
    weight: float
    duration: float
    steps: t.List[Step]
    distance: float
    summary: str
    geometry: t.Optional[Geometry] = None

class Route(BaseModelWithConfig):
    weight_name: str
    weight: float
    duration: float
    distance: float
    legs: t.List[Leg]
    geometry: Geometry
    voiceLocale: str

class DirectionsResponse(BaseModelWithConfig):
    routes: t.List[Route]
    waypoints: t.List[Location]
    code: str
    uuid: str

# Search API Models
class AddressContext(BaseModelWithConfig):
    name: str
    address_number: t.Optional[str] = None
    street_name: t.Optional[str] = None

class CountryContext(BaseModelWithConfig):
    name: str
    country_code: t.Optional[str] = None
    country_code_alpha_3: t.Optional[str] = None

class PostcodeContext(BaseModelWithConfig):
    id: t.Optional[str] = None
    name: str

class PlaceContext(BaseModelWithConfig):
    id: t.Optional[str] = None
    name: str

class NeighborhoodContext(BaseModelWithConfig):
    id: t.Optional[str] = None
    name: str

class StreetContext(BaseModelWithConfig):
    name: str

class Context(BaseModelWithConfig):
    country: CountryContext
    postcode: PostcodeContext
    place: t.Optional[PlaceContext] = None
    neighborhood: t.Optional[NeighborhoodContext] = None
    address: AddressContext
    street: StreetContext

class ExternalIds(BaseModelWithConfig):
    id_osm: t.Optional[str] = None
    dataplor: t.Optional[str] = None

class Suggestion(BaseModelWithConfig):
    name: str
    mapbox_id: str
    feature_type: str
    address: str
    full_address: str
    place_formatted: str
    context: Context
    language: str
    maki: str
    poi_category: t.List[str] = []
    poi_category_ids: t.List[str]
    external_ids: ExternalIds
    distance: float
    operational_status: t.Optional[str] = None
    metadata: t.Optional[t.Dict[str, t.Any]] = None

class SearchResponse(BaseModelWithConfig):
    suggestions: t.List[Suggestion]
    attribution: str
    response_id: str
    url: str

# Error Models
class DirectionsError(BaseModelWithConfig):
    code: str
    message: str

# Retrieve Models
class Coordinates(BaseModelWithConfig):
    latitude: float
    longitude: float
    routable_points: t.Optional[t.List[t.Dict[str, t.Any]]] = None

class LocalityContext(BaseModelWithConfig):
    id: t.Optional[str] = None
    name: str

class RetrieveContext(BaseModelWithConfig):
    country: CountryContext
    postcode: PostcodeContext
    place: PlaceContext
    locality: t.Optional[LocalityContext] = None
    address: AddressContext
    street: StreetContext

class FeatureProperties(BaseModelWithConfig):
    name: str
    mapbox_id: str
    feature_type: str
    address: str
    full_address: str
    place_formatted: str
    context: RetrieveContext
    coordinates: Coordinates
    language: str
    maki: str
    poi_category: t.List[str]
    poi_category_ids: t.List[str]
    external_ids: t.Dict[str, t.Any] = t.Field(default_factory=dict)
    metadata: t.Optional[t.Dict[str, t.Any]] = None
    operational_status: t.Optional[str] = None

class Feature(BaseModelWithConfig):
    type: t.Literal["Feature"]
    geometry: t.Dict[str, t.Any]
    properties: FeatureProperties

class RetrieveResponse(BaseModelWithConfig):
    type: t.Literal["FeatureCollection"]
    features: t.List[Feature]
    attribution: str

# FastAPI App
app = FastAPI(title="Mapbox Service")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Frontend Routes
@app.get("/")
async def home(request: Request):
    """Serve the main page with environment variables"""
    return templates.TemplateResponse(
        "mapbox.html", 
        {
            "request": request,
            "mapbox_token": MAPBOX_TOKEN,
            "map_center_lat": MAP_CENTER_LAT,
            "map_center_lng": MAP_CENTER_LNG,
            "map_zoom": MAP_ZOOM,
        }
    )

@app.get("/llm")
async def home(request: Request):
    """Serve the main page with environment variables"""
    return templates.TemplateResponse(
        "mapbox-llm.html", 
        {
            "request": request,
            "mapbox_token": MAPBOX_TOKEN,
            "map_center_lat": MAP_CENTER_LAT,
            "map_center_lng": MAP_CENTER_LNG,
            "map_zoom": MAP_ZOOM,
        }
    )

# Location API endpoint
@app.get("/api/location")
async def get_location():
    """Get current location coordinates by calling external location service"""
    try:
        async with utils.httpx.AsyncClient(verify=False) as client:  # verify=False since it's https on localhost
            response = await client.get(f"{URL_SVC_MAP}/api/location")
            response.raise_for_status()
            data = response.json()
            
            # Extract just the coordinates from the full response
            return {
                "coordinates": {
                    "latitude": data["coordinates"]["latitude"],
                    "longitude": data["coordinates"]["longitude"]
                }
            }
    except Exception as e:
        logger.error(f"Error fetching location: {str(e)}")
        # Fallback to defaults if the call fails
        return {
            "coordinates": {
                "latitude": DEFAULT_START_LAT,
                "longitude": DEFAULT_START_LNG
            }
        }

async def get_current_location() -> t.Tuple[float, float]:
    """
    Utility function to get current location coordinates.
    Returns tuple of (longitude, latitude)
    """
    try:
        async with utils.httpx.AsyncClient(verify=False) as client:
            response = await client.get(f"{URL_SVC_MAP}/api/location")
            response.raise_for_status()
            data = response.json()
            return (
                data["coordinates"]["longitude"],
                data["coordinates"]["latitude"]
            )
    except Exception as e:
        logger.error(f"Error fetching location: {str(e)}")
        return (DEFAULT_START_LNG, DEFAULT_START_LAT)

# API Functions
async def get_mapbox_directions(
    start_lng: float,
    start_lat: float,
    end_lng: float,
    end_lat: float,
) -> t.Dict:
    base_url = f"{URL_MAPBOX}/directions/v5/mapbox/driving"
    coordinates = f"{start_lng},{start_lat};{end_lng},{end_lat}"
    
    params = {
        "alternatives": "true",
        "annotations": "distance,congestion,duration",
        "banner_instructions": "true",
        "geometries": "geojson",
        "language": "en",
        "overview": "full",
        "roundabout_exits": "true",
        "steps": "true",
        "voice_instructions": "true",
        "voice_units": "imperial",
        "access_token": MAPBOX_API_KEY
    }
    
    try:
        async with utils.httpx.AsyncClient() as client:
            response = await client.get(
                f"{base_url}/{utils.quote(coordinates)}",
                params=params,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except utils.httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Request to Mapbox API timed out")
    except utils.httpx.HTTPError as e:
        logger.error(f"Mapbox API error: {str(e)}")
        raise HTTPException(status_code=e.response.status_code if hasattr(e, 'response') else 500,
                          detail="Error communicating with Mapbox API")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def get_mapbox_search(
    query: str,
    language: str,
    limit: int,
    navigation_profile: str,
    country: str,
    proximity_lng: float,
    proximity_lat: float,
    origin_lng: float,
    origin_lat: float,
) -> t.Dict:
    base_url = f"{URL_MAPBOX}/search/searchbox/v1/suggest"
    
    params = {
        "q": query,
        "language": language,
        "limit": limit,
        "navigation_profile": navigation_profile,
        "country": country,
        "proximity": f"{proximity_lng},{proximity_lat}",
        "origin": f"{origin_lng},{origin_lat}",
        "session_token": str(utils.uuid4()),
        "access_token": MAPBOX_API_KEY
    }
    
    try:
        async with utils.httpx.AsyncClient() as client:
            response = await client.get(
                base_url,
                params=params,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except utils.httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Request to Mapbox API timed out")
    except utils.httpx.HTTPError as e:
        logger.error(f"Mapbox API error: {str(e)}")
        raise HTTPException(status_code=e.response.status_code if hasattr(e, 'response') else 500,
                          detail="Error communicating with Mapbox API")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def get_mapbox_retrieve(
    mapbox_id: str,
) -> t.Dict:
    """
    Retrieve detailed information about a specific place using its Mapbox ID.
    """
    base_url = f"{URL_MAPBOX}/search/searchbox/v1/retrieve/{mapbox_id}"
    
    params = {
        "session_token": str(utils.uuid4()),
        "access_token": MAPBOX_API_KEY
    }
    
    try:
        async with utils.httpx.AsyncClient() as client:
            response = await client.get(
                base_url,
                params=params,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except utils.httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Request to Mapbox API timed out")
    except utils.httpx.HTTPError as e:
        logger.error(f"Mapbox API error: {str(e)}")
        raise HTTPException(status_code=e.response.status_code if hasattr(e, 'response') else 500,
                          detail="Error communicating with Mapbox API")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# API Routes
@app.get("/api/directions/")
async def get_directions(
    start_lng: t.Optional[float] = Query(None, description="Starting point longitude", ge=-180, le=180),
    start_lat: t.Optional[float] = Query(None, description="Starting point latitude", ge=-90, le=90),
    end_lng: float = Query(DEFAULT_END_LNG, description="Destination longitude", ge=-180, le=180),
    end_lat: float = Query(DEFAULT_END_LAT, description="Destination latitude", ge=-90, le=90),
):
    """Get driving directions between two points using Mapbox Directions API."""
    # If start coordinates not provided, get current location
    if start_lng is None or start_lat is None:
        start_lng, start_lat = await get_current_location()
    
    return await get_mapbox_directions(
        start_lng=start_lng,
        start_lat=start_lat,
        end_lng=end_lng,
        end_lat=end_lat,
    )

@app.get("/api/search/")
async def search(
    query: str = Query(..., description="Search query"),
    language: str = Query("en", description="Response language"),
    limit: int = Query(5, description="Maximum number of results", ge=1, le=10),
    navigation_profile: str = Query("driving", description="Navigation profile"),
    country: str = Query("vn", description="Country code"),
    proximity_lng: t.Optional[float] = Query(None, description="Proximity longitude", ge=-180, le=180),
    proximity_lat: t.Optional[float] = Query(None, description="Proximity latitude", ge=-90, le=90),
):
    """Search for places using Mapbox Searchbox API."""
    # Get current location for proximity and origin if not provided
    if proximity_lng is None or proximity_lat is None:
        proximity_lng, proximity_lat = await get_current_location()
    
    return await get_mapbox_search(
        query=query,
        language=language,
        limit=limit,
        navigation_profile=navigation_profile,
        country=country,
        proximity_lng=proximity_lng,
        proximity_lat=proximity_lat,
        origin_lng=proximity_lng,
        origin_lat=proximity_lat
    )

@app.get("/api/retrieve/{mapbox_id}")
async def retrieve(
    mapbox_id: str = Path(..., description="Mapbox ID of the place to retrieve")
):
    """Retrieve detailed information about a specific place using its Mapbox ID."""
    return await get_mapbox_retrieve(mapbox_id)

@app.get("/api/stored-places")
async def get_stored_places():
    """Get stored places from Redis"""
    try:
        places_json = client_redis.get(f"{REDIS_KEY_PREFIX_PLACES}")
        if places_json:
            return {
                "success": True,
                "places": utils.json.loads(places_json)
            }
        return {"success": False, "places": []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stored-directions")
async def get_stored_directions():
    """Get stored directions from Redis"""
    try:
        directions_json = client_redis.get(f"{REDIS_KEY_PREFIX_DIRECTIONS}")
        if directions_json:
            return {
                "success": True,
                "directions": utils.json.loads(directions_json)
            }
        return {"success": False, "directions": None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    current_lng, current_lat = await get_current_location()
    return {
        "status": "healthy",
        "mapbox_api_key_configured": bool(MAPBOX_API_KEY),
        "mapbox_token_configured": bool(MAPBOX_TOKEN),
        "current_location": {
            "longitude": current_lng,
            "latitude": current_lat
        },
        "default_coordinates": {
            "end": [DEFAULT_END_LNG, DEFAULT_END_LAT]
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=utils.os.getenv("PORT_SVC_MAPBOX"))
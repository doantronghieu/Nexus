import packages # Must be included
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, List
import uvicorn
import ssl, os, subprocess, webbrowser, threading, time, platform, httpx
from loguru import logger
from urllib.parse import quote

# Store latest location data
latest_location: Dict = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: open browser in a separate thread
    browser_thread = threading.Thread(target=lambda: (
        time.sleep(2),  # Wait for server to start
        webbrowser.open(f'https://localhost:{os.getenv("PORT_SVC_MAP")}')
    ), daemon=True)
    browser_thread.start()
    
    yield  # Server is running
    
    # Cleanup (if needed)
    pass

# Update FastAPI app initialization
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Location(BaseModel):
    latitude: float
    longitude: float
    accuracy: Optional[float] = None
    timestamp: Optional[float] = None

class LocationResponse(BaseModel):
    coordinates: Dict
    address: Dict
    maps: Dict
    timestamp: float

class PlaceSearch(BaseModel):
    keyword: str
    latitude: Optional[float] = 0
    longitude: Optional[float] = 0
    radius: Optional[float] = 5000  # Default radius in meters
    limit: Optional[int] = 10  # Default number of results

class Place(BaseModel):
    name: str
    category: Optional[str]
    distance: float  # Distance in meters
    latitude: float
    longitude: float
    address: str


def read_html_template():
    """Read the HTML template from file"""
    template_path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
    try:
        with open(template_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        logger.error(f"Template file not found at {template_path}")
        return "Error: Template file not found"
    except Exception as e:
        logger.error(f"Error reading template file: {str(e)}")
        return f"Error: {str(e)}"

def install_mkcert():
    """Install mkcert and generate locally-trusted certificates"""
    try:
        system = platform.system().lower()
        
        # Install mkcert based on operating system
        if system == "darwin":  # macOS
            # Check if homebrew is installed
            if subprocess.run(['which', 'brew'], capture_output=True).returncode != 0:
                print("Homebrew not found. Please install homebrew first.")
                return False
            
            # Install mkcert using homebrew
            subprocess.run(['brew', 'install', 'mkcert'], check=True)
            subprocess.run(['brew', 'install', 'nss'], check=True)  # Required for Firefox
            
        elif system == "linux":
            # For Ubuntu/Debian
            subprocess.run(['sudo', 'apt-get', 'update'], check=True)
            subprocess.run(['sudo', 'apt-get', 'install', '-y', 'libnss3-tools'], check=True)
            
            # Download and install mkcert
            subprocess.run([
                'sudo', 'wget', 'https://github.com/FiloSottile/mkcert/releases/download/v1.4.3/mkcert-v1.4.3-linux-amd64',
                '-O', '/usr/local/bin/mkcert'
            ], check=True)
            subprocess.run(['sudo', 'chmod', '+x', '/usr/local/bin/mkcert'], check=True)
            
        elif system == "windows":
            # For Windows using chocolatey
            subprocess.run(['choco', 'install', 'mkcert'], check=True)
        
        # Install the local CA
        subprocess.run(['mkcert', '-install'], check=True)
        
        # Generate certificates for localhost
        subprocess.run([
            'mkcert',
            'localhost',
            '127.0.0.1',
            '::1'
        ], check=True)
        
        # Rename the certificates to match our application
        os.rename('localhost+2.pem', 'domain.crt')
        os.rename('localhost+2-key.pem', 'domain.key')
        
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"Error during mkcert installation: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def open_browser():
    """Function to open browser after a short delay"""
    time.sleep(2)  # Wait for server to start
    webbrowser.open(f'https://localhost:{os.getenv("PORT_SVC_MAP")}')

def generate_map_links(lat: float, lon: float, address: str = "") -> Dict:
    """Generate map links for a given location"""
    return {
        "google_maps": f"https://www.google.com/maps?q={lat},{lon}",
        "google_maps_directions": f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}"
    }

def create_location_response(latitude: float, longitude: float, accuracy: Optional[float], 
                           timestamp: float, address_details: Optional[Dict] = None) -> Dict:
    """Create a standardized location response"""
    # Base coordinates structure
    coordinates = {
        "latitude": latitude,
        "longitude": longitude,
        "accuracy": accuracy
    }

    # Generate map links
    maps = generate_map_links(latitude, longitude)

    # Process address details
    if not address_details:
        address = {
            "street": "Unknown",
            "house_number": "",
            "city": "Unknown",
            "state": "",
            "country": "",
            "postal_code": "",
            "neighborhood": "",
            "full_address": "Address information unavailable"
        }
    else:
        addr = address_details.get('address', {})
        address = {
            "street": addr.get('road', 'Unknown'),
            "house_number": addr.get('house_number', ''),
            "city": addr.get('city', addr.get('town', addr.get('village', 'Unknown'))),
            "state": addr.get('state', ''),
            "country": addr.get('country', ''),
            "postal_code": addr.get('postcode', ''),
            "neighborhood": addr.get('suburb', ''),
            "full_address": address_details.get('display_name', 'Full address unavailable')
        }

    return {
        "coordinates": coordinates,
        "address": address,
        "maps": maps,
        "timestamp": timestamp
    }

async def get_location_details(lat: float, lon: float) -> dict:
    """Get detailed location information using OpenStreetMap Nominatim API"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
            headers = {
                "User-Agent": "FastAPI_Geolocation_App/1.0"
            }
            response = await client.get(url, headers=headers)
            logger.info(f"Nominatim API response status: {response.status_code}")
            
            if response.status_code == 200:
                return response.json()
            
            logger.error(f"Failed to get location details: {response.status_code}")
            return None
            
    except Exception as e:
        logger.error(f"Error fetching location details: {str(e)}")
        return None

@app.post("/api/location", response_model=LocationResponse)
async def save_location(location: Location):
    """Save and process new location data"""
    try:
        logger.info(f"Received location update: {location.latitude}, {location.longitude}")
        details = await get_location_details(location.latitude, location.longitude)
        
        # Create standardized response
        result = create_location_response(
            latitude=location.latitude,
            longitude=location.longitude,
            accuracy=location.accuracy,
            timestamp=location.timestamp,
            address_details=details
        )
        
        # Store the latest location
        global latest_location
        latest_location = result
        logger.info("Successfully updated location with full details")
        return result
        
    except Exception as e:
        logger.error(f"Error processing location update: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/location", response_model=LocationResponse)
async def get_location():
    """Get the latest location information"""
    if not latest_location:
        raise HTTPException(
            status_code=404,
            detail="No location data available"
        )
    return latest_location

@app.get("/api/coordinates")
async def get_coordinates():
    """Get just the latest coordinates and maps links"""
    if not latest_location:
        raise HTTPException(status_code=404, detail="No location data available")
    return {
        "coordinates": latest_location["coordinates"],
        "maps": latest_location["maps"],
        "timestamp": latest_location["timestamp"]
    }

@app.get("/api/address")
async def get_address():
    """Get just the latest address information"""
    if not latest_location:
        raise HTTPException(status_code=404, detail="No location data available")
    return {
        "address": latest_location["address"],
        "timestamp": latest_location["timestamp"]
    }

@app.get("/", response_class=HTMLResponse)
async def get_html():
    """Serve the main HTML page"""
    return read_html_template()

async def search_nearby_places(lat: float, lon: float, keyword: str, radius: float = 1000, limit: int = 10) -> List[Dict]:
    """
    Search for nearby places using OpenStreetMap's Nominatim API with improved search parameters
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Calculate bounding box based on approximate radius
            # 0.01 degrees is roughly 1.11km at the equator
            deg_radius = (radius / 111000) * 1.5  # Adding 50% to ensure coverage
            
            encoded_keyword = quote(keyword)
            url = (
                f"https://nominatim.openstreetmap.org/search"
                f"?q={encoded_keyword}"
                f"&format=json"
                f"&lat={lat}"
                f"&lon={lon}"
                f"&limit={limit * 2}"  # Request more results to account for filtering
                f"&addressdetails=1"
                f"&bounded=1"
                f"&viewbox={lon-deg_radius},{lat+deg_radius},{lon+deg_radius},{lat-deg_radius}"
                f"&exclude_place_ids="  # Avoid duplicate results
            )
            
            headers = {
                "User-Agent": "FastAPI_Geolocation_App/1.0"
            }
            
            response = await client.get(url, headers=headers)
            logger.info(f"Nominatim search API response status: {response.status_code}")
            
            if response.status_code != 200:
                logger.error(f"Failed to search places: {response.status_code}")
                return []
            
            results = response.json()
            if not results:
                # Try a second search with different parameters
                url = (
                    f"https://nominatim.openstreetmap.org/search"
                    f"?q={encoded_keyword}"
                    f"&format=json"
                    f"&limit={limit * 2}"
                    f"&addressdetails=1"
                    f"&bounded=1"
                    f"&viewbox={lon-deg_radius},{lat+deg_radius},{lon+deg_radius},{lat-deg_radius}"
                )
                response = await client.get(url, headers=headers)
                results = response.json()
            
            places = []
            
            for place in results:
                # Calculate distance using haversine formula
                from math import radians, sin, cos, sqrt, atan2
                
                def haversine_distance(lat1, lon1, lat2, lon2):
                    R = 6371000  # Earth's radius in meters
                    phi1 = radians(lat1)
                    phi2 = radians(lat2)
                    delta_phi = radians(lat2 - lat1)
                    delta_lambda = radians(lon2 - lon1)
                    
                    a = sin(delta_phi/2)**2 + cos(phi1) * cos(phi2) * sin(delta_lambda/2)**2
                    c = 2 * atan2(sqrt(a), sqrt(1-a))
                    return R * c
                
                try:
                    place_lat = float(place['lat'])
                    place_lon = float(place['lon'])
                    distance = haversine_distance(lat, lon, place_lat, place_lon)
                    
                    # Only include places within the specified radius
                    if distance <= radius:
                        # Get a meaningful name from the place data
                        name_parts = place.get('display_name', '').split(',')
                        name = name_parts[0].strip()
                        
                        # Get category from available data
                        category = place.get('type') or place.get('category') or place.get('class', None)
                        
                        places.append({
                            "name": name,
                            "category": category,
                            "distance": round(distance),
                            "latitude": place_lat,
                            "longitude": place_lon,
                            "address": place.get('display_name', '')
                        })
                except (ValueError, KeyError) as e:
                    logger.warning(f"Skipping invalid place data: {str(e)}")
                    continue
            
            # Sort by distance
            places.sort(key=lambda x: x['distance'])
            return places[:limit]
            
    except Exception as e:
        logger.error(f"Error searching nearby places: {str(e)}")
        return []

@app.post("/api/places/nearby", response_model=List[Place])
async def find_nearby_places(search: PlaceSearch):
    """Find nearby places based on keyword search"""
    try:
        # Use latest_location if coordinates not provided
        if search.latitude == 0 or search.longitude == 0:
            if not latest_location or 'coordinates' not in latest_location:
                raise HTTPException(
                    status_code=400,
                    detail="No location available. Please provide coordinates or ensure location tracking is active."
                )
            search.latitude = latest_location['coordinates']['latitude']
            search.longitude = latest_location['coordinates']['longitude']
        
        places = await search_nearby_places(
            lat=search.latitude,
            lon=search.longitude,
            keyword=search.keyword,
            radius=search.radius,
            limit=search.limit
        )
        
        if not places:
            raise HTTPException(
                status_code=404,
                detail=f"No places found matching '{search.keyword}' within {search.radius}m"
            )
        
        return places
        
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error processing nearby places search: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Check if certificates exist, if not generate them using mkcert
    if not (os.path.exists('domain.crt') and os.path.exists('domain.key')):
        print("Generating trusted certificates using mkcert...")
        if not install_mkcert():
            print("Failed to generate trusted certificates. Exiting...")
            exit(1)
    
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain('domain.crt', 'domain.key')
    
    # Start server
    print("Starting server and opening browser...")
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=os.getenv("PORT_SVC_MAP"), 
        ssl_keyfile="domain.key",
        ssl_certfile="domain.crt"
    )
import packages # Must include this
from context.infra import clients

from toolkit.db import rediz
from configs import settings

from services.map.mapbox import (
    REDIS_KEY_PREFIX_DIRECTIONS, REDIS_KEY_PREFIX_PLACES, REDIS_TTL_DIRECTIONS, 
    REDIS_TTL_PLACES
)

from toolkit.utils.llm import main as utils_llm
from toolkit.llm.llama_index import cores, messages
import os
import httpx
from typing import Dict, Any, List, Optional, Tuple, Union
from rapidfuzz import fuzz, process
from enum import Enum
from dataclasses import dataclass
from loguru import logger
import yaml
import os
import json
from uuid import uuid4

URL_SVC_MAPBOX = f"http://localhost:{os.getenv('PORT_SVC_MAPBOX')}"
os.environ["IN_PROD"] = "True" # toggle
IS_DEBUG = os.getenv("IN_PROD") is None

# Use the redis_client from toolkit
# client_redis = rediz.REDIS_CLIENT
client_redis = clients.client_redis

class MapAction(str, Enum):
    SEARCH = "search"  
    CONFIRM_PLACE = "confirm_place"
    GET_DIRECTIONS = "get_directions"

@dataclass
class SearchAction:
    query: str

@dataclass 
class ConfirmPlaceAction:
    search_query: str
    confirm_query: str

@dataclass
class GetDirectionsAction:
    place_details: Dict[str, Any]

@dataclass
class MapOperationResponse:
    success: bool
    action: MapAction
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

class MapOperationError(Exception):
    def __init__(self, message: str, details: Optional[Dict] = None):
        self.message = message
        self.details = details
        super().__init__(self.message)

async def search(query: str) -> List[Dict[str, Any]]:
    """
    Search for places and return a simplified list of results.
    
    Args:
        query (str): The search query string
        
    Returns:
        List[Dict[str, Any]]: List of places with name, id, and details
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{URL_SVC_MAPBOX}/api/search/",
                params={"query": query}
            )
            response.raise_for_status()
            data = response.json()
            
            return [{
                'name': place['name'],
                'mapbox_id': place['mapbox_id'],
                'place_formatted': place['place_formatted'],
                'poi_category': place['poi_category'],
                'maki': place.get('maki', '')
            } for place in data['suggestions']]
            
    except httpx.HTTPStatusError as e:
        raise MapOperationError("Search request failed", {"status": e.response.status_code, "detail": e.response.text})
    except httpx.RequestError as e:
        raise MapOperationError("Network error during search", {"error": str(e)})

async def get_place_by_name(places: List[Dict[str, Any]], name: str, threshold: int = 50) -> Optional[Dict[str, Any]]:
    """
    Find a place from the search results by name using fuzzy matching.
    
    Args:
        places (List[Dict[str, Any]]): List of places from search
        name (str): Name to look for
        threshold (int): Minimum similarity score (0-100) to consider a match
        
    Returns:
        Optional[Dict[str, Any]]: Best matching place or None if no match above threshold
    """
    if not places:
        return None
        
    place_names = [place['name'] for place in places]
    
    best_match, score, index = process.extractOne(
        name,
        place_names,
        scorer=fuzz.token_sort_ratio
    )
    
    if score >= threshold:
        return {
            **places[index],
            'match_score': score
        }
    
    return None

async def retrieve_place_details(place: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get detailed information about a place using its Mapbox ID.
    
    Args:
        place (Dict[str, Any]): Place information from search/get_place_by_name
        
    Returns:
        Dict[str, Any]: Detailed place information including coordinates
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{URL_SVC_MAPBOX}/api/retrieve/{place['mapbox_id']}"
            )
            response.raise_for_status()
            data = response.json()
            
            feature = data['features'][0]
            return {
                **place,
                'coordinates': {
                    'longitude': feature['properties']['coordinates']['longitude'],
                    'latitude': feature['properties']['coordinates']['latitude']
                }
            }
            
    except httpx.HTTPStatusError as e:
        raise MapOperationError("Failed to retrieve place details", {"status": e.response.status_code, "detail": e.response.text})
    except httpx.RequestError as e:
        raise MapOperationError("Network error retrieving place details", {"error": str(e)})

async def get_directions_to_place(place_details: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get directions to a place using its coordinates.
    
    Args:
        place_details (Dict[str, Any]): Place details from retrieve_place_details
        
    Returns:
        Dict[str, Any]: Route information
    """
    try:
        coords = place_details['coordinates']
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{URL_SVC_MAPBOX}/api/directions/",
                params={
                    "end_lng": coords['longitude'],
                    "end_lat": coords['latitude']
                }
            )
            response.raise_for_status()
            return response.json()
            
    except httpx.HTTPStatusError as e:
        raise MapOperationError("Failed to get directions", {"status": e.response.status_code, "detail": e.response.text})
    except httpx.RequestError as e:
        raise MapOperationError("Network error getting directions", {"error": str(e)})

async def parse_user_query(user_query: str) -> Dict[str, Any]:
    """Parse user input using LLM to determine the intended action"""
    try:
        # Load prompts
        prompts =  settings.prompts_agent_car

        if "llama" in dict(cores.Settings.llm)["model"]:
            prompt = prompts["map"]["ParseUserInput"]["dev"]
        else:
            prompt = prompts["map"]["ParseUserInput"]["dev"]  # Default to dev for now

        # Create prompt template
        prompt_template = messages.PromptTemplate(prompt)
        
        # Get examples from prompts
        examples = prompts["map"]["ParseUserInput"]["examples"]
        examples = await utils_llm.convert_examples_to_string(examples)
        
        # Format prompt with examples
        msg = messages.ChatMessage(
            role="user",
            content=prompt_template.format(
                user_query=user_query,
                examples=examples
            )
        )

        # Get LLM response
        result = await cores.Settings.llm.achat([msg])
        parsed = await utils_llm.parse_json(result.message.content)
        
        logger.info(f"Parsed user query: {parsed}")
        return parsed
            
    except Exception as e:
        logger.exception(f"Error parsing user query: {str(e)}")
        raise

async def do_map_operation(
    action: MapAction,
    action_data: Union[SearchAction, ConfirmPlaceAction, GetDirectionsAction]
) -> MapOperationResponse:
    """
    Execute the map operation based on parsed LLM output.
    
    Args:
        action: Type of operation to perform
        action_data: Dataclass containing operation-specific parameters
    
    Returns:
        MapOperationResponse containing operation results
    """
    try:
        if action == MapAction.SEARCH:
            assert isinstance(action_data, SearchAction)
            places = await search(action_data.query)
            return MapOperationResponse(
                success=True,
                action=action,
                data={"places": places}
            )

        elif action == MapAction.CONFIRM_PLACE:
            assert isinstance(action_data, ConfirmPlaceAction)
            places = await search(action_data.search_query)
            place = await get_place_by_name(places, action_data.confirm_query)
            
            if not place:
                return MapOperationResponse(
                    success=False,
                    action=action,
                    error=f"No match found for: {action_data.confirm_query}"
                )
            
            place_details = await retrieve_place_details(place)
            return MapOperationResponse(
                success=True,
                action=action,
                data={"place": place_details}
            )

        elif action == MapAction.GET_DIRECTIONS:
            assert isinstance(action_data, GetDirectionsAction)
            directions = await get_directions_to_place(action_data.place_details)
            return MapOperationResponse(
                success=True,
                action=action,
                data={"directions": directions}
            )

        else:
            return MapOperationResponse(
                success=False,
                action=action,
                error=f"Unknown action: {action}"
            )

    except MapOperationError as e:
        return MapOperationResponse(
            success=False,
            action=action,
            error=e.message,
            details=e.details
        )
    except Exception as e:
        return MapOperationResponse(
            success=False,
            action=action,
            error=str(e)
        )

async def process_user_query(user_query: str) -> Tuple[Dict[str, Any], MapOperationResponse]:
    """
    Process user query and execute appropriate map operations with Redis caching.
    
    This function handles:
    1. Parsing user query using LLM
    2. Executing search or confirm place operations
    3. Caching search results and directions in Redis using consistent keys
    4. Getting directions for confirmed places
    
    Both places and directions use single, consistent Redis keys throughout the app:
    - Places cache key: f"{REDIS_KEY_PREFIX_PLACES}query"
    - Directions cache key: f"{REDIS_KEY_PREFIX_DIRECTIONS}query"
    """
    try:
        # Parse query using LLM to determine action
        parsed = await parse_user_query(user_query)
        action = MapAction(parsed.get("action"))
        
        # Use consistent Redis keys
        places_redis_key = f"{REDIS_KEY_PREFIX_PLACES}"
        directions_redis_key = f"{REDIS_KEY_PREFIX_DIRECTIONS}"
        
        if action == MapAction.SEARCH:
            # Handle search operation
            action_data = SearchAction(query=parsed["query"])
            
            # Execute search
            result = await do_map_operation(action, action_data)
            
            # Cache successful search results in Redis
            if result.success and result.data and 'places' in result.data:
                try:
                    # Store results with consistent key
                    client_redis.setex(
                        places_redis_key,
                        REDIS_TTL_PLACES,
                        json.dumps(result.data["places"])
                    )
                    logger.info("Stored search results in Redis with standard key")
                except Exception as e:
                    logger.error(f"Failed to store search results in Redis: {str(e)}")
            
            return parsed, result

        elif action == MapAction.CONFIRM_PLACE:
            # Handle confirm place operation
            action_data = ConfirmPlaceAction(
                search_query=parsed["search_query"],
                confirm_query=parsed["confirm_query"]
            )
            
            # Try to get cached search results using consistent key
            places = None
            try:
                cached_data = client_redis.get(places_redis_key)
                if cached_data:
                    places = json.loads(cached_data)
                    logger.info("Retrieved places from Redis cache using standard key")
            except Exception as e:
                logger.error(f"Failed to get places from Redis: {str(e)}")
            
            # Fallback to new search if cache miss
            if places is None:
                places = await search(action_data.search_query)
            
            # Find specific place from results
            place = await get_place_by_name(places, action_data.confirm_query)
            print(place)
            if not place:
                return parsed, MapOperationResponse(
                    success=False,
                    action=action,
                    error=f"No match found for: {action_data.confirm_query}"
                )
            
            # Get detailed place information and calculate route
            place_details = await retrieve_place_details(place)
            directions_data = GetDirectionsAction(
                place_details=place_details
            )
            directions_result = await do_map_operation(
                MapAction.GET_DIRECTIONS,
                directions_data
            )
            
            # Extract route information
            route = directions_result.data["directions"]["routes"][0]
            
            # Store directions in Redis with consistent key
            try:
                client_redis.setex(
                    directions_redis_key,
                    REDIS_TTL_DIRECTIONS,
                    json.dumps(directions_result.data["directions"])
                )
                logger.info("Stored directions in Redis with standard key")
            except Exception as e:
                logger.error(f"Failed to store directions in Redis: {str(e)}")
            
            # Prepare response data
            response_data = {
                "place": place_details,
                "duration": route["duration"],  # in seconds
                "distance": route["distance"]   # in meters
            }
            
            # Include full directions in debug mode
            if IS_DEBUG:
                response_data["directions"] = directions_result.data["directions"]
            
            return parsed, MapOperationResponse(
                success=True,
                action=action,
                data=response_data
            )
        
        else:
            raise ValueError(f"Unknown action type: {action}")
            
    except Exception as e:
        logger.exception(f"Error processing user query: {str(e)}")
        raise
        
# Example usage:
"""
import asyncio

async def main():
    # Example 1: Search for places
    search_result = await process_user_query("Tìm quán cháo vịt xung quanh")
    print("Search result:", search_result)

    # Example 2: Confirm specific place
    confirm_result = await process_user_query("Chỉ đường đến Quán Ăn Cháo Gỏi Vịt Lái Thiêu")
    print("Confirm result:", confirm_result)

if __name__ == "__main__":
    asyncio.run(main())
"""
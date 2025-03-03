import packages

from context.utils import typer as t
from context.infra.clients import logger, client_redis

from toolkit.utils import utils
from toolkit.utils.utils import rp_print
from toolkit.utils.llm import main as utils_llm

import context.instances as inst

from enum import Enum
from rapidfuzz import fuzz, process

from toolkit.llm.langchain.models import prompts as prompts_lc
from services.llm.agents.vehicle.context import prompts_agent_navigation
#*------------------------------------------------------------------------------
from services.navigation.mapbox import (
REDIS_KEY_PREFIX_DIRECTIONS, REDIS_KEY_PREFIX_PLACES, 
REDIS_TTL_DIRECTIONS, REDIS_TTL_PLACES
)

from context.infra.services_info import URL_SVC_MAPBOX
#*==============================================================================

class NavigationAction(str, Enum):
    SEARCH = "search"
    CONFIRM_PLACE = "confirm_place"
    GET_DIRECTIONS = "get_directions"

class NavigationOperationError(Exception):
    def __init__(self, message: str, details: t.Optional[t.Dict] = None):
        self.message = message
        self.details = details
        super().__init__(self.message)

class ToolNavigation:
    def __init__(self):
        self.redis_client = client_redis
        self.places_redis_key = REDIS_KEY_PREFIX_PLACES
        self.directions_redis_key = REDIS_KEY_PREFIX_DIRECTIONS
        self.is_debug = utils.os.getenv("IN_PROD") is None

    @utils.print_async_function_name
    async def _search(self, query: str) -> t.List[t.Dict[str, t.Any]]:
        """Search for places and return a simplified list of results."""
        try:
            async with utils.httpx.AsyncClient() as client:
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
                
        except utils.httpx.HTTPStatusError as e:
            raise NavigationOperationError("Search request failed", {"status": e.response.status_code, "detail": e.response.text})
        except utils.httpx.RequestError as e:
            raise NavigationOperationError("Network error during search", {"error": str(e)})

    @utils.print_async_function_name
    async def _get_place_by_name(
        self, 
        places: t.List[t.Dict[str, t.Any]], 
        name: str, 
        threshold: int = 50
    ) -> t.Optional[t.Dict[str, t.Any]]:
        """Find a place from the search results by name using fuzzy matching."""
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

    @utils.print_async_function_name
    async def _retrieve_place_details(self, place: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
        """Get detailed information about a place using its Mapbox ID."""
        try:
            async with utils.httpx.AsyncClient() as client:
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
                
        except utils.httpx.HTTPStatusError as e:
            raise NavigationOperationError("Failed to retrieve place details", 
                                {"status": e.response.status_code, "detail": e.response.text})
        except utils.httpx.RequestError as e:
            raise NavigationOperationError("Network error retrieving place details", {"error": str(e)})

    @utils.print_async_function_name
    async def _get_directions_to_place(self, place_details: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
        """Get directions to a place using its coordinates."""
        try:
            coords = place_details['coordinates']
            async with utils.httpx.AsyncClient() as client:
                response = await client.get(
                    f"{URL_SVC_MAPBOX}/api/directions/",
                    params={
                        "end_lng": coords['longitude'],
                        "end_lat": coords['latitude']
                    }
                )
                response.raise_for_status()
                return response.json()
                
        except utils.httpx.HTTPStatusError as e:
            raise NavigationOperationError("Failed to get directions", 
                                {"status": e.response.status_code, "detail": e.response.text})
        except utils.httpx.RequestError as e:
            raise NavigationOperationError("Network error getting directions", {"error": str(e)})

    @utils.print_async_function_name
    async def parse_user_query(
        self,
        user_query: str = t.Field(description="User input for map operations")
    ) -> t.Dict[str, t.Any]:
        """Parse user input using LLM to determine the intended action."""
        prompt_tpl = prompts_lc.PromptTemplate.from_template(prompts_agent_navigation["parse_query"]["prompt"])

        prompt_examples = await utils_llm.convert_examples_to_string(
            prompts_agent_navigation["parse_query"]["examples"]
        )
        
        prompt = await prompt_tpl.aformat(
            examples = prompt_examples,
            user_query = user_query,
        )

        result = await inst.llm_main.ainvoke(prompt)
        result = result.content
        result = await utils_llm.parse_json(result)

        logger.info(f"Parsed user query result: {result}")

        return result
                
    @utils.print_async_function_name
    async def execute(self, user_query: str) -> t.Dict[str, t.Any]:
        """Execute map operations based on the parsed user input."""
        try:
            # Parse query using LLM to determine action
            parsed = await self.parse_user_query(user_query)
            action = NavigationAction(parsed.get("action"))
            
            if action == NavigationAction.SEARCH:
                # Handle search operation
                places = await self._search(parsed["query"])
                
                # Cache successful search results in Redis
                try:
                    self.redis_client.setex(
                        self.places_redis_key,
                        REDIS_TTL_PLACES,
                        utils.json.dumps(places)
                    )
                    logger.info("Stored search results in Redis")
                except Exception as e:
                    logger.error(f"Failed to store search results in Redis: {str(e)}")
                
                places_formatted = [(place["name"], place["place_formatted"]) for place in places]
                
                return {
                    "success": True,
                    "action": action.value,
                    "data": {"places": places_formatted}
                }

            elif action == NavigationAction.CONFIRM_PLACE:
                # Try to get cached search results
                places = None
                try:
                    cached_data = self.redis_client.get(self.places_redis_key)
                    if cached_data:
                        places = utils.json.loads(cached_data)
                        logger.info("Retrieved places from Redis cache")
                except Exception as e:
                    logger.error(f"Failed to get places from Redis: {str(e)}")
                
                # Fallback to new search if cache miss
                if places is None:
                    places = await self._search(parsed["search_query"])
                
                # Find specific place from results
                place = await self._get_place_by_name(places, parsed["confirm_query"])
                if not place:
                    return {
                        "success": False,
                        "action": action,
                        "error": f"No match found for: {parsed['confirm_query']}"
                    }
                
                # Get detailed place information and calculate route
                place_details = await self._retrieve_place_details(place)
                directions = await self._get_directions_to_place(place_details)
                
                # Extract route information
                route = directions["routes"][0]
                
                # Store directions in Redis
                try:
                    self.redis_client.setex(
                        self.directions_redis_key,
                        REDIS_TTL_DIRECTIONS,
                        utils.json.dumps(directions)
                    )
                    logger.info("Stored directions in Redis")
                except Exception as e:
                    logger.error(f"Failed to store directions in Redis: {str(e)}")
                
                # Prepare response data
                response_data = {
                    "place": place_details,
                    "duration": route["duration"],  # in seconds
                    "distance": route["distance"]   # in meters
                }
                
                # Include full directions in debug mode
                if self.is_debug:
                    response_data["directions"] = directions
                
                """
                response_data["place"]["name]
                response_data["duration]
                response_data["distance"]
                """
                response_data = {
                    "place": place_details["name"],
                    "duration": route["duration"],  # in seconds
                    "distance": route["distance"]   # in meters
                }
                
                return {
                    "success": True,
                    "action": action.value,
                    "data": response_data
                }
            
            else:
                return {
                    "success": False,
                    "action": action,
                    "error": f"Unknown action type: {action}"
                }
                
        except Exception as e:
            logger.exception(f"Error processing user query: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

#*==============================================================================
tool_navigation = ToolNavigation()
#*==============================================================================
# tests = [
# 	"Tìm quán cháo vịt quanh đây",
# 	"Tìm quán trà sữa quanh đây",
#     "Find neardy HighLand Coffee",
#     "Give direction to Le Quy Don HighLand coffe",
# ]
# result = await tool_navigation.execute(tests[2])
# rp_print(result)

import packages

from context.utils import typer as t
from context.infra.clients import logger, client_redis
from enum import Enum

from toolkit.utils import utils
from toolkit.utils.utils import rp_print
from toolkit.utils.llm import main as utils_llm

import context.instances as inst

from toolkit.llm.langchain.models import prompts as prompts_lc
from services.llm.agents.vehicle.context import prompts_agent_music

from context.infra.services_info import URL_SVC_MUSIC
#*==============================================================================

class MusicAction(str, Enum):
    SEARCH = "search"
    SEARCH_ADD_TO_PLAYLIST = "search_add_to_playlist"
    SEE_PLAYLIST = "see_playlist"
    PLAY_PLAYLIST = "play_playlist"
    DELETE_PLAYLIST = "delete_playlist"
    STOP = "stop"
    CONTINUE = "continue"

class MusicOperationError(Exception):
    def __init__(self, message: str, details: t.Optional[t.Dict] = None):
        self.message = message
        self.details = details
        super().__init__(self.message)

class ToolMusic:
    def __init__(self):
        self.is_debug = utils.os.getenv("IN_PROD") is None
        self.redis_client = client_redis
        self.redis_namespace = "music"
        self.current_video_key = f"{self.redis_namespace}:current_video"
        self.playing_status_key = f"{self.redis_namespace}:playing_status"
        self.continue_play_key = f"{self.redis_namespace}:continue_play"

    @utils.print_async_function_name
    async def _search_music(self, query: str) -> t.Dict[str, t.Any]:
        """Search for music based on keyword"""
        try:
            # Use a longer timeout for potentially slow services
            async with utils.httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{URL_SVC_MUSIC}/search",
                    params={"query": query, "autoplay": True, "mode": "llm"}
                )
                response.raise_for_status()
                search_result = response.json()
                
                # Store current video in Redis if most_viewed_id is available
                most_viewed_id = search_result.get("most_viewed_id")
                if most_viewed_id:
                    # Store in Redis
                    try:
                        track_title = next(
                            (r.get("title") for r in search_result.get("results", []) 
                            if r.get("id") == most_viewed_id), 
                            "Unknown Track"
                        )
                        
                        # Store video information
                        self.redis_client.setex(
                            self.current_video_key,
                            3600,  # 1 hour expiration
                            utils.json.dumps({
                                'video_id': most_viewed_id,
                                'query': query,
                                'title': track_title
                            })
                        )
                        
                        # Set playing status to true - this explicitly starts playback
                        self.redis_client.setex(
                            self.playing_status_key,
                            3600,  # 1 hour expiration
                            "true"
                        )
                        
                        # Reset continue play flag if it exists
                        self.redis_client.delete(self.continue_play_key)
                        
                        logger.info(f"Stored current video in Redis: {track_title} (ID: {most_viewed_id}) and set playing status to true")
                    except Exception as e:
                        logger.error(f"Failed to store video in Redis: {str(e)}")
                
                return search_result
                
        except utils.httpx.ReadTimeout:
            logger.error(f"Timeout connecting to music service for query: {query}")
            # Return a graceful fallback response
            return {
                "results": [],
                "most_viewed_id": None,
                "error": "Music service connection timeout"
            }
        except utils.httpx.HTTPStatusError as e:
            logger.error(f"Search request failed: {str(e)}")
            raise MusicOperationError("Search request failed", {"status": e.response.status_code, "detail": e.response.text})
        except utils.httpx.RequestError as e:
            logger.error(f"Network error during search: {str(e)}")
            raise MusicOperationError("Network error during search", {"error": str(e)})

    @utils.print_async_function_name
    async def _search_add_to_playlist(self, query: str, playlist_name: str) -> t.Dict[str, t.Any]:
        """Search for music and add to a playlist"""
        try:
            if not query:
                return {
                    "success": False,
                    "message": "No search query provided"
                }
                
            if not playlist_name:
                playlist_name = "My Playlist"  # Default playlist name
                
            logger.info(f"Adding track '{query}' to playlist '{playlist_name}'")
            
            # First check if playlist exists, create if not
            playlist_exists = await self._ensure_playlist_exists(playlist_name)
            if not playlist_exists:
                return {
                    "success": False,
                    "message": f"Failed to create or verify playlist '{playlist_name}'"
                }
            
            # Search for the track
            try:
                search_result = await self._search_music(query)
                
                # Check if there was an error in the search
                if search_result.get("error"):
                    return {
                        "success": False,
                        "message": f"Search failed: {search_result.get('error')}"
                    }
                    
                # Get most viewed video ID
                most_viewed_id = search_result.get("most_viewed_id")
                if not most_viewed_id:
                    return {
                        "success": False,
                        "message": "No suitable tracks found"
                    }
                    
                # Find the track in results
                results = search_result.get("results", [])
                track = next((r for r in results if r.get("id") == most_viewed_id), None)
                
                if not track:
                    return {
                        "success": False,
                        "message": "Track information not found in results"
                    }
                    
                # Add to playlist using a dedicated POST request
                async with utils.httpx.AsyncClient(timeout=30.0) as client:
                    action_response = await client.post(
                        f"{URL_SVC_MUSIC}/playlist-action",
                        json={
                            "action": "add",
                            "playlist_name": playlist_name,
                            "track_info": track
                        }
                    )
                    action_response.raise_for_status()
                    
                return {
                    "success": True,
                    "added_track": track,
                    "playlist": playlist_name
                }
                
            except Exception as e:
                logger.error(f"Error in search or adding to playlist: {str(e)}")
                return {
                    "success": False,
                    "message": f"Error adding track to playlist: {str(e)}"
                }
                
        except Exception as e:
            logger.error(f"Error in _search_add_to_playlist: {str(e)}")
            return {
                "success": False,
                "message": f"Failed to add track to playlist: {str(e)}"
            }

    @utils.print_async_function_name
    async def _ensure_playlist_exists(self, playlist_name: str) -> bool:
        """Check if playlist exists, create if not"""
        try:
            logger.info(f"Checking if playlist exists: {playlist_name}")
            # Try to get the playlist first
            async with utils.httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(f"{URL_SVC_MUSIC}/playlists/{playlist_name}")
                
                # If playlist exists
                if response.status_code == 200:
                    logger.info(f"Playlist '{playlist_name}' exists")
                    return True
                    
                # If playlist doesn't exist (404), create it
                if response.status_code == 404:
                    logger.info(f"Playlist '{playlist_name}' not found, creating...")
                    create_response = await client.post(
                        f"{URL_SVC_MUSIC}/playlists",
                        json={"name": playlist_name, "description": f"Playlist created for {playlist_name}"}
                    )
                    create_response.raise_for_status()
                    logger.info(f"Playlist '{playlist_name}' created successfully")
                    return True
                    
                # Handle other status codes
                response.raise_for_status()
                return True
                
        except utils.httpx.HTTPStatusError as e:
            logger.error(f"HTTP error checking/creating playlist: {e.response.status_code} - {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Error checking/creating playlist: {str(e)}")
            return False

    @utils.print_async_function_name
    async def _see_playlist(self, playlist_name: str) -> t.Dict[str, t.Any]:
        """Get details of a specific playlist"""
        try:
            async with utils.httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(f"{URL_SVC_MUSIC}/playlists/{playlist_name}")
                response.raise_for_status()
                return response.json()
                
        except utils.httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return {
                    "success": False,
                    "message": f"Playlist '{playlist_name}' not found"
                }
            raise MusicOperationError("Failed to get playlist", {"status": e.response.status_code, "detail": e.response.text})
        except utils.httpx.RequestError as e:
            raise MusicOperationError("Network error getting playlist", {"error": str(e)})

    @utils.print_async_function_name
    async def _get_all_playlists(self) -> t.Dict[str, t.Any]:
        """Get all playlists"""
        try:
            async with utils.httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(f"{URL_SVC_MUSIC}/playlists")
                response.raise_for_status()
                return response.json()
                
        except utils.httpx.HTTPStatusError as e:
            raise MusicOperationError("Failed to get playlists", {"status": e.response.status_code, "detail": e.response.text})
        except utils.httpx.RequestError as e:
            raise MusicOperationError("Network error getting playlists", {"error": str(e)})

    @utils.print_async_function_name
    async def _play_playlist(self, playlist_name: str) -> t.Dict[str, t.Any]:
        """Play a track from a playlist"""
        try:
            # Get the playlist
            playlist_data = await self._see_playlist(playlist_name)
            
            if not playlist_data.get("success", True):  # If success key exists and is False
                return playlist_data
                
            # Check if playlist has tracks
            tracks = playlist_data.get("tracks", [])
            if not tracks:
                return {
                    "success": False,
                    "message": f"Playlist '{playlist_name}' is empty"
                }
                
            # Get the first track's ID
            first_track = tracks[0]
            track_id = first_track.get("id")
            
            if not track_id:
                return {
                    "success": False,
                    "message": "Invalid track data in playlist"
                }
                
            # Store in Redis
            try:
                self.redis_client.setex(
                    self.current_video_key,
                    3600,  # 1 hour expiration
                    utils.json.dumps({
                        'video_id': track_id,
                        'query': first_track.get("title", "Unknown Track"),
                        'playlist': playlist_name,
                        'title': first_track.get("title", "Unknown Track")
                    })
                )
                
                # Set playing status to true
                self.redis_client.setex(
                    self.playing_status_key,
                    3600,  # 1 hour expiration
                    "true"
                )
                
                # Reset continue play flag if it exists
                self.redis_client.delete(self.continue_play_key)
                
                logger.info(f"Stored playlist track in Redis: {first_track.get('title')} (ID: {track_id}) and set playing status to true")
            except Exception as e:
                logger.error(f"Failed to store playlist track in Redis: {str(e)}")
                
            # Play the track (we don't actually stream it here, just return the track info)
            return {
                "success": True,
                "action": "play_playlist",
                "playlist": playlist_name,
                "selected_track": first_track.get("title", "Unknown Track"),
                "track_info": first_track
            }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to play playlist: {str(e)}"
            }

    @utils.print_async_function_name
    async def _delete_playlist(self, playlist_name: str) -> t.Dict[str, t.Any]:
        """Delete a playlist"""
        try:
            async with utils.httpx.AsyncClient(timeout=30.0) as client:
                response = await client.delete(f"{URL_SVC_MUSIC}/playlists/{playlist_name}")
                response.raise_for_status()
                return {
                    "success": True,
                    "message": f"Playlist '{playlist_name}' deleted successfully"
                }
                
        except utils.httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return {
                    "success": False,
                    "message": f"Playlist '{playlist_name}' not found"
                }
            raise MusicOperationError("Failed to delete playlist", {"status": e.response.status_code, "detail": e.response.text})
        except utils.httpx.RequestError as e:
            raise MusicOperationError("Network error deleting playlist", {"error": str(e)})

    @utils.print_async_function_name
    async def _stop_music(self) -> t.Dict[str, t.Any]:
        """Stop the currently playing music and update Redis"""
        try:
            # Get current track info
            current_track = await self.get_current_track()
            
            if not current_track:
                return {
                    "success": False,
                    "message": "No music is currently playing"
                }
                
            # Set playing status to false
            try:
                self.redis_client.setex(
                    self.playing_status_key,
                    3600,  # 1 hour expiration
                    "false"
                )
                
                # Remove any continue play flag
                self.redis_client.delete(self.continue_play_key)
                
                logger.info(f"Set playing status to false for track: {current_track.get('title', current_track.get('query', 'Unknown'))}")
                
                return {
                    "success": True,
                    "stopped_track": current_track.get("title", current_track.get("query", "Unknown Track"))
                }
            except Exception as e:
                logger.error(f"Failed to update playing status in Redis: {str(e)}")
                return {
                    "success": False,
                    "message": f"Failed to stop music: {str(e)}"
                }
                
        except Exception as e:
            logger.error(f"Error stopping music: {str(e)}")
            return {
                "success": False,
                "message": f"Error stopping music: {str(e)}"
            }
    
    @utils.print_async_function_name
    async def _continue_music(self) -> t.Dict[str, t.Any]:
        """Continue playing previously stopped music and update Redis"""
        try:
            # Get current track info
            current_track = await self.get_current_track()
            
            if not current_track:
                return {
                    "success": False,
                    "message": "No music available to continue playing"
                }
                
            # Check if music is already playing - handle different value types
            playing_status = self.redis_client.get(self.playing_status_key)
            if playing_status:
                # Handle different types of values
                is_playing = False
                if isinstance(playing_status, bytes):
                    is_playing = playing_status.decode('utf-8').lower() == "true"
                elif isinstance(playing_status, str):
                    is_playing = playing_status.lower() == "true"
                elif isinstance(playing_status, bool):
                    is_playing = playing_status
                else:
                    is_playing = str(playing_status).lower() == "true"
                    
                if is_playing:
                    return {
                        "success": True,
                        "message": "Music is already playing",
                        "continued_track": current_track.get("title", current_track.get("query", "Unknown Track"))
                    }
            
            # Set playing status to true and set continue flag
            try:
                # Set playing status to true
                self.redis_client.setex(
                    self.playing_status_key,
                    3600,  # 1 hour expiration
                    "true"
                )
                
                # Set continue play flag to true
                self.redis_client.setex(
                    self.continue_play_key,
                    3600,  # 1 hour expiration
                    "true"
                )
                
                logger.info(f"Set continue play to true for track: {current_track.get('title', current_track.get('query', 'Unknown'))}")
                
                return {
                    "success": True,
                    "continued_track": current_track.get("title", current_track.get("query", "Unknown Track"))
                }
            except Exception as e:
                logger.error(f"Failed to update playing status in Redis: {str(e)}")
                return {
                    "success": False,
                    "message": f"Failed to continue music: {str(e)}"
                }
                    
        except Exception as e:
            logger.error(f"Error continuing music: {str(e)}")
            return {
                "success": False,
                "message": f"Error continuing music: {str(e)}"
            }

    @utils.print_async_function_name
    async def is_music_playing(self) -> bool:
        """Check if music is currently playing"""
        try:
            playing_status = self.redis_client.get(self.playing_status_key)
            if playing_status:
                return playing_status.decode('utf-8').lower() == "true"
            # Set default to false if key doesn't exist
            self.redis_client.setex(
                self.playing_status_key,
                3600,  # 1 hour expiration
                "false"
            )
            return False
        except Exception as e:
            logger.error(f"Error checking playing status: {str(e)}")
            return False

    @utils.print_async_function_name
    async def get_current_track(self) -> t.Optional[t.Dict[str, t.Any]]:
        """Get the currently playing track from Redis"""
        try:
            current_video = self.redis_client.get(self.current_video_key)
            if current_video:
                return utils.json.loads(current_video)
            return None
        except Exception as e:
            logger.error(f"Error getting current track from Redis: {str(e)}")
            return None

    @utils.print_async_function_name
    async def parse_user_query(
        self,
        user_query: str = t.Field(description="User input for music operations")
    ) -> t.Dict[str, t.Any]:
        """Parse user input using LLM to determine the intended action."""
        prompt_tpl = prompts_lc.PromptTemplate.from_template(prompts_agent_music["parse_query"]["prompt"])

        prompt_examples = await utils_llm.convert_examples_to_string(
            prompts_agent_music["parse_query"]["examples"]
        )
        
        prompt = await prompt_tpl.aformat(
            examples=prompt_examples,
            user_query=user_query,
        )

        result = await inst.llm_main.ainvoke(prompt)
        result = result.content
        result = await utils_llm.parse_json(result)

        logger.info(f"Parsed music query result: {result}")

        return result
                
    @utils.print_async_function_name
    async def execute(self, user_query: str) -> t.Dict[str, t.Any]:
        """Execute music operations based on the parsed user input."""
        try:
            # Parse query using LLM to determine action
            parsed = await self.parse_user_query(user_query)
            action = MusicAction(parsed.get("action", "search"))
            
            if action == MusicAction.SEARCH:
                # Handle search operation
                search_result = await self._search_music(parsed.get("query", user_query))
                
                # Check if there was an error in the search
                if search_result.get("error"):
                    return {
                        "success": False,
                        "action": action.value,
                        "error": search_result.get("error"),
                        "message": "Unable to play music at this time."
                    }
                
                # Format the response
                return {
                    "success": True,
                    "action": action.value,
                    "query": parsed.get("query", user_query),
                    "data": {
                        "selected_track": next(
                            (r.get("title") for r in search_result.get("results", []) 
                             if r.get("id") == search_result.get("most_viewed_id")), 
                            "Unknown Track"
                        )
                    }
                }
                
            elif action == MusicAction.SEARCH_ADD_TO_PLAYLIST:
                # Handle search and add to playlist operation
                query = parsed.get("query", "")
                playlist = parsed.get("playlist", "My Playlist")
                
                if not query:
                    return {
                        "success": False,
                        "action": action.value,
                        "message": "No search query provided"
                    }
                
                logger.info(f"Adding track to playlist: {query} to {playlist}")
                result = await self._search_add_to_playlist(query, playlist)
                
                if result.get("success"):
                    track_info = result.get("added_track", {})
                    return {
                        "success": True,
                        "action": action.value,
                        "query": query,
                        "playlist": playlist,
                        "data": {
                            "added_track": track_info.get("title", "Unknown Track")
                        }
                    }
                else:
                    return {
                        "success": False,
                        "action": action.value,
                        "message": result.get("message", "Failed to add track to playlist")
                    }
                    
            elif action == MusicAction.SEE_PLAYLIST:
                # Handle see playlist operation
                playlist_name = parsed.get("playlist", "My Playlist")
                
                if playlist_name.lower() == "all":
                    # Get all playlists
                    playlists_result = await self._get_all_playlists()
                    playlist_names = [p.get("name") for p in playlists_result.get("playlists", [])]
                    
                    return {
                        "success": True,
                        "action": "see_all_playlists",
                        "data": {
                            "playlists": playlist_names
                        }
                    }
                else:
                    # Get specific playlist
                    playlist_result = await self._see_playlist(playlist_name)
                    
                    if not playlist_result.get("success", True):  # If success key exists and is False
                        return playlist_result
                        
                    tracks = playlist_result.get("tracks", [])
                    track_titles = [t.get("title") for t in tracks]
                    
                    return {
                        "success": True,
                        "action": action.value,
                        "playlist": playlist_name,
                        "data": {
                            "tracks_count": len(tracks),
                            "tracks": track_titles
                        }
                    }
                    
            elif action == MusicAction.PLAY_PLAYLIST:
                # Handle play playlist operation
                playlist_name = parsed.get("playlist", "My Playlist")
                result = await self._play_playlist(playlist_name)
                
                return result
                
            elif action == MusicAction.DELETE_PLAYLIST:
                # Handle delete playlist operation
                playlist_name = parsed.get("playlist", "")
                
                if not playlist_name:
                    return {
                        "success": False,
                        "action": action.value,
                        "message": "No playlist name provided"
                    }
                    
                result = await self._delete_playlist(playlist_name)
                
                return {
                    "success": result.get("success", False),
                    "action": action.value,
                    "playlist": playlist_name,
                    "message": result.get("message", "")
                }
                
            elif action == MusicAction.STOP:
                # Handle stop playback operation
                result = await self._stop_music()
                
                if result.get("success"):
                    return {
                        "success": True,
                        "action": action.value,
                        "data": {
                            "stopped_track": result.get("stopped_track", "Unknown Track")
                        }
                    }
                else:
                    return {
                        "success": False,
                        "action": action.value,
                        "message": result.get("message", "No music playing or failed to stop")
                    }
                    
            elif action == MusicAction.CONTINUE:
                # Handle continue playback operation
                result = await self._continue_music()
                
                if result.get("success"):
                    return {
                        "success": True,
                        "action": action.value,
                        "data": {
                            "continued_track": result.get("continued_track", "Unknown Track")
                        }
                    }
                else:
                    return {
                        "success": False,
                        "action": action.value,
                        "message": result.get("message", "No music available or failed to continue")
                    }
                    
            else:
                return {
                    "success": False,
                    "action": action.value,
                    "error": f"Unknown action type: {action}"
                }
                
        except Exception as e:
            logger.exception(f"Error processing music query: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

#*==============================================================================
tool_music = ToolMusic()
#*==============================================================================
# tests = [
# 	"Play Shape of You by Ed Sheeran",
# 	"Play Hello by Adele",
# 	"Add Hello by Adele to my favorites playlist",
#   "Show me my favorites playlist",
# 	"Play my workout playlist",
# 	"Delete my old playlist",
#   "Stop the music",
#   "Continue playing"
# ]
# result = await tool_music.execute(tests[-1])
# rp_print(result)
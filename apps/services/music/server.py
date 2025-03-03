import packages
from context.infra.clients import logger
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
import yt_dlp
import json
import asyncio
import aiohttp
import aiofiles
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from context.infra import clients

app = FastAPI(
    title="Music Service",
    description="Music streaming service that allows all external connections"
)

# Configure CORS to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

templates = Jinja2Templates(directory="templates")
thread_pool = ThreadPoolExecutor(max_workers=4)

# Redis namespace for music service
redis_manager = clients.manager_redis.get_namespace("music")
CURRENT_VIDEO_KEY = "current_video"

# Playlist storage
PLAYLISTS_FILE = Path("playlists.json")

# Base config for yt-dlp
YDL_OPTS = {
    'format': 'bestaudio/best',
    'quiet': True,
    'no_warnings': True
}

class SearchResult(BaseModel):
    id: str
    title: str
    duration: str
    thumbnail: str
    view_count: int

class SearchResponse(BaseModel):
    results: List[SearchResult]
    most_viewed_id: Optional[str] = None

class PlayKeywordRequest(BaseModel):
    keyword: str
    playlist: Optional[str] = None

class Playlist(BaseModel):
    name: str
    description: Optional[str] = ""
    tracks: List[Dict[str, Any]] = Field(default_factory=list)

class PlaylistsResponse(BaseModel):
    playlists: List[Dict[str, Any]]

class PlaylistRequest(BaseModel):
    name: str
    description: Optional[str] = ""

class PlaylistActionRequest(BaseModel):
    action: str  # add, remove, clear
    playlist_name: str
    track_id: Optional[str] = None
    track_info: Optional[Dict[str, Any]] = None

async def extract_video_info(url: str, opts: dict) -> dict:
    """Run yt-dlp extraction in a thread pool"""
    loop = asyncio.get_event_loop()
    with yt_dlp.YoutubeDL(opts) as ydl:
        return await loop.run_in_executor(
            thread_pool,
            lambda: ydl.extract_info(url, download=False)
        )

async def get_best_audio_format(video_info: Dict[str, Any]) -> Dict[str, Any]:
    """Extract best audio format from video info"""
    formats = video_info['formats']
    audio_formats = [f for f in formats if f.get('acodec') != 'none' and f.get('vcodec') == 'none']
    if not audio_formats:
        audio_formats = [f for f in formats if f.get('acodec') != 'none']
    
    if not audio_formats:
        raise HTTPException(status_code=404, detail="No audio stream found")
    
    return max(audio_formats, key=lambda f: f.get('abr', 0) if f.get('abr') else 0)

async def stream_audio(url: str):
    """Stream audio content in chunks"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            async for chunk in response.content.iter_chunked(8192):
                yield chunk

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Main UI with tabs for both modes"""
    return templates.TemplateResponse("ui.html", {"request": request})

@app.get("/search")
async def search(query: str, autoplay: bool = False, mode: str = "normal", playlist: Optional[str] = None) -> SearchResponse:
    """Enhanced search endpoint supporting both modes"""
    try:
        search_results = await extract_video_info(
            f"ytsearch5:{query}",
            {**YDL_OPTS, 'extract_flat': False}
        )
        
        if not search_results.get('entries'):
            raise HTTPException(status_code=404, detail="No results found")

        results = []
        most_viewed = {'id': None, 'views': 0}
        
        for entry in search_results['entries']:
            view_count = entry.get('view_count', 0)
            result = SearchResult(
                id=entry['id'],
                title=entry['title'],
                duration=str(entry['duration']),
                thumbnail=entry['thumbnail'],
                view_count=view_count
            )
            results.append(result)
            
            if view_count > most_viewed['views']:
                most_viewed = {'id': entry['id'], 'views': view_count}
        
        # Store most viewed video ID in Redis for LLM mode
        if mode == "llm" and most_viewed['id']:
            await redis_manager.set_value(
                CURRENT_VIDEO_KEY,
                {
                    'video_id': most_viewed['id'],
                    'query': query
                }
            )
            
        # Add most viewed result to the specified playlist if provided
        if playlist and most_viewed['id']:
            most_viewed_result = next((r for r in results if r.id == most_viewed['id']), None)
            if most_viewed_result:
                await add_track_to_playlist(
                    playlist,
                    {
                        'id': most_viewed_result.id,
                        'title': most_viewed_result.title,
                        'thumbnail': most_viewed_result.thumbnail,
                        'duration': most_viewed_result.duration,
                        'view_count': most_viewed_result.view_count
                    }
                )
        
        return SearchResponse(
            results=results,
            most_viewed_id=most_viewed['id'] if autoplay else None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/current-video")
async def get_current_video():
    """Get the currently playing video ID from Redis"""
    try:
        result = await redis_manager.get_value(CURRENT_VIDEO_KEY)
        if not result['success']:
            return JSONResponse({
                "video_id": None,
                "query": None
            })
        return JSONResponse(result['value'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_audio_stream(video_id: str) -> StreamingResponse:
    """Get audio stream for a video ID"""
    try:
        video_info = await extract_video_info(
            f"https://www.youtube.com/watch?v={video_id}",
            YDL_OPTS
        )
        
        if not video_info:
            raise HTTPException(status_code=404, detail="Video not found")
        
        best_audio = await get_best_audio_format(video_info)
        
        return StreamingResponse(
            content=stream_audio(best_audio['url']),
            media_type="audio/mp4",
            headers={"Accept-Ranges": "bytes"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/play/{video_id}")
async def play_audio(video_id: str):
    """Play audio endpoint shared by both modes"""
    return await get_audio_stream(video_id)

@app.post("/play-keyword")
async def play_keyword(request: PlayKeywordRequest):
    """Play by keyword, supporting both modes"""
    try:
        search_results = await extract_video_info(
            f"ytsearch5:{request.keyword}",
            {**YDL_OPTS, 'extract_flat': False}
        )
        
        if not search_results.get('entries'):
            raise HTTPException(status_code=404, detail="No results found")
        
        most_viewed = max(
            search_results['entries'], 
            key=lambda x: x.get('view_count', 0)
        )
        
        # Store in Redis
        await redis_manager.set_value(
            CURRENT_VIDEO_KEY,
            {
                'video_id': most_viewed['id'],
                'query': request.keyword
            }
        )
        
        return await get_audio_stream(most_viewed['id'])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Playlist management helper functions
async def get_all_playlists() -> List[Dict[str, Any]]:
    """Get all playlists from JSON file"""
    try:
        if not PLAYLISTS_FILE.exists():
            return []
            
        async with aiofiles.open(PLAYLISTS_FILE, 'r') as f:
            content = await f.read()
            return json.loads(content) if content else []
    except Exception as e:
        print(f"Error reading playlists: {e}")
        return []

async def save_playlists(playlists: List[Dict[str, Any]]) -> bool:
    """Save playlists to JSON file"""
    try:
        # Create parent directory if it doesn't exist
        PLAYLISTS_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        async with aiofiles.open(PLAYLISTS_FILE, 'w') as f:
            await f.write(json.dumps(playlists, indent=2))
        return True
    except Exception as e:
        print(f"Error saving playlists: {e}")
        return False

async def add_track_to_playlist(playlist_name: str, track_info: Dict[str, Any]) -> bool:
    """Add a track to a playlist"""
    playlists = await get_all_playlists()
    
    # Find the playlist or create a new one
    playlist = next((p for p in playlists if p['name'] == playlist_name), None)
    if not playlist:
        playlist = {'name': playlist_name, 'description': "", 'tracks': []}
        playlists.append(playlist)
    
    # Add track if it doesn't exist
    if not any(t['id'] == track_info['id'] for t in playlist['tracks']):
        playlist['tracks'].append(track_info)
        
    return await save_playlists(playlists)

async def remove_track_from_playlist(playlist_name: str, track_id: str) -> bool:
    """Remove a track from a playlist"""
    playlists = await get_all_playlists()
    
    playlist = next((p for p in playlists if p['name'] == playlist_name), None)
    if not playlist:
        return False
    
    playlist['tracks'] = [t for t in playlist['tracks'] if t['id'] != track_id]
    
    return await save_playlists(playlists)

async def clear_playlist(playlist_name: str) -> bool:
    """Clear all tracks from a playlist"""
    playlists = await get_all_playlists()
    
    playlist = next((p for p in playlists if p['name'] == playlist_name), None)
    if not playlist:
        return False
    
    playlist['tracks'] = []
    
    return await save_playlists(playlists)

# Playlist Management Endpoints
@app.get("/playlists", response_model=PlaylistsResponse)
async def get_playlists():
    """Get all playlists"""
    try:
        playlists = await get_all_playlists()
        return PlaylistsResponse(playlists=playlists)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/playlists")
async def create_playlist(request: PlaylistRequest):
    """Create a new playlist"""
    try:
        playlists = await get_all_playlists()
        
        # Check if playlist already exists
        if any(p['name'] == request.name for p in playlists):
            raise HTTPException(status_code=400, detail=f"Playlist '{request.name}' already exists")
        
        # Create new playlist
        new_playlist = {
            'name': request.name,
            'description': request.description,
            'tracks': []
        }
        
        playlists.append(new_playlist)
        success = await save_playlists(playlists)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to save playlist")
        
        return JSONResponse({"status": "success", "message": f"Playlist '{request.name}' created successfully"})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/playlists/{playlist_name}")
async def delete_playlist(playlist_name: str):
    """Delete a playlist"""
    try:
        playlists = await get_all_playlists()
        
        # Filter out the playlist to delete
        updated_playlists = [p for p in playlists if p['name'] != playlist_name]
        
        if len(updated_playlists) == len(playlists):
            raise HTTPException(status_code=404, detail=f"Playlist '{playlist_name}' not found")
        
        success = await save_playlists(updated_playlists)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete playlist")
        
        return JSONResponse({"status": "success", "message": f"Playlist '{playlist_name}' deleted successfully"})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/playlist-action")
async def playlist_action(request: PlaylistActionRequest):
    """Unified endpoint for playlist actions (add, remove, clear)"""
    try:
        if request.action == "add" and request.track_info:
            success = await add_track_to_playlist(request.playlist_name, request.track_info)
            if success:
                return JSONResponse({"status": "success", "message": f"Track added to '{request.playlist_name}' successfully"})
        
        elif request.action == "remove" and request.track_id:
            success = await remove_track_from_playlist(request.playlist_name, request.track_id)
            if success:
                return JSONResponse({"status": "success", "message": f"Track removed from '{request.playlist_name}' successfully"})
        
        elif request.action == "clear":
            success = await clear_playlist(request.playlist_name)
            if success:
                return JSONResponse({"status": "success", "message": f"Playlist '{request.playlist_name}' cleared successfully"})
        
        else:
            raise HTTPException(status_code=400, detail="Invalid action or missing required parameters")
        
        raise HTTPException(status_code=500, detail="Failed to perform playlist action")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/playlists/{playlist_name}")
async def get_playlist(playlist_name: str):
    """Get a specific playlist by name"""
    try:
        playlists = await get_all_playlists()
        playlist = next((p for p in playlists if p['name'] == playlist_name), None)
        
        if not playlist:
            raise HTTPException(status_code=404, detail=f"Playlist '{playlist_name}' not found")
        
        return JSONResponse(playlist)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/playing-status")
async def get_playing_status():
    """Get the current playing status from Redis"""
    try:
        # Get playing status from Redis - using await for async functions
        playing_status_result = await redis_manager.get_value("playing_status")
        continue_play_result = await redis_manager.get_value("continue_play")
        
        # Default values if keys don't exist
        playing_status = False
        continue_play = False
        
        # Check if operation was successful and extract values
        if playing_status_result["success"]:
            value = playing_status_result["value"]
            # Properly handle the value regardless of type
            if isinstance(value, bool):
                playing_status = value
            elif isinstance(value, str):
                playing_status = value.lower() == "true"
            else:
                # For any other type, convert to string and check
                playing_status = str(value).lower() == "true"
        
        if continue_play_result["success"]:
            value = continue_play_result["value"]
            # Properly handle the value regardless of type
            if isinstance(value, bool):
                continue_play = value
            elif isinstance(value, str):
                continue_play = value.lower() == "true"
            else:
                # For any other type, convert to string and check
                continue_play = str(value).lower() == "true"
        
        return JSONResponse({
            "playing": playing_status,
            "continuePlay": continue_play
        })
    except Exception as e:
        logger.error(f"Error getting playing status: {str(e)}")
        return JSONResponse({
            "playing": False,
            "continuePlay": False
        }, status_code=500)

@app.post("/reset-continue-play")
async def reset_continue_play():
    """Reset the continue play flag in Redis"""
    try:
        # Reset the continue play flag
        result = await redis_manager.set_value("continue_play", "false")
        return JSONResponse({"success": result["success"]})
    except Exception as e:
        logger.error(f"Error resetting continue play flag: {str(e)}")
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)
        
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT_SVC_MUSIC", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
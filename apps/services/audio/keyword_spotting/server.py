"""
Keyword Spotting Service
Provides real-time keyword detection through WebSocket communication.
"""

import os
from collections import deque, defaultdict
import numpy as np
import time
import torch
from typing import Any, Dict, Optional, List, Callable, Set, Union, Tuple
from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from loguru import logger

import packages
from services.bases.server import (
    ServiceConfig,
    FastAPIService,
    EndpointType,
    HTTPMethod,
    WebSocketMessageType,
    WebSocketDataType
)
from services.audio.keyword_spotting.impl.clap_ipa import ClapIPA, ClapIPAConfig
from services.audio.keyword_spotting.utils.vad import VoiceActivityDetector

class AudioConfig:
    """Audio processing configuration"""
    SAMPLE_RATE: int = 16000
    CHUNK_SIZE: int = 1280  # 80ms chunks at 16kHz
    CHUNK_DURATION_MS: float = CHUNK_SIZE / SAMPLE_RATE * 1000
    BUFFER_DURATION: float = 3.0  # Buffer 3 seconds of audio
    MIN_CHUNK_SIZE: int = 1280  # Minimum chunk size for processing

class DetectionConfig:
    """Configuration for detection parameters"""
    THRESHOLD: float = 0.7  # Confidence threshold
    MIN_GAP: float = 0.5  # Minimum confidence gap for multiple detections
    COOLDOWN: float = 0.5  # Seconds between detections of same keyword

class KeywordRequest(BaseModel):
    """Request model for keyword management"""
    keyword: str
    ipa_string: Union[str, List[str]] = Field(..., description="IPA pronunciation(s)")

class ConfigUpdate(BaseModel):
    """Configuration update request"""
    threshold: Optional[float] = Field(None, ge=0.0, le=1.0, description="Detection threshold")
    cooldown: Optional[float] = Field(None, gt=0.0, description="Detection cooldown period")
    min_gap: Optional[float] = Field(None, ge=0.0, le=1.0, description="Minimum confidence gap")
    vad_threshold: Optional[float] = Field(None, gt=0.0, description="VAD energy threshold")
    vad_silence: Optional[float] = Field(None, gt=0.0, description="VAD silence duration")

class KeywordSpottingService(FastAPIService):
    """FastAPI service for keyword spotting through WebSocket"""
    
    def __init__(
        self,
        name: str,
        config: Optional[Union[Dict[str, Any], ServiceConfig]] = None,
        routes: Optional[List[Dict[str, Any]]] = None,
        middleware: Optional[List[Dict[str, Any]]] = None,
        dependencies: Optional[List[Callable]] = None   
    ) -> None:
        """Initialize keyword spotting service"""
        super().__init__(
            name=name, 
            config=config,
            routes=routes,
            middleware=middleware,
            dependencies=dependencies
        )
        
        # Initialize configurations
        self.audio_config = AudioConfig()
        self.detection_config = DetectionConfig()
        
        # Initialize components
        self.spotter = None
        self.vad = VoiceActivityDetector()
        
        # Tracking state
        self.audio_buffer = deque(maxlen=int(self.audio_config.SAMPLE_RATE * 
                                           self.audio_config.BUFFER_DURATION))
        self.last_detections = defaultdict(float)  # Last detection time per keyword
        self.last_global_detection = 0.0  # Global last detection time
        self.last_scores_update = 0.0
        self.score_update_interval = 0.1  # Update scores every 100ms
        
        # Detection statistics
        self.detection_counts = defaultdict(int)
        self.recognition_times = defaultdict(list)

    def _normalize_scores(self, scores: Dict[str, float]) -> Dict[str, float]:
        """Normalize detection scores to [0, 1] range"""
        if not scores:
            return {}
            
        max_score = max(scores.values())
        if max_score <= 0:
            return {k: 0.0 for k in scores}
            
        return {k: float(v / max_score) for k, v in scores.items()}

    def _process_detection_scores(
        self, 
        scores: Dict[str, float]
    ) -> Tuple[List[Dict[str, Any]], Dict[str, float]]:
        """
        Process detection scores to determine valid detections.
        
        Args:
            scores: Dictionary mapping keywords to confidence scores
            
        Returns:
            Tuple of (detections, normalized_scores)
        """
        current_time = time.time()
        detections = []
        
        # Check global cooldown first
        if current_time - self.last_global_detection < self.detection_config.COOLDOWN:
            return [], self._normalize_scores(scores)
        
        # Sort keywords by score
        sorted_scores = sorted(
            scores.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        # Only consider detections above threshold
        candidates = [
            (kw, score) for kw, score in sorted_scores
            if score > self.detection_config.THRESHOLD
        ]
        
        if candidates:
            top_keyword, top_score = candidates[0]
            next_score = candidates[1][1] if len(candidates) > 1 else 0
            
            # Check if top score has sufficient gap from others
            if top_score - next_score >= self.detection_config.MIN_GAP:
                detections.append({
                    "keyword": top_keyword,
                    "confidence": float(top_score),
                    "gap": float(top_score - next_score)
                })
                
                # Update detection statistics
                self.detection_counts[top_keyword] += 1
                self.last_detections[top_keyword] = current_time
                self.last_global_detection = current_time
                
                # Store recognition time if speech start is known
                if self.vad.speaking_started is not None:
                    recognition_time = (current_time - self.vad.speaking_started) * 1000
                    self.recognition_times[top_keyword].append(recognition_time)
        
        # Return detections and normalized scores
        return detections, self._normalize_scores(scores)

    def _setup_app(self) -> FastAPI:
        """Setup FastAPI application"""
        app = super()._setup_app()
        
        # Register REST endpoints
        app.get("/keywords")(self.get_keywords)
        app.post("/keywords")(self.add_keyword)
        app.delete("/keywords/{keyword}")(self.remove_keyword)
        app.put("/config")(self.update_config)
        app.get("/stats")(self.get_statistics)  # New endpoint for statistics
        
        @app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket) -> None:
            await self.accept_websocket(websocket)
            client_id = id(websocket)
            
            await websocket.send_json({
                "type": "log",
                "log_type": "system",
                "message": f"WebSocket connection opened. Client ID: {client_id}"
            })
            
            try:
                if not self.spotter:
                    await websocket.send_json({
                        "type": "log",
                        "log_type": "warning",
                        "message": "Keyword spotter not initialized, creating new instance"
                    })
                    self._initialize_spotter()
                
                while True:
                    try:
                        # Receive audio data
                        audio_data = await websocket.receive_bytes()
                        
                        # Validate chunk size
                        if len(audio_data) < self.audio_config.MIN_CHUNK_SIZE * 2:
                            continue
                        
                        # Convert to numpy array
                        audio_data_np = np.frombuffer(audio_data, dtype=np.int16)
                        audio_float = audio_data_np.astype(np.float32) / 32768.0
                        
                        # Add to buffer
                        self.audio_buffer.extend(audio_float)
                        current_buffer = np.array(list(self.audio_buffer))
                        
                        # Check voice activity
                        is_speaking, speech_start = self.vad.detect(current_buffer)
                        
                        # Only process for keywords if speech is detected
                        if is_speaking and len(current_buffer) >= self.audio_config.SAMPLE_RATE * 0.5:
                            # Get initial scores
                            features = await self.spotter.extract_features(current_buffer)
                            scores = await self.spotter.get_detection_scores(features)
                            max_scores = {k: float(v.max()) for k, v in scores.items()}
                            
                            # Process detections
                            detections, normalized_scores = self._process_detection_scores(max_scores)
                            current_time = time.time()
                            
                            # Send detections if any
                            if detections:
                                for detection in detections:
                                    await websocket.send_json({
                                        "type": "result",
                                        "data": {
                                            "status": "success",
                                            "keyword_detected": True,
                                            "keyword": detection["keyword"],
                                            "confidence": detection["confidence"],
                                            "gap": detection["gap"],
                                            "start_time": speech_start,
                                            "end_time": current_time,
                                            "speech_active": True,
                                            "scores": normalized_scores
                                        }
                                    })
                            
                            # Send score updates periodically
                            elif current_time - self.last_scores_update >= self.score_update_interval:
                                await websocket.send_json({
                                    "type": "result",
                                    "data": {
                                        "status": "success",
                                        "keyword_detected": False,
                                        "scores": normalized_scores,
                                        "speech_active": True
                                    }
                                })
                                self.last_scores_update = current_time
                                
                        else:
                            # Reset scores when not speaking
                            await websocket.send_json({
                                "type": "result",
                                "data": {
                                    "status": "success",
                                    "keyword_detected": False,
                                    "scores": {k: 0.0 for k in self.spotter.get_keywords()},
                                    "speech_active": False
                                }
                            })
                        
                    except WebSocketDisconnect:
                        await websocket.send_json({
                            "type": "log",
                            "log_type": "system",
                            "message": f"WebSocket disconnected. Client ID: {client_id}"
                        })
                        break
                    except Exception as e:
                        await websocket.send_json({
                            "type": "log",
                            "log_type": "error",
                            "message": f"Error processing audio: {str(e)}"
                        })
                        
            except Exception as e:
                await websocket.send_json({
                    "type": "log",
                    "log_type": "error",
                    "message": f"Error in WebSocket connection: {str(e)}"
                })
            finally:
                await self.disconnect_websocket(websocket)
                self.audio_buffer.clear()
        
        return app

    async def get_statistics(self) -> Dict[str, Any]:
        """Get detection statistics endpoint"""
        stats = {
            "global": {
                "total_detections": sum(self.detection_counts.values()),
                "last_detection": self.last_global_detection
            },
            "keywords": {}
        }
        
        for keyword in self.spotter.get_keywords():
            times = self.recognition_times[keyword]
            stats["keywords"][keyword] = {
                "detections": self.detection_counts[keyword],
                "last_detection": self.last_detections[keyword],
                "avg_recognition_time": np.mean(times) if times else 0,
                "min_recognition_time": min(times) if times else 0,
                "max_recognition_time": max(times) if times else 0
            }
        
        return stats

    def _initialize_spotter(self) -> None:
        """Initialize keyword spotter"""
        if self.spotter is None:
            clap_config = ClapIPAConfig(
                sample_rate=self.audio_config.SAMPLE_RATE,
                device="cpu",  # TODO: Make configurable
                detection_threshold=self.detection_config.THRESHOLD
            )
            
            self.spotter = ClapIPA(
                name="CLAP-IPA-KWS",
                model_config=clap_config
            )
            self.spotter.initialize()
            logger.info("Keyword spotter initialized")

    def setup_initial_keywords(self) -> None:
        """Setup initial set of keywords"""
        try:
            keywords = {
                'hello': "həˈloʊ",
                'goodbye': ["ɡʊdˈbaɪ", "ɡʊdˈbaɪ"],
                'computer': "kəmˈpjuːtər"
            }
            
            for keyword, ipa in keywords.items():
                self.spotter.add_keyword(keyword, ipa)
                self.last_detections[keyword] = 0  # Initialize detection timestamps
            
            logger.info(f"Added initial keywords: {list(keywords.keys())}")
            
        except Exception as e:
            logger.error(f"Failed to add initial keywords: {e}")
            raise

    def _initialize_impl(self) -> None:
        """Implementation-specific initialization"""
        super()._initialize_impl()
        self._initialize_spotter()
        self.setup_initial_keywords()

    def _cleanup_resources(self) -> None:
        """Cleanup resources"""
        if self.spotter:
            self.spotter.shutdown()
            self.spotter = None
        
        self.audio_buffer.clear()
        self.last_detections.clear()
        self.detection_counts.clear()
        self.recognition_times.clear()

    async def add_keyword(self, request: KeywordRequest) -> Dict[str, Any]:
        """Add a new keyword endpoint"""
        try:
            if not self.spotter:
                raise HTTPException(status_code=500, detail="Keyword spotter not initialized")
                
            # Clear existing detection timestamp
            self.last_detections[request.keyword] = 0
            self.detection_counts[request.keyword] = 0
            self.recognition_times[request.keyword] = []
            
            self.spotter.add_keyword(request.keyword, request.ipa_string)
            return {
                "status": "success",
                "message": f"Added keyword: {request.keyword}",
                "keyword": request.keyword,
                "ipa": request.ipa_string
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def remove_keyword(self, keyword: str) -> Dict[str, Any]:
        """Remove a keyword endpoint"""
        try:
            if not self.spotter:
                raise HTTPException(status_code=500, detail="Keyword spotter not initialized")
                
            # Clear tracking data
            if keyword in self.last_detections:
                del self.last_detections[keyword]
            if keyword in self.detection_counts:
                del self.detection_counts[keyword]
            if keyword in self.recognition_times:
                del self.recognition_times[keyword]
                
            self.spotter.remove_keyword(keyword)
            return {
                "status": "success",
                "message": f"Removed keyword: {keyword}"
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def get_keywords(self) -> Dict[str, List[str]]:
        """Get active keywords endpoint with IPA pronunciations"""
        if not self.spotter:
            raise HTTPException(status_code=500, detail="Keyword spotter not initialized")
            
        try:
            # Get keywords with their IPA pronunciations from spotter
            return {
                keyword: data['ipa']
                for keyword, data in self.spotter.keyword_data.items()
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def update_config(self, config: ConfigUpdate) -> Dict[str, Any]:
        """Update detection configuration endpoint"""
        try:
            if not self.spotter:
                raise HTTPException(status_code=500, detail="Keyword spotter not initialized")
                
            # Update detection parameters
            if config.threshold is not None:
                self.detection_config.THRESHOLD = config.threshold
                self.spotter.set_threshold(config.threshold)
                logger.info(f"Updated detection threshold: {config.threshold}")
            
            if config.cooldown is not None:
                self.detection_config.COOLDOWN = config.cooldown
                logger.info(f"Updated detection cooldown: {config.cooldown}")
            
            if config.min_gap is not None:
                self.detection_config.MIN_GAP = config.min_gap
                logger.info(f"Updated minimum gap: {config.min_gap}")
                
            if config.vad_threshold is not None:
                self.vad.threshold = config.vad_threshold
                logger.info(f"Updated VAD threshold: {config.vad_threshold}")
                
            if config.vad_silence is not None:
                self.vad.silence_duration = config.vad_silence
                logger.info(f"Updated VAD silence duration: {config.vad_silence}")
            
            # Reset detection state on config change
            self.last_detections.clear()
            self.last_global_detection = 0.0
            
            return {
                "status": "success",
                "message": "Configuration updated",
                "config": {
                    "threshold": self.detection_config.THRESHOLD,
                    "cooldown": self.detection_config.COOLDOWN,
                    "min_gap": self.detection_config.MIN_GAP,
                    "vad_threshold": self.vad.threshold,
                    "vad_silence": self.vad.silence_duration
                }
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    # Service configuration
    config = {
        "port": int(os.getenv("PORT_SVC_KWS", 8000)),
    }
    
    # Create and run service
    service = KeywordSpottingService(
        name="KeywordSpotter",
        config=config
    )
    
    service.run()
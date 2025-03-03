import streamlit as st
import websockets
import asyncio
import json
import time
import pandas as pd
import requests
from typing import Optional
from streamlit_async import async_support
from config import server_config, app_config

class WebSocketManager:
    """Manage WebSocket connection for Streamlit."""
    def __init__(self):
        self.logger = app_config.setup_logging('WebSocketManager')
        self.ws = None
        self.connected = False
        
    async def connect(self) -> bool:
        """Establish WebSocket connection."""
        try:
            uri = f"ws://localhost:{server_config.FASTAPI_PORT}/ws"
            self.ws = await websockets.connect(uri)
            self.connected = True
            self.logger.info("WebSocket connection established")
            return True
        except Exception as e:
            self.logger.error(f"WebSocket connection error: {e}")
            self.connected = False
            return False
            
    async def listen(self) -> Optional[dict]:
        """Listen for WebSocket messages."""
        try:
            if self.ws and self.connected:
                message = await self.ws.recv()
                return json.loads(message)
        except websockets.exceptions.ConnectionClosed:
            self.logger.error("WebSocket connection closed")
            self.connected = False
        except Exception as e:
            self.logger.error(f"WebSocket error: {e}")
            self.connected = False
        return None
        
    async def send_heartbeat(self):
        """Send heartbeat to keep connection alive."""
        try:
            if self.ws and self.connected:
                await self.ws.send('ping')
        except Exception as e:
            self.logger.error(f"Heartbeat error: {e}")
            self.connected = False
            
    async def close(self):
        """Close WebSocket connection."""
        if self.ws:
            await self.ws.close()
            self.connected = False
            self.logger.info("WebSocket connection closed")

class StreamlitUI:
    """Main Streamlit UI manager."""
    def __init__(self):
        self.logger = app_config.setup_logging('StreamlitUI')
        self.ws_manager = WebSocketManager()
        
    def initialize_session_state(self):
        """Initialize Streamlit session state variables."""
        if 'is_awake' not in st.session_state:
            st.session_state.is_awake = False
        if 'ws_connected' not in st.session_state:
            st.session_state.ws_connected = False
        if 'event_history' not in st.session_state:
            st.session_state.event_history = []
            
    def setup_page(self):
        """Configure Streamlit page settings."""
        st.set_page_config(
            page_title="Wake Word Detection",
            page_icon="🎤",
            layout="wide"
        )
        
    @async_support
    async def handle_websocket(self):
        """Handle WebSocket connection and messages."""
        if not st.session_state.ws_connected:
            connected = await self.ws_manager.connect()
            st.session_state.ws_connected = connected
            
        if st.session_state.ws_connected:
            # Send heartbeat
            await self.ws_manager.send_heartbeat()
            
            # Check for messages
            message = await self.ws_manager.listen()
            if message and message.get('event') == 'wake_word':
                st.session_state.is_awake = True
                # Add to event history
                event_time = time.strftime(
                    '%Y-%m-%d %H:%M:%S',
                    time.localtime(message.get('timestamp', time.time()))
                )
                st.session_state.event_history.append({
                    'time': event_time,
                    'status': message.get('status', 'unknown'),
                    'confidence': message.get('confidence', 0.0)
                })
                
    def display_status(self):
        """Display connection and wake word status."""
        col1, col2 = st.columns(2)
        
        with col1:
            status = "🟢 Connected" if st.session_state.ws_connected else "🔴 Disconnected"
            st.write(f"### Connection Status: {status}")
            
        with col2:
            if st.session_state.is_awake:
                st.success("👋 Xin chào! Tôi đang lắng nghe...")
                time.sleep(2)
                st.session_state.is_awake = False
            else:
                st.info("😴 Đang chờ wake word...")
                
    def display_event_history(self):
        """Display wake word event history."""
        st.write("### Event History")
        if st.session_state.event_history:
            df = pd.DataFrame(
                reversed(st.session_state.event_history[-10:])  # Show last 10 events
            )
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.write("No events recorded yet")
            
    def display_metrics(self):
        """Display system metrics."""
        try:
            response = requests.get(
                f"http://localhost:{server_config.FASTAPI_PORT}/health"
            )
            if response.status_code == 200:
                metrics = response.json()
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "System Status",
                        metrics.get('status', 'unknown')
                    )
                    
                with col2:
                    st.metric(
                        "WebSocket Clients",
                        metrics.get('websocket_clients', 0)
                    )
                    
                with col3:
                    st.metric(
                        "Redis Connected",
                        "Yes" if metrics.get('redis_connected', False) else "No"
                    )
        except Exception as e:
            st.error(f"Error fetching metrics: {e}")
            
    def display_config(self):
        """Display system configuration."""
        with st.expander("System Configuration", expanded=False):
            try:
                response = requests.get(
                    f"http://localhost:{server_config.FASTAPI_PORT}/config"
                )
                if response.status_code == 200:
                    config = response.json()
                    st.json(config)
            except Exception as e:
                st.error(f"Error fetching configuration: {e}")
    
    @async_support
    async def run(self):
        """Main UI loop."""
        self.setup_page()
        self.initialize_session_state()
        
        st.title("🎤 Wake Word Detection System")
        
        # Handle WebSocket connection and messages
        await self.handle_websocket()
        
        # Display UI elements
        self.display_status()
        self.display_metrics()
        self.display_event_history()
        self.display_config()
        
        # Auto refresh
        time.sleep(1)
        st.rerun()

def main():
    """Main application entry point."""
    try:
        ui = StreamlitUI()
        ui.run()
    except Exception as e:
        st.error("Application Error")
        st.exception(e)
        app_config.setup_logging('StreamlitApp').error(f"Fatal error: {e}")

if __name__ == "__main__":
    main()
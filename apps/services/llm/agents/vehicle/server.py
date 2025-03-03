import packages
import json
import redis
from typing import Dict, List
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from context.infra import clients
from context.infra.services_info import PORT_APP_VEHICLE
from services.llm.agents.vehicle.manager import agent_main

app = FastAPI()

# Store active WebSocket connections
active_connections: List[WebSocket] = []

async def broadcast_message(message: str):
    """Broadcast message to all connected clients"""
    for connection in active_connections:
        await connection.send_text(message)

@app.get("/agent-status")
async def get_agent_status():
    """Get current agent status from Redis"""
    result = await clients.namespace_redis_llm.get_value(
    "agent"
)
    result = result["value"]["current"]
    return {
        "current": result
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class AgentInput(BaseModel):
    text: str

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            # Keep the connection alive
            await websocket.receive_text()
    except:
        # Remove connection when client disconnects
        active_connections.remove(websocket)

@app.post("/agent")
async def agent_endpoint(input_data: AgentInput):
    result = await agent_main.core.ainvoke(
        input={"messages": [("user", input_data.text)]}, config=agent_main.config,
    )
    # Broadcast the result to all connected WebSocket clients
    await broadcast_message(result["result"])
    return {"response": result["result"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(PORT_APP_VEHICLE))

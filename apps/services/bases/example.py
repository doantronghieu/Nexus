from typing import Dict, Any, Optional, Union, List
from fastapi import WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
import operator
from decimal import Decimal, InvalidOperation
from datetime import datetime
import json

from services.bases.service import BaseService
from services.bases.server import (
    FastAPIService, 
    EndpointType, 
    HTTPMethod,
    WebSocketMessageType,
    WebSocketDataType
)

class CalculationRequest(BaseModel):
    """Pydantic model for calculation requests"""
    operation: str = Field(..., description="Operation to perform")
    x: float = Field(..., description="First operand")
    y: float = Field(..., description="Second operand")

class CalculationResponse(BaseModel):
    """Pydantic model for calculation responses"""
    operation: str
    result: float
    input_values: Dict[str, float]
    timestamp: str

class CalculationHistory(BaseModel):
    """Pydantic model for calculation history"""
    timestamp: str
    operation: str
    input_values: Dict[str, float]
    result: float

class CalculatorService(FastAPIService):
    """Calculator service with HTTP and WebSocket support"""
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None) -> None:
        # Define available operations
        self._operations = {
            'add': operator.add,
            'subtract': operator.sub,
            'multiply': operator.mul,
            'divide': operator.truediv,
            'power': operator.pow,
            'modulo': operator.mod
        }
        
        # Initialize calculation history
        self._history: List[CalculationHistory] = []
        
        super().__init__(name, config)

    async def handle_websocket(self, websocket: WebSocket) -> None:
        """Handle WebSocket connections"""
        await self.accept_websocket(websocket)
        try:
            while True:
                try:
                    # Receive message
                    message = await websocket.receive()
                    
                    if message["type"] == "websocket.disconnect":
                        break
                    
                    if message["type"] == "websocket.receive":
                        if "text" in message:
                            try:
                                # Parse JSON message
                                data = json.loads(message["text"])
                                if data.get("type") == "calculation":
                                    # Handle calculation request
                                    if not all(k in data for k in ["operation", "x", "y"]):
                                        raise ValueError("Missing required fields: operation, x, y")
                                    
                                    result = self._perform_calculation(
                                        data["operation"],
                                        float(data["x"]),
                                        float(data["y"])
                                    )
                                    
                                    response = {
                                        "type": "calculation_result",
                                        "operation": data["operation"],
                                        "result": result,
                                        "input_values": {
                                            "x": float(data["x"]),
                                            "y": float(data["y"])
                                        },
                                        "timestamp": datetime.utcnow().isoformat()
                                    }
                                    
                                    await websocket.send_json(response)
                                    
                                    # Store in history
                                    self._add_to_history(
                                        data["operation"],
                                        response["input_values"],
                                        result
                                    )
                                else:
                                    # Echo other messages back
                                    await websocket.send_json({
                                        "type": "echo",
                                        "data": data,
                                        "timestamp": datetime.utcnow().isoformat()
                                    })
                                
                            except json.JSONDecodeError:
                                await websocket.send_json({
                                    "type": "error",
                                    "message": "Invalid JSON format",
                                    "timestamp": datetime.utcnow().isoformat()
                                })
                            except Exception as e:
                                await websocket.send_json({
                                    "type": "error",
                                    "message": str(e),
                                    "timestamp": datetime.utcnow().isoformat()
                                })
                        
                        elif "bytes" in message:
                            # Handle binary data (files, media streams)
                            try:
                                data_type = self._detect_binary_type(message["bytes"])
                                await websocket.send_json({
                                    "type": "binary_received",
                                    "data_type": data_type.value,
                                    "size": len(message["bytes"]),
                                    "timestamp": datetime.utcnow().isoformat()
                                })
                            except Exception as e:
                                await websocket.send_json({
                                    "type": "error",
                                    "message": f"Error processing binary data: {str(e)}",
                                    "timestamp": datetime.utcnow().isoformat()
                                })
                
                except WebSocketDisconnect:
                    break
                except Exception as e:
                    await websocket.send_json({
                        "type": "error",
                        "message": str(e),
                        "timestamp": datetime.utcnow().isoformat()
                    })
        finally:
            await self.disconnect_websocket(websocket)

    def _perform_calculation(self, operation: str, x: float, y: float) -> float:
        """Perform a calculation operation"""
        if operation not in self._operations:
            raise ValueError(f"Unsupported operation: {operation}")

        try:
            # Convert to Decimal for more precise arithmetic
            dx = Decimal(str(x))
            dy = Decimal(str(y))
            
            # Handle division by zero
            if operation == 'divide' and dy == 0:
                raise ValueError("Division by zero is not allowed")
            
            # Perform calculation
            result = float(self._operations[operation](dx, dy))
            return result
            
        except (InvalidOperation, ValueError) as e:
            raise ValueError(f"Calculation error: {str(e)}")
        except Exception as e:
            raise ValueError(f"Unexpected error: {str(e)}")

    def _add_to_history(self, operation: str, inputs: Dict[str, float], result: float) -> None:
        """Add calculation to history"""
        history_entry = CalculationHistory(
            timestamp=datetime.utcnow().isoformat(),
            operation=operation,
            input_values=inputs,
            result=result
        )
        
        self._history.append(history_entry)
        
        # Maintain maximum history size
        if len(self._history) > self.config.get("max_history", 100):
            self._history.pop(0)

if __name__ == "__main__":
    # Service configuration
    config = {
        "host": "localhost",
        "port": 8000,
        "api_prefix": "/api/v1",
        "cors_origins": ["*"],
        "max_history": 100,
        "websocket_ping_interval": 30,
        "max_message_size": 10 * 1024 * 1024  # 10MB
    }
    
    # Create and run service
    calculator = CalculatorService(
        name="CalculatorAPI",
        config=config
    )
    
    calculator.initialize()
    calculator()
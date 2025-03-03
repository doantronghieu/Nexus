import websockets
import asyncio

async def test():
    uri = "ws://localhost:5000/ws"
    async with websockets.connect(uri) as websocket:
        print("Connected")
        await asyncio.sleep(2)
        print("Done")

asyncio.run(test())
import asyncio
import websockets
import json
import random
from datetime import datetime

async def send_heart_rate():
    uri = "ws://iot_gateway:5000/ws/health"  # Cambia esto al endpoint de tu servidor WS
    async with websockets.connect(uri) as websocket:
        while True:
            data = {
                "id": "sensor-ws-heart-1",
                "heart_rate": random.randint(60, 100),                                                                                "timestamp": datetime.utcnow().isoformat()
            }
           
            print(f'Sent data: id: "{data["id"]}"', flush=True)
            print(f'heart_rate: {data["heart_rate"]}', flush=True)
            print(f'timestamp: "{data["timestamp"]}"', flush=True)

            await websocket.send(json.dumps(data))
            
            response = await websocket.recv()
            print(f'Response: {response}', flush=True)

            await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(send_heart_rate())

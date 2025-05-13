import grpc
from concurrent import futures
import time
import threading
import asyncio
import websockets
from flask import Flask, request
import paho.mqtt.client as mqtt

import sensor_pb2_grpc
from grpc_handler import GRPCSensorService
from websocket_handler import WSSensorService

# === MQTT Client ===
mqtt_client = mqtt.Client()
mqtt_client.connect("mqtt", 1883, 60)  # 'mqtt' es el nombre del contenedor del broker en docker-compose

def publish_to_mqtt(data):
    mqtt_client.publish("sensor/data", str(data))
    print(f"[MQTT] Published: {data}", flush=True)

# === gRPC Server ===
class GRPCSensorServiceWithMQTT(GRPCSensorService):
    def SendData(self, request, context):
        data = {
            "id": request.id,
            "temperature": request.temperature,
            "timestamp": request.timestamp
        }
        print(f"[gRPC] Received: {data}", flush=True)
        publish_to_mqtt(data)
        return super().SendData(request, context)

def start_grpc_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sensor_pb2_grpc.add_SensorServiceServicer_to_server(GRPCSensorServiceWithMQTT(), server)
    server.add_insecure_port('[::]:50051')
    print("[gRPC] Starting server on port 50051...", flush=True)
    server.start()
    return server

# === WebSocket Server ===
async def WSSensorServiceWithMQTT(websocket, path):
    async for message in websocket:
        print(f"[WebSocket] Received: {message}", flush=True)
        publish_to_mqtt(message)

def start_websocket_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    start_server = websockets.serve(WSSensorServiceWithMQTT, "0.0.0.0", 5000)
    print("[WebSocket] Starting server on port 5000...", flush=True)
    loop.run_until_complete(start_server)
    loop.run_forever()

# === REST Server (Flask) ===
app = Flask(__name__)

@app.route('/data', methods=['POST'])
def receive_rest_data():
    data = request.json
    print(f"[REST] Received: {data}", flush=True)
    publish_to_mqtt(data)
    return "REST data received", 200

def start_rest_server():
    print("[REST] Starting Flask server on port 8000...", flush=True)
    app.run(host='0.0.0.0', port=8000)

# === Main ===
if __name__ == '__main__':
    grpc_server = start_grpc_server()

    # Iniciar servidores REST y WebSocket en hilos separados
    rest_thread = threading.Thread(target=start_rest_server, daemon=True)
    rest_thread.start()

    ws_thread = threading.Thread(target=start_websocket_server, daemon=True)
    ws_thread.start()

    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("Shutting down...", flush=True)
        grpc_server.stop(0)
        rest_thread.join()
        ws_thread.join()

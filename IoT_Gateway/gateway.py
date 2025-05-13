import grpc
from concurrent import futures
import time
import threading
import asyncio
import websockets

import sensor_pb2_grpc
from grpc_handler import GRPCSensorService
from websocket_handler import WSSensorService

def start_grpc_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sensor_pb2_grpc.add_SensorServiceServicer_to_server(GRPCSensorService(), server)
    server.add_insecure_port('[::]:50051')
    print("Starting gRPC server on port 50051...", flush=True)
    server.start()
    return server


def start_websocket_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    start_server = websockets.serve(WSSensorService, "0.0.0.0", 5000)
    print("Starting WebSocket server on port 5000...", flush=True)
    loop.run_until_complete(start_server)
    loop.run_forever()


if __name__ == '__main__':
    grpc_server = start_grpc_server()

    ws_thread = threading.Thread(target=start_websocket_server, daemon=True)
    ws_thread.start()
    
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("Shutting down...")
        grpc_server.stop(0)
        ws_thread.join()

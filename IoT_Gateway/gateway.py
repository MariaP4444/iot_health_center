import grpc
from concurrent import futures
import time

import sensor_pb2_grpc
from grpc_handler import SensorService

def start_grpc_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sensor_pb2_grpc.add_SensorServiceServicer_to_server(SensorService(), server)
    server.add_insecure_port('[::]:50051')
    print("Starting gRPC server on port 50051...")
    server.start()
    return server

if __name__ == '__main__':
    grpc_server = start_grpc_server()
 
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("Shutting down...")
        grpc_server.stop(0)


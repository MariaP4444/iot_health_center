import grpc
import time
import random
from datetime import datetime

import sensor_pb2
import sensor_pb2_grpc

def run():
    channel = grpc.insecure_channel('iot_gateway:50051')  # 'gateway' es el nombre del servicio en docker-compose
    stub = sensor_pb2_grpc.SensorServiceStub(channel)
    while True:
            data = sensor_pb2.SensorData(
                id="sensor-grpc-1",
                temperature=round(random.uniform(20.0, 30.0), 2),
                timestamp=datetime.utcnow().isoformat()
            )
            response = stub.SendData(data)
            print(f"Sent data: {data} | Response: {response.message}")
            time.sleep(5)

if __name__ == '__main__':
    run()


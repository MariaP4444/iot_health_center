import sensor_pb2
import sensor_pb2_grpc

class SensorService(sensor_pb2_grpc.SensorServiceServicer):
    def SendData(self, request, context):
        print(f"[gRPC] Received from {request.id}: {request.temperature}°C at {request.timestamp}")
        return sensor_pb2.SensorResponse(message="Data received")

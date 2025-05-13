import requests
import time
import random
from datetime import datetime

GATEWAY_URL = "http://iot_gateway:8000/data"  # Dirección del gateway REST

def run():
    while True:
        data = {
            "id": "sensor-rest-1",
            "blood_pressure": round(random.uniform(80.0, 120.0), 1),  # presión simulada
            "timestamp": datetime.utcnow().isoformat()
        }
        try:
            response = requests.post(GATEWAY_URL, json=data)
            print(f"Sent: {data} | Response: {response.text}", flush=True)
        except Exception as e:
            print("Error sending data:", e)
        time.sleep(5)

if __name__ == '__main__':
    run()

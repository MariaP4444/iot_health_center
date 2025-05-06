# iot_health_center
IoT project for the healthcare sector where simulated sensors send medical data (temperature, heart rate, blood pressure) via gRPC, Rest, and WebSockets. A Gateway publishes data to MQTT, and a subscriber stores it in PostgreSQL, all running in Docker containers orchestrated with Docker Compose.

# iot_health_center
### Descripción del sistema
Este proyecto implementa un sistema de IoT para el sector de salud que recopila datos de sensores médicos simulados, se transmite a través de un Gateway IoT y se almacena en una base de datos PostgreSQL para su analisís. Este sistema hace uso del protocolo MQTT para la comunicación entre el Gateway y el suscriptor.

### Prerrequisitos
- Docker y Docker Compose
### Estructura del Proyecto

```
iot_health_center/
│
├── docker-compose.yml              # Orquestación general
│
├── IoT_Gateway/                    # Gateway central
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── gateway.py
│   ├── grpc_handler.py             # Manejo de peticiones gRPC
│   └── sensor.proto                # Definición del servicio gRPC
│
├── mosquitto/                      # Broker MQTT (Mosquitto)
│   ├── config/mosquitto.conf
│   └── data/mosquitto.db
│
├── MQTT_Subscriber/                # Cliente MQTT que guarda en DB
│   ├── Dockerfile
│   ├── requirements.txt
│   └── subscriber.py
│
├── Sensores/
│   ├── SensorGRPC/                 # Sensor usando gRPC
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── client.py
│   │   └── sensor.proto
│   ├── SensorRest/                 # Sensor usando REST
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── client.py
│
├── DB/
│   └── init.sql                    # Script para crear tablas
│
└── README.md

```
### Ejecución
 Inicia los servicios con Docker Compose:
   ```bash
   docker-compose up --build
   ```

### Componentes del sistema
1. ### Sensores:
    - __SensorGRPC:__ Envía los datos de temperatura corporal mediante  el protocolo gRPC.
    - __SensorRest:__ Envía datos de presión arterial mediante el protocolo REST.
    - __SensorwS:__ Envía datos de ritmo cardíaco mediante el protocolo Websocket.
2. ### IoT_Gateway
  Recibe los datos de los sensores (por gRPC o REST), los procesa y los publica en un topic MQTT (salud/datos) para su posterior almacenamiento. Actúa como puente entre los sensores y el resto del sistema.

3. ### Broker MQTT (Mosquitto)
  Es el intermediario de mensajería. Se encarga de recibir y distribuir los mensajes publicados por el gateway a todos los suscriptores interesados. 

4. ### MQTT Subscriber
  Se suscribe al tópico MQTT donde se publican los datos médicos. Cada mensaje recibido es insertado en la base de datos PostgreSQL para su almacenamiento y análisis posterior.

5. ### Base de Datos (PostgreSQL)
   Almacena toda la información recibida de los sensores, organizada por paciente y con su respectiva marca temporal. Es la base del sistema de almacenamiento para análisis futuros.

  

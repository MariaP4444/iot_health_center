import os
import json
import psycopg2
import paho.mqtt.client as mqtt

# Variables de entorno (configuradas en docker-compose)
DB_HOST = os.getenv('DB_HOST', 'postgres')
DB_NAME = os.getenv('DB_NAME', 'iot_db')
DB_USER = os.getenv('DB_USER', 'user')
DB_PASS = os.getenv('DB_PASS', 'password')
MQTT_BROKER = os.getenv('MQTT_BROKER', 'mqtt')  # Igual que el gateway

# Callback cuando llega un mensaje del broker
def on_message(client, userdata, msg):
    print(f"[MQTT] Mensaje recibido en {msg.topic}: {msg.payload.decode()}", flush=True)
    try:
        # Parsear JSON del mensaje recibido
        payload = msg.payload.decode()
        payload = payload.replace("'", '"')
        data = json.loads(payload)
        id_sensor = data.get('id')
        print("Dataaaaaaaaaa: ", data, flush=True)

        valor = None 
        if (data.get('temperature')):
            valor = data.get('temperature')
        elif (data.get('blood_pressure')):
            valor = data.get('blood_pressure')
        elif (data.get('heart_rate')):
            valor = data.get('heart_rate')

        timestamp = data.get('timestamp')

        # Conectar a la base de datos PostgreSQL
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        
        cursor = conn.cursor()
        # Insertar en la tabla sensores
        cursor.execute(
                "INSERT INTO log_sensores (id_sensor, valor, time) VALUES (%s, %s, to_timestamp(%s, 'YYYY-MM-DD\"T\"HH24:MI:SS.US'))",
            (id_sensor, valor, timestamp)
        )
        
        conn.commit()
        cursor.close()
        conn.close()

        print(f"[DB] Insertado en PostgreSQL: {id_sensor}, {valor}, {timestamp}", flush=True)

    except Exception as e:
        print(f"[ERROR] No se pudo insertar en PostgreSQL: {e}", flush=True)

# Configuración del cliente MQTT
client = mqtt.Client()
client.on_message = on_message

print(f"[MQTT] Conectando a broker {MQTT_BROKER}...", flush=True)

client.connect(MQTT_BROKER, 1883, 60)

client.subscribe("sensor/data")
print("[MQTT] Suscrito a 'sensor/data'", flush=True)

client.loop_forever()

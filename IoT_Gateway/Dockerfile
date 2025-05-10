# Usamos la imagen base de Python
FROM python:3.12-slim-bookworm

# Establecemos el directorio de trabajo
WORKDIR /app

# Instalamos las dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copiamos el archivo requirements.txt y lo usamos para instalar las dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Exponemos los puertos necesarios para gRPC, REST y WebSockets
EXPOSE 50051 5000 8080

# Copiamos el código fuente
COPY . .

# Comando para ejecutar el IoT Gateway
CMD ["python", "gateway.py"]

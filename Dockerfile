FROM python:3.12-slim

# evita output bufferizado (logs inmediatamente)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# directorio de trabajo
WORKDIR /app

# dependencias de sistema para psycopg2
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       gcc \
       libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# copiamos requirements primero (mejor cache)
COPY requirements.txt .

# instalamos dependencias python
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# copiamos el resto del codigo
COPY . .

COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# puerto gRPC (documentacion, no obligatorio)
EXPOSE 50052

# comando por defecto
CMD ["python", "-m", "app.rpc.server"]

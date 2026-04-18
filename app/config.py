import os


DATABASE_URL = os.getenv("DATABASE_URL")
ORDER_SERVICE_PORT = os.getenv("ORDER_SERVICE_PORT")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

if not ORDER_SERVICE_PORT:
    raise RuntimeError("ORDER_SERVICE_PORT is not set")

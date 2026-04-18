#!/usr/bin/env bash
set -e

echo "Waiting for database to be ready..."

until alembic upgrade head; do
  echo "Database not ready yet, retrying in 3 seconds..."
  sleep 3
done

echo "Migrations completed successfully."

echo "Starting service..."
exec "$@"

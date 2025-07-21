#!/bin/sh

# Appliquer les migrations Alembic
echo "Applying database migrations..."
uv run alembic upgrade head

# Démarrer l'API
echo "Starting the API..."
uv run app/main.py --port 80 --host 0.0.0.0
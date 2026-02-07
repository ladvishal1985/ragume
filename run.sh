#!/bin/bash

# Activate virtual environment (only if running locally)
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Set environment variables from .env file (only if running locally)
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Check if running in production (Render) or local
if [ -z "$PORT" ]; then
    echo "Running in LOCAL mode..."
    # Local development - use reload
    python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
else
    echo "Running in PRODUCTION mode on port $PORT..."
    # Production - no reload, optimized for deployment
    python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
fi

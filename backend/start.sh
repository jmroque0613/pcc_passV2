#!/bin/bash

echo "🚀 Starting PCC-PASS Backend Server..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
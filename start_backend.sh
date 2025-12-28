#!/bin/bash
# Backend Start Script

cd "$(dirname "$0")/server"

echo "Starting Backend on port 8000..."
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000

#!/bin/bash

# Metronavix - Quick Start Script (Manual / Non-Docker)

echo "Starting Backend..."
cd server
pip install -r requirements.txt
python3 reset_admin.py  # Ensures admin/admin123 exists
export PYTHONPATH=$PYTHONPATH:.
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

echo "Starting Frontend..."
cd ../client/estatevision-ai---professional-property-video-generator
npm install
npm run dev -- --host --port 3000 &
FRONTEND_PID=$!

echo "------------------------------------------------"
echo "Project is running!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "Login: admin / admin123"
echo "------------------------------------------------"
echo "To share with client, run:"
echo "ngrok http 3000"
echo "ngrok http 8000"
echo "------------------------------------------------"

# Keep script alive
wait $BACKEND_PID $FRONTEND_PID

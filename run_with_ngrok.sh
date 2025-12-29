#!/bin/bash

# Script to run the EstateVision AI application and expose it via ngrok

echo "Setting up EstateVision AI with ngrok..."

# Start the backend in the background
echo "Starting backend..."
cd server
# Skip pip install since requirements may already be installed
python3 reset_admin.py  # Ensures admin/admin123 exists
export PYTHONPATH=$PYTHONPATH:.
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

# Wait a moment for the backend to start
sleep 8

# Start the frontend in the background
echo "Starting frontend..."
cd client/estatevision-ai---professional-property-video-generator
# Skip npm install if dependencies are already there
if [ ! -d "node_modules" ] || [ -z "$(ls -A node_modules)" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi
npx vite --host 0.0.0.0 --port 3000 &
FRONTEND_PID=$!
cd ../..

# Wait a moment for the frontend to start
sleep 8

# Start ngrok tunnels in the background
echo "Starting ngrok tunnels..."

# Expose backend via ngrok
./ngrok http 8000 &
NGROK_BACKEND_PID=$!

# Wait a moment for the first ngrok to start
sleep 5

# Expose frontend via ngrok
./ngrok http 3000 &
NGROK_FRONTEND_PID=$!

echo "------------------------------------------------"
echo "Application is running!"
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo "Backend ngrok PID: $NGROK_BACKEND_PID"
echo "Frontend ngrok PID: $NGROK_FRONTEND_PID"
echo "------------------------------------------------"

# Get ngrok URLs
echo "Waiting for ngrok URLs..."
sleep 10

echo "Backend ngrok URL:"
curl -s http://localhost:4040/api/tunnels | grep -o 'https://[^"]*.ngrok.io' | head -n 1

echo "Frontend ngrok URL:"
curl -s http://localhost:4040/api/tunnels | grep -o 'https://[^"]*.ngrok.io' | tail -n 1

echo "------------------------------------------------"
echo "If the URLs above don't appear, you can manually access them at:"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "Then open a separate terminal and run:"
echo "./ngrok http 8000  # for backend"
echo "./ngrok http 3000  # for frontend"
echo ""
echo "Login credentials: admin / admin123"
echo "------------------------------------------------"

# Keep script alive
wait $BACKEND_PID $FRONTEND_PID $NGROK_BACKEND_PID $NGROK_FRONTEND_PID
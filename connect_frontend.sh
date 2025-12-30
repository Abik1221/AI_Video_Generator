#!/bin/bash

# Check if URL is provided
if [ -z "$1" ]; then
  echo "⚠️  Error: Missing Ngrok URL."
  echo "Usage: ./connect_frontend.sh <YOUR_NGROK_URL>"
  echo "Example: ./connect_frontend.sh https://abcd-1234.ngrok-free.app"
  exit 1
fi

BACKEND_URL=$1
echo "------------------------------------------------"
echo "🔌 Connecting Frontend to Backend: $BACKEND_URL"
echo "------------------------------------------------"

# 1. Stop existing frontend
echo "🛑 Stopping currently running frontend..."
pkill -f "vite" || echo "No Vite process found (that's okay)"
pkill -f "npm run dev" || echo "No NPM process found (that's okay)"

# Wait for ports to clear
sleep 2

# 2. Start new frontend with environment variable
echo "🚀 Starting Frontend with public API link..."
cd client/estatevision-ai---professional-property-video-generator

# Set the environment variable just for this process
export VITE_API_URL=$BACKEND_URL

# Start in background
npm run dev -- --host --port 3000 &
FRONTEND_PID=$!

echo "------------------------------------------------"
echo "✅ Frontend is restarting with PID $FRONTEND_PID"
echo "   Backend Link: $BACKEND_URL"
echo "------------------------------------------------"
echo "👉 NEXT STEP:"
echo "1. Wait 10 seconds for frontend to boot."
echo "2. Open a NEW terminal."
echo "3. Run: 'ngrok http 3000'"
echo "4. Share THAT new https link with your client."
echo "------------------------------------------------"

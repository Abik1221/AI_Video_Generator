# Metronavix - Client Access Information

## Current Status
✅ **Backend is running** on port 8000
⚠️ **Frontend needs manual check** on port 3000

## Login Credentials
```
Username: admin
Password: admin123
```

## How to Share with Your Client

### Option 1: Using Ngrok (Recommended)
1. Download Ngrok from https://ngrok.com/download
2. Run these two commands in separate terminals:
   ```bash
   ngrok http 3000  # For Frontend
   ngrok http 8000  # For Backend
   ```
3. Ngrok will give you two public URLs like:
   - Frontend: `https://abc123.ngrok-free.app`
   - Backend: `https://xyz789.ngrok-free.app`

4. **IMPORTANT**: Update the frontend environment variable:
   ```bash
   cd client/estatevision-ai---professional-property-video-generator
   echo "VITE_API_URL=https://xyz789.ngrok-free.app" > .env
   ```
   Then restart the frontend.

5. Send the **Frontend URL** to your client.

### Option 2: Using Your Local IP (Same Network Only)
If your client is on the same network:
```
Get your IP: hostname -I
Frontend: http://YOUR_IP:3000
Backend: http://YOUR_IP:8000
```

## Services Running
- Backend API: http://localhost:8000
- Frontend UI: http://localhost:3000
- Admin User: admin / admin123
- Credits: 10000

## To Stop The Services
```bash
pkill -f uvicorn  # Stop backend
pkill -f vite     # Stop frontend
```

## To Restart
```bash
cd /home/nahomkeneni/upwork_projects/chebude_dande
bash run_locally.sh
```

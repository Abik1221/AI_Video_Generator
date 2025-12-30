# How to Share with Client using Ngrok

You need to expose both the **Backend** (API) and the **Frontend** (UI) to the internet so your client can access it.

### Step 0: Set up Ngrok Authtoken (Recommended)
If you haven't used ngrok before, you should sign up for a free account at [dashboard.ngrok.com](https://dashboard.ngrok.com) to get your Authtoken. This prevents the session from expiring quickly.
1. Run: `ngrok config add-authtoken <YOUR_TOKEN>`

### Step 1: Expose Backend
1. Open a new terminal.
2. Run: `ngrok http 8000`
3. Copy the Forwarding URL (e.g., `https://aaaa-111-222.ngrok-free.app`).  
   **Let's call this `BACKEND_URL`.**

### Step 2: Configure and Run Frontend
1. Stop your current frontend server (Ctrl+C).
2. Start it again with the `BACKEND_URL` you just copied:
   ```bash
   # Replace with your actual ngrok URL from Step 1
   export VITE_API_URL=https://aaaa-111-222.ngrok-free.app 
   cd client/estatevision-ai---professional-property-video-generator
   npm run dev -- --host --port 3000
   ```

### Step 3: Expose Frontend
1. Open another new terminal.
2. Run: `ngrok http 3000`
### Troubleshooting
**Error: "The endpoint is already online"**
If you see this error, it means an old ngrok process is still running.
Run this command to stop it:
```bash
pkill -f ngrok
```
Then try starting your tunnel again.
Send the **Frontend URL** (from Step 3) to your client. 
They will open it, and it will correctly talk to your backend via the URL you configured in Step 2.

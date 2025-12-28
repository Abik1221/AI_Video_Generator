# Deployment Guide - Metronavix

This guide covers the deployment of the Metronavix Property Video Engine, which consists of a FastAPI backend and a React/Vite frontend.

## 1. Prerequisites
- Docker and Docker Compose installed on your server.
- OpenAI API Key.
- Google Cloud JSON credentials (if using Google Cloud services).

## 2. Environment Configuration

### Backend (.env)
Create a `.env` file in the `server/` directory with the following variables:
```env
# Database Configuration
DATABASE_URL=sqlite:///./estatevision_ai.db

# API Keys
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_GEMINI_API_KEY=your_gemini_api_key_here
# Optional: Only if using Google Cloud TTS
# GOOGLE_CLOUD_CREDENTIALS_PATH=/app/google-cloud-credentials.json

# Application Settings
APP_NAME=Metronavix API
HOST=0.0.0.0
PORT=8000

# OpenAI TTS Settings
OPENAI_TTS_MODEL=tts-1
OPENAI_TTS_VOICE=alloy
```

### Frontend (.env)
Create a `.env` file in `client/estatevision-ai---professional-property-video-generator/` with:
```env
VITE_API_URL=http://your-server-ip:8000
```
*Note: Replace `your-server-ip` with your actual domain or IP address.*

## 3. Deployment Methods

### Method A: Docker Compose (Recommended)
This method runs both services and orchestrates them.

1. **Clone the repository** (if not already done).
2. **Configure environment files** as described above.
3. **Run the stack**:
   ```bash
   docker-compose up -d --build
   ```
4. **Access the application**:
   - Frontend: `http://localhost:3000` (or your domain/IP)
   - Backend API: `http://localhost:8000`
   - API Docs: `http://localhost:8000/docs`

### Method B: Manual (Development)
If you want to run without Docker:

**Backend:**
```bash
cd server
pip install -r requirements.txt
python init_db.py
python seed_user.py
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd client/estatevision-ai---professional-property-video-generator
npm install
npm run build
# Then serve the 'dist' folder using a web server or 'npm run dev' for development
npm run dev
```

## 4. GitHub Actions CI/CD Secrets

If you want to use the automated deployment pipelines via GitHub Actions, you must set the following Secrets in your GitHub Repository settings.

### How to set up:
1. Go to your GitHub Repository -> **Settings** -> **Secrets and variables** -> **Actions**.
2. Click **New repository secret**.
3. Add each of the following keys and their corresponding values.

### Required Secrets:

| Secret Name | Description |
| :--- | :--- |
| `DOCKERHUB_USERNAME` | Your Docker Hub username. |
| `DOCKERHUB_TOKEN` | Your Docker Hub personal access token. |
| `RAILWAY_TOKEN` | Your Railway project API token. |
| `VERCEL_TOKEN` | Your Vercel account API token. |
| `VERCEL_ORG_ID` | Your Vercel organization ID. |
| `VERCEL_PROJECT_ID` | Your Vercel project ID. |
| `OPENAI_API_KEY` | (Optional) If you want to run tests in CI. |
| `GOOGLE_GEMINI_API_KEY` | (Optional) If you want to run translation tests in CI. |

## 5. Manual Deployment from GitHub

You can manually trigger a deployment at any time without pushing new code:

1. Go to your GitHub Repository.
2. Click on the **Actions** tab at the top.
3. In the left sidebar, select either **Backend Deployment** or **Frontend Deployment**.
4. Click the **Run workflow** dropdown button on the right.
5. Select the branch (usually `main`) and click **Run workflow**.

This will manually start the deployment process to Railway (for Backend) or Vercel (for Frontend).

## 6. Initial Platform Setup (Connecting for the first time)

To get the Secrets required for GitHub Actions, follow these steps on each platform:

### Railway (Backend)
1. Go to [Railway.app](https://railway.app) and create a new project.
2. Provision a **PostgreSQL** or **SQLite** database if needed (SQLite is used by default in this project).
3. Go to **Settings** -> **Tokens** in your Railway project.
4. Create a new **Project Token** and copy it as `RAILWAY_TOKEN`.

### Vercel (Frontend)
1. Go to [Vercel.com](https://vercel.com) and click **Add New** -> **Project**.
2. Import your GitHub repository.
3. Once the project is created, go to your **Account Settings** -> **Tokens** to create a `VERCEL_TOKEN`.
4. To get `VERCEL_ORG_ID` and `VERCEL_PROJECT_ID`:
   - Install the Vercel CLI locally: `npm install -g vercel`
   - Run `vercel link` in the frontend directory.
   - Look at the `.vercel/project.json` file created in your project to find `orgId` and `projectId`.

## 7. Alternative: Full Railway Deployment (Backend + Frontend)

If you prefer to keep everything on Railway instead of using Vercel for the frontend:

1. **Create a new service** in your Railway project.
2. **Point it to the frontend folder**: `/client/estatevision-ai---professional-property-video-generator`.
3. **Railway will use the `Dockerfile`**: It will automatically build and deploy the React app.
4. **URL**: Railway will generate a unique URL (e.g., `metronavix-ui.up.railway.app`). You do **not** need to use an IP address.

**Note**: If you choose this path, you will need to update the `VITE_API_URL` environment variable for the frontend service to point to your Railway Backend URL.

## 8. Troubleshooting
- **Database issues**: Ensure `estatevision_ai.db` is writable by the container.
- **CORS issues**: Ensure the backend allows the frontend's origin in `app/main.py`.
- **FFmpeg**: The Docker image includes FFmpeg. If running manually, ensure FFmpeg is installed on your system.

## 9. Deploying to a Virtual Private Server (VPS) via IP Address

If you want a fixed IP address for your client and want to run both services for free, here are the best options:

### Free VPS Providers (Always Free Tiers)
1. **Oracle Cloud**: Offers the most generous free tier (4 ARM cores, 24GB RAM).
2. **Google Cloud (GCP)**: Offers an `e2-micro` instance for free in specific regions (US West, Central, East).
3. **AWS**: Offers a `t2.micro` or `t3.micro` instance free for the first 12 months.

### Step-by-Step VPS Setup:
1. **Provision a Linux Server** (Ubuntu 22.04 recommended).
2. **Install Docker and Docker Compose**:
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   ```
3. **Open Firewall Ports**:
   You must open these ports in your provider's dashboard (Security Groups/Ingress Rules):
   - **Port 8000**: Backend API
   - **Port 3000**: Frontend UI
   - **Port 22**: SSH (usually open by default)
4. **Deploy using Docker Compose**:
   - Clone your repo to the server.
   - Create the `.env` files (especially `VITE_API_URL=http://YOUR_SERVER_IP:8000`).
   - Run `docker-compose up -d --build`.

Your app will then be accessible at `http://YOUR_SERVER_IP:3000`.

## 10. Free Hosting WITHOUT Credit Card (No Card Required)

If you don't have a credit card for verification, use these platforms. They support Docker and give you a public URL.

### Option 1: Hugging Face Spaces (Highly Recommended)
This is the best option because it provides **16GB RAM** for free, which is perfect for processing property videos with FFmpeg.
1. Create a free account on [Hugging Face](https://huggingface.co).
2. Create a **New Space**.
3. Select **Docker** as the SDK.
4. Upload all files from the `/server` folder.
5. Set your `OPENAI_API_KEY` and `GOOGLE_GEMINI_API_KEY` in the **Settings -> Variables and Secrets** tab.
6. Your app will be live at `https://your-username-your-space.hf.space`.

### Option 2: Koyeb
Koyeb allows you to deploy Docker containers directly from GitHub without a credit card.
1. Sign up at [Koyeb.com](https://koyeb.com).
2. Create a new **App** and connect your GitHub repository.
3. Set the **Docker context** to `/server`.
4. Add your Environment Variables in the Koyeb UI.

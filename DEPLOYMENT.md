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

## 5. Troubleshooting
- **Database issues**: Ensure `estatevision_ai.db` is writable by the container.
- **CORS issues**: Ensure the backend allows the frontend's origin in `app/main.py`.
- **FFmpeg**: The Docker image includes FFmpeg. If running manually, ensure FFmpeg is installed on your system.

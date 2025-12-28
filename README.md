# Metronavix - Property Video Engine

An AI-powered system that generates property videos with audio descriptions in multiple languages.

## Admin Credentials

- **Username**: `Metronavix`
- **Password**: `Metronavix123admin`

## Project Structure

- `server/`: FastAPI backend with AI narration logic.
- `client/estatevision-ai---professional-property-video-generator/`: React frontend with a premium black-and-white aesthetic.

## Deployment

### Docker
Run the entire stack using Docker Compose:
```bash
docker-compose up --build
```

### CI/CD
- **Backend**: Deployed to Railway.
- **Frontend**: Deployed to Vercel.

## Quick Start (Local)

1. **Backend**:
   ```bash
   cd server
   pip install -r requirements.txt
   python init_db.py
   python seed_user.py
   uvicorn app.main:app --reload
   ```

2. **Frontend**:
   ```bash
   cd client/estatevision-ai---professional-property-video-generator
   npm install
   npm run dev
   ```

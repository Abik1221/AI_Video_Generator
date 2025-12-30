from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from app.api.v1.api import api_router
from app.database import create_all_tables
from app.config import settings
from seed_user import seed_admin_user
import os
from pathlib import Path

app = FastAPI(
    title="EstateVision AI - Property Video Generator API",
    description="API for generating property videos with AI narration",
    version="1.0.0"
)

# Initialize database tables and seed admin user
create_all_tables()
seed_admin_user()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router (must be before static files)
app.include_router(api_router)

# Mount static files for uploads/outputs
os.makedirs(settings.upload_folder, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.upload_folder), name="uploads")

# Path to frontend dist folder (from /server/app/main.py -> /client/.../dist)
FRONTEND_DIST = Path(__file__).parent.parent.parent / "client" / "estatevision-ai---professional-property-video-generator" / "dist"

# Serve frontend static assets if the dist folder exists
if FRONTEND_DIST.exists():
    # Mount assets folder for JS, CSS, images
    assets_path = FRONTEND_DIST / "assets"
    if assets_path.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_path)), name="frontend_assets")

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is running"}

# Catch-all route to serve frontend for SPA routing
@app.get("/{full_path:path}")
async def serve_frontend(request: Request, full_path: str):
    """Serve frontend files or index.html for SPA routing"""
    # Don't serve frontend for API routes
    if full_path.startswith("api/"):
        return {"error": "Not found"}
    
    if FRONTEND_DIST.exists():
        # Try to serve the exact file
        file_path = FRONTEND_DIST / full_path
        if file_path.is_file():
            return FileResponse(str(file_path))
        
        # For SPA routing, serve index.html
        index_path = FRONTEND_DIST / "index.html"
        if index_path.exists():
            return FileResponse(str(index_path))
    
    # Fallback API response if no frontend
    return {"message": "EstateVision AI - Property Video Generator API", "docs": "/docs"}
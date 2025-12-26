from fastapi import APIRouter
from app.api.v1.endpoints import jobs, languages, settings, auth

api_router = APIRouter()
api_router.include_router(jobs.router, prefix="/api/v1", tags=["jobs"])
api_router.include_router(languages.router, prefix="/api/v1", tags=["languages"])
api_router.include_router(settings.router, prefix="/api/v1", tags=["settings"])
api_router.include_router(auth.router, prefix="/api/v1", tags=["auth"])
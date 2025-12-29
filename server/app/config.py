from pydantic_settings import BaseSettings
from typing import List, Optional
from pydantic import field_validator
import json


class Settings(BaseSettings):
    # Database settings
    database_url: str = "sqlite:///./estatevision_ai.db"
    
    # API Keys
    openai_api_key: Optional[str] = None
    google_cloud_credentials: Optional[str] = None
    google_service_account_file: Optional[str] = None
    google_gemini_api_key: Optional[str] = None  # New Google Gemini API key
    google_application_credentials: Optional[str] = None  # Added this field
    
    # Security
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS settings
    cors_origins: List[str] = ["*"]  # Change in production
    
    # TTS settings
    default_tts_voice: str = "nova"
    
    # Video processing settings
    max_video_size_mb: int = 100
    max_description_length: int = 5000
    video_processing_quality: str = "720p"
    upload_folder: str = "./uploads"
    allowed_video_formats: List[str] = ["mp4", "avi", "mov", "mkv", "webm", "flv", "3gp", "wmv"]
    
    # System settings
    enable_tts_fallback: bool = True
    tts_fallback_service: str = "google"
    
    # Email settings
    enable_email_notifications: bool = False
    email_smtp_server: str = "smtp.gmail.com"
    email_smtp_port: int = 587
    
    # API rate limiting
    enable_api_rate_limiting: bool = True
    api_rate_limit_requests: int = 100
    api_rate_limit_window: int = 3600
    
    # Background processing
    enable_background_processing: bool = True
    max_concurrent_jobs: int = 5
    
    # Application settings
    app_name: str = "EstateVision AI API"
    app_version: str = "1.0.0"
    host: str = "0.0.0.0"
    port: int = 8000
    
    # File storage settings
    output_folder: str = "outputs"
    temp_folder: str = "temp"
    upload_folder: str = "uploads"
    
    # Job processing settings
    job_timeout_seconds: int = 3600
    
    # OpenAI TTS settings
    openai_tts_model: str = "tts-1"
    openai_tts_voice: str = "nova"

    @field_validator('allowed_video_formats', mode='before')
    @classmethod
    def parse_allowed_video_formats(cls, v):
        if v is None or (isinstance(v, str) and v.strip() == ""):
            # Return default value if None or empty string
            return ["mp4", "avi", "mov", "mkv", "webm", "flv", "3gp", "wmv"]
        if isinstance(v, str):
            if v.startswith('[') and v.endswith(']'):
                # It's a JSON array string
                try:
                    return json.loads(v)
                except json.JSONDecodeError:
                    # If JSON parsing fails, fall back to comma-separated
                    return [item.strip() for item in v.split(',')]
            else:
                # It's a comma-separated string
                return [item.strip() for item in v.split(',')]
        return v

    @field_validator('cors_origins', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        if v is None or (isinstance(v, str) and v.strip() == ""):
            # Return default value if None or empty string
            return ["*"]
        if isinstance(v, str):
            if v.startswith('[') and v.endswith(']'):
                # It's a JSON array string
                try:
                    return json.loads(v)
                except json.JSONDecodeError:
                    # If JSON parsing fails, fall back to comma-separated
                    return [item.strip() for item in v.split(',')]
            else:
                # It's a comma-separated string
                return [item.strip() for item in v.split(',')]
        return v

    class Config:
        env_file = ".env"
        extra = "allow"  # Allow extra fields to prevent validation errors


settings = Settings()
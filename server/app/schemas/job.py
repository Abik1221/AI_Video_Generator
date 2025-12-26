from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class JobCreate(BaseModel):
    description_text: str
    target_language: str = "en"


class JobResponse(BaseModel):
    id: int
    status: str
    progress: int
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    output_file_path: Optional[str] = None

    class Config:
        from_attributes = True
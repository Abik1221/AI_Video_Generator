from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.job import Job
from app.schemas.job import JobCreate, JobResponse
from app.workflows.video_generation import compiled_workflow
from app.services.tts_service import TTSManager
from app.services.video_service import VideoProcessor
import os
import tempfile
from datetime import datetime

router = APIRouter()


@router.post("/generate", summary="Generate property video with AI narration")
async def generate_video(
    video_file: UploadFile = File(...),
    description_text: str = "",
    target_language: str = "en",
    db: Session = Depends(get_db)
):
    """
    Generate a property video with AI narration
    """
    # Validate inputs
    if not description_text or len(description_text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Description text is required")
    
    if len(description_text) > 5000:  # From settings
        raise HTTPException(status_code=400, detail="Description text too long")
    
    # Validate video file
    allowed_extensions = [".mp4", ".mov", ".avi", ".mkv", ".wmv"]
    file_extension = os.path.splitext(video_file.filename)[1].lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid video file format")
    
    # Check file size (max 100MB)
    video_file.file.seek(0, 2)  # Seek to end
    file_size = video_file.file.tell()
    video_file.file.seek(0)  # Seek back to beginning
    
    max_size_mb = 100  # From settings
    if file_size > max_size_mb * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"File size exceeds {max_size_mb}MB limit")
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
        contents = await video_file.read()
        temp_file.write(contents)
        input_video_path = temp_file.name
    
    try:
        # Create job record
        job = Job(
            status="PENDING",
            input_file_path=input_video_path,
            description_text=description_text,
            target_language=target_language,
            progress=0
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        
        # Prepare workflow inputs
        tts_manager = TTSManager()
        video_processor = VideoProcessor()
        
        workflow_inputs = {
            "input_video_path": input_video_path,
            "description_text": description_text,
            "target_language": target_language,
            "job_id": job.id,
            "db_session": db,
            "tts_manager": tts_manager,
            "video_processor": video_processor,
            "error_message": "",
            "progress": 0
        }
        
        # Run the workflow (in a real implementation, this would be run asynchronously)
        # For now, we'll just update the job status to show it's processing
        job.status = "PROCESSING"
        job.progress = 10
        db.commit()
        
        # In a real implementation, you would run:
        # result = await compiled_workflow.ainvoke(workflow_inputs)
        
        return {
            "id": job.id,
            "status": job.status,
            "progress": job.progress
        }
        
    except Exception as e:
        # Clean up temp file if there was an error
        if os.path.exists(input_video_path):
            os.remove(input_video_path)
        
        # Update job status to failed
        if 'job' in locals():
            job.status = "FAILED"
            job.error_message = str(e)
            db.commit()
        
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{job_id}", response_model=JobResponse, summary="Get job status")
async def get_job_status(job_id: int, db: Session = Depends(get_db)):
    """
    Get the status of a video generation job
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return JobResponse(
        id=job.id,
        status=job.status,
        progress=job.progress,
        error_message=job.error_message,
        created_at=job.created_at,
        updated_at=job.updated_at,
        output_file_path=job.output_file_path
    )


@router.get("/jobs", response_model=List[JobResponse], summary="Get all jobs")
async def get_all_jobs(db: Session = Depends(get_db)):
    """
    Get all video generation jobs
    """
    jobs = db.query(Job).order_by(Job.created_at.desc()).all()
    return [
        JobResponse(
            id=job.id,
            status=job.status,
            progress=job.progress,
            error_message=job.error_message,
            created_at=job.created_at,
            updated_at=job.updated_at,
            output_file_path=job.output_file_path
        ) for job in jobs
    ]


@router.delete("/jobs/{job_id}", summary="Delete a job")
async def delete_job(job_id: int, db: Session = Depends(get_db)):
    """
    Delete a video generation job
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    db.delete(job)
    db.commit()
    
    return {"message": "Job deleted successfully"}


@router.post("/upload", summary="Upload video file without starting generation")
async def upload_video(video_file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload a video file without starting generation
    """
    # Validate video file
    allowed_extensions = [".mp4", ".mov", ".avi", ".mkv", ".wmv"]
    file_extension = os.path.splitext(video_file.filename)[1].lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid video file format")
    
    # Check file size (max 100MB)
    video_file.file.seek(0, 2)  # Seek to end
    file_size = video_file.file.tell()
    video_file.file.seek(0)  # Seek back to beginning
    
    max_size_mb = 100  # From settings
    if file_size > max_size_mb * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"File size exceeds {max_size_mb}MB limit")
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
        contents = await video_file.read()
        temp_file.write(contents)
        file_path = temp_file.name
    
    return {
        "filename": video_file.filename,
        "size": file_size,
        "path": file_path
    }
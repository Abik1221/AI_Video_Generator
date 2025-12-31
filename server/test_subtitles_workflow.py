import asyncio
import os
from app.workflows.video_generation import VideoGenerationWorkflow
from app.database import SessionLocal
from app.models.job import Job

async def test_workflow():
    db = SessionLocal()
    try:
        # Create a mock job in DB
        job = Job(
            input_file_path="test_video.mp4",
            description_text="This is a beautiful 3-bedroom apartment with a modern kitchen and a spacious living room. It's located in the heart of the city, close to all amenities.",
            target_language="en",
            status="PENDING"
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        
        print(f"Created job {job.id}")
        
        workflow = VideoGenerationWorkflow()
        input_data = {
            'input_file_path': job.input_file_path,
            'description_text': job.description_text,
            'target_language': job.target_language,
            'job_id': job.id
        }
        
        print("Running workflow...")
        result = await workflow.run_workflow(input_data)
        
        print(f"Workflow Status: {result.status}")
        print(f"Workflow Progress: {result.progress}")
        print(f"Output Path: {result.output_path}")
        print(f"Error: {result.error_message}")
        
    finally:
        db.close()

if __name__ == "__main__":
    if not os.path.exists("test_video.mp4"):
        print("Creating dummy video file for testing...")
        # Create a 5-second silence video if it doesn't exist
        os.system("ffmpeg -f lavfi -i color=c=black:s=640x480:d=5 -vcodec libx264 test_video.mp4")
    
    asyncio.run(test_workflow())

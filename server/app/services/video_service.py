import os
import subprocess
import tempfile
import asyncio
from pathlib import Path
from typing import Optional
from loguru import logger
from app.config import settings


class VideoProcessingService:
    """
    Service for handling video processing tasks using FFmpeg
    """
    
    def __init__(self):
        # Verify FFmpeg is available
        if not self._check_ffmpeg():
            raise RuntimeError("FFmpeg is not installed or not available in PATH")
    
    def _check_ffmpeg(self) -> bool:
        """
        Check if FFmpeg is available in the system
        """
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    async def merge_audio_video(self, video_path: str, audio_path: str, output_path: str) -> str:
        """
        Merge audio and video files using FFmpeg
        This version ensures that both streams are the same duration by using the video duration
        as the reference and extending the output to match it.
        """
        try:
            # Create temporary file for output to avoid conflicts
            temp_output = tempfile.NamedTemporaryFile(
                delete=False, 
                suffix='.mp4',
                dir=os.path.dirname(output_path)
            )
            temp_output.close()
            
            # Get video duration to use as reference
            video_duration = await self.extract_video_duration(video_path)
            
            # FFmpeg command to merge audio and video
            # Instead of using -shortest, we'll set the duration explicitly
            cmd = [
                'ffmpeg',
                '-i', video_path,      # Input video
                '-i', audio_path,      # Input audio
                '-c:v', 'copy',        # Copy video codec (preserve quality)
                '-c:a', 'aac',         # Audio codec
                '-strict', 'experimental',
                '-t', str(video_duration),  # Set output duration to match video
                '-y',                  # Overwrite output file
                temp_output.name       # Output file
            ]
            
            logger.info(f"Merging audio: {audio_path} with video: {video_path}")
            logger.info(f"Video duration: {video_duration}s")
            logger.info(f"FFmpeg command: {' '.join(cmd)}")
            
            # Run FFmpeg command asynchronously
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode()
                logger.error(f"FFmpeg error: {error_msg}")
                raise RuntimeError(f"FFmpeg failed with error: {error_msg}")
            
            # Move temp file to final location
            os.rename(temp_output.name, output_path)
            
            logger.info(f"Video successfully merged: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error merging audio and video: {e}")
            # Clean up temp file if it exists
            if 'temp_output' in locals() and os.path.exists(temp_output.name):
                os.remove(temp_output.name)
            raise
    
    async def extract_audio_duration(self, audio_path: str) -> float:
        """
        Extract duration of audio file using FFmpeg
        """
        try:
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-show_entries', 'format=duration',
                '-of', 'csv=p=0',
                audio_path
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode()
                logger.error(f"ffprobe error: {error_msg}")
                raise RuntimeError(f"ffprobe failed with error: {error_msg}")
            
            duration = float(stdout.decode().strip())
            return duration
            
        except Exception as e:
            logger.error(f"Error extracting audio duration: {e}")
            raise
    
    async def extract_video_duration(self, video_path: str) -> float:
        """
        Extract duration of video file using FFmpeg
        """
        try:
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-show_entries', 'format=duration',
                '-of', 'csv=p=0',
                video_path
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode()
                logger.error(f"ffprobe error: {error_msg}")
                raise RuntimeError(f"ffprobe failed with error: {error_msg}")
            
            duration = float(stdout.decode().strip())
            return duration
            
        except Exception as e:
            logger.error(f"Error extracting video duration: {e}")
            raise
    
    async def adjust_audio_to_video_duration(self, audio_path: str, video_path: str, output_path: str) -> str:
        """
        Adjust audio duration to match video duration
        """
        try:
            video_duration = await self.extract_video_duration(video_path)
            audio_duration = await self.extract_audio_duration(audio_path)
            
            if abs(video_duration - audio_duration) < 0.1:  # If durations are similar
                # Just copy the audio file
                import shutil
                shutil.copy2(audio_path, output_path)
                return output_path
            
            logger.info(f"Video duration: {video_duration}s, Audio duration: {audio_duration}s")
            
            # Adjust audio to match video duration
            if audio_duration > video_duration:
                # Trim audio to video duration
                cmd = [
                    'ffmpeg',
                    '-i', audio_path,
                    '-t', str(video_duration),
                    '-y',
                    output_path
                ]
                logger.info(f"Trimming audio from {audio_duration}s to {video_duration}s")
            else:
                # Loop or pad audio to match video duration
                # Use a combination of apad and atempo for better quality
                cmd = [
                    'ffmpeg',
                    '-i', audio_path,
                    '-af', f'apad=pad_len={int(video_duration * 48000)}',  # pad_len expects samples, assuming 48kHz
                    '-y',
                    output_path
                ]
                
                # Alternative approach: first try to loop the audio
                try:
                    # Calculate how many times to loop
                    loop_times = int(video_duration / audio_duration) + 1
                    if loop_times > 1:
                        # Create a command that loops the audio
                        temp_looped = output_path.replace('.mp3', '_looped.mp3')
                        loop_cmd = [
                            'ffmpeg',
                            '-stream_loop', str(loop_times - 1),  # Loop n-1 times
                            '-i', audio_path,
                            '-t', str(video_duration),
                            '-y',
                            temp_looped
                        ]
                        
                        logger.info(f"Looping audio to match video duration: {video_duration}s")
                        
                        process = await asyncio.create_subprocess_exec(
                            *loop_cmd,
                            stdout=asyncio.subprocess.PIPE,
                            stderr=asyncio.subprocess.PIPE
                        )
                        
                        stdout, stderr = await process.communicate()
                        
                        if process.returncode == 0:
                            # Successfully looped, now move to final output
                            os.rename(temp_looped, output_path)
                            logger.info(f"Audio successfully looped and adjusted: {output_path}")
                            return output_path
                        else:
                            logger.warning(f"Looping failed, falling back to padding: {stderr.decode()}")
                            # Remove temp file if it exists
                            if os.path.exists(temp_looped):
                                os.remove(temp_looped)
                except Exception as loop_error:
                    logger.warning(f"Looping approach failed, using padding: {loop_error}")
                    
                # Fallback: pad with silence
                cmd = [
                    'ffmpeg',
                    '-i', audio_path,
                    '-af', f'apad=pad_dur={video_duration-audio_duration}',
                    '-y',
                    output_path
                ]
                logger.info(f"Padding audio from {audio_duration}s to {video_duration}s using silence")
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode()
                logger.error(f"FFmpeg error: {error_msg}")
                raise RuntimeError(f"FFmpeg failed with error: {error_msg}")
            
            logger.info(f"Audio duration adjusted: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error adjusting audio duration: {e}")
            raise
    
    async def validate_video_format(self, video_path: str) -> bool:
        """
        Validate if the video format is supported
        """
        try:
            file_extension = Path(video_path).suffix.lower().lstrip('.')
            return file_extension in settings.allowed_video_formats
        except Exception as e:
            logger.error(f"Error validating video format: {e}")
            return False
    
    async def get_video_info(self, video_path: str) -> dict:
        """
        Get video information (duration, resolution, etc.)
        """
        try:
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                video_path
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode()
                logger.error(f"ffprobe error: {error_msg}")
                raise RuntimeError(f"ffprobe failed with error: {error_msg}")
            
            import json
            info = json.loads(stdout.decode())
            return info
            
        except Exception as e:
            logger.error(f"Error getting video info: {e}")
            raise


import subprocess
import os
from typing import Tuple
import ffmpeg


class VideoProcessor:
    """
    Service for processing video files using FFmpeg
    """
    
    def __init__(self):
        # Verify that FFmpeg is available
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE)
            if result.returncode != 0:
                raise Exception("FFmpeg not found in system")
        except FileNotFoundError:
            raise Exception("FFmpeg not found in system")
    
    def merge_audio_video(self, video_path: str, audio_path: str) -> str:
        """
        Merge audio and video files using FFmpeg
        """
        # Create output path
        output_path = video_path.replace('.mp4', '_with_audio.mp4')
        
        try:
            # Use ffmpeg-python to merge audio and video
            (
                ffmpeg
                .input(video_path)
                .input(audio_path)
                .output(output_path, vcodec='copy', acodec='aac', strict='experimental')
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
            
            return output_path
        except Exception as e:
            raise Exception(f"Error merging audio and video: {str(e)}")
    
    def adjust_audio_duration(self, audio_path: str, target_duration: float) -> str:
        """
        Adjust audio duration to match target duration
        """
        output_path = audio_path.replace('.mp3', '_adjusted.mp3')
        
        try:
            # Use ffmpeg to adjust audio duration
            (
                ffmpeg
                .input(audio_path)
                .output(output_path, t=target_duration, acodec='copy')
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
            
            return output_path
        except Exception as e:
            raise Exception(f"Error adjusting audio duration: {str(e)}")
    
    def get_video_duration(self, video_path: str) -> float:
        """
        Get the duration of a video file in seconds
        """
        try:
            probe = ffmpeg.probe(video_path)
            video_stream = next((stream for stream in probe['streams'] 
                                if stream['codec_type'] == 'video'), None)
            if video_stream is None:
                raise Exception("No video stream found in file")
            
            duration = float(video_stream['duration'])
            return duration
        except Exception as e:
            raise Exception(f"Error getting video duration: {str(e)}")
    
    def get_video_info(self, video_path: str) -> dict:
        """
        Get video information (resolution, format, etc.)
        """
        try:
            probe = ffmpeg.probe(video_path)
            video_stream = next((stream for stream in probe['streams'] 
                                if stream['codec_type'] == 'video'), None)
            if video_stream is None:
                raise Exception("No video stream found in file")
            
            info = {
                'width': int(video_stream['width']),
                'height': int(video_stream['height']),
                'duration': float(video_stream['duration']),
                'format': probe['format']['format_name'],
                'size': int(probe['format']['size'])
            }
            
            return info
        except Exception as e:
            raise Exception(f"Error getting video info: {str(e)}")

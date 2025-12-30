import subprocess
import os

def log(msg):
    print(msg)
    with open("test_merge_debug.txt", "a") as f:
        f.write(msg + "\n")

# Clear log
with open("test_merge_debug.txt", "w") as f:
    f.write("Starting merge test...\n")

video_path = "test_video.mp4"
audio_path = "test_audio_output.wav"
output_path = "test_output.mp4"

# 1. Generate test video
log("Generating test video...")
cmd_gen_video = [
    'ffmpeg', '-y', '-f', 'lavfi', '-i', 'color=c=black:s=1280x720:r=30', '-t', '5', video_path
]
subprocess.run(cmd_gen_video, capture_output=True)

if not os.path.exists(video_path):
    log("Failed to create test video")
    exit(1)

if not os.path.exists(audio_path):
    log("Missing test_audio_output.wav. Run test_audio_gen.py first.")
    exit(1)

# 2. Merge
log("Merging video and audio...")
ffmpeg_cmd = [
    'ffmpeg', '-y',  # -y to overwrite output file
    '-i', video_path,  # Input video (index 0)
    '-i', audio_path,  # Input audio (index 1)
    '-map', '0:v:0',   # Map video from first input
    '-map', '1:a:0',   # Map audio from second input (AI narration)
    '-c:v', 'copy',    # Copy video stream
    '-c:a', 'aac',     # Encode audio as AAC
    '-b:a', '192k',    # Higher audio bitrate for better quality
    '-shortest',       # Truncate to the shortest stream (video)
    output_path
]
result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)

if result.returncode != 0:
    log(f"Merge failed: {result.stderr}")
else:
    log("Merge successful")
    
    # 3. Check output audio
    log("Checking output audio volume...")
    cmd_check = f"ffmpeg -i {output_path} -af volumedetect -f null /dev/null"
    res_check = subprocess.run(cmd_check, shell=True, capture_output=True, text=True)
    log(res_check.stderr)


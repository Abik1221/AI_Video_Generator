import os
import sys

# Add server directory to python path
sys.path.append(os.path.join(os.getcwd(), 'server'))

def log(msg):
    print(msg)
    with open("test_audio_debug.txt", "a") as f:
        f.write(msg + "\n")

# Clear log
with open("test_audio_debug.txt", "w") as f:
    f.write("Starting test...\n")

try:
    from app.services.simple_tts import SimpleTTSService
    log("Import successful")
except Exception as e:
    log(f"Import failed: {e}")
    sys.exit(1)

def test_tts():
    log("Initializing SimpleTTSService...")
    try:
        tts = SimpleTTSService()
        
        text = "This is a test of the automatic narration system."
        lang = "en"
        voice = "nova"
        
        log(f"Synthesizing speech for: '{text}'")
        audio_content = tts.synthesize_speech(text, lang, voice)
        
        log(f"Audio content length: {len(audio_content)} bytes")
        
        if len(audio_content) < 1000:
            log("WARNING: Audio content seems too small!")
        else:
            log("SUCCESS: Audio content generated.")
            
        output_file = "test_audio_output.wav"
        with open(output_file, "wb") as f:
            f.write(audio_content)
            
        log(f"Saved audio to {output_file}")
        
    except Exception as e:
        log(f"Error synthesizing speech: {e}")
        import traceback
        log(traceback.format_exc())

if __name__ == "__main__":
    test_tts()

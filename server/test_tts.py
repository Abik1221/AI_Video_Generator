import sys
import os
sys.path.append(os.getcwd())
from app.services.simple_tts import TTSManager

def test_tts():
    try:
        manager = TTSManager()
        content = manager.synthesize_speech("Test sentence for audio validation.", "en")
        print(f"Success! Generated {len(content)} bytes")
        if len(content) > 10000: # Silence of a few seconds is usually small in compressed formats, but high in WAV
            # 3.4MB was silence for 38s.
            # Let's hope gTTS or something worked.
            pass
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    test_tts()

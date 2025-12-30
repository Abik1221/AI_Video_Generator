import os
import sys
import datetime

# Add server directory to python path
sys.path.append(os.path.join(os.getcwd(), 'server'))

def log(msg):
    print(msg)
    with open("test_translation_debug.txt", "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {msg}\n")

# Clear log
with open("test_translation_debug.txt", "w") as f:
    f.write("Starting translation test...\n")

try:
    from dotenv import load_dotenv
    # Explicitly load server/.env
    env_path = os.path.join(os.getcwd(), 'server', '.env')
    loaded = load_dotenv(env_path, override=True)
    log(f"Loaded .env from {env_path}: {loaded}")

    from app.services.simple_tts import SimpleTTSService
    from app.config import settings
    log("Import successful")
    
    key = settings.google_gemini_api_key
    masked_key = f"{key[:4]}...{key[-4:]}" if key and len(key) > 8 else "None"
    log(f"Gemini API Key configured: {masked_key}")
except Exception as e:
    log(f"Import failed: {e}")
    sys.exit(1)

def test_translation_flow():
    log("Initializing SimpleTTSService...")
    try:
        tts = SimpleTTSService()
        
        # Test Case: English -> Spanish
        original_text = "Hello, this is a test of the video generation system."
        target_lang = "es" # Spanish
        
        log(f"--- Testing Translation (en -> {target_lang}) ---")
        log(f"Original: {original_text}")
        
        # 1. Test Translation
        translated_text = tts.translate_text(original_text, target_lang)
        log(f"Translated: {translated_text}")
        
        if translated_text == original_text:
            log("WARNING: Text was NOT translated (or translation equals original). Check Gemini API.")
        else:
            log("SUCCESS: Text translated.")

        # 2. Test TTS with translated text
        log(f"--- Testing TTS Generation for {target_lang} ---")
        voice = "novel" # Dummy voice, simple_tts handles mapping
        
        audio_content = tts.synthesize_speech(translated_text, target_lang, voice)
        log(f"Audio content length: {len(audio_content)} bytes")
        
        if len(audio_content) < 1000:
            log("WARNING: Audio content seems too small!")
        else:
            log("SUCCESS: Audio content generated.")
            
        output_file = f"test_translation_{target_lang}.wav"
        with open(output_file, "wb") as f:
            f.write(audio_content)
        log(f"Saved audio to {output_file}")

    except Exception as e:
        log(f"Error in translation flow: {e}")
        import traceback
        log(traceback.format_exc())
    
    # Dump tts_debug.log
    if os.path.exists("tts_debug.log"):
        log("\n--- tts_debug.log content ---")
        with open("tts_debug.log", "r") as f:
            log(f.read())

if __name__ == "__main__":
    test_translation_flow()

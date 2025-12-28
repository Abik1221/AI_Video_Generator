import os
import sys
from pathlib import Path

# Add the server directory to the python path
server_dir = Path(__file__).resolve().parent / "server"
sys.path.append(str(server_dir))

from app.config import settings
from app.services.tts_service import GoogleGeminiTranslationService

def test_translation():
    api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
    if not api_key:
        print("Error: GOOGLE_GEMINI_API_KEY environment variable not set.")
        return

    # Temporarily override settings for test
    settings.google_gemini_api_key = api_key
    
    translator = GoogleGeminiTranslationService()
    text = "Beautiful luxury villa with a swimming pool and 5 bedrooms."
    target_lang = "hi" # Hindi
    
    print(f"Translating: '{text}' to {target_lang}...")
    try:
        translated = translator.translate_text(text, target_lang)
        print(f"Result: {translated}")
    except Exception as e:
        print(f"Translation failed: {e}")

if __name__ == "__main__":
    test_translation()

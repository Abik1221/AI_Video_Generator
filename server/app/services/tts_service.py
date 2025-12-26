import os
import openai
from abc import ABC, abstractmethod
from google.cloud import texttospeech
from google.oauth2 import service_account
from app.config import settings
from app.models.job import Language
from sqlalchemy.orm import Session
import requests
import json
from typing import Optional


class TTSInterface(ABC):
    @abstractmethod
    def synthesize_speech(self, text: str, language_code: str, voice_name: str) -> bytes:
        pass


class OpenAITTSService(TTSInterface):
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.openai_api_key)

    def synthesize_speech(self, text: str, language_code: str, voice_name: str) -> bytes:
        try:
            response = self.client.audio.speech.create(
                model="tts-1",
                voice=voice_name,
                input=text
            )
            return response.content
        except Exception as e:
            raise Exception(f"OpenAI TTS Error: {str(e)}")


class GoogleCloudTTSService(TTSInterface):
    def __init__(self):
        if settings.google_service_account_file:
            credentials = service_account.Credentials.from_service_account_file(
                settings.google_service_account_file
            )
            self.client = texttospeech.TextToSpeechClient(credentials=credentials)
        else:
            # Use application default credentials
            self.client = texttospeech.TextToSpeechClient()

    def synthesize_speech(self, text: str, language_code: str, voice_name: str) -> bytes:
        try:
            synthesis_input = texttospeech.SynthesisInput(text=text)

            # Set the voice parameters
            voice = texttospeech.VoiceSelectionParams(
                language_code=language_code,
                name=voice_name  # e.g., "en-US-Standard-C"
            )

            # Select the type of audio file
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )

            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )

            return response.audio_content
        except Exception as e:
            raise Exception(f"Google Cloud TTS Error: {str(e)}")


class GoogleGeminiTranslationService:
    """
    Service to use Google Gemini for translation
    """
    def __init__(self):
        self.api_key = settings.google_gemini_api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    
    def translate_text(self, text: str, target_language: str) -> str:
        """
        Translate text using Google Gemini
        """
        if not self.api_key:
            raise Exception("Google Gemini API key not configured")
        
        # Map language codes to names for better prompting
        language_names = {
            "en": "English",
            "te": "Telugu",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "it": "Italian",
            "pt": "Portuguese",
            "ru": "Russian",
            "ja": "Japanese",
            "ko": "Korean",
            "zh": "Chinese",
            "hi": "Hindi",
            "ar": "Arabic",
            "bn": "Bengali",
            "pa": "Punjabi"
        }
        
        target_lang_name = language_names.get(target_language, target_language)
        
        prompt = f"""
        Translate the following text to {target_lang_name}. 
        Only return the translated text, nothing else:
        
        {text}
        """
        
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.1,
                "maxOutputTokens": 8192,
                "topP": 0.8,
                "topK": 40
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}?key={self.api_key}",
                headers=headers,
                data=json.dumps(data)
            )
            
            if response.status_code == 200:
                result = response.json()
                if "candidates" in result and len(result["candidates"]) > 0:
                    translated_text = result["candidates"][0]["content"]["parts"][0]["text"].strip()
                    return translated_text
                else:
                    raise Exception("No translation returned from Gemini")
            else:
                raise Exception(f"Gemini API Error: {response.status_code} - {response.text}")
        except Exception as e:
            raise Exception(f"Translation Error: {str(e)}")


class TTSManager:
    def __init__(self):
        self.openai_service = OpenAITTSService() if settings.openai_api_key else None
        self.google_service = GoogleCloudTTSService() if settings.google_cloud_credentials else None
        self.translation_service = GoogleGeminiTranslationService()

    def synthesize_speech(self, text: str, target_language: str, voice_name: str = "nova") -> bytes:
        # First, translate the text if needed using Gemini
        if target_language != "en":
            try:
                translated_text = self.translation_service.translate_text(text, target_language)
            except Exception as e:
                # If translation fails, use original text
                print(f"Translation failed, using original text: {str(e)}")
                translated_text = text
        else:
            translated_text = text
        
        # Try OpenAI first, then fallback to Google Cloud
        if self.openai_service:
            try:
                return self.openai_service.synthesize_speech(translated_text, target_language, voice_name)
            except Exception as e:
                print(f"OpenAI TTS failed: {str(e)}")
        
        if self.google_service:
            try:
                return self.google_service.synthesize_speech(translated_text, target_language, voice_name)
            except Exception as e:
                print(f"Google Cloud TTS failed: {str(e)}")
        
        raise Exception("All TTS services failed")

    def get_supported_languages(self, db: Session) -> list:
        """
        Get supported languages from database, with fallback to default languages
        """
        languages = db.query(Language).filter(Language.is_active == True).all()
        
        if not languages:
            # Default languages if none in database
            default_languages = [
                Language(code="en", name="English", tts_voice="en-US-Standard-C"),
                Language(code="te", name="Telugu", tts_voice="te-IN-Standard-A"),
                Language(code="es", name="Spanish", tts_voice="es-ES-Standard-A"),
                Language(code="fr", name="French", tts_voice="fr-FR-Standard-A"),
                Language(code="de", name="German", tts_voice="de-DE-Standard-A"),
            ]
            for lang in default_languages:
                db.add(lang)
            db.commit()
            return default_languages
        
        return languages
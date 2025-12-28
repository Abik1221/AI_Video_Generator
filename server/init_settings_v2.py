import sys
import os
# Add current directory to path
sys.path.append(os.getcwd())

try:
    from app.database import SessionLocal
    from app.services.settings_service import SettingsService
    print("Imports success")
except Exception as e:
    print(f"Import error: {e}")
    sys.exit(1)

db = SessionLocal()
try:
    print("Database session opened")
    service = SettingsService(db)
    
    defaults = {
        "enable_tts": "true",
        "default_tts_voice": "nova",
        "tts_speed": "1.0",
        "enable_tts_fallback": "true",
        "tts_fallback_service": "google",
        "max_video_size_mb": "100",
        "max_description_length": "5000",
        "video_processing_quality": "720p",
        "enable_background_processing": "true",
        "max_concurrent_jobs": "5"
    }
    
    for key, value in defaults.items():
        type_val = "boolean" if value in ("true", "false") else ("integer" if value.isdigit() else "string")
        service.set_setting(key, value, type=type_val)
        print(f"Set {key} to {value} (type: {type_val})")
        
    db.commit()
    print("Initialization complete. Committed to DB.")
except Exception as e:
    print(f"Runtime error: {e}")
finally:
    db.close()

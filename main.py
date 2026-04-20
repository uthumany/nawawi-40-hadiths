from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import json
import os
from config import get_config
from audio_endpoints import router as audio_router
from sync_transliteration_endpoints import router as sync_trans_router

# Get configuration
config = get_config()

app = FastAPI(
    title=config.API_TITLE,
    description=config.API_DESCRIPTION,
    version=config.API_VERSION
)

# Configuration
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "hadiths.json")

def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def load_sync_data(hadith_number: int, language: str = "ar"):
    """Load word-by-word sync data for a hadith."""
    sync_dir = "sync" if language == "ar" else "sync_en"
    sync_path = os.path.join(
        os.path.dirname(__file__), 
        "api", 
        sync_dir, 
        f"hadith_{hadith_number}.json"
    )
    if os.path.exists(sync_path):
        with open(sync_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def load_transliterations():
    """Load all transliterations."""
    trans_path = os.path.join(
        os.path.dirname(__file__), 
        "api", 
        "transliterations.json"
    )
    if os.path.exists(trans_path):
        with open(trans_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@app.get("/")
async def root():
    """Root endpoint with API information and available endpoints."""
    return {
        "message": "Welcome to the Nawawi's 40 Hadiths API",
        "version": config.API_VERSION,
        "endpoints": config.get_endpoints_dict(),
        "documentation": "/docs"
    }

@app.get("/config")
async def get_api_config():
    """Get API configuration including base URLs, supported languages, and endpoints."""
    return config.get_config_dict()

@app.get("/hadiths")
async def get_all_hadiths():
    """Get all hadiths with metadata."""
    data = load_data()
    return data

@app.get("/hadiths/{number}")
async def get_hadith(number: int):
    """Get a specific hadith by number with basic metadata."""
    if number < 1 or number > config.TOTAL_HADITHS:
        raise HTTPException(
            status_code=400, 
            detail=f"Hadith number must be between 1 and {config.TOTAL_HADITHS}"
        )
    
    data = load_data()
    for hadith in data["hadiths"]:
        if hadith["hadith_number"] == number:
            return hadith
    raise HTTPException(status_code=404, detail="Hadith not found")

@app.get("/hadiths/{number}/audio/english")
async def get_hadith_english_audio(number: int):
    """Get English audio URL and metadata for a hadith."""
    if number < 1 or number > config.TOTAL_HADITHS:
        raise HTTPException(
            status_code=400, 
            detail=f"Hadith number must be between 1 and {config.TOTAL_HADITHS}"
        )
    
    data = load_data()
    for hadith in data["hadiths"]:
        if hadith["hadith_number"] == number:
            return {
                "hadith_number": number,
                "title": hadith.get("title", ""),
                "audio_url": config.get_audio_url("en", number),
                "sync_url": config.get_sync_url("en", number),
                "language": "en",
                "description": "English audio translation with word-level synchronization"
            }
    raise HTTPException(status_code=404, detail="Hadith not found")

@app.get("/hadiths/{number}/sync/english")
async def get_hadith_english_sync(number: int):
    """Get word-by-word sync data for English audio of a hadith."""
    if number < 1 or number > config.TOTAL_HADITHS:
        raise HTTPException(
            status_code=400, 
            detail=f"Hadith number must be between 1 and {config.TOTAL_HADITHS}"
        )
    
    sync_data = load_sync_data(number, language="en")
    if sync_data:
        return sync_data
    raise HTTPException(status_code=404, detail="English sync data not found for this hadith")

@app.get("/hadiths/{number}/sync/arabic")
async def get_hadith_arabic_sync(number: int):
    """Get word-by-word sync data for Arabic audio of a hadith."""
    if number < 1 or number > config.TOTAL_HADITHS:
        raise HTTPException(
            status_code=400, 
            detail=f"Hadith number must be between 1 and {config.TOTAL_HADITHS}"
        )
    
    sync_data = load_sync_data(number, language="ar")
    if sync_data:
        return sync_data
    raise HTTPException(status_code=404, detail="Arabic sync data not found for this hadith")

# The direct audio file endpoint is now handled by the audio_router
# at /audio/english/hadith/{hadith_number}/file (if implemented)
# or we can keep it here but rename it to avoid conflict.
# For now, let's just remove it as we have the GitHub raw URL.

@app.get("/hadiths/{number}/full")
async def get_hadith_full(number: int):
    """
    Get complete hadith data including Arabic and English audio with word-by-word synchronization.
    This is the most comprehensive endpoint for accessing all hadith information.
    """
    if number < 1 or number > config.TOTAL_HADITHS:
        raise HTTPException(
            status_code=400, 
            detail=f"Hadith number must be between 1 and {config.TOTAL_HADITHS}"
        )
    
    data = load_data()
    for hadith in data["hadiths"]:
        if hadith["hadith_number"] == number:
            sync_en = load_sync_data(number, language="en")
            sync_ar = load_sync_data(number, language="ar")
            
            return {
                **hadith,
                "audio": {
                    "english": {
                        "url": config.get_audio_url("en", number),
                        "sync_url": config.get_sync_url("en", number),
                        "sync": sync_en,
                        "language": "en",
                        "description": "English audio translation"
                    },
                    "arabic": {
                        "url": hadith.get("audio_url", ""),
                        "sync_url": config.get_sync_url("ar", number),
                        "sync": sync_ar,
                        "language": "ar",
                        "description": "Arabic audio recitation"
                    }
                }
            }
    raise HTTPException(status_code=404, detail="Hadith not found")

# Include audio endpoints
app.include_router(audio_router)

# Include sync-transliteration endpoints
app.include_router(sync_trans_router)

@app.get("/transliterations")
async def get_transliterations():
    """Get all hadiths with Arabic transliterations."""
    transliterations = load_transliterations()
    if not transliterations:
        raise HTTPException(
            status_code=404, 
            detail="Transliterations not found"
        )
    return {
        "total_hadiths": len(transliterations),
        "hadiths": transliterations,
        "transliteration_url": config.get_transliteration_url()
    }

@app.get("/transliterations/{number}")
async def get_transliteration(number: int):
    """Get transliteration for a specific hadith."""
    if number < 1 or number > config.TOTAL_HADITHS:
        raise HTTPException(
            status_code=400, 
            detail=f"Hadith number must be between 1 and {config.TOTAL_HADITHS}"
        )
    
    transliterations = load_transliterations()
    for trans in transliterations:
        if trans["hadith_number"] == number:
            return trans
    raise HTTPException(status_code=404, detail="Transliteration not found")

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "version": config.API_VERSION,
        "total_hadiths": config.TOTAL_HADITHS
    }

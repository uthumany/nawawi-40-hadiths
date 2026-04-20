"""
Enhanced sync endpoints that include transliteration data for real-time word-by-word highlighting.
This module provides endpoints that combine audio sync data with transliteration information.
"""

from fastapi import APIRouter, HTTPException
import json
import os
from config import get_config

config = get_config()
router = APIRouter(prefix="/sync-transliteration", tags=["sync-transliteration"])

def load_sync_data(hadith_number: int, language: str = "en"):
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

def load_transliteration(hadith_number: int):
    """Load transliteration for a specific hadith."""
    trans_path = os.path.join(
        os.path.dirname(__file__), 
        "api", 
        "transliterations.json"
    )
    if os.path.exists(trans_path):
        with open(trans_path, "r", encoding="utf-8") as f:
            transliterations = json.load(f)
            for trans in transliterations:
                if trans["hadith_number"] == hadith_number:
                    return trans
    return None

@router.get("/hadith/{hadith_number}/english")
async def get_english_sync_with_transliteration(hadith_number: int):
    """Get English sync data with transliteration for real-time highlighting."""
    if hadith_number < 1 or hadith_number > config.TOTAL_HADITHS:
        raise HTTPException(
            status_code=400,
            detail=f"Hadith number must be between 1 and {config.TOTAL_HADITHS}"
        )
    
    sync_data = load_sync_data(hadith_number, language="en")
    transliteration = load_transliteration(hadith_number)
    
    if not sync_data:
        raise HTTPException(status_code=404, detail="Sync data not found for this hadith")
    
    return {
        "hadith_number": hadith_number,
        "language": "en",
        "sync": sync_data,
        "transliteration": transliteration,
        "description": "English audio sync with Arabic transliteration for real-time word highlighting"
    }

@router.get("/hadith/{hadith_number}/arabic")
async def get_arabic_sync_with_transliteration(hadith_number: int):
    """Get Arabic sync data with transliteration for real-time highlighting."""
    if hadith_number < 1 or hadith_number > config.TOTAL_HADITHS:
        raise HTTPException(
            status_code=400,
            detail=f"Hadith number must be between 1 and {config.TOTAL_HADITHS}"
        )
    
    sync_data = load_sync_data(hadith_number, language="ar")
    transliteration = load_transliteration(hadith_number)
    
    if not sync_data:
        raise HTTPException(status_code=404, detail="Sync data not found for this hadith")
    
    return {
        "hadith_number": hadith_number,
        "language": "ar",
        "sync": sync_data,
        "transliteration": transliteration,
        "description": "Arabic audio sync with transliteration for real-time word highlighting"
    }

@router.get("/hadith/{hadith_number}/both")
async def get_both_sync_with_transliteration(hadith_number: int):
    """Get both Arabic and English sync data with transliteration."""
    if hadith_number < 1 or hadith_number > config.TOTAL_HADITHS:
        raise HTTPException(
            status_code=400,
            detail=f"Hadith number must be between 1 and {config.TOTAL_HADITHS}"
        )
    
    sync_ar = load_sync_data(hadith_number, language="ar")
    sync_en = load_sync_data(hadith_number, language="en")
    transliteration = load_transliteration(hadith_number)
    
    if not sync_ar or not sync_en:
        raise HTTPException(status_code=404, detail="Sync data not found for this hadith")
    
    return {
        "hadith_number": hadith_number,
        "arabic": {
            "sync": sync_ar,
            "language": "ar"
        },
        "english": {
            "sync": sync_en,
            "language": "en"
        },
        "transliteration": transliteration,
        "description": "Both Arabic and English audio sync with transliteration for real-time word highlighting"
    }

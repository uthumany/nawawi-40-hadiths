"""
Enhanced Audio Endpoints Module for Nawawi's 40 Hadiths
Provides comprehensive English audio support with word-by-word synchronization.
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, List, Optional
import json
import os
from config import get_config

router = APIRouter(prefix="/audio", tags=["audio"])
config = get_config()

def load_sync_data(hadith_number: int, language: str = "en") -> Optional[Dict]:
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


@router.get("/english/config")
async def get_english_audio_config():
    """
    Get English audio configuration including base URL and available hadiths.
    
    Returns:
        - audio_base_url: Base URL for English audio files
        - total_hadiths: Total number of hadiths with English audio
        - format: Audio file format (mp3)
        - naming_convention: File naming pattern
    """
    return {
        "audio_base_url": config.AUDIO_BASE_URL,
        "language": "en",
        "language_name": "English",
        "total_hadiths": config.TOTAL_HADITHS,
        "format": config.AUDIO_FORMAT,
        "naming_convention": "Hadith_{number:02d}_English.mp3",
        "description": "English audio translation with word-level synchronization",
        "sync_available": True,
        "sync_directory": "sync_en"
    }


@router.get("/english/list")
async def list_english_audio():
    """
    Get a list of all available English audio files with metadata.
    
    Returns:
        List of hadith numbers with their audio URLs and sync data availability.
    """
    audio_files = []
    for i in range(1, config.TOTAL_HADITHS + 1):
        sync_data = load_sync_data(i, language="en")
        audio_files.append({
            "hadith_number": i,
            "audio_url": config.get_audio_url("en", i),
            "sync_url": config.get_sync_url("en", i),
            "sync_available": sync_data is not None,
            "sync_words_count": len(sync_data.get("words", [])) if sync_data else 0
        })
    return {
        "total_available": len(audio_files),
        "audio_files": audio_files
    }


@router.get("/english/hadith/{hadith_number}/metadata")
async def get_english_audio_metadata(hadith_number: int):
    """
    Get metadata for English audio of a specific hadith.
    
    Parameters:
        hadith_number: The hadith number (1-42)
    
    Returns:
        - hadith_number: The hadith number
        - audio_url: Direct URL to the audio file
        - sync_url: URL to the word-by-word sync data
        - sync_data: Embedded sync data with word timestamps
        - duration_estimate: Estimated audio duration based on last word timestamp
        - language: Language code (en)
    """
    if hadith_number < 1 or hadith_number > config.TOTAL_HADITHS:
        raise HTTPException(
            status_code=400,
            detail=f"Hadith number must be between 1 and {config.TOTAL_HADITHS}"
        )
    
    sync_data = load_sync_data(hadith_number, language="en")
    if not sync_data:
        raise HTTPException(
            status_code=404,
            detail=f"English audio metadata not found for hadith {hadith_number}"
        )
    
    # Calculate duration from last word's end time
    duration = 0
    if sync_data.get("words"):
        duration = sync_data["words"][-1].get("end", 0)
    
    return {
        "hadith_number": hadith_number,
        "audio_url": config.get_audio_url("en", hadith_number),
        "sync_url": config.get_sync_url("en", hadith_number),
        "language": "en",
        "format": "mp3",
        "duration_seconds": round(duration, 2),
        "sync_available": True,
        "total_words": len(sync_data.get("words", []))
    }


@router.get("/english/hadith/{hadith_number}/sync")
async def get_english_audio_sync(hadith_number: int):
    """
    Get complete word-by-word synchronization data for English audio.
    
    Parameters:
        hadith_number: The hadith number (1-42)
    
    Returns:
        - hadith_number: The hadith number
        - text: Full English text of the hadith
        - words: Array of word objects with timing information
            - word: The word text
            - start: Start time in seconds
            - end: End time in seconds
    """
    if hadith_number < 1 or hadith_number > config.TOTAL_HADITHS:
        raise HTTPException(
            status_code=400,
            detail=f"Hadith number must be between 1 and {config.TOTAL_HADITHS}"
        )
    
    sync_data = load_sync_data(hadith_number, language="en")
    if not sync_data:
        raise HTTPException(
            status_code=404,
            detail=f"English sync data not found for hadith {hadith_number}"
        )
    
    return sync_data


@router.get("/english/hadith/{hadith_number}/words")
async def get_english_audio_words(hadith_number: int):
    """
    Get only the word list with timing information for English audio.
    
    Parameters:
        hadith_number: The hadith number (1-42)
    
    Returns:
        - hadith_number: The hadith number
        - total_words: Total number of words
        - words: Array of word objects with timing
    """
    if hadith_number < 1 or hadith_number > config.TOTAL_HADITHS:
        raise HTTPException(
            status_code=400,
            detail=f"Hadith number must be between 1 and {config.TOTAL_HADITHS}"
        )
    
    sync_data = load_sync_data(hadith_number, language="en")
    if not sync_data:
        raise HTTPException(
            status_code=404,
            detail=f"English sync data not found for hadith {hadith_number}"
        )
    
    words = sync_data.get("words", [])
    return {
        "hadith_number": hadith_number,
        "total_words": len(words),
        "words": words
    }


@router.get("/english/hadith/{hadith_number}/word/{word_index}")
async def get_english_audio_word(hadith_number: int, word_index: int):
    """
    Get a specific word and its timing information from English audio.
    
    Parameters:
        hadith_number: The hadith number (1-42)
        word_index: The index of the word (0-based)
    
    Returns:
        - hadith_number: The hadith number
        - word_index: The index of the word
        - word: The word text
        - start: Start time in seconds
        - end: End time in seconds
        - duration: Duration of the word in seconds
    """
    if hadith_number < 1 or hadith_number > config.TOTAL_HADITHS:
        raise HTTPException(
            status_code=400,
            detail=f"Hadith number must be between 1 and {config.TOTAL_HADITHS}"
        )
    
    sync_data = load_sync_data(hadith_number, language="en")
    if not sync_data:
        raise HTTPException(
            status_code=404,
            detail=f"English sync data not found for hadith {hadith_number}"
        )
    
    words = sync_data.get("words", [])
    if word_index < 0 or word_index >= len(words):
        raise HTTPException(
            status_code=400,
            detail=f"Word index must be between 0 and {len(words) - 1}"
        )
    
    word_obj = words[word_index]
    return {
        "hadith_number": hadith_number,
        "word_index": word_index,
        "word": word_obj.get("word"),
        "start": word_obj.get("start"),
        "end": word_obj.get("end"),
        "duration": round(word_obj.get("end", 0) - word_obj.get("start", 0), 3)
    }


@router.get("/english/hadith/{hadith_number}/text-at-time/{time_seconds}")
async def get_english_audio_text_at_time(hadith_number: int, time_seconds: float):
    """
    Get the word being spoken at a specific time in the English audio.
    
    Parameters:
        hadith_number: The hadith number (1-42)
        time_seconds: The time in seconds
    
    Returns:
        - hadith_number: The hadith number
        - current_time: The requested time
        - current_word_index: Index of the word at this time
        - current_word: The word being spoken
        - current_word_start: Start time of the current word
        - current_word_end: End time of the current word
        - previous_word: Previous word (if available)
        - next_word: Next word (if available)
    """
    if hadith_number < 1 or hadith_number > config.TOTAL_HADITHS:
        raise HTTPException(
            status_code=400,
            detail=f"Hadith number must be between 1 and {config.TOTAL_HADITHS}"
        )
    
    sync_data = load_sync_data(hadith_number, language="en")
    if not sync_data:
        raise HTTPException(
            status_code=404,
            detail=f"English sync data not found for hadith {hadith_number}"
        )
    
    words = sync_data.get("words", [])
    current_word_index = -1
    
    # Find the word at the given time
    for i, word_obj in enumerate(words):
        if word_obj.get("start", 0) <= time_seconds < word_obj.get("end", 0):
            current_word_index = i
            break
    
    result = {
        "hadith_number": hadith_number,
        "current_time": time_seconds,
        "current_word_index": current_word_index,
        "current_word": None,
        "current_word_start": None,
        "current_word_end": None,
        "previous_word": None,
        "next_word": None
    }
    
    if current_word_index >= 0:
        current_word_obj = words[current_word_index]
        result["current_word"] = current_word_obj.get("word")
        result["current_word_start"] = current_word_obj.get("start")
        result["current_word_end"] = current_word_obj.get("end")
        
        if current_word_index > 0:
            prev_word_obj = words[current_word_index - 1]
            result["previous_word"] = {
                "index": current_word_index - 1,
                "word": prev_word_obj.get("word"),
                "start": prev_word_obj.get("start"),
                "end": prev_word_obj.get("end")
            }
        
        if current_word_index < len(words) - 1:
            next_word_obj = words[current_word_index + 1]
            result["next_word"] = {
                "index": current_word_index + 1,
                "word": next_word_obj.get("word"),
                "start": next_word_obj.get("start"),
                "end": next_word_obj.get("end")
            }
    
    return result


@router.get("/english/hadith/{hadith_number}/search")
async def search_english_audio_words(hadith_number: int, query: str):
    """
    Search for words in the English audio sync data.
    
    Parameters:
        hadith_number: The hadith number (1-42)
        query: Search query (case-insensitive)
    
    Returns:
        - hadith_number: The hadith number
        - query: The search query
        - results: List of matching words with their indices and timing
    """
    if hadith_number < 1 or hadith_number > config.TOTAL_HADITHS:
        raise HTTPException(
            status_code=400,
            detail=f"Hadith number must be between 1 and {config.TOTAL_HADITHS}"
        )
    
    sync_data = load_sync_data(hadith_number, language="en")
    if not sync_data:
        raise HTTPException(
            status_code=404,
            detail=f"English sync data not found for hadith {hadith_number}"
        )
    
    words = sync_data.get("words", [])
    query_lower = query.lower()
    results = []
    
    for i, word_obj in enumerate(words):
        word_text = word_obj.get("word", "").lower()
        if query_lower in word_text:
            results.append({
                "index": i,
                "word": word_obj.get("word"),
                "start": word_obj.get("start"),
                "end": word_obj.get("end"),
                "match_position": word_text.find(query_lower)
            })
    
    return {
        "hadith_number": hadith_number,
        "query": query,
        "total_matches": len(results),
        "results": results
    }

"""
Configuration module for Nawawi's 40 Hadiths API.
Manages base URLs, endpoints, and environment variables.
"""

import os
from typing import Dict, List

class Config:
    """API Configuration class."""
    
    # Audio hosting configuration
    AUDIO_BASE_URL = os.getenv(
        "AUDIO_BASE_URL",
        "https://raw.githubusercontent.com/uthumany/nawawi-40-hadiths/main/audio"
    )
    
    # API base URL
    API_BASE_URL = os.getenv(
        "API_BASE_URL",
        "https://uthumany.github.io/nawawi-40-hadiths/api"
    )
    
    # Server configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    
    # API metadata
    API_TITLE = "Nawawi's 40 Hadiths API"
    API_VERSION = "2.0.0"
    API_DESCRIPTION = "RESTful API for accessing the 40 Hadiths of Imam Nawawi with audio and word-by-word synchronization"
    
    # Hadith configuration
    TOTAL_HADITHS = 42
    SUPPORTED_LANGUAGES = ["ar", "en"]
    
    # Audio configuration
    AUDIO_FORMAT = "mp3"
    AUDIO_LANGUAGES = {
        "ar": {
            "name": "Arabic",
            "directory": "arabic",
            "sync_directory": "sync",
            "description": "Arabic audio recitation"
        },
        "en": {
            "name": "English",
            "directory": "english",
            "sync_directory": "sync_en",
            "description": "English audio translation"
        }
    }
    
    @classmethod
    def get_audio_url(cls, language: str, hadith_number: int) -> str:
        """Get the audio URL for a specific hadith and language."""
        if language not in cls.AUDIO_LANGUAGES:
            raise ValueError(f"Unsupported language: {language}")
        
        audio_dir = cls.AUDIO_LANGUAGES[language]["directory"]
        
        if language == "ar":
            # Arabic audio uses different naming convention
            return f"{cls.AUDIO_BASE_URL}/{audio_dir}/hadith_{hadith_number:02d}.mp3"
        else:
            # English audio
            return f"{cls.AUDIO_BASE_URL}/{audio_dir}/Hadith_{hadith_number:02d}_English.mp3"
    
    @classmethod
    def get_sync_url(cls, language: str, hadith_number: int) -> str:
        """Get the sync data URL for a specific hadith and language."""
        if language not in cls.AUDIO_LANGUAGES:
            raise ValueError(f"Unsupported language: {language}")
        
        sync_dir = cls.AUDIO_LANGUAGES[language]["sync_directory"]
        return f"{cls.API_BASE_URL}/{sync_dir}/hadith_{hadith_number}.json"
    
    @classmethod
    def get_config_dict(cls) -> Dict:
        """Get configuration as a dictionary."""
        return {
            "title": cls.API_TITLE,
            "version": cls.API_VERSION,
            "description": cls.API_DESCRIPTION,
            "audio_base_url": cls.AUDIO_BASE_URL,
            "api_base_url": cls.API_BASE_URL,
            "total_hadiths": cls.TOTAL_HADITHS,
            "supported_languages": cls.SUPPORTED_LANGUAGES,
            "audio_languages": cls.AUDIO_LANGUAGES,
            "endpoints": cls.get_endpoints_dict()
        }
    
    @classmethod
    def get_endpoints_dict(cls) -> Dict[str, str]:
        """Get all available endpoints."""
        return {
            "root": "/",
            "config": "/config",
            "all_hadiths": "/hadiths",
            "single_hadith": "/hadiths/{number}",
            "hadith_full": "/hadiths/{number}/full",
            "english_audio": "/hadiths/{number}/audio/english",
            "english_sync": "/hadiths/{number}/sync/english",
            "arabic_sync": "/hadiths/{number}/sync/arabic",
            "audio_file": "/audio/english/{hadith_number}"
        }


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = True
    TESTING = True


def get_config(environment: str = None) -> Config:
    """Get configuration based on environment."""
    if environment is None:
        environment = os.getenv("ENVIRONMENT", "development").lower()
    
    config_map = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig
    }
    
    return config_map.get(environment, DevelopmentConfig)()

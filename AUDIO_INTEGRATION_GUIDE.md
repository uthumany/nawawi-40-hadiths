# Audio Integration and Word-by-Word Highlighting Guide

## Overview

This document describes the new audio integration features added to the Nawawi's 40 Hadiths API, including support for English audio files and word-by-word text synchronization for both Arabic and English versions.

## Base URLs

The API and audio assets are hosted at the following base URLs:

| Service | Base URL |
|---------|----------|
| **API Base URL** | `https://uthumany.github.io/nawawi-40-hadiths/api` |
| **Audio Base URL** | `https://raw.githubusercontent.com/uthumany/nawawi-40-hadiths/main/audio` |

## New Features

### 1. English Audio Support

All 42 hadiths now have English audio recordings available. The audio files are stored in the `/audio/english/` directory with the naming convention: `Hadith_{number:02d}_English.mp3`

**Example:** Hadith 1 audio file: `Hadith_01_English.mp3`

### 2. Word-by-Word Synchronization

Two synchronization datasets are available:

- **Arabic Sync** (`/api/sync/`): Word-level timestamps for Arabic audio
- **English Sync** (`/api/sync_en/`): Word-level timestamps for English audio

Each sync file contains:
- `hadith_number`: The hadith number (1-42)
- `text`: Full text of the hadith in the respective language
- `words`: Array of word objects with timing information

#### Sync Data Structure

```json
{
  "hadith_number": 1,
  "text": "Full text of the hadith...",
  "words": [
    {
      "word": "word_text",
      "start": 0.0,
      "end": 0.64
    },
    {
      "word": "next_word",
      "start": 0.64,
      "end": 1.22
    }
  ]
}
```

## API Endpoints

### Configuration Endpoint

**GET** `/config`

Returns API configuration including base URLs and supported languages.

```json
{
  "audio_base_url": "https://raw.githubusercontent.com/uthumany/nawawi-40-hadiths/main/audio",
  "api_base_url": "https://uthumany.github.io/nawawi-40-hadiths/api",
  "supported_languages": ["ar", "en"],
  "total_hadiths": 42
}
```

### English Audio Endpoint

**GET** `/hadiths/{number}/audio/english`

Get English audio URL and metadata for a specific hadith.

**Parameters:**
- `number` (integer): Hadith number (1-42)

**Response:**
```json
{
  "hadith_number": 1,
  "title": "Actions Are By Intention",
  "audio_url": "https://raw.githubusercontent.com/uthumany/nawawi-40-hadiths/main/audio/english/Hadith_01_English.mp3",
  "sync_url": "https://uthumany.github.io/nawawi-40-hadiths/api/sync_en/hadith_1.json",
  "language": "en"
}
```

### English Sync Endpoint

**GET** `/hadiths/{number}/sync/english`

Get word-by-word synchronization data for English audio.

**Parameters:**
- `number` (integer): Hadith number (1-42)

**Response:** Word-by-word sync data with timestamps

### Arabic Sync Endpoint

**GET** `/hadiths/{number}/sync/arabic`

Get word-by-word synchronization data for Arabic audio.

**Parameters:**
- `number` (integer): Hadith number (1-42)

**Response:** Word-by-word sync data with timestamps

### Full Hadith Endpoint

**GET** `/hadiths/{number}/full`

Get complete hadith data including both Arabic and English audio with synchronization.

**Parameters:**
- `number` (integer): Hadith number (1-42)

**Response:**
```json
{
  "hadith_number": 1,
  "title": "Actions Are By Intention",
  "narrator": "ʿUmar bin al-Khaṭṭāb",
  "source": "al-Bukhārī, Muslim",
  "arabic_text": "...",
  "english_translation": "...",
  "audio": {
    "english": {
      "url": "https://raw.githubusercontent.com/uthumany/nawawi-40-hadiths/main/audio/english/Hadith_01_English.mp3",
      "sync_url": "https://uthumany.github.io/nawawi-40-hadiths/api/sync_en/hadith_1.json",
      "sync": { /* sync data */ }
    },
    "arabic": {
      "url": "https://raw.githubusercontent.com/uthumany/audio-hosting/main/hadith_01.mp3",
      "sync_url": "https://uthumany.github.io/nawawi-40-hadiths/api/sync/hadith_1.json",
      "sync": { /* sync data */ }
    }
  }
}
```

### Direct Audio File Endpoint

**GET** `/audio/english/{hadith_number}`

Serve English audio file directly.

**Parameters:**
- `hadith_number` (integer): Hadith number (1-42)

**Response:** MP3 audio file

## Frontend Implementation

Working frontend assets are available in the repository under `/frontend/assets/`:
- `hadith-player.js`: JavaScript implementation for both Arabic and English highlighting.
- `hadith-player.css`: CSS styling for both Arabic (RTL) and English (LTR) layouts.

### Usage Example

```javascript
// Initialize the player
const player = new HadithPlayer('hadith-text-container');

// Load Hadith 1 in English
await player.loadHadith(1, 'en');

// Play the audio
player.play();

// Load Hadith 1 in Arabic
await player.loadHadith(1, 'ar');
```

### CSS Highlighting

The player uses the `.highlighted` class to indicate the currently spoken word. You can customize this in `hadith-player.css`.

```css
.hadith-word.highlighted {
    background-color: #4caf50; /* Green highlight */
    color: #ffffff;
    font-weight: bold;
}
```

## Environment Variables

Configure the API using environment variables:

```bash
# Audio hosting base URL
AUDIO_BASE_URL=https://raw.githubusercontent.com/uthumany/nawawi-40-hadiths/main/audio

# API base URL
API_BASE_URL=https://uthumany.github.io/nawawi-40-hadiths/api

# Server configuration
HOST=0.0.0.0
PORT=8000
```

## Directory Structure

```
nawawi-40-hadiths/
├── api/
│   ├── sync/              # Arabic word-by-word sync data
│   └── sync_en/           # English word-by-word sync data
├── audio/
│   └── english/           # English audio files
├── frontend/
│   └── assets/            # Frontend JS and CSS assets
├── data/
│   └── hadiths.json       # Hadith content data
├── main.py                # FastAPI application
└── config.py              # API configuration module
```

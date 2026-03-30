# Audio Integration and Word-by-Word Highlighting Guide

## Overview

This document describes the new audio integration features added to the Nawawi's 40 Hadiths API, including support for English audio files and word-by-word text synchronization for both Arabic and English versions.

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
      "sync": { /* sync data */ }
    },
    "arabic": {
      "url": "https://raw.githubusercontent.com/uthumany/audio-hosting/main/hadith_01.mp3",
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

## Implementation Guide

### Frontend Implementation for Word-by-Word Highlighting

Here's an example of how to implement word-by-word highlighting in a frontend application:

```javascript
// Fetch sync data and audio
async function loadHadithAudio(hadithNumber) {
  const response = await fetch(`/hadiths/${hadithNumber}/full`);
  const hadith = await response.json();
  
  const audioElement = new Audio(hadith.audio.english.url);
  const syncData = hadith.audio.english.sync;
  
  // Highlight words as audio plays
  audioElement.addEventListener('timeupdate', () => {
    const currentTime = audioElement.currentTime;
    
    syncData.words.forEach((word, index) => {
      const wordElement = document.getElementById(`word-${index}`);
      
      if (currentTime >= word.start && currentTime < word.end) {
        wordElement.classList.add('highlighted');
      } else {
        wordElement.classList.remove('highlighted');
      }
    });
  });
  
  return { audioElement, syncData };
}

// Render text with word elements
function renderTextWithWords(syncData) {
  const container = document.getElementById('text-container');
  
  syncData.words.forEach((word, index) => {
    const span = document.createElement('span');
    span.id = `word-${index}`;
    span.textContent = word.word + ' ';
    span.style.cursor = 'pointer';
    
    // Allow seeking to word
    span.addEventListener('click', () => {
      audioElement.currentTime = word.start;
    });
    
    container.appendChild(span);
  });
}
```

### CSS for Highlighting

```css
#text-container span {
  transition: background-color 0.1s ease;
}

#text-container span.highlighted {
  background-color: #FFD700;
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
│   │   ├── hadith_1.json
│   │   ├── hadith_2.json
│   │   └── ...
│   └── sync_en/           # English word-by-word sync data
│       ├── hadith_1.json
│       ├── hadith_2.json
│       └── ...
├── audio/
│   └── english/           # English audio files
│       ├── Hadith_01_English.mp3
│       ├── Hadith_02_English.mp3
│       └── ...
├── data/
│   └── hadiths.json       # Hadith content data
├── main.py                # FastAPI application
└── .env.example           # Environment configuration template
```

## Running the API

### Development

```bash
# Install dependencies
pip install fastapi uvicorn python-dotenv

# Run the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production

```bash
# Using Gunicorn with Uvicorn workers
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Testing the Endpoints

### Using curl

```bash
# Get configuration
curl http://localhost:8000/config

# Get English audio for hadith 1
curl http://localhost:8000/hadiths/1/audio/english

# Get English sync data for hadith 1
curl http://localhost:8000/hadiths/1/sync/english

# Get full hadith data with audio
curl http://localhost:8000/hadiths/1/full

# Download English audio file
curl -O http://localhost:8000/audio/english/1
```

### Using Python

```python
import requests

# Get full hadith data
response = requests.get('http://localhost:8000/hadiths/1/full')
hadith = response.json()

# Access audio URLs
english_audio_url = hadith['audio']['english']['url']
english_sync = hadith['audio']['english']['sync']

# Print word timings
for word in english_sync['words']:
    print(f"{word['word']}: {word['start']}s - {word['end']}s")
```

## Audio Specifications

- **Format:** MP3
- **Encoding:** Standard MP3 encoding
- **Sample Rate:** 44.1 kHz (typical)
- **Bitrate:** 128-192 kbps (typical)
- **Language:** English
- **Total Hadiths:** 42

## Sync Data Generation

The English sync data was generated using OpenAI's Whisper model with word-level timestamp extraction. This provides accurate word-by-word timing information for implementing audio-text synchronization features.

### Regenerating Sync Data

If you need to regenerate the sync data:

```bash
# Install Whisper
pip install openai-whisper

# Run the sync generation script
python generate_sync.py
```

## Future Enhancements

- Support for additional languages
- Improved sync accuracy using manual correction
- Real-time audio streaming
- Batch audio processing
- Advanced search with audio timestamps
- User annotations with timestamps

## Support

For issues or questions about the audio integration, please open an issue on the GitHub repository.

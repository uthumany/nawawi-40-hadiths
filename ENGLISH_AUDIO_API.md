# English Audio API Documentation

## Overview

The English Audio API provides comprehensive endpoints for accessing English audio files and word-by-word synchronization data for all 42 hadiths. This documentation covers all available endpoints, their parameters, and response formats.

## Base URLs

| Service | URL |
|---------|-----|
| **API Base URL** | `https://uthumany.github.io/nawawi-40-hadiths` |
| **Audio Base URL** | `https://raw.githubusercontent.com/uthumany/nawawi-40-hadiths/main/audio` |

## Audio Files

All English audio files are stored in MP3 format with the naming convention:
```
Hadith_{number:02d}_English.mp3
```

**Example:** `Hadith_01_English.mp3` for Hadith 1

## Endpoints

### 1. Audio Configuration Endpoint

**GET** `/audio/english/config`

Get English audio configuration including base URL and available hadiths.

**Response:**
```json
{
  "audio_base_url": "https://raw.githubusercontent.com/uthumany/nawawi-40-hadiths/main/audio",
  "language": "en",
  "language_name": "English",
  "total_hadiths": 42,
  "format": "mp3",
  "naming_convention": "Hadith_{number:02d}_English.mp3",
  "description": "English audio translation with word-level synchronization",
  "sync_available": true,
  "sync_directory": "sync_en"
}
```

---

### 2. List All English Audio Files

**GET** `/audio/english/list`

Get a list of all available English audio files with metadata.

**Response:**
```json
{
  "total_available": 42,
  "audio_files": [
    {
      "hadith_number": 1,
      "audio_url": "https://raw.githubusercontent.com/uthumany/nawawi-40-hadiths/main/audio/english/Hadith_01_English.mp3",
      "sync_url": "https://uthumany.github.io/nawawi-40-hadiths/api/sync_en/hadith_1.json",
      "sync_available": true,
      "sync_words_count": 145
    },
    {
      "hadith_number": 2,
      "audio_url": "https://raw.githubusercontent.com/uthumany/nawawi-40-hadiths/main/audio/english/Hadith_02_English.mp3",
      "sync_url": "https://uthumany.github.io/nawawi-40-hadiths/api/sync_en/hadith_2.json",
      "sync_available": true,
      "sync_words_count": 203
    }
    // ... more hadiths
  ]
}
```

---

### 3. Get Audio Metadata

**GET** `/audio/english/{hadith_number}/metadata`

Get metadata for English audio of a specific hadith.

**Parameters:**
- `hadith_number` (integer): The hadith number (1-42)

**Response:**
```json
{
  "hadith_number": 1,
  "audio_url": "https://raw.githubusercontent.com/uthumany/nawawi-40-hadiths/main/audio/english/Hadith_01_English.mp3",
  "sync_url": "https://uthumany.github.io/nawawi-40-hadiths/api/sync_en/hadith_1.json",
  "language": "en",
  "format": "mp3",
  "duration_seconds": 49.66,
  "sync_available": true,
  "total_words": 145
}
```

---

### 4. Get Complete Sync Data

**GET** `/audio/english/{hadith_number}/sync`

Get complete word-by-word synchronization data for English audio.

**Parameters:**
- `hadith_number` (integer): The hadith number (1-42)

**Response:**
```json
{
  "hadith_number": 1,
  "text": "On the authority of the commander of the faithful, Abu Haths, Omar, Ibn Al-Qatab...",
  "words": [
    {
      "word": "On",
      "start": 0.0,
      "end": 0.64
    },
    {
      "word": "the",
      "start": 0.64,
      "end": 0.74
    },
    {
      "word": "authority",
      "start": 0.74,
      "end": 1.22
    }
    // ... more words
  ]
}
```

---

### 5. Get Word List Only

**GET** `/audio/english/{hadith_number}/words`

Get only the word list with timing information for English audio.

**Parameters:**
- `hadith_number` (integer): The hadith number (1-42)

**Response:**
```json
{
  "hadith_number": 1,
  "total_words": 145,
  "words": [
    {
      "word": "On",
      "start": 0.0,
      "end": 0.64
    },
    {
      "word": "the",
      "start": 0.64,
      "end": 0.74
    }
    // ... more words
  ]
}
```

---

### 6. Get Specific Word

**GET** `/audio/english/{hadith_number}/word/{word_index}`

Get a specific word and its timing information from English audio.

**Parameters:**
- `hadith_number` (integer): The hadith number (1-42)
- `word_index` (integer): The index of the word (0-based)

**Response:**
```json
{
  "hadith_number": 1,
  "word_index": 0,
  "word": "On",
  "start": 0.0,
  "end": 0.64,
  "duration": 0.64
}
```

---

### 7. Get Word at Specific Time

**GET** `/audio/english/{hadith_number}/text-at-time/{time_seconds}`

Get the word being spoken at a specific time in the English audio.

**Parameters:**
- `hadith_number` (integer): The hadith number (1-42)
- `time_seconds` (float): The time in seconds

**Response:**
```json
{
  "hadith_number": 1,
  "current_time": 5.5,
  "current_word_index": 10,
  "current_word": "Haths,",
  "current_word_start": 4.76,
  "current_word_end": 5.5,
  "previous_word": {
    "index": 9,
    "word": "Abu",
    "start": 4.54,
    "end": 4.76
  },
  "next_word": {
    "index": 11,
    "word": "Omar,",
    "start": 5.6,
    "end": 5.94
  }
}
```

---

### 8. Search Words

**GET** `/audio/english/{hadith_number}/search?query={search_query}`

Search for words in the English audio sync data.

**Parameters:**
- `hadith_number` (integer): The hadith number (1-42)
- `query` (string): Search query (case-insensitive)

**Response:**
```json
{
  "hadith_number": 1,
  "query": "intention",
  "total_matches": 3,
  "results": [
    {
      "index": 43,
      "word": "intention,",
      "start": 21.14,
      "end": 21.7,
      "match_position": 0
    },
    {
      "index": 50,
      "word": "intended.",
      "start": 26.14,
      "end": 26.54,
      "match_position": 0
    }
    // ... more matches
  ]
}
```

---

### 9. Direct Audio File Endpoint

**GET** `/audio/english/{hadith_number}`

Serve English audio file directly from the server.

**Parameters:**
- `hadith_number` (integer): The hadith number (1-42)

**Response:** MP3 audio file with `Content-Type: audio/mpeg`

---

### 10. Get Hadith English Audio Info

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
  "language": "en",
  "description": "English audio translation with word-level synchronization"
}
```

---

### 11. Get Hadith English Sync Data

**GET** `/hadiths/{number}/sync/english`

Get word-by-word synchronization data for English audio.

**Parameters:**
- `number` (integer): Hadith number (1-42)

**Response:** Word-by-word sync data with timestamps (same format as endpoint #4)

---

### 12. Get Complete Hadith Data

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
      "sync": {
        "hadith_number": 1,
        "text": "...",
        "words": [ /* word data */ ]
      },
      "language": "en",
      "description": "English audio translation"
    },
    "arabic": {
      "url": "https://raw.githubusercontent.com/uthumany/audio-hosting/main/hadith_01.mp3",
      "sync_url": "https://uthumany.github.io/nawawi-40-hadiths/api/sync/hadith_1.json",
      "sync": {
        "hadith_number": 1,
        "text": "...",
        "words": [ /* word data */ ]
      },
      "language": "ar",
      "description": "Arabic audio recitation"
    }
  }
}
```

---

## Sync Data Format

All sync endpoints return data in the following format:

```json
{
  "hadith_number": 1,
  "text": "Full text of the hadith in English...",
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

### Field Descriptions

- **hadith_number** (integer): The hadith number (1-42)
- **text** (string): Full English text of the hadith
- **words** (array): Array of word objects
  - **word** (string): The word text as spoken in the audio
  - **start** (float): Start time in seconds
  - **end** (float): End time in seconds

---

## Usage Examples

### JavaScript Example

```javascript
// Load and display hadith with word highlighting
const player = new HadithPlayerEnhanced('hadith-container');

// Load hadith 1 in English
await player.loadHadith(1, 'en');

// Play the audio
player.play();

// Search for a word
const results = player.searchWords('intention');
console.log(`Found ${results.length} matches`);

// Get word at specific time
const word = player.getWordAtTime(5.5);
console.log(`At 5.5 seconds: ${word.word}`);

// Set playback speed
player.setPlaybackSpeed(1.5);
```

### Fetch API Example

```javascript
// Get English audio metadata
const response = await fetch('/audio/english/1/metadata');
const metadata = await response.json();
console.log(`Duration: ${metadata.duration_seconds} seconds`);
console.log(`Total words: ${metadata.total_words}`);

// Get sync data
const syncResponse = await fetch('/audio/english/1/sync');
const syncData = await syncResponse.json();
console.log(`Hadith text: ${syncData.text}`);

// Search for words
const searchResponse = await fetch('/audio/english/1/search?query=intention');
const searchResults = await searchResponse.json();
console.log(`Found ${searchResults.total_matches} matches`);
```

### cURL Example

```bash
# Get audio configuration
curl https://uthumany.github.io/nawawi-40-hadiths/audio/english/config

# Get metadata for hadith 1
curl https://uthumany.github.io/nawawi-40-hadiths/audio/english/1/metadata

# Get sync data for hadith 1
curl https://uthumany.github.io/nawawi-40-hadiths/audio/english/1/sync

# Search for words
curl "https://uthumany.github.io/nawawi-40-hadiths/audio/english/1/search?query=intention"

# Download audio file
curl -o hadith_01.mp3 https://uthumany.github.io/nawawi-40-hadiths/audio/english/1
```

---

## Error Responses

All endpoints return appropriate HTTP status codes:

| Status Code | Description |
|-------------|-------------|
| **200** | Successful request |
| **400** | Bad request (invalid hadith number, word index, etc.) |
| **404** | Resource not found (hadith or sync data doesn't exist) |
| **500** | Server error |

### Error Response Format

```json
{
  "detail": "Hadith number must be between 1 and 42"
}
```

---

## Rate Limiting

There are no rate limits on the API. Feel free to make as many requests as needed.

---

## CORS Support

All endpoints support CORS (Cross-Origin Resource Sharing), allowing requests from any domain.

---

## Caching

Audio files and sync data are cached by CDN. For optimal performance:

- Audio files are cached for 30 days
- Sync data is cached for 7 days

---

## Frontend Integration

### Using the Enhanced Player

```html
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="hadith-player-enhanced.css">
</head>
<body>
    <div id="hadith-container"></div>
    
    <script src="hadith-player-enhanced.js"></script>
    <script>
        const player = new HadithPlayerEnhanced('hadith-container');
        
        player.loadHadith(1, 'en').then(() => {
            player.play();
        });
    </script>
</body>
</html>
```

---

## Support

For issues, questions, or suggestions, please open an issue on the GitHub repository:
https://github.com/uthumany/nawawi-40-hadiths

---

## License

This API and all associated content are provided under the same license as the main repository.

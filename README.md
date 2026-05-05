# Nawawi's Forty Hadiths API

A complete JSON API for Imam al-Nawawi's Forty Hadiths, including Arabic text, English translation, audio URLs, and word-by-word synchronization data for highlighting.

## API Endpoints

### Base URLs
- **Main API**: `https://uthumany.github.io/nawawi-40-hadiths/api`
- **Audio Hosting**: `https://raw.githubusercontent.com/uthumany/nawawi-40-hadiths/main/audio`
- **Sync Data (Arabic)**: `https://uthumany.github.io/nawawi-40-hadiths/api/sync`
- **Sync Data (English)**: `https://uthumany.github.io/nawawi-40-hadiths/api/sync_en`
- **Transliteration Data**: `https://uthumany.github.io/nawawi-40-hadiths/api/transliterations.json`
- **Hadith Covers Data**: `https://uthumany.github.io/nawawi-40-hadiths/api/hadith_covers.json`

### Endpoints
- **All Hadiths (Arabic Focus)**: [hadiths.json](https://uthumany.github.io/nawawi-40-hadiths/api/hadiths.json)
- **All Hadiths (English Focus)**: [all_english.json](https://uthumany.github.io/nawawi-40-hadiths/api/all_english.json)
- **Individual Hadith**: `https://uthumany.github.io/nawawi-40-hadiths/api/hadith_{number}.json` (e.g., [hadith_1.json](https://uthumany.github.io/nawawi-40-hadiths/api/hadith_1.json))
- **Word-by-Word Sync (Arabic)**: `https://uthumany.github.io/nawawi-40-hadiths/api/sync/hadith_{number}.json` (e.g., [hadith_1.json](https://uthumany.github.io/nawawi-40-hadiths/api/sync/hadith_1.json))
- **Word-by-Word Sync (English)**: `https://uthumany.github.io/nawawi-40-hadiths/api/sync_en/hadith_{number}.json` (e.g., [hadith_1.json](https://uthumany.github.io/nawawi-40-hadiths/api/sync_en/hadith_1.json))
- **English Audio URL**: `https://raw.githubusercontent.com/uthumany/nawawi-40-hadiths/main/audio/english/Hadith_{number:02d}_English.mp3` (e.g., [Hadith_01_English.mp3](https://raw.githubusercontent.com/uthumany/nawawi-40-hadiths/main/audio/english/Hadith_01_English.mp3))
- **Full Hadith Payload (with English audio + sync)**: `/hadiths/{number}/full`
- **All Transliterations**: `/transliterations`
- **Individual Transliteration**: `/transliterations/{number}`
- **Enhanced Sync with Transliteration (English)**: `/sync-transliteration/hadith/{hadith_number}/english`
- **Enhanced Sync with Transliteration (Arabic)**: `/sync-transliteration/hadith/{hadith_number}/arabic`
- **Enhanced Sync with Transliteration (Both)**: `/sync-transliteration/hadith/{hadith_number}/both`
- **Hadith Cover Images**: `/hadiths/covers` or [hadith_covers.json](https://uthumany.github.io/nawawi-40-hadiths/api/hadith_covers.json)

## Features

- **Complete Data**: Includes metadata, narrator, source, Arabic text, English translation, and Arabic transliteration.
- **Audio Integration**: Direct links to high-quality Arabic recitations and English translations.
- **Word-by-Word Highlighting**: Precise timestamps for every word in both Arabic and English texts to enable synchronized highlighting during audio playback.
- **Arabic Transliteration**: Provides clean, consistent, and human-readable transliteration for all Arabic texts.
- **Enhanced Sync**: New endpoints combine audio sync data with transliteration for a richer real-time highlighting experience.

## Implementation Guide: Word-by-Word Highlighting & Transliteration

To implement highlighting and transliteration in your application, you can use the provided `HadithPlayerWithTransliteration` class:

1.  **Include Assets**: Ensure you include `hadith-player-enhanced.js`, `hadith-player-transliteration.js`, and `hadith-player-transliteration.css` in your frontend.
2.  **Initialize Player**: Create an instance of `HadithPlayerWithTransliteration`, providing container IDs for both the main hadith text and the transliteration text.
3.  **Load Hadith**: Use the `loadHadith` method to fetch data and render the player.

```javascript
// Example usage for HadithPlayerWithTransliteration
import { HadithPlayerWithTransliteration } from \'./hadith-player-transliteration.js\';

const player = new HadithPlayerWithTransliteration(
    \'hadith-text-container\', 
    \'transliteration-container\', 
    { 
        language: \'ar\', // or \'en\'
        apiBaseUrl: \'https://uthumany.github.io/nawawi-40-hadiths/api\'
    }
);

// Load Hadith 1 in Arabic
player.loadHadith(1, \'ar\')
    .then(() => {
        console.log(\'Hadith loaded and player ready.\');
        // You can now play the audio
        // player.play();
    })
    .catch(error => console.error(\'Failed to load hadith:\', error));

// To manually implement highlighting without the class:
// 1. Fetch Hadith Data from `/hadiths/{number}/full`.
// 2. Fetch Enhanced Sync Data from `/sync-transliteration/hadith/{hadith_number}/english` or `/arabic`.
// 3. Sync Playback:
//    - Listen to the `timeupdate` event of your audio player.
//    - Match the `currentTime` with the `start` and `end` timestamps in the sync JSON.
//    - Highlight the corresponding word in both the original text and the transliteration UI.
```

## Data Structure

### Hadith Object
```json
{
  "hadith_number": 1,
  "title": "Actions Are By Intention",
  "narrator": "ʿUmar bin al-Khaṭṭāb",
  "source": "al-Bukhārī, Muslim",
  "arabic_text": "...",
  "english_translation": "...",
  "audio_url": "...",
  "sync_url": "...",
  "english_audio_url": "...",
  "english_sync_url": "..."
}
```

### Transliteration Object
```json
{
  "hadith_number": 1,
  "title": "",
  "narrator": "ʿ",
  "source": "",
  "Arabic_Transliteration_text": ""
}
```

### Enhanced Sync Payload (Example for English)
```json
{
  "hadith_number": 1,
  "language": "en",
  "sync": {
    "text": "...",
    "words": [
      { "word": "From", "start": 0.5, "end": 0.8 },
      ...
    ]
  },
  "transliteration": {
    "hadith_number": 1,
    "title": "Actions Are By Intention",
    "narrator": "ʿUmar bin al-Khaṭṭāb",
    "source": "al-Bukhārī, Muslim",
    "Arabic_Transliteration_text": "Al-ḥadīth al-awwal ʿan Amīr al-muʾminīn..."
  },
  "description": "English audio sync with Arabic transliteration for real-time word highlighting"
}
```

### Sync Object
```json
{
  "hadith_number": 1,
  "text": "...",
  "words": [
    { "word": "From", "start": 0.5, "end": 0.8 },
    ...
  ]
}
```

### Hadith Cover Object
```json
{
  "hadith_number": 1,
  "title": "Actions Are By Intention",
  "narrator": "ʿUmar bin al-Khaṭṭāb",
  "source": "al-Bukhārī, Muslim",
  "book_cover_url": "https://..."
}
```

---
*Maintained by [uthumany](https://github.com/uthumany)*

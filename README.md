# Nawawi's Forty Hadiths API

A complete JSON API for Imam al-Nawawi's Forty Hadiths, including Arabic text, English translation, audio URLs, and word-by-word synchronization data for highlighting.

## API Endpoints

### Base URLs
- **Main API**: `https://uthumany.github.io/nawawi-40-hadiths/api`
- **Audio Hosting**: `https://raw.githubusercontent.com/uthumany/nawawi-40-hadiths/main/audio`
- **Sync Data (Arabic)**: `https://uthumany.github.io/nawawi-40-hadiths/api/sync`
- **Sync Data (English)**: `https://uthumany.github.io/nawawi-40-hadiths/api/sync_en`

### Endpoints
- **All Hadiths (Arabic Focus)**: [hadiths.json](https://uthumany.github.io/nawawi-40-hadiths/api/hadiths.json)
- **All Hadiths (English Focus)**: [all_english.json](https://uthumany.github.io/nawawi-40-hadiths/api/all_english.json)
- **Individual Hadith**: `https://uthumany.github.io/nawawi-40-hadiths/api/hadith_{number}.json` (e.g., [hadith_1.json](https://uthumany.github.io/nawawi-40-hadiths/api/hadith_1.json))
- **Word-by-Word Sync (Arabic)**: `https://uthumany.github.io/nawawi-40-hadiths/api/sync/hadith_{number}.json` (e.g., [hadith_1.json](https://uthumany.github.io/nawawi-40-hadiths/api/sync/hadith_1.json))
- **Word-by-Word Sync (English)**: `https://uthumany.github.io/nawawi-40-hadiths/api/sync_en/hadith_{number}.json` (e.g., [hadith_1.json](https://uthumany.github.io/nawawi-40-hadiths/api/sync_en/hadith_1.json))
- **English Audio URL**: `https://raw.githubusercontent.com/uthumany/nawawi-40-hadiths/main/audio/english/Hadith_{number:02d}_English.mp3` (e.g., [Hadith_01_English.mp3](https://raw.githubusercontent.com/uthumany/nawawi-40-hadiths/main/audio/english/Hadith_01_English.mp3))
- **Full Hadith Payload (with English audio + sync)**: `/hadiths/{number}/full`

## Features

- **Complete Data**: Includes metadata, narrator, source, Arabic text, and English translation.
- **Audio Integration**: Direct links to high-quality Arabic recitations and English translations.
- **Word-by-Word Highlighting**: Precise timestamps for every word in both Arabic and English texts to enable synchronized highlighting during audio playback.

## Implementation Guide: Word-by-Word Highlighting

To implement highlighting in your application:

1.  **Fetch Hadith Data**: Get the Hadith details from the main API.
2.  **Fetch Sync Data**: Use the `sync_url` (Arabic) or `english_sync_url` (English) provided in the Hadith JSON.
3.  **Sync Playback**:
    - Listen to the `timeupdate` event of your audio player.
    - Match the `currentTime` with the `start` and `end` timestamps in the sync JSON.
    - Highlight the corresponding word in your UI.

```javascript
// Example logic for English audio
const englishAudio = document.getElementById('english-audio-player');
const englishSyncUrl = 'https://uthumany.github.io/nawawi-40-hadiths/api/sync_en/hadith_1.json'; // Example for Hadith 1

fetch(englishSyncUrl)
  .then(response => response.json())
  .then(syncData => {
    englishAudio.addEventListener('timeupdate', () => {
      const currentTime = englishAudio.currentTime;
      const currentWord = syncData.words.find(w => currentTime >= w.start && currentTime <= w.end);
      if (currentWord) {
        console.log('Currently speaking:', currentWord.word);
        // Call your UI highlighting function here
        highlightEnglishWordInUI(currentWord.word);
      }
    });
  });
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

---
*Maintained by [uthumany](https://github.com/uthumany)*

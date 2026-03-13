# Nawawi's Forty Hadiths API

A complete JSON API for Imam al-Nawawi's Forty Hadiths, including Arabic text, English translation, audio URLs, and word-by-word synchronization data for highlighting.

## API Endpoints

### Base URLs
- **Main API**: `https://uthumany.github.io/nawawi-40-hadiths/api`
- **Audio Hosting**: `https://raw.githubusercontent.com/uthumany/audio-hosting/main`
- **Sync Data**: `https://uthumany.github.io/nawawi-40-hadiths/api/sync`

### Endpoints
- **All Hadiths**: [hadiths.json](https://uthumany.github.io/nawawi-40-hadiths/api/hadiths.json)
- **Individual Hadith**: `https://uthumany.github.io/nawawi-40-hadiths/api/hadith_{number}.json` (e.g., [hadith_1.json](https://uthumany.github.io/nawawi-40-hadiths/api/hadith_1.json))
- **Word-by-Word Sync**: `https://uthumany.github.io/nawawi-40-hadiths/api/sync/hadith_{number}.json` (e.g., [hadith_1.json](https://uthumany.github.io/nawawi-40-hadiths/api/sync/hadith_1.json))

## Features

- **Complete Data**: Includes metadata, narrator, source, Arabic text, and English translation.
- **Audio Integration**: Direct links to high-quality Arabic recitations.
- **Word-by-Word Highlighting**: Precise timestamps for every word in the Arabic text to enable synchronized highlighting during audio playback.

## Implementation Guide: Word-by-Word Highlighting

To implement highlighting in your application:

1.  **Fetch Hadith Data**: Get the Hadith details from the main API.
2.  **Fetch Sync Data**: Use the `sync_url` provided in the Hadith JSON.
3.  **Sync Playback**:
    - Listen to the `timeupdate` event of your audio player.
    - Match the `currentTime` with the `start` and `end` timestamps in the sync JSON.
    - Highlight the corresponding word in your UI.

```javascript
// Example logic
const currentTime = audio.currentTime;
const currentWord = syncData.words.find(w => currentTime >= w.start && currentTime <= w.end);
if (currentWord) {
  highlightWordInUI(currentWord.word);
}
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
  "sync_url": "..."
}
```

### Sync Object
```json
{
  "hadith_number": 1,
  "text": "...",
  "words": [
    { "word": "عَنْ", "start": 0.5, "end": 0.8 },
    ...
  ]
}
```

---
*Maintained by [uthumany](https://github.com/uthumany)*

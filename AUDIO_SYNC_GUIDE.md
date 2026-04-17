# Audio-Text Synchronization Guide for Nawawi 40 Hadiths API

To implement **word-by-word highlighting** in your Hadith application, you need to provide the frontend with **timestamp data** for each word in the Arabic and English texts. This guide explains how to generate and use this data.

## 1. The Synchronization Data Format

For each Hadith, you should have corresponding JSON files (e.g., `api/sync/hadith_1.json` for Arabic and `api/sync_en/hadith_1.json` for English) that contain the start and end times for every word in the audio.

### Example JSON Structure (Arabic):
```json
{
  "hadith_number": 1,
  "text": "عَنْ أَمِيرِ الْمُؤْمِنِينَ أَبِي حَفْصٍ عُمَرَ بْنِ الْخَطَّابِ رَضِيَ اللهُ عَنْهُ قَالَ: سَمِعْتُ رَسُولَ اللَّهِ صلى الله عليه وسلم يَقُولُ: \"",
  "words": [
    { "word": "عَنْ", "start": 0.5, "end": 0.8 },
    { "word": "أَمِيرِ", "start": 0.9, "end": 1.2 },
    { "word": "الْمُؤْمِنِينَ", "start": 1.3, "end": 1.8 },
    ...
  ]
}
```

### Example JSON Structure (English):
```json
{
  "hadith_number": 1,
  "text": "From the Chief of the Believers, Abī Hafṣ ʿUmar bin al-Khaṭṭāb (raḍiyallāhu anhu) who said: I heard the Messenger of Allaah (ṣallallāhu ʿalayhi wasallam) saying: 'Verily actions are based upon the intentions (behind them) and every man shall have (in accordance) with what he intended. Thus, he whose migration was (for the sake of) Allāh and His Messenger, then his migration was indeed for Allāh and His Messenger. And he whose migration was to attain a portion of the world or to take some woman in marriage, then his migration was for that for which he migrated.'",
  "words": [
    { "word": "From", "start": 0.5, "end": 0.8 },
    { "word": "the", "start": 0.8, "end": 0.9 },
    { "word": "Chief", "start": 0.9, "end": 1.2 },
    ...
  ]
}
```

## 2. How to Generate the Data

You can use **OpenAI's Whisper API** or **WhisperX** (a local Python library) to perform "Forced Alignment." This process takes the audio and the text and calculates exactly when each word is spoken.

### Option A: Using OpenAI Whisper API (Recommended for Ease)
You can use the `whisper-1` model with `timestamp_granularities=["word"]`. The `generate_english_sync.py` script in this repository demonstrates this for English audio.

### Option B: Using WhisperX (Recommended for Accuracy)
WhisperX is an open-source tool that provides very precise word-level timestamps by aligning the audio with the text using a phoneme-based model.

## 3. Frontend Implementation (How to Highlight)

In your web or mobile app, you can use the following logic:

1.  **Load the Audio**: Use an HTML5 `<audio>` element or a library like `Howler.js`.
2.  **Load the Sync Data**: Fetch the appropriate `sync_hadith_X.json` (Arabic) or `sync_en/hadith_X.json` (English) file.
3.  **Listen for Time Updates**: Use the `timeupdate` event of the audio player.
4.  **Find the Current Word**:
    ```javascript
    // For Arabic audio
    const arabicAudio = document.getElementById("arabic-audio-player");
    const arabicSyncUrl = "https://uthumany.github.io/nawawi-40-hadiths/api/sync/hadith_1.json"; // Example for Hadith 1

    fetch(arabicSyncUrl)
      .then(response => response.json())
      .then(syncData => {
        arabicAudio.addEventListener("timeupdate", () => {
          const currentTime = arabicAudio.currentTime;
          const currentWord = syncData.words.find(w => currentTime >= w.start && currentTime <= w.end);
          if (currentWord) {
            console.log("Currently speaking (Arabic):", currentWord.word);
            // Call your UI highlighting function here for Arabic
            highlightArabicWordInUI(currentWord.word);
          }
        });
      });

    // For English audio
    const englishAudio = document.getElementById("english-audio-player");
    const englishSyncUrl = "https://uthumany.github.io/nawawi-40-hadiths/api/sync_en/hadith_1.json"; // Example for Hadith 1

    fetch(englishSyncUrl)
      .then(response => response.json())
      .then(syncData => {
        englishAudio.addEventListener("timeupdate", () => {
          const currentTime = englishAudio.currentTime;
          const currentWord = syncData.words.find(w => currentTime >= w.start && currentTime <= w.end);
          if (currentWord) {
            console.log("Currently speaking (English):", currentWord.word);
            // Call your UI highlighting function here for English
            highlightEnglishWordInUI(currentWord.word);
          }
        });
      });
    ```
5.  **Apply CSS Class**: If a word is found, apply a `.highlight` class to the corresponding word in your UI.

## 4. Next Steps

1.  **Download Audio Files**: Ensure you have the MP3 files locally to process them.
2.  **Run the Generator**: Use the provided scripts (e.g., `generate_english_sync.py`) or a tool like WhisperX to generate the JSON files for all 42 Hadiths in both languages.
3.  **Update API**: Host these JSON files in your `api/sync/` (Arabic) and `api/sync_en/` (English) directories so your app can access them.

---
*Prepared by Manus AI Agent*

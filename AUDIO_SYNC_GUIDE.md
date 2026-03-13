# Audio-Text Synchronization Guide for Nawawi 40 Hadiths API

To implement **word-by-word highlighting** in your Hadith application, you need to provide the frontend with **timestamp data** for each word in the Arabic text. This guide explains how to generate and use this data.

## 1. The Synchronization Data Format

For each Hadith, you should have a corresponding JSON file (e.g., `api/sync_hadith_1.json`) that contains the start and end times for every word in the audio.

### Example JSON Structure:
```json
{
  "hadith_number": 1,
  "words": [
    { "word": "عَنْ", "start": 0.5, "end": 0.8 },
    { "word": "أَمِيرِ", "start": 0.9, "end": 1.2 },
    { "word": "الْمُؤْمِنِينَ", "start": 1.3, "end": 1.8 },
    ...
  ]
}
```

## 2. How to Generate the Data

You can use **OpenAI's Whisper API** or **WhisperX** (a local Python library) to perform "Forced Alignment." This process takes the audio and the text and calculates exactly when each word is spoken.

### Option A: Using OpenAI Whisper API (Recommended for Ease)
You can use the `whisper-1` model with `timestamp_granularities=["word"]`. I have created a prototype script `whisper_sync_prototype.py` in this repository that demonstrates this.

### Option B: Using WhisperX (Recommended for Accuracy)
WhisperX is an open-source tool that provides very precise word-level timestamps by aligning the audio with the text using a phoneme-based model.

## 3. Frontend Implementation (How to Highlight)

In your web or mobile app, you can use the following logic:

1.  **Load the Audio**: Use an HTML5 `<audio>` element or a library like `Howler.js`.
2.  **Load the Sync Data**: Fetch the `sync_hadith_X.json` file.
3.  **Listen for Time Updates**: Use the `timeupdate` event of the audio player.
4.  **Find the Current Word**:
    ```javascript
    const currentTime = audio.currentTime;
    const currentWord = syncData.words.find(w => currentTime >= w.start && currentTime <= w.end);
    ```
5.  **Apply CSS Class**: If a word is found, apply a `.highlight` class to the corresponding word in your UI.

## 4. Next Steps

1.  **Download Audio Files**: You need to have the MP3 files locally to process them.
2.  **Run the Generator**: Use the provided script or a tool like WhisperX to generate the JSON files for all 42 Hadiths.
3.  **Update API**: Host these JSON files in your `api/` directory so your app can access them.

---
*Prepared by Manus AI Agent*

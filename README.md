# Nawawi's 40 Hadiths API

A simple JSON API for Imam al-Nawawi's Forty Hadith, including audio URLs for each Hadith.

## API Endpoints

- **Base URL**: `https://uthumany.github.io/nawawi-40-hadiths/api` (Static JSON)
- **All Hadiths**: `/hadiths.json`
- **Single Hadith**: `/hadith_{number}.json`

## Data Structure

Each Hadith object contains:
- `hadith_number`: The number of the Hadith (1-42)
- `title`: The title of the Hadith
- `narrator`: The companion who narrated the Hadith
- `source`: The primary source (e.g., Bukhari, Muslim)
- `arabic_text`: The original Arabic text
- `english_translation`: The English translation
- `description`: A brief explanation or context
- `audio_url`: A direct link to the audio file (hosted on GitHub)

## Audio Hosting

Audio files are hosted in a separate repository: [audio-hosting](https://github.com/uthumany/audio-hosting)

import os
import json
from openai import OpenAI

# Initialize OpenAI client (API key and base URL are pre-configured in the environment)
client = OpenAI()

def get_word_timestamps(audio_file_path):
    """
    Uses OpenAI Whisper API to get word-level timestamps for an audio file.
    Note: This requires the audio file to be present locally.
    """
    if not os.path.exists(audio_file_path):
        return {"error": f"File {audio_file_path} not found."}

    try:
        with open(audio_file_path, "rb") as audio_file:
            # Request transcription with word-level timestamps
            transcript = client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-1",
                response_format="verbose_json",
                timestamp_granularities=["word"],
                language="ar" # Specify Arabic
            )
            
            # Extract word data
            words_data = []
            if hasattr(transcript, 'words'):
                for word in transcript.words:
                    words_data.append({
                        "word": word.word,
                        "start": word.start,
                        "end": word.end
                    })
            
            return {
                "text": transcript.text,
                "words": words_data
            }
    except Exception as e:
        return {"error": str(e)}

def save_sync_data(hadith_number, sync_data):
    """Saves the synchronization data to a JSON file."""
    output_path = f"api/sync_hadith_{hadith_number}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(sync_data, f, ensure_ascii=False, indent=2)
    print(f"Saved sync data to {output_path}")

if __name__ == "__main__":
    # This is a prototype. In a real scenario, you would loop through your audio files.
    # Example usage (commented out as we don't have the actual audio files locally):
    # sync_info = get_word_timestamps("downloads/hadith_1.mp3")
    # save_sync_data(1, sync_info)
    
    print("Whisper Sync Prototype Script Created.")
    print("To use this, you need to download the MP3 files and run this script for each.")

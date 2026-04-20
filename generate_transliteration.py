import json
import os
from openai import OpenAI

client = OpenAI()

def generate_transliteration(arabic_text):
    prompt = f"Please provide a clean, consistent, and human-readable Arabic transliteration for the following text. Use standard academic transliteration (e.g., using symbols like ʿ for Ayin and ʾ for Hamza where appropriate, but keep it readable for a general audience). Return ONLY the transliterated text, nothing else.\n\nArabic Text: {arabic_text}"
    
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are an expert in Arabic-to-English transliteration, specifically for Islamic texts and Hadiths."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def main():
    data_path = "data/hadiths.json"
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    transliterations = []
    
    for hadith in data["hadiths"]:
        num = hadith["hadith_number"]
        print(f"Generating transliteration for Hadith {num}...")
        
        # We use the sync text if available as it might be cleaner, otherwise the arabic_text
        sync_path = f"api/sync/hadith_{num}.json"
        if os.path.exists(sync_path):
            with open(sync_path, "r", encoding="utf-8") as sf:
                sync_data = json.load(sf)
                arabic_text = sync_data["text"]
        else:
            arabic_text = hadith["arabic_text"]
            
        trans_text = generate_transliteration(arabic_text)
        
        trans_obj = {
            "hadith_number": num,
            "title": hadith["title"],
            "narrator": hadith["narrator"],
            "source": hadith["source"],
            "Arabic_Transliteration_text": trans_text
        }
        transliterations.append(trans_obj)
    
    output_path = "api/transliterations.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(transliterations, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully generated transliterations for all {len(transliterations)} hadiths.")

if __name__ == "__main__":
    main()

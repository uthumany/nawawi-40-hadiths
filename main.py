from fastapi import FastAPI, HTTPException
import json
import os

app = FastAPI(title="Nawawi's 40 Hadiths API")

# Load data
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "hadiths.json")

def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/")
async def root():
    return {"message": "Welcome to the Nawawi's 40 Hadiths API", "endpoints": ["/hadiths", "/hadiths/{number}"]}

@app.get("/hadiths")
async def get_all_hadiths():
    data = load_data()
    return data

@app.get("/hadiths/{number}")
async def get_hadith(number: int):
    data = load_data()
    for hadith in data["hadiths"]:
        if hadith["hadith_number"] == number:
            return hadith
    raise HTTPException(status_code=404, detail="Hadith not found")

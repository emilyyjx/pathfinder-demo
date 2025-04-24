from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
import spacy.cli
spacy.cli.download("en_core_web_sm")
from nlp_utils import extract_keywords


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "YOUR_COLLEGE_SCORECARD_API_KEY"
API_URL = "https://api.data.gov/ed/collegescorecard/v1/schools"

@app.get("/search")
async def search_colleges(query: str = Query(...)):
    keywords = extract_keywords(query)
    async with httpx.AsyncClient() as client:
        params = {
            "api_key": API_KEY,
            "fields": "id,school.name,school.city,school.state,school.size,school.tuition.in_state",
            "per_page": 5,
            "school.degrees_awarded.predominant": "3",
        }
        response = await client.get(API_URL, params=params)
        data = response.json()
        return {
            "keywords": keywords,
            "results": data.get("results", [])
        }

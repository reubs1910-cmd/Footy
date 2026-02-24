from fastapi import FastAPI
import httpx
from app.config import FOOTBALL_API_KEY

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Footy API is alive!"}


@app.get("/matches/today")
async def get_todays_matches():
    url = "https://api.football-data.org/v4/matches"
    headers = {"X-Auth-Token" : FOOTBALL_API_KEY}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        data = response.json()

    return data
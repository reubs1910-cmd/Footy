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

    #retrieves all data
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        data = response.json()

    #extracts just what we need
    matches = []
    for match in data.get("matches", []):
        matches.append({
            "id": match.get("id"),
            "time": match.get("utcDate"),
            "status": match.get("status"),
            "competition": match.get("competition", {}).get("name"),
            "home_team": match.get("homeTeam", {}).get("name"),
            "away_team": match.get("awayTeam", {}).get("name"),
            "score": {
                "home": match.get("score", {}).get("fullTime", {}).get("home"),
                "away": match.get("score", {}).get("fullTime", {}).get("away"),
            }
        })

    return {"count": len(matches), "matches": matches}
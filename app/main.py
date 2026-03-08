from fastapi import FastAPI
import httpx
from app.config import FOOTBALL_API_KEY

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Footy API is alive!"}

#endpoint to get today's matches
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

    return {
        "count": len(matches), 
        "matches": matches
    }

#endpoint to get standings from different leagues
@app.get("/standings/{competition_code}")
async def get_standings(competition_code: str):
    url = f"https://api.football-data.org/v4/competitions/{competition_code}/standings"
    headers = {"X-Auth-Token": FOOTBALL_API_KEY}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        data = response.json()

    #since multiple tables (home, away, etc), we only want the Total one
    standings = data.get("standings", [])
    table = None;
    for standing in standings:
        if standing.get("type") == "TOTAL":
            table = standing.get("table", [])

    cleaned_table = []
    for row in table:
        cleaned_table.append({
            "position": row.get("position"),
            "team": row.get("team", {}).get("name"),
            "logo": row.get("team", {}).get("crest"),
            "gamesPlayed": row.get("playedGames"),
            "form": row.get("form"),
            "won": row.get("won"),
            "draw": row.get("draw"),
            "lost": row.get("lost"),
            "points": row.get("points"),
            "goalsFor": row.get("goalsFor"),
            "goalsAgainst": row.get("goalsAgainst"),
            "goalDiff": row.get("goalDifference")
        })

    return {
        "league": data.get("competition", {}).get("name"),
        "table": cleaned_table
    }

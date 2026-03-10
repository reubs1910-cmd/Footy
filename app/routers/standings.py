from fastapi import APIRouter
import httpx
from app.config import FOOTBALL_API_KEY

router = APIRouter()

#endpoint to get standings from different leagues
@router.get("/{competition_code}")
async def get_standings(competition_code: str):
    url = f"https://api.football-data.org/v4/competitions/{competition_code}/standings"
    headers = {"X-Auth-Token": FOOTBALL_API_KEY}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        data = response.json()

    #since multiple tables (home, away, etc), we only want the Total one
    standings = data.get("standings", [])
    table = [];
    for standing in standings:
        if standing.get("type") == "TOTAL":
            table = standing.get("table", [])
            break

    #if table is empty and standings exists, use the first table
    if not table and standings:
        table = standings[0].get("table", [])

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
from fastapi import FastAPI
from app.routers import matches, standings

app = FastAPI(title="Soccer Stats API")

#include routers, attatches them to the app
app.include_router(matches.router, prefix="/matches", tags=["Matches"]) #all routes in matches.py get /matches prepended
app.include_router(standings.router, prefix="/standings", tags=["Standings"]) #same applies for all routers included

@app.get("/")
def root():
    return {"message": "Footy API is alive!"}




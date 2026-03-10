from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import matches, standings

app = FastAPI(title="Soccer Stats API")

#add CORS (cross-origin resource sharing) Middleware; gives frontend permission to access backend
#without this, browser will block api calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], #frontend react server, "*" if u want to allow any website
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#include routers, attatches them to the app
app.include_router(matches.router, prefix="/matches", tags=["Matches"]) #all routes in matches.py get /matches prepended
app.include_router(standings.router, prefix="/standings", tags=["Standings"]) #same applies for all routers included

@app.get("/")
def root():
    return {"message": "Footy API is alive!"}




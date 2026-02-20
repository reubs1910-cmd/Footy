from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Footy API is alive!"}
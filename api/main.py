from fastapi import FastAPI

from api.routes.spotify import router as spotify_router

from dotenv import load_dotenv

load_dotenv()


app = FastAPI(title="InstaVibely API")

app.include_router(spotify_router, prefix="/auth/spotify", tags=["spotify"])

@app.get("/")
async def root():
    return {"status": "ok"}

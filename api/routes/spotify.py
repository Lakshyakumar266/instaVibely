from fastapi import Request
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from urllib.parse import urlencode
import os
from dotenv import load_dotenv
import httpx

load_dotenv()

print("CLIENT_ID =", os.getenv("SPOTIFY_CLIENT_ID"))

print("REDIRECT_URI =", os.getenv("SPOTIFY_REDIRECT_URI"))


router = APIRouter()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")

SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")


@router.get("/")
async def connect_spotify(
    user: str,
):
    scopes = [
        "playlist-modify-private",
        "playlist-read-private",
        "playlist-modify-public",
        "user-read-email",
    ]

    params = {
        "client_id": SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "scope": " ".join(scopes),
        "state": user,
    }

    url = "https://accounts.spotify.com/authorize?" + urlencode(params)

    return RedirectResponse(url)


@router.get("/callback")
async def spotify_callback(
    code: str,
    state: str,
):
    async with httpx.AsyncClient() as client:

        # Exchange code for token
        token_response = await client.post(
            "https://accounts.spotify.com/api/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": os.getenv("SPOTIFY_REDIRECT_URI"),
                "client_id": os.getenv("SPOTIFY_CLIENT_ID"),
                "client_secret": os.getenv("SPOTIFY_CLIENT_SECRET"),
            },
        )

        token_data = token_response.json()

        if "access_token" not in token_data:
            return {"spotify_error": token_data}

        access_token = token_data["access_token"]

        print("TOKEN RESPONSE:")
        print(token_response.status_code)
        print(token_response.text)

        # Get Spotify user profile
        profile_response = await client.get(
            "https://api.spotify.com/v1/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        print("PROFILE STATUS:", profile_response.status_code)
        print("PROFILE HEADERS:", profile_response.headers)
        print("PROFILE TEXT:")
        print(profile_response.text)

        return {
            "status": profile_response.status_code,
            "body": profile_response.text,
        }

        profile = profile_response.json()

        # Create playlist
        playlist_response = await client.post(
            f"https://api.spotify.com/v1/users/{profile['id']}/playlists",
            headers={"Authorization": f"Bearer {access_token}"},
            json={
                "name": "InstaVibely • Saved Music",
                "description": "Songs discovered through InstaVibely",
                "public": False,
            },
        )

        playlist = playlist_response.json()

        return {
            "spotify_user": profile,
            "playlist": playlist,
        }

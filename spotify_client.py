import os

import spotipy
from dotenv import dotenv_values
from spotipy.oauth2 import SpotifyOAuth

secrets = dotenv_values(".env")

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID", secrets.get("SPOTIPY_CLIENT_ID"))
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET", secrets.get("SPOTIPY_CLIENT_SECRET"))
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI", secrets.get("SPOTIPY_REDIRECT_URI"))
SCOPE = "user-library-read user-top-read"


def create_oauth(cache_handler=None):
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        cache_handler=cache_handler,
        show_dialog=True,
    )


def sp_instance():
    return spotipy.Spotify(auth_manager=create_oauth())
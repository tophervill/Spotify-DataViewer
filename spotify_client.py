from dotenv import dotenv_values

import spotipy
from spotipy.oauth2 import SpotifyOAuth

secrets = dotenv_values(".env")

CLIENT_ID = secrets["SPOTIPY_CLIENT_ID"]
CLIENT_SECRET = secrets["SPOTIPY_CLIENT_SECRET"]
REDIRECT_URI = secrets["SPOTIPY_REDIRECT_URI"]
SCOPE = 'user-library-read, user-top-read'

def sp_instance():
    sp_oauth = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    )

    spotify_instance = spotipy.Spotify(auth_manager=sp_oauth)
    return spotify_instance
# Soundboard

A friendly Flask dashboard for exploring your Spotify listening history. It shows top tracks, top artists, saved library tracks, and a small overview of playlists, saved tracks, and genres.

## Setup

1. Create or open a Spotify application at the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).
2. Add the redirect URI `http://127.0.0.1:5000/callback` to the application settings.
3. Activate the project environment and install dependencies:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

4. Create a `.env` file in this directory:

```text
SPOTIPY_CLIENT_ID=your-client-id
SPOTIPY_CLIENT_SECRET=your-client-secret
SPOTIPY_REDIRECT_URI=http://127.0.0.1:5000/callback
FLASK_SECRET_KEY=replace-with-a-random-local-secret
```

5. Start the dashboard:

```bash
python app.py
```

Open `http://127.0.0.1:5000` in a browser and choose **Connect Spotify**.

On the login screen, leave **Keep me signed in for 30 days** unchecked to remove the browser session when the browser closes. Selecting it creates a secure, HTTP-only permanent session that expires after 30 days.

## Dashboard controls

- **Listening range:** last 4 weeks, last 6 months, or all time.
- **Top tracks and artists:** ranked by Spotify for the selected range.
- **Your soundtracks:** a preview of saved tracks from the Spotify library.
- **Overview:** playlist count, saved-track count, and common genres.

The local app keeps the OAuth token in an in-memory store keyed to the browser session. Restarting the development server logs users out. A production multi-user deployment should replace this with a persistent per-user server-side token store.

## Tests

Run the focused tests without Spotify credentials:

```bash
python -m unittest test_app.py
python -m compileall app.py spotify_client.py spotify_service.py
```

Never commit `.env` or token cache files.

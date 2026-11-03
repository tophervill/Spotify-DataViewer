import os
import secrets
from datetime import timedelta

from flask import Flask, flash, redirect, render_template, request, session, url_for
from spotipy import Spotify
from spotipy.cache_handler import MemoryCacheHandler

from spotify_client import create_oauth
from spotify_service import dashboard_metrics, saved_tracks, top_artists, top_tracks, validate_limit, validate_time_range

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", secrets.token_hex(32))
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=30)
app.config["SESSION_REFRESH_EACH_REQUEST"] = False
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
oauth_sessions = {}


def _session_key():
    if "auth_key" not in session:
        session["auth_key"] = secrets.token_urlsafe(24)
    return session["auth_key"]


def _spotify_for_current_user():
    auth_state = oauth_sessions.get(session.get("auth_key"))
    if not auth_state:
        return None
    oauth = auth_state["oauth"]
    token = oauth.cache_handler.get_cached_token()
    if not token:
        return None
    return Spotify(auth_manager=oauth)


@app.route("/")
def dashboard():
    spotify = _spotify_for_current_user()
    if spotify is None:
        return render_template("login.html")

    selected_range = request.args.get("range", "medium")
    try:
        selected_range = validate_time_range(selected_range)
        limit = validate_limit(request.args.get("limit", 8), default=8)
        data = {
            "metrics": dashboard_metrics(spotify),
            "tracks": top_tracks(limit, selected_range, spotify),
            "artists": top_artists(limit, selected_range, spotify),
            "soundtracks": saved_tracks(limit, spotify),
        }
    except Exception:
        flash("Spotify could not load your listening data right now. Please try again.", "error")
        data = {"metrics": None, "tracks": [], "artists": [], "soundtracks": []}
    return render_template("dashboard.html", selected_range=selected_range, **data)


@app.route("/login", methods=["GET", "POST"])
def login():
    session.permanent = request.form.get("remember") == "1"
    auth_key = _session_key()
    oauth = create_oauth(cache_handler=MemoryCacheHandler())
    oauth_sessions[auth_key] = {"oauth": oauth}
    return redirect(oauth.get_authorize_url())


@app.route("/callback")
def callback():
    auth_state = oauth_sessions.get(session.get("auth_key"))
    if not auth_state:
        flash("Your login session expired. Please start again.", "error")
        return redirect(url_for("dashboard"))
    try:
        code = request.args.get("code")
        if not code:
            raise ValueError("Missing Spotify authorization code")
        auth_state["oauth"].get_access_token(code, as_dict=True)
    except Exception:
        oauth_sessions.pop(session.get("auth_key"), None)
        session.pop("auth_key", None)
        flash("Spotify login was not completed. Please try again.", "error")
    return redirect(url_for("dashboard"))


@app.route("/logout")
def logout():
    oauth_sessions.pop(session.pop("auth_key", None), None)
    flash("You have been logged out of Spotify.", "success")
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
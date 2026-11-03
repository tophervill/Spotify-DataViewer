from spotify_client import sp_instance

TIME_RANGES = {
    "short": "short_term",
    "medium": "medium_term",
    "long": "long_term",
}


def validate_time_range(time_range):
    normalized = str(time_range).lower()
    if normalized not in TIME_RANGES:
        raise ValueError("Time range must be short, medium, or long.")
    return normalized


def validate_limit(limit, default=10):
    try:
        value = int(limit)
    except (TypeError, ValueError):
        return default
    return max(1, min(value, 20))


def _track_data(track, position):
    artists = track.get("artists", [])
    images = track.get("album", {}).get("images", [])
    return {
        "position": position,
        "name": track.get("name", "Unknown track"),
        "artists": ", ".join(artist.get("name", "Unknown artist") for artist in artists),
        "image": images[0].get("url") if images else None,
        "url": track.get("external_urls", {}).get("spotify"),
    }


def _artist_data(artist, position):
    images = artist.get("images", [])
    return {
        "position": position,
        "name": artist.get("name", "Unknown artist"),
        "genres": artist.get("genres", [])[:2],
        "image": images[0].get("url") if images else None,
        "url": artist.get("external_urls", {}).get("spotify"),
    }


def top_tracks(limit, time_range, spotify=None):
    spotify = spotify or sp_instance()
    selected_range = validate_time_range(time_range)
    response = spotify.current_user_top_tracks(
        limit=validate_limit(limit), offset=0, time_range=TIME_RANGES[selected_range]
    )
    return [_track_data(track, index + 1) for index, track in enumerate(response.get("items", []))]


def top_artists(limit, time_range, spotify=None):
    spotify = spotify or sp_instance()
    selected_range = validate_time_range(time_range)
    response = spotify.current_user_top_artists(
        limit=validate_limit(limit), offset=0, time_range=TIME_RANGES[selected_range]
    )
    return [_artist_data(artist, index + 1) for index, artist in enumerate(response.get("items", []))]


def saved_tracks(limit=10, spotify=None):
    spotify = spotify or sp_instance()
    response = spotify.current_user_saved_tracks(limit=validate_limit(limit))
    return [_track_data(item.get("track", {}), index + 1) for index, item in enumerate(response.get("items", []))]


def dashboard_metrics(spotify=None):
    spotify = spotify or sp_instance()
    profile = spotify.current_user()
    playlists = spotify.current_user_playlists(limit=1)
    saved = spotify.current_user_saved_tracks(limit=1)
    artists = spotify.current_user_top_artists(limit=20, time_range="medium_term")
    genres = {}
    for artist in artists.get("items", []):
        for genre in artist.get("genres", []):
            genres[genre] = genres.get(genre, 0) + 1

    return {
        "profile": profile,
        "playlist_count": playlists.get("total", 0),
        "saved_track_count": saved.get("total", 0),
        "top_genres": [genre for genre, _ in sorted(genres.items(), key=lambda item: item[1], reverse=True)[:5]],
    }


def get_user_info():
    return sp_instance().current_user()
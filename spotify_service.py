from spotify_client import sp_instance

def top_tracks(limit, time_range):
    sp = sp_instance()

    print(f"Displaying top tracks from a {time_range} time range:\n")

    time_range = time_range.lower() + "_term"

    user_top_tracks = sp.current_user_top_tracks(limit=limit, offset=0, time_range=time_range)

    print("---------")
    for idx, track in enumerate(user_top_tracks['items']):
        print(f"{idx + 1}. {track['name']} by {', '.join([artist['name'] for artist in track['artists']])}")
    print("---------")

    print("\nEnding top tracks display.\n")

def top_artists(limit, time_range):
    sp = sp_instance()

    print("Displaying top artists:\n")

    time_range = time_range.lower() + "_term"

    user_top_artists = sp.current_user_top_artists(limit=limit, offset=0, time_range=time_range)

    print("---------")
    for idx, artist in enumerate(user_top_artists['items']):
        print(f"{idx + 1}. {artist['name']}")
    print("---------")

    print("\nEnding top artists display.\n")

def get_user_info():

    # Checks for valid Spotify credentials and returns the current user's information
    if not sp_instance():
        raise Exception("Spotify credentials are invalid or missing. Please check your .env file.")
    else:
        print("Spotify credentials are valid. \nFetching user information...\n")

    # Checks if instance is valid or expired, and refreshes the token if necessary
    if not sp_instance().auth_manager.is_token_expired(sp_instance().auth_manager.cache_handler.get_cached_token()):
        print("Spotify token is valid. Fetching user information...\n")

    else:
        print("Spotify token is expired. Refreshing token...\n")
        sp_instance().auth_manager.refresh_access_token(sp_instance().auth_manager.cache_handler.get_cached_token()['refresh_token'])
        print(f"Token has been refreshed. It will expire in {sp_instance().auth_manager.cache_handler.get_cached_token()['expires_in'] // 60} minutes. \n")

    spotify_instance = sp_instance()
    user = spotify_instance.current_user()

    return user
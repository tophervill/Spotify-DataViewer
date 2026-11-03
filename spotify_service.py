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

# TODO: Implement the top_artists function to fetch and display user's top artists
def top_artists():
    pass

def get_user_info():
    
    # Checks for valid Spotify credentials and returns the current user's information
    if not sp_instance():
        raise Exception("Spotify credentials are invalid or missing. Please check your .env file.")
    else:
        print("Spotify credentials are valid. Fetching user information...\n")

    # Checks if instance is valid or expired, and refreshes the token if necessary
    if not sp_instance().auth_manager.is_token_expired(sp_instance().auth_manager.cache_handler.get_cached_token()):
        print("Spotify token is valid. Fetching user information...\n")

    else:
        print("Spotify token is expired. Refreshing token...\n")

    
    spotify_instance = sp_instance()
    user = spotify_instance.current_user()

    return user
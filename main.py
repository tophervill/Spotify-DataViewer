from dotenv import dotenv_values

import spotipy
from spotipy.oauth2 import SpotifyOAuth

# TODO: Add functionality to choose time range for top artists
# TODO: Implement pagination for large lists of tracks/artists
# TODO: Add unit tests for functions

secrets = dotenv_values(".env")

CLIENT_ID = secrets["SPOTIPY_CLIENT_ID"]
CLIENT_SECRET = secrets["SPOTIPY_CLIENT_SECRET"]
REDIRECT_URI = secrets["SPOTIPY_REDIRECT_URI"]
SCOPE = 'user-library-read, user-top-read'

def main():
    print("Welcome to Topher's Spotify API App!\n")
    while True:
        print("==== Main Menu ====")
        print("1. View top tracks")
        print("2. View top artists")
        print("3. Quit")
        print("================")
        response = input("> ")

        if response == "1":
            limit = input("How many tracks would you like to see? (default 10): \n> ")
            if not limit.isdigit() or int(limit) <= 0:
                limit = 10
            else:
                limit = int(limit)

            time_range = input("Select time range - (short, medium, long) (default medium): \n> ")
            if time_range not in ['short', 'medium', 'long']:
                time_range = 'medium'

            print(f"\nGot it! Fetching your top {limit} tracks...\n")

            top_tracks(limit, time_range)

        elif response == "2":
            top_artists()

        elif response == "3":
            print("Closing program... Goodbye!")
            break
        else:
            print("Please enter a valid option.\n")

def top_tracks(limit, time_range):
    user = sp_instance()

    print(f"Displaying top tracks from a {time_range} time range:\n")

    time_range = time_range.lower() + "_term"

    user_top_tracks = user.current_user_top_tracks(limit=limit, offset=0, time_range=time_range)

    print("---------")
    for idx, track in enumerate(user_top_tracks['items']):
        print(f"{idx + 1}. {track['name']} by {', '.join([artist['name'] for artist in track['artists']])}")
    print("---------")

    print("\nEnding top tracks display.\n")

# TODO: Implement the top_artists function to fetch and display user's top artists
def top_artists():
    pass

def sp_instance():
    sp_oauth = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    )

    spotify_instance = spotipy.Spotify(auth_manager=sp_oauth)
    return spotify_instance

def get_user_info():
    spotify_instance = sp_instance()
    user = spotify_instance.current_user()
    return user


if __name__ == "__main__":
    main()

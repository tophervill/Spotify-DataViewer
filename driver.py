from spotify_service import top_tracks, top_artists

# TODO: Add functionality to choose time range for top artists
# TODO: Implement pagination for large lists of tracks/artists
# TODO: Add unit tests for functions

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

if __name__ == "__main__":
    main()

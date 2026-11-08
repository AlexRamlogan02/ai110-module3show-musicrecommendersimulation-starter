"""Command-line runner for the Music Recommender Simulation."""

if __package__:
    from .recommender import load_songs, recommend_songs
else:
    from recommender import load_songs, recommend_songs


def main(* args) -> None:
    """Load songs and display recommendations for five sample profiles."""
    songs = load_songs("data/songs.csv") 
    print(f"Loaded {len(songs)} songs.")

    user_profiles = [
        {"genre": "pop", "mood": "happy", "energy": 0.82},
        {"genre": "lofi", "mood": "chill", "energy": 0.0},
        {"genre": "rock", "mood": "intense", "energy": 1.0},
        {"genre": "classical", "mood": "chill", "energy": 0.28},
        {"genre": "classical", "mood": "melancholic", "energy": 0.4},
    ]

    for index, user_prefs in enumerate(user_profiles, start=1):
        print(
            f"\nProfile {index}: genre={user_prefs['genre']}, "
            f"mood={user_prefs['mood']}, energy={user_prefs['energy']}"
        )
        print("Top recommendations:\n")
        for song, score, explanation in recommend_songs(user_prefs, songs, k=5):
            print(f"{song['title']} - Score: {score:.2f}")
            print(f"Because: {explanation}")
            print()


if __name__ == "__main__":
    main()

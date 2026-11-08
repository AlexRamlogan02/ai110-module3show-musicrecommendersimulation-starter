import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        """Store the songs available for recommendation."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return up to k songs for the user (ranking is not yet implemented)."""
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a placeholder explanation for a recommendation."""
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load song dictionaries from CSV, converting numeric attributes."""
    required_fields = {
        "id", "title", "artist", "genre", "mood", "energy", "tempo_bpm",
        "valence", "danceability", "acousticness",
    }
    float_fields = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")
    songs = []

    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        missing_fields = required_fields - set(reader.fieldnames or [])
        if missing_fields:
            raise ValueError(f"Missing CSV columns: {', '.join(sorted(missing_fields))}")

        for row in reader:
            if None in row or any(not row[field] for field in required_fields):
                raise ValueError(f"Invalid song data near CSV line {reader.line_num}")
            try:
                song: Dict = dict(row)
                song["id"] = int(row["id"])
                for field in float_fields:
                    song[field] = float(row[field])
            except ValueError as exc:
                raise ValueError(f"Invalid numeric value near CSV line {reader.line_num}") from exc
            songs.append(song)

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score genre, mood, and energy against the user's preferences."""
    user_energy = user_prefs["energy"]
    song_energy = song["energy"]
    for label, value in (("user energy", user_energy), ("song energy", song_energy)):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{label} must be a number between 0 and 1")
        if not 0 <= value <= 1:
            raise ValueError(f"{label} must be a number between 0 and 1")

    score = 0.0
    reasons = []
    if song["genre"] == user_prefs["genre"]:
        score += 2
        reasons.append(f"Genre matches: {song['genre']}")
    if song["mood"] == user_prefs["mood"]:
        score += 2
        reasons.append(f"Mood matches: {song['mood']}")

    energy_closeness = 1 - abs(song_energy - user_energy)
    score += energy_closeness
    reasons.append(
        f"Energy {song_energy:.2f} compared with target {user_energy:.2f} "
        f"(closeness: {energy_closeness:.2f})"
    )
    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Return up to k songs ranked by score, with explanations."""
    recommendations = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        recommendations.append((song, score, explanation))

    recommendations.sort(key=lambda x: x[1], reverse=True)
    return recommendations[:k]

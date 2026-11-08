from pathlib import Path

import pytest

from src.recommender import Song, UserProfile, Recommender, load_songs, score_song, recommend_songs


def test_load_songs_reads_dataset_with_numeric_attributes():
    csv_path = Path(__file__).resolve().parents[1] / "data" / "songs.csv"
    songs = load_songs(str(csv_path))

    assert len(songs) >= 1
    assert songs[0] == {
        "id": 1,
        "title": "Sunrise City",
        "artist": "Neon Echo",
        "genre": "pop",
        "mood": "happy",
        "energy": 0.82,
        "tempo_bpm": 118.0,
        "valence": 0.84,
        "danceability": 0.79,
        "acousticness": 0.18,
    }
    assert isinstance(songs[0]["id"], int)
    assert all(
        isinstance(songs[0][field], float)
        for field in ("energy", "tempo_bpm", "valence", "danceability", "acousticness")
    )


def test_load_songs_handles_quoted_text_and_header_only_files(tmp_path):
    csv_path = tmp_path / "songs.csv"
    header = "id,title,artist,genre,mood,energy,tempo_bpm,valence,danceability,acousticness\n"
    csv_path.write_text(header, encoding="utf-8")
    assert load_songs(str(csv_path)) == []

    csv_path.write_text(
        header + '1,"Rain, Again",Artist,lofi,chill,0.4,80,0.6,0.5,0.9\n',
        encoding="utf-8",
    )
    assert load_songs(str(csv_path))[0]["title"] == "Rain, Again"


@pytest.mark.parametrize(
    ("content", "message"),
    [
        ("id,title\n1,Song\n", "Missing CSV columns"),
        (
            "id,title,artist,genre,mood,energy,tempo_bpm,valence,danceability,acousticness\n"
            "1,Song,Artist,pop,happy,not-a-number,120,0.8,0.7,0.2\n",
            "Invalid numeric value near CSV line 2",
        ),
        (
            "id,title,artist,genre,mood,energy,tempo_bpm,valence,danceability,acousticness\n"
            "1,Song,Artist,pop,happy,0.8,120,0.8,0.7\n",
            "Invalid song data near CSV line 2",
        ),
    ],
)
def test_load_songs_rejects_invalid_data(tmp_path, content, message):
    csv_path = tmp_path / "songs.csv"
    csv_path.write_text(content, encoding="utf-8")

    with pytest.raises(ValueError, match=message):
        load_songs(str(csv_path))


def test_load_songs_raises_for_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_songs(str(tmp_path / "missing.csv"))


@pytest.mark.parametrize(
    ("song", "expected", "reason_count"),
    [
        ({"genre": "pop", "mood": "happy", "energy": 0.7}, 5.0, 3),
        ({"genre": "pop", "mood": "happy", "energy": 0.8}, 4.9, 3),
        ({"genre": "pop", "mood": "chill", "energy": 0.7}, 3.0, 2),
        ({"genre": "lofi", "mood": "happy", "energy": 0.7}, 3.0, 2),
        ({"genre": "lofi", "mood": "chill", "energy": 0.2}, 0.5, 1),
    ],
)
def test_score_song_matches_documented_rule(song, expected, reason_count):
    score, reasons = score_song({"genre": "pop", "mood": "happy", "energy": 0.7}, song)

    assert score == pytest.approx(expected)
    assert len(reasons) == reason_count
    assert "Energy" in reasons[-1]


def test_score_song_extreme_energy_difference():
    score, reasons = score_song(
        {"genre": "pop", "mood": "happy", "energy": 0},
        {"genre": "lofi", "mood": "chill", "energy": 1},
    )

    assert score == 0
    assert "closeness: 0.00" in reasons[0]


@pytest.mark.parametrize("value", [-0.1, 1.1, float("nan"), float("inf"), "0.5", True])
@pytest.mark.parametrize("source", ["user", "song"])
def test_score_song_rejects_invalid_energy(value, source):
    user = {"genre": "pop", "mood": "happy", "energy": 0.7}
    song = {"genre": "pop", "mood": "happy", "energy": 0.8}
    (user if source == "user" else song)["energy"] = value

    with pytest.raises(ValueError, match=f"{source} energy"):
        score_song(user, song)


def test_score_song_with_loaded_song():
    csv_path = Path(__file__).resolve().parents[1] / "data" / "songs.csv"
    song = load_songs(str(csv_path))[0]

    score, reasons = score_song({"genre": "pop", "mood": "happy", "energy": 0.8}, song)

    assert score == pytest.approx(4.98)
    assert len(reasons) == 3


def test_score_song_requires_preferences_and_song_fields():
    with pytest.raises(KeyError):
        score_song({"genre": "pop", "mood": "happy"}, {"energy": 0.8})


def test_recommend_songs_ranks_limits_and_preserves_ties():
    user = {"genre": "pop", "mood": "happy", "energy": 0.7}
    songs = [
        {"title": "Low", "genre": "lofi", "mood": "chill", "energy": 0.7},
        {"title": "First", "genre": "pop", "mood": "happy", "energy": 0.7},
        {"title": "Second", "genre": "pop", "mood": "happy", "energy": 0.7},
    ]

    results = recommend_songs(user, songs, k=2)

    assert [song["title"] for song, _, _ in results] == ["First", "Second"]
    assert [score for _, score, _ in results] == [5.0, 5.0]
    assert all("Genre matches: pop" in explanation for _, _, explanation in results)
    assert recommend_songs(user, songs, k=0) == []


def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""

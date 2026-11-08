import csv
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.mark.parametrize("arguments", [("-m", "src.main"), ("src/main.py",)])
def test_cli_displays_ranked_recommendations(arguments):
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, *arguments],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    )

    with (root / "data" / "songs.csv").open(newline="", encoding="utf-8") as csv_file:
        song_count = sum(1 for _ in csv.DictReader(csv_file))
    assert f"Loaded {song_count} songs." in result.stdout
    sections = result.stdout.split("\nProfile ")[1:]
    expected_profiles = [
        ("1: genre=pop, mood=happy, energy=0.82", "Sunrise City - Score: 5.00"),
        ("2: genre=lofi, mood=chill, energy=0.0", "Quiet Window - Score: 4.36"),
        ("3: genre=rock, mood=intense, energy=1.0", "Storm Runner - Score: 4.82"),
        ("4: genre=classical, mood=chill, energy=0.28", "Spacewalk Thoughts - Score: 3.00"),
        ("5: genre=classical, mood=melancholic, energy=0.4", "Focus Flow - Score: 1.00"),
    ]
    assert len(sections) == len(expected_profiles)
    for section, (header, expected_top) in zip(sections, expected_profiles):
        assert section.splitlines()[0] == header
        entries = [line for line in section.splitlines() if " - Score: " in line]
        assert len(entries) == min(5, song_count)
        assert entries[0] == expected_top
        scores = [float(line.rsplit(" - Score: ", 1)[1]) for line in entries]
        assert scores == sorted(scores, reverse=True)
        assert section.count("Because: ") == len(entries)
    assert not result.stderr

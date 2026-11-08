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
    entries = [
        line for line in result.stdout.splitlines()
        if " - Score: " in line
    ]
    assert len(entries) == min(5, song_count)
    scores = [float(line.rsplit(" - Score: ", 1)[1]) for line in entries]
    assert scores == sorted(scores, reverse=True)
    assert result.stdout.count("Because: ") == len(entries)
    assert not result.stderr

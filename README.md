# 🎵 Music Recommender Simulation

## Project Summary

This classroom simulation loads a catalog of 20 example songs and recommends
music using a user's preferred genre, mood, and energy. It scores and ranks
each song, explains the score, and demonstrates the results for five profiles,
including preferences that do not match the catalog.

---

## How The System Works

The content-based recommender compares each song's attributes with a user's
taste profile. The functional scoring and ranking rules below are implemented;
the object-oriented recommender is still planned.

Each `Song` stores an ID, title, artist, genre, mood, energy, tempo in beats
per minute, valence, danceability, and acousticness. The initial scoring rule
uses genre, mood, and energy. The remaining audio attributes could be used in a
future version.

The `UserProfile` stores a favorite genre, favorite mood, target energy, and
whether the user likes acoustic music. The initial scoring rule does not yet
use the acoustic preference.

**Scoring rule (one song):**

- Add 2 points if the song's genre matches the user's favorite genre.
- Add 2 points if the song's mood matches the user's favorite mood.
- Add an energy closeness score of
  `max(0, 1 - 2 * abs(song.energy - user.target_energy))`. An exact match
  adds 1 point; a difference of 0.5 or greater adds 0 points. The factor of 2
  makes closeness decrease twice as quickly as in the original rule.

Both energy values must be numeric and between 0 and 1; invalid values raise an
error. The total score ranges from 0 to 5. For example, a song matching both genre and
mood with energy 0.8 for a user targeting 0.7 scores `2 + 2 + 0.8 = 4.8`.
Genre and mood therefore each have twice the maximum weight of energy.

**Ranking rule (a list of songs):** Score every song using the same rule, sort
the songs from highest to lowest score, and recommend the first `k` songs. If
scores tie, keep the songs in their original order.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app from the repository root. It displays the top five
   recommendations for each of five sample profiles, including energy
   extremes and preferences with no matching genre or mood:

```bash
python -m src.main
```

### Running Tests

Run the tests from the repository root with:

```bash
python -m pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Example excerpt for the first profile:

```text
Loaded 20 songs.

Profile 1: genre=pop, mood=happy, energy=0.82
Top recommendations:

Sunrise City - Score: 5.00
Because: Genre matches: pop; Mood matches: happy; Energy 0.82 compared with target 0.82 (closeness: 1.00)
...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

The following output is from the original closeness rule, before increasing
energy sensitivity. The current rule can produce different scores and ties.

``` bash

Profile 1: genre=pop, mood=happy, energy=0.82
Top recommendations:

Sunrise City - Score: 5.00
Because: Genre matches: pop; Mood matches: happy; Energy 0.82 compared with target 0.82 (closeness: 1.00)

Golden Hour Walk - Score: 4.88
Because: Genre matches: pop; Mood matches: happy; Energy 0.70 compared with target 0.82 (closeness: 0.88)

Rooftop Lights - Score: 2.94
Because: Mood matches: happy; Energy 0.76 compared with target 0.82 (closeness: 0.94)

Running Wild - Score: 2.92
Because: Genre matches: pop; Energy 0.90 compared with target 0.82 (closeness: 0.92)

Window Seat - Score: 2.91
Because: Mood matches: happy; Energy 0.73 compared with target 0.82 (closeness: 0.91)


Profile 2: genre=lofi, mood=chill, energy=0.0
Top recommendations:

Quiet Window - Score: 4.68
Because: Genre matches: lofi; Mood matches: chill; Energy 0.32 compared with target 0.00 (closeness: 0.68)

Library Rain - Score: 4.65
Because: Genre matches: lofi; Mood matches: chill; Energy 0.35 compared with target 0.00 (closeness: 0.65)

Midnight Coding - Score: 4.58
Because: Genre matches: lofi; Mood matches: chill; Energy 0.42 compared with target 0.00 (closeness: 0.58)

Distant Planets - Score: 2.76
Because: Mood matches: chill; Energy 0.24 compared with target 0.00 (closeness: 0.76)

Spacewalk Thoughts - Score: 2.72
Because: Mood matches: chill; Energy 0.28 compared with target 0.00 (closeness: 0.72)


Profile 3: genre=rock, mood=intense, energy=1.0
Top recommendations:

Storm Runner - Score: 4.91
Because: Genre matches: rock; Mood matches: intense; Energy 0.91 compared with target 1.00 (closeness: 0.91)

Electric Horizon - Score: 4.88
Because: Genre matches: rock; Mood matches: intense; Energy 0.88 compared with target 1.00 (closeness: 0.88)

Gym Hero - Score: 2.93
Because: Mood matches: intense; Energy 0.93 compared with target 1.00 (closeness: 0.93)

Running Wild - Score: 2.90
Because: Mood matches: intense; Energy 0.90 compared with target 1.00 (closeness: 0.90)

Sunrise City - Score: 0.82
Because: Energy 0.82 compared with target 1.00 (closeness: 0.82)


Profile 4: genre=classical, mood=chill, energy=0.28
Top recommendations:

Spacewalk Thoughts - Score: 3.00
Because: Mood matches: chill; Energy 0.28 compared with target 0.28 (closeness: 1.00)

Quiet Window - Score: 2.96
Because: Mood matches: chill; Energy 0.32 compared with target 0.28 (closeness: 0.96)

Distant Planets - Score: 2.96
Because: Mood matches: chill; Energy 0.24 compared with target 0.28 (closeness: 0.96)

Library Rain - Score: 2.93
Because: Mood matches: chill; Energy 0.35 compared with target 0.28 (closeness: 0.93)

Midnight Coding - Score: 2.86
Because: Mood matches: chill; Energy 0.42 compared with target 0.28 (closeness: 0.86)


Profile 5: genre=classical, mood=melancholic, energy=0.4
Top recommendations:

Focus Flow - Score: 1.00
Because: Energy 0.40 compared with target 0.40 (closeness: 1.00)

Paper Skies - Score: 0.99
Because: Energy 0.39 compared with target 0.40 (closeness: 0.99)

Midnight Coding - Score: 0.98
Because: Energy 0.42 compared with target 0.40 (closeness: 0.98)

Open Pages - Score: 0.98
Because: Energy 0.38 compared with target 0.40 (closeness: 0.98)

Coffee Shop Stories - Score: 0.97
Because: Energy 0.37 compared with target 0.40 (closeness: 0.97)
```

The first profile produces an exact match. The two boundary-energy profiles
still favor genre and mood matches, then use energy closeness to distinguish
them. The fourth profile has no matching genre, so mood and energy determine
its ranking. The fifth has neither a matching genre nor mood, so its
recommendations depend entirely on energy.

After the sensitivity change, the same five songs remained in the same order
for every profile. Scores for non-exact energy matches decreased: for example,
Quiet Window's score fell from 4.68 to 4.36 and Storm Runner's from 4.91 to
4.82, while both remained first for their profiles. Exact-energy top matches
retained their scores. See the [model card evaluation](model_card.md#7-evaluation)
for the comparison across all five profiles.

These examples do not establish whether real users would like the results.
The sensitivity change is covered by automated tests, but other weight or
additional feature comparisons have not yet been tested.

---

## Limitations and Risks

- The catalog has only 20 songs and does not include every genre or mood.
- Genre and mood matches each outweigh the entire energy contribution.
- Energy differences of 0.5 or more all receive the same zero closeness score,
  so the model cannot distinguish between them on energy alone.
- The score ignores acousticness, tempo, valence, danceability, lyrics, and
  listening history. A user who dislikes acoustic music could still receive
  acoustic recommendations.
- Missing category matches can produce recommendations based only on energy,
  without warning that no genre or mood matches exist.
- The simulation has not been evaluated with real listeners, so its
  usefulness and fairness are unknown.

---

## Reflection

[**Model Card**](model_card.md)

I found it interesting to use a user profile to build a basic recommendation
system. I expected the algorithm to be more complicated, but I realized I
had been overthinking the basic idea: preferences can be turned into scores
that determine an ordering.

I am concerned that genre and mood matches could produce acoustic
recommendations even for someone who dislikes acoustic music. Because the
system ignores acousticness, and because the small catalog does not represent
every taste, the results may work better for some users than others.

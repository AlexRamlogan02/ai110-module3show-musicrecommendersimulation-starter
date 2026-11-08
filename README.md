# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

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
- Add an energy closeness score of `1 - abs(song.energy - user.target_energy)`.
  Assuming both energy values are between 0 and 1, an exact match adds 1 point
  and the largest possible difference adds 0 points.

Both energy values must be numeric and between 0 and 1; invalid values raise an
error. The total score ranges from 0 to 5. For example, a song matching both genre and
mood with energy 0.8 for a user targeting 0.7 scores `2 + 2 + 0.9 = 4.9`.
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

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

``` bash
Loaded 20 songs.

Top recommendations:

Sunrise City - Score: 4.98
Because: Genre matches: pop; Mood matches: happy; Energy 0.82 compared with target 0.80 (closeness: 0.98)

Golden Hour Walk - Score: 4.90
Because: Genre matches: pop; Mood matches: happy; Energy 0.70 compared with target 0.80 (closeness: 0.90)

Rooftop Lights - Score: 2.96
Because: Mood matches: happy; Energy 0.76 compared with target 0.80 (closeness: 0.96)

Window Seat - Score: 2.93
Because: Mood matches: happy; Energy 0.73 compared with target 0.80 (closeness: 0.93)

Running Wild - Score: 2.90
Because: Genre matches: pop; Energy 0.90 compared with target 0.80 (closeness: 0.90)

```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this

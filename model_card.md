# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**Music Recommender Simulation**

## 2. Intended Use

This application is intended to recommend songs from a relatively small catalog to understand how content-based recommendations work. It assumes a user can express one preferred genre, one preferred mood, and a target energy between 0 and 1.

## 3. How the Model Works

The functional recommender compares each song with a user's preferences. It
adds two points for a matching genre, two for a matching mood, and up to one
for energy close to the user's target. Energy closeness now drops by 0.2 for
each 0.1 difference in energy, reaching zero at a difference of 0.5 or more.
It sorts songs by score and returns
the top five in the sample command-line run. Each recommendation includes
reasons for its score.

This replaces the functional starter placeholders with CSV loading, scoring,
and ranking. The separate object-oriented recommender is still a placeholder.
The acoustic preference in `UserProfile` is not used in the functional score.

## 4. Data

The catalog contains 20 example songs.
Genres include pop, lofi, rock, ambient, jazz, synthwave, and indie pop; moods
include happy, chill, intense, relaxed, moody, and focused. Each record also
contains energy, tempo, valence, danceability, and acousticness.

## 5. Strengths

- The scoring is simple and explanations show which attributes contributed.
- For the pop, happy profile, Sunrise City matches all three preferences
  exactly and scores 5.00.
- The low-energy lofi and high-energy rock profiles rank songs matching both
  genre and mood above songs matching only mood, with energy distinguishing
  songs within those groups.
- If a genre is absent, the system can still rank songs by mood and energy.

These are observations from the five example profiles, not evidence that
real users will enjoy the recommendations.

## 6. Limitations and Bias

- The catalog is small and unevenly represented. Users seeking a genre or
  mood missing from the catalog cannot receive an exact match.
- Genre and mood are exact matches worth two points each; energy contributes
  at most one. A genre or mood match can therefore outweigh a closer energy
  match, and related genre or mood labels are treated as entirely different.
- The system does not use tempo, valence, danceability, acousticness, lyrics,
  or listening history. Even if a user dislikes acoustic music, matching
  genre and mood may lead to acoustic recommendations.
- When both genre and mood are absent, recommendations depend only on energy,
  which may not reflect the user's taste. The system still returns up to five
  results rather than warning that category matches are unavailable.
- Energy differences of 0.5 or more all receive zero closeness, so energy
  alone cannot distinguish between those songs.
- There is no user feedback, diversity requirement, or fairness evaluation.
  The catalog and labels may favor some listeners' tastes over others.

## 7. Evaluation

The same five profiles were run before and after increasing energy
sensitivity. The original rule deducted one point per unit of energy
difference; the revised rule deducts two, with closeness capped at zero.

| Profile | Preference | Top result | Previous score | Revised score | Change |
|---|---|---|---:|---:|---:|
| 1 | pop, happy, energy 0.82 | Sunrise City | 5.00 | 5.00 | 0.00 |
| 2 | lofi, chill, energy 0.0 | Quiet Window | 4.68 | 4.36 | -0.32 |
| 3 | rock, intense, energy 1.0 | Storm Runner | 4.91 | 4.82 | -0.09 |
| 4 | classical, chill, energy 0.28 | Spacewalk Thoughts | 3.00 | 3.00 | 0.00 |
| 5 | classical, melancholic, energy 0.4 | Focus Flow | 1.00 | 1.00 | 0.00 |

**Ranking movement:** In these results, all five profiles retained the same
top five songs in the same order. No song entered or left the top five. The
exact-energy top matches for profiles 1, 4, and 5 kept their scores; other
results lost points according to their energy difference. For example, Golden
Hour Walk fell from 4.88 to 4.76 but stayed second in profile 1, while Library
Rain fell from 4.65 to 4.30 but stayed second in profile 2.

The increased penalty widened score gaps between songs with different energy
distances. Profile 4's Quiet Window and Distant Planets both display 2.92
after the change, compared with 2.96 before; their displayed order did not
change. Profile 5 still relies entirely on energy because neither preferred
category appears in the catalog.

These cases check an exact match, both energy boundaries, and missing
categories; automated tests also check scoring and each profile's top result.
They do not measure recommendation quality, accuracy, or fairness for real
listeners. Other weights and additional features have not yet been compared.

## 8. Future Work

- Experiment with genre, mood, and energy weights and compare the results.
- Incorporate an explicit acoustic preference and consider other audio
  features such as tempo and valence.
- Expand the catalog and support related genres, multiple preferences, and
  missing-match warnings.
- Explore recommendation diversity and evaluate with real user feedback.
- Implement the object-oriented recommender and its explanations.

## 9. Personal Reflection

I found it interesting to use user profiles to create a basic recommendation
system. I expected the algorithm to be more complicated, but I realized I
had been overthinking how the basic scoring works. I am concerned that genre
and mood matches could produce acoustic recommendations even when a user does not like acoustic music, because the current score does not consider thatpreference.

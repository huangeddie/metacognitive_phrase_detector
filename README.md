# Metacognitive phrase detector

This project is the result of research on automatic detection of metacognition (thinking about thinking) from user-generated text. If you would like to learn more, see this paper:

> Huang, E., Valdiviejas, H., & Bosch, N. (in press). I'm sure! Automatic detection of metacognition in online course discussion forums. In Proceedings of the 8th International Conference on Affective Computing and Intelligent Interaction (ACII 2019). Piscataway, NJ: IEEE.

## Installation

Clone this repository to your project directory, so that your script that uses this package is in the level of the tree. For example, you may create a script called `my_test.py` and set up your project like this:

```bash
my_project/my_test.py
my_project/metacognitive_phrase_detector/*
```

## Example usage

```python
from metacognitive_phrase_detector.algorithm import analyze_text

text = "Although your estimate doesn't agree with mine of 20, I believe you bring up a very valid point. I had not even considered that the star formation rate was much faster long ago than it is now. Many of the stars in the galaxy that we can see today could very well have been born billions of years ago. It's a smart idea to consider not just rely on what we can see in the sky, but on the changes in the galaxy that occur. Although with this new information I do not know what my new estimate would be, but I believe that there is undoubtedly merit in your reasoning and estimate"

mc_phrases, annotated_post = analyze_text(text)
print(annotated_post)
```

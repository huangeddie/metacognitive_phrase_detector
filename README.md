# Usage

```
from algorithm.data import MCOracle, Connotation
from algorithm import algorithm

text = "Although your estimate doesn't agree with mine of 20, I believe you bring up a very valid point. I had not even considered that the star formation rate was much faster long ago than it is now. Many of the stars in the galaxy that we can see today could very well have been born billions of years ago. It's a smart idea to consider not just rely on what we can see in the sky, but on the changes in the galaxy that occur. Although with this new information I do not know what my new estimate would be, but I believe that there is undoubtedly merit in your reasoning and estimate"

mc_phrases, annotated_post = algorithm.analyze_text(text)

print(annotated_post)

```

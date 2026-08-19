# Controlled chat observation

The three-turn sequence used with the 14B model was repeated:

1. Confirm audio-style presence: `やあ、聞こえてる？`
2. Ask about `原っぱ大学` without further context.
3. Explain that it is a play-oriented school in Zushi, Kanagawa.

## Behavior

- The first response was normal and fast.
- The model appropriately said it could not identify `原っぱ大学` and requested clarification.
- It nevertheless claimed that it had searched for information even though the local chat harness provides no browsing tool.
- After the location hint, it speculated that the user might mean `原っぱピアノスクール`, without evidence.
- Unlike the 14B model, it did not invent a founding year, a municipal school, a detailed mission, or an attached kindergarten.

## Interpretation

The 32B response was more restrained than the 14B response but still hallucinated both tool use and a possible institution name. Model scale reduced the severity in this one sample; it did not make factual chat trustworthy.

# Result

## Controlled slugify outcome

- Task success: Yes
- Tests before: 1/5 passing
- Tests after first inference turn: 5/5 passing
- Human correction prompts: 0
- Inference turns: 1
- Files changed: 1 (`slugify.py`)
- Tests modified: No

The model replaced punctuation with spaces, collapsed all whitespace to one hyphen, and stripped boundary hyphens. This avoided the repeated-hyphen mistake made by both smaller models.

## Three-model comparison

| Measure | 7B BF16 | 14B AWQ | 32B AWQ |
|---|---:|---:|---:|
| Tests after first turn | 3/5 | 4/5 | 5/5 |
| Tests after three turns | 3/5 | 5/5 | 5/5 |
| Human corrections | 2 | 2 | 0 |
| Final result | Partial | Success | Success |

## Initial interpretation

This is the clearest capability scaling result so far. On the deterministic task, 32B understood the interaction between punctuation and whitespace on the first attempt and required no human recovery prompt.

The result does not yet establish practical usability. The controlled chat still produced unsupported claims, and the generated game remains minimal. Human interaction with the game is required before judging whether the 32B tier crosses the user's adoption threshold.

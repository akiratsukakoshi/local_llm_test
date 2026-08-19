# Result

## Outcome

- Task success: Yes
- Tests before: 1/5 passing
- Tests after first inference turn: 4/5 passing
- Tests after first correction: 4/5 passing
- Tests after second correction: 5/5 passing
- Human correction prompts: 2
- Files changed: 1 (`slugify.py`)
- Tests modified: No

## Turn-by-turn behavior

1. The model handled whitespace, numbers, and leading/trailing separators, improving the fixture from 1/5 to 4/5. It still converted adjacent punctuation and whitespace into separate hyphens.
2. Given the exact remaining failure, it added `+` to the punctuation regex. This correctly described punctuation runs but did not address the hyphens created separately from surrounding whitespace, so the output and failing test were unchanged.
3. Explicitly told that the output was unchanged, it added a final repeated-hyphen collapse. All five tests then passed.

## Comparison with Experiment 001

| Measure | 7B BF16 | 14B AWQ |
|---|---:|---:|
| Tests after first turn | 3/5 | 4/5 |
| Tests after three turns | 3/5 | 5/5 |
| Successful self-corrections | 0 | 1 |
| Final result | Partial | Success |

## Attribution

- Model capability: The larger practical configuration performed better and eventually converted explicit failure evidence into a correct edit.
- Remaining weakness: It still missed a simple interaction between two substitutions twice and required detailed human steering.
- Coding-agent harness: Aider applied each emitted edit correctly and did not modify the read-only tests.
- Inference runtime: Stable; all API calls completed normally.
- GPU / VRAM: Not limiting at the configured 8,192-token context. vLLM reserved 21,787 MiB and reported a 10.06 GiB KV cache.
- Quantization: A confounding variable. This experiment cannot attribute the improvement solely to parameter count because the 14B model used AWQ 4-bit while the 7B model used BF16.

## Interesting observation

The 14B configuration crossed the success threshold on this small task, unlike the 7B baseline. The improvement is real for this fixture but modest in agentic terms: the model still needed two precise correction prompts for a short regex function.

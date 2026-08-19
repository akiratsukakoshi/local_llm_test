# Initial Stage 2 comparison matrix

Use Qwen3.8-27B Q4_K_M, RTX 3090 24GB, llama.cpp, 16K context, Q8 KV cache, Aider 0.86.2, the same fixture, and the same endpoint settings unless a row explicitly changes one variable.

| Order | Contract | Main question | Major variable |
|---|---|---|---|
| 1 | `smoke-autonomous-control.json` | Can the outer loop complete the known fixture with minimal behavioral guidance? | Control condition |
| 2 | `smoke-autonomous.json` | Do common and autonomous rules improve behavior? | Rule packet |
| 3 | `smoke-plan.json` | Can Qwen produce a useful evidence-based plan without editing? | Plan-only mode |
| 4 | `smoke-delegated.json` | Can Qwen implement a bounded upstream specification and defer approval? | Delegated role |

Rows 1 and 2 are the only direct rule comparison. Rows 3 and 4 test different roles and must not be interpreted as a rule-only comparison.

Repeat stochastic conditions before drawing a strong conclusion. Preserve every run rather than replacing a prior result.

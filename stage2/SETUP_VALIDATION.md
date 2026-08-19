# Stage 2 setup validation

- Date: 2026-08-19 JST
- Live Qwen request: not performed
- RunPod resource created or started: no

## Verified locally

1. Python compilation completed for the Stage 2 package.
2. All 11 unit tests passed.
3. The autonomous, plan, delegated, and autonomous-control task contracts validated.
4. Four fixture copies were prepared as independent clean Git repositories.
5. The intentionally broken fixture started with 3/5 tests passing and two known failures.
6. Dry runs created prompts and exact Aider commands without contacting the model.
7. Autonomous and delegated commands expose only `slugify.py` as editable and load `test_slugify.py` read-only.
8. Plan mode loads both implementation and test files read-only with Aider ask mode.
9. Rule files are loaded with `--read` and cannot be edited through the supplied file set.
10. A no-model integration run performed two bounded attempts, fed the first real test failure into the second prompt, stopped with `tests_failed`, and left the workspace clean.

## Unit-test result

```text
Ran 11 tests in 0.148s

OK
```

## No-model integration result

```json
{
  "task_id": "s2-harness-noop",
  "status": "tests_failed",
  "attempts": 2,
  "tests_passed": false
}
```

Both attempt gate reports contained zero changed files and zero violations. The second prompt contained the actual two-test failure from attempt one.

## Deliberately not yet verified

- Qwen3.8 instruction adherence under the new rule packets;
- Aider live editing through the outer loop;
- successful-test and review recording after a live implementation;
- scratch-adapter tool calling;
- automatic high-end-AI task-packet generation or review;
- performance, VRAM, wall time, and RunPod cost for Stage 2.

The first live comparison should use `experiments/COMPARISON_MATRIX.md` and begin with the autonomous control contract so the rule packet remains the only major variable in the next run.

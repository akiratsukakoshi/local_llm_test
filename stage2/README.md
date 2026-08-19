# Stage 2 — Coding-agent harness lab

Stage 2 asks a different question from the model/GPU baselines in Stage 1:

> Can Qwen3.8-27B become a dependable implementation worker when rules, deterministic gates, tests, and eventually an upstream high-end AI surround it?

The long-term target is a planner-worker-reviewer system in which a high-end AI defines and reviews bounded work while the local model performs repository investigation, implementation, test-driven correction, and reporting.

No GPU resource is created or started by this directory. A live run requires the user to start the intended RunPod endpoint and SSH tunnel explicitly.

## Architecture implemented now

```text
Task contract
  -> Stage 2 outer orchestrator
       -> validates clean isolated Git workspace
       -> injects mode-specific read-only rules
       -> calls Aider once per bounded attempt
       -> checks changed paths and diff limits
       -> runs only pre-approved test commands
       -> returns real failures for the next attempt
       -> requires human or upstream-AI review
  -> Aider 0.86.2
  -> OpenAI-compatible Qwen3.8-27B endpoint
```

Rules are soft behavioral guidance. Path, diff, test, attempt, and review gates are deterministic outer-harness decisions.

## Directory map

```text
stage2/
  configs/            # model and Aider endpoint settings
  contracts/          # task-contract JSON Schema
  fixtures/           # immutable source fixtures for controlled tests
  orchestrator/       # standard-library Python outer harness
  rules/              # common and mode-specific read-only instructions
  tasks/              # executable task packets
  tests/              # tests for contract validation and gates
  workspaces/         # disposable nested Git repositories; ignored
  runs/               # raw prompts, logs, diffs, and results; ignored
  experiments/        # promoted, durable experiment summaries
```

The project root currently is not a Git repository. Each Stage 2 task workspace is therefore initialized as its own isolated Git repository. This is intentional: gates compare every live change against a known clean fixture commit without altering Stage 1 artifacts.

## Three modes

### `autonomous`

Qwen investigates and edits within a bounded file scope. The harness executes declared tests and may return failures for up to `max_attempts`.

### `plan`

All repository files are read-only. Aider uses ask mode, and the harness rejects any filesystem change. The output is reviewed as a plan rather than applied as code.

### `delegated`

The task contract represents an upstream AI's specification. Qwen implements it but cannot approve its own work. Even after all tests pass, status remains `awaiting_review` until the reviewer records a decision.

## Local validation without a GPU

Run from `/home/tukapontas/local_llm_test`:

```bash
python3 -m unittest discover -s stage2/tests -v

python3 -m stage2.orchestrator validate \
  stage2/tasks/smoke-autonomous.json
```

Prepare an immutable-fixture copy as a clean nested Git repository:

```bash
python3 -m stage2.orchestrator prepare \
  stage2/tasks/smoke-autonomous.json
```

Build and record the exact Aider command without contacting Qwen:

```bash
python3 -m stage2.orchestrator run \
  stage2/tasks/smoke-autonomous.json \
  --config stage2/configs/aider-qwen38.json \
  --dry-run
```

Preparation never overwrites an existing workspace. Use a new task id and workspace for a new controlled run. The harness also refuses to start a new run if the selected Git workspace is dirty.

## Live Qwen run

Before a live run, explicitly confirm:

1. The intended RunPod GPU and current hourly price.
2. The Qwen3.8 llama.cpp server is running.
3. The SSH tunnel exposes the endpoint at `http://127.0.0.1:8000/v1`.
4. The selected workspace is clean.

Then omit `--dry-run`:

```bash
python3 -m stage2.orchestrator run \
  stage2/tasks/smoke-autonomous.json \
  --config stage2/configs/aider-qwen38.json
```

The run produces `stage2/runs/<timestamp>-<task-id>/result.json`, prompts, the exact Aider command, Aider logs, gate reports, test logs, and `final.diff`.

Passing tests do not imply acceptance. Record the review after inspecting the diff and logs:

```bash
python3 -m stage2.orchestrator review \
  stage2/runs/<run-directory> \
  --decision approve \
  --reviewer human \
  --notes "Scope and behavior verified."
```

Decisions are `approve`, `request_changes`, or `reject`.

## Safety properties

The current harness enforces:

- task, rule, fixture, and workspace paths stay inside their Stage 2 areas;
- implementation workspaces must be clean standalone Git repositories;
- protected paths cannot change;
- every changed path must match `allowed_paths`;
- new files are blocked unless the contract explicitly permits them;
- changed file and line totals have fixed upper bounds;
- `git diff --check` must pass;
- only test commands written by the task author are executed;
- test processes have timeouts;
- attempts have a fixed upper bound;
- approval is separate from implementation.

The model is not given a general shell tool. Aider is called non-interactively with shell suggestions disabled, and the outer harness runs declared test commands itself.

## Current limits

- The first adapter is Aider; the scratch tool-calling agent is a later controlled variable.
- Existing files are the reliable initial edit scope. New-file tasks require an explicit contract change and further evaluation.
- The upstream-AI interface is currently the JSON task packet plus run artifacts. Automatic Codex/Claude API invocation is intentionally deferred until the manual delegated loop is understood.
- Review records a decision but does not automatically commit, merge, push, deploy, or discard changes.
- A gate violation leaves the workspace intact for diagnosis. The harness does not erase or reset work automatically.

See `PROTOCOL.md` for the progression from the Aider wrapper to the planner-worker-reviewer target.

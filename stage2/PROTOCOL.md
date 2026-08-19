# Stage 2 experimental protocol

## Research objective

Discover the smallest dependable harness in which Qwen3.8-27B can contribute to real software development, especially as an implementation worker directed and reviewed by a higher-end AI.

The experiment must distinguish model capability, Aider behavior, outer-gate behavior, task-specification quality, upstream planner/reviewer quality, and runtime/context limitations.

Change one major variable at a time and promote completed raw runs into durable records under `stage2/experiments`.

## Phase 1 — Outer orchestrator around unchanged Aider

Purpose: establish safety, repeatability, and measurable autonomous correction without modifying Aider.

1. Validate the orchestrator with no model endpoint.
2. Run the same slugify fixture with and without mode-specific rules.
3. Measure rule adherence, scope violations, test outcomes, retries, latency, and human review result.
4. Advance to an unfamiliar single-file bug.
5. Advance to a bounded multi-file feature with protected tests.
6. Run an adversarial task packet containing one incorrect premise.

Exit evidence:

- gate tests pass;
- every run is reproducible from a task contract and clean commit;
- no protected change can pass the gate;
- Qwen can use real test feedback across bounded retries;
- Aider-specific limitations are documented rather than attributed to the model without evidence.

## Phase 2 — Minimal scratch harness

Purpose: remove Aider as a variable and measure Qwen's own tool selection and repository navigation.

Planned tools are bounded file listing/search, file reads, structured patch proposal, validated patch application, approved test requests, and finish/blocked reporting.

Use the same task contracts, fixtures, gates, metrics, and Qwen endpoint as Phase 1. Compare Aider and scratch adapters on identical tasks before adding new capabilities.

Exit evidence:

- structured tool calls are reliable enough for repeated runs, or a text protocol is selected based on observed failures;
- context and repository-map strategy are recorded;
- loops, malformed actions, and recovery behavior are measured;
- the adapter comparison identifies whether Aider helps or limits Qwen.

## Phase 3 — High-end planner/reviewer with local implementation worker

Purpose: test the intended practical architecture.

```text
High-end AI: inspect, plan, bound scope, define acceptance criteria
  -> machine-readable task contract
Qwen3.8-27B: implement and respond to approved test evidence
  -> diff, test logs, assumptions, unresolved risks
High-end AI: review against contract and repository evidence
  -> approve, request changes, or reject
Human: retain authority for sensitive changes and final adoption
```

Start with manually copied task packets and review artifacts. Automate the high-end connector only after the packet format and review responsibilities stabilize.

Evaluate at least a small deterministic bug fix, unfamiliar debugging task, bounded multi-file feature, ambiguous or incorrect upstream premise, and real but non-critical project change.

## Practical-development candidate criteria

A configuration becomes a candidate for real development only when evidence shows:

- protected-path violations are consistently blocked;
- accepted changes pass declared tests without test weakening;
- the reviewer can understand the complete provenance from task packet to diff;
- failures stop within fixed time/attempt budgets;
- the local worker reports ambiguity instead of silently expanding scope;
- human intervention, latency, and supervision are acceptable for the task class;
- repeated success is demonstrated across multiple tasks, not one showcase;
- cost and operational complexity are favorable compared with giving the whole task to the hosted agent.

No fixed success percentage is assumed yet. Set a threshold only after the first task suite reveals realistic variance and failure severity.

## Core run metrics

- contract id, mode, fixture commit, and exact prompt;
- model, quantization, runtime, context, GPU, and VRAM;
- Aider or scratch-adapter version;
- inference attempts and test attempts;
- changed files and changed lines;
- gate violations;
- tests passed/failed;
- wall-clock time and model generation performance;
- human interventions;
- upstream review decision and requested corrections;
- final task outcome: success, partial, blocked, or unsafe proposal;
- qualitative trust and daily-use assessment.

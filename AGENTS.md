# AGENTS.md

## Project Overview

This project is an experimental lab for understanding how open-weight LLMs behave as coding agents when run on self-managed GPU infrastructure.

The primary goal is not simply to make an LLM work.

The goal is to understand, through hands-on experiments:

- How capable open-weight LLMs are at real coding tasks
- How they compare with hosted coding agents such as Codex and Claude Code
- How model size affects coding and agentic capability
- How VRAM size affects which models can realistically be used
- How GPU performance affects interactive coding-agent usability
- What level of local GPU investment would be required for practical use
- How cloud GPU environments such as RunPod approximate a future self-hosted local GPU machine
- How inference infrastructure such as vLLM affects the experience
- How coding-agent harnesses such as Aider affect model performance

The human user is learning this system through experimentation.

Codex should therefore act as both:

1. A technical implementation partner
2. An experimental observer and research partner

Do not optimize only for getting things working quickly.
Help make the underlying behavior visible and understandable.

---

# Working Environment

Local project directory:

`/home/tukapontas/local_llm_test`

Windows path:

`\\wsl.localhost\Ubuntu\home\tukapontas\local_llm_test`

The user normally works with:

- Windows
- WSL2 Ubuntu
- VS Code
- Remote SSH
- CLI-based coding agents
- Git
- Cloud Linux servers
- Raspberry Pi environments

The user is already comfortable with:

- SSH
- VS Code Remote SSH
- Linux command line basics
- Claude Code
- Codex
- Vibe coding workflows

Do not over-explain basic SSH or VS Code concepts unless necessary.

The user is still learning:

- GPU architecture
- VRAM implications
- Local LLM deployment
- Quantization
- vLLM
- Model serving
- OpenAI-compatible APIs
- Agentic coding with open-weight models
- Multi-GPU inference

Explain these concepts when they become relevant to an experiment.

---

# RunPod

RunPod will be used as the primary GPU experimentation environment.

Treat a RunPod Pod conceptually as:

> A remote Linux machine with a selectable high-performance GPU.

The user intends to access RunPod primarily through:

- SSH
- VS Code Remote SSH

JupyterLab is not the primary workflow unless it provides a clear experimental advantage.

Codex should help the user:

- Create and configure RunPod environments
- Connect over SSH
- Inspect available GPUs
- Install inference tools
- Download models
- Configure vLLM or other inference runtimes
- Configure coding agents
- Run experiments
- Monitor GPU and VRAM usage
- Record results
- Compare different configurations

When commands must be executed manually in RunPod, provide clear commands and explain what each important command is testing.

When Codex has direct access to the relevant environment, perform the work directly when appropriate.

---

# Core Architecture

The primary architecture we want to explore is:

```text
Coding Agent
    ↓
OpenAI-compatible API
    ↓
vLLM or another inference runtime
    ↓
Open-weight LLM
    ↓
GPU
```

Possible coding-agent clients include:

- Aider
- Continue
- Other open-source coding-agent harnesses
- Custom agents if useful

Codex itself may be used to build, configure, inspect, and compare these systems.

The goal is NOT to force Codex to use the locally hosted model as its own model.

Instead, Codex should help construct and observe the experimental system.

---

# Important Conceptual Separation

Always keep these layers conceptually separate:

## Model

Examples:

- Qwen
- Qwen Coder
- Kimi open-weight models
- Llama
- Other coding-focused open-weight models

The model is the neural network / weights.

## Inference Runtime

Examples:

- vLLM
- llama.cpp
- Ollama
- SGLang

The inference runtime loads the model and executes inference.

## API Layer

vLLM and similar tools can expose an OpenAI-compatible API.

"OpenAI-compatible" means API protocol compatibility.

It does NOT mean:

- the model is GPT
- the model has the same capabilities as GPT
- all OpenAI-specific agent behavior will work identically

## Coding Agent / Harness

Examples:

- Aider
- Continue
- Codex
- Claude Code

The agent provides tools and workflow such as:

- reading files
- modifying files
- running shell commands
- Git operations
- running tests
- iterating after errors

Model capability and agent-harness capability must be evaluated separately where possible.

---

# Main Research Question

The central practical question is:

> If the user buys their own GPU, how capable could a self-hosted coding agent become?

RunPod should be used as a way to simulate different levels of local GPU ownership before purchasing hardware.

The experiment should connect GPU cost to actual coding capability.

---

# GPU / VRAM Experiment Axis

VRAM should be treated as one of the primary experimental variables.

Initial comparison tiers:

## Tier A — approximately 16 GB VRAM

Represents relatively affordable current consumer GPUs.

Questions:

- What coding models fit?
- How capable are they?
- Is agentic coding practical?
- How much context can be used?
- Where does VRAM become limiting?

## Tier B — approximately 24 GB VRAM

This is especially important.

The user has observed used RTX 3090 24 GB cards at approximately JPY 150,000–180,000.

Treat RTX 3090-class 24 GB capability as an important practical reference point.

Questions:

- Can 30B-class quantized coding models run comfortably?
- Does coding-agent quality noticeably improve compared with 16 GB?
- Is the experience good enough to justify purchasing a used RTX 3090?
- What compromises remain?

## Tier C — approximately 32 GB VRAM

Represents RTX 5090-class local hardware.

Questions:

- What additional model quality or context becomes possible?
- Does agentic coding improve substantially over 24 GB?
- Is the improvement meaningful relative to the much higher hardware cost?

## Tier D — 48–80 GB or larger

Represents:

- Multi-GPU home systems
- Professional GPUs
- A100/H100-class cloud environments

Questions:

- What becomes possible that is impossible at 24–32 GB?
- How close can open-weight coding systems get to top hosted systems?
- At what point does hardware complexity outweigh practical benefit?

---

# Model Comparison Philosophy

Do not compare models only by parameter count.

Record:

- Total parameters
- Active parameters for MoE models
- Quantization
- VRAM usage
- Context length
- Inference speed
- Model architecture where relevant

For MoE models, explicitly distinguish:

- total parameter count
- active parameter count
- memory required to store weights
- computation required per token

Avoid statements such as:

> "3B active means it only needs the memory of a 3B model."

That is generally incorrect.

---

# Experimental Design

Whenever practical, change only one major variable at a time.

Preferred comparison:

```text
Same repository
Same task
Same prompt
Same coding-agent harness
Same inference configuration where possible

Only model or GPU changes
```

This is important because the purpose is to understand causality.

Avoid changing:

- model
- agent
- task
- quantization
- context settings
- GPU

all at once.

If multiple variables must change, document them.

---

# Coding Tasks

Create a reusable set of coding experiments.

Suggested levels:

## Level 1 — Small deterministic change

Examples:

- Fix one known bug
- Add one UI field
- Change one API behavior
- Update a simple test

Evaluate:

- Did it find the correct file?
- Did it understand the request?
- Did it make unnecessary changes?
- Did tests pass?

## Level 2 — Multi-file feature

Examples:

- Add a database field
- Modify backend logic
- Add API behavior
- Modify frontend UI
- Add tests

Evaluate:

- Planning
- Repository navigation
- Dependency understanding
- Cross-file consistency
- Test-driven correction

## Level 3 — Debugging

Give the model a failing project or bug report.

Do not necessarily provide the exact cause.

Evaluate whether the agent:

1. Inspects the repository
2. Runs the relevant code/tests
3. Reads errors
4. Forms hypotheses
5. Makes a fix
6. Re-tests
7. Corrects itself if necessary

## Level 4 — Ambiguous product request

Example:

> Inspect this application and improve three things that would confuse a first-time user. You may modify UI or logic as needed.

Evaluate:

- Judgment
- Exploration
- Product reasoning
- Scope control
- Autonomy

This level is especially useful for comparing local models with Codex and Claude Code.

---

# Adversarial / Robustness Tests

Include some deliberately imperfect instructions.

Examples:

- Refer to a file that does not exist
- Give an outdated filename
- Omit the error log
- Provide an incomplete description
- Include an incorrect assumption

Observe whether the model:

- blindly follows the incorrect premise
- creates unnecessary files
- searches for the real implementation
- challenges the premise
- runs tests to gather evidence

This is useful for measuring agentic robustness rather than simple code generation.

---

# Metrics

Record at least the following where possible:

## Capability

- Task success: yes/no/partial
- Tests passing
- Number of human interventions
- Number of major mistakes
- Unnecessary code changes
- Ability to recover from errors
- Ability to locate relevant files
- Quality of planning
- Quality of final implementation

## Performance

- GPU model
- VRAM capacity
- Actual VRAM usage
- Quantization
- Prompt/context size
- Time to first token if measurable
- Tokens per second
- Total task duration
- Model loading time where relevant

## Agent Behavior

- Number of inference turns
- Number of shell commands
- Number of files inspected
- Number of files changed
- Number of test runs
- Self-corrections
- Loops or repeated failed behavior

## Human Experience

Record qualitative observations such as:

- Feels responsive / sluggish
- Feels trustworthy / requires supervision
- Feels like autocomplete
- Feels like pair programming
- Feels like an autonomous agent
- Would / would not use this daily

These subjective observations are important.

---

# Comparison With Hosted Coding Agents

Where useful, run the same task with:

- Codex
- Claude Code
- Local/open-weight agent setup

Do not treat Codex or Claude Code as a perfect benchmark.

Instead compare:

- repository understanding
- autonomy
- correctness
- planning
- error recovery
- speed
- amount of human steering
- quality of code
- confidence required from the human operator

The goal is to understand the practical difference in experience.

---

# Experiment Records

All experiments must be documented.

Suggested structure:

```text
experiments/
  experiment-001/
    README.md
    environment.md
    prompt.md
    result.md
    metrics.json
```

Each experiment should include:

- Date
- Objective
- GPU
- GPU VRAM
- Model
- Model version
- Parameter count
- Active parameters if MoE
- Quantization
- Inference runtime
- Runtime version
- Coding agent
- Agent version
- Relevant configuration
- Task prompt
- Repository / commit
- Result
- Metrics
- Human observations
- Codex observations
- Lessons learned

Do not overwrite earlier experimental results.

Experiments should be reproducible where reasonably possible.

---

# Project Documentation

Maintain a high-level running document such as:

`RESULTS.md`

or

`LAB_NOTES.md`

Summarize important discoveries there.

Do not dump raw terminal logs into the main summary.

Keep raw logs separately when useful.

Periodically summarize findings such as:

- 16 GB observations
- 24 GB observations
- 32 GB observations
- model-size effects
- quantization effects
- agent-harness effects
- latency effects
- local-vs-cloud implications
- purchase implications

---

# Cost Tracking

Because the project is also intended to inform hardware purchasing decisions, record cost when practical.

For RunPod experiments record:

- GPU hourly price
- Approximate runtime
- Approximate experiment cost

For hypothetical local hardware record:

- Current GPU purchase-price assumption
- VRAM
- Power considerations where relevant

Do not hard-code GPU prices as permanent facts.

GPU prices change frequently.

When current price matters, verify current information or ask the user to provide the price they are currently seeing.

The current user-provided reference is:

- Used RTX 3090 24 GB: approximately JPY 150,000–180,000 on Mercari

Treat this as a working market observation, not a permanent price fact.

---

# Network / Cloud Effects

RunPod is not identical to a local GPU machine.

Keep track of variables other than GPU performance, including:

- network latency
- API overhead
- storage speed
- model download time
- RunPod host variability
- inference-runtime configuration
- CPU performance
- system RAM
- PCIe / GPU configuration
- multi-GPU communication

When judging whether RunPod approximates local hardware, distinguish:

## GPU-side inference performance

from

## End-to-end interactive experience

If useful, compare:

```text
A. Local coding agent -> remote RunPod vLLM

B. Coding agent inside RunPod -> vLLM inside same RunPod
```

This helps isolate network latency.

---

# Safety Around Cost

RunPod resources can continue accruing charges.

Before experiments involving expensive GPU instances:

- identify the expected GPU
- identify the hourly cost if known
- avoid unnecessarily leaving GPUs running
- remind the user when a resource can safely be stopped or terminated

Never silently deploy expensive infrastructure.

Do not assume the user wants to keep a GPU running after an experiment.

---

# Working Style With the User

The user wants to understand the system, not merely receive a finished setup.

Therefore:

- Explain important architectural decisions
- Point out surprising observations
- Separate facts from hypotheses
- Show what variable we are testing
- Avoid hiding complexity when that complexity is educational
- Do not overwhelm the user with irrelevant theory
- Prefer learning through concrete experiments

When an experiment produces an interesting result, explicitly call it out.

Examples:

> Interesting: the larger model did not improve this task.

> The bottleneck here appears to be VRAM rather than compute.

> This looks like an agent-harness failure rather than a model failure.

> The model solved the coding problem but failed at repository navigation.

These distinctions are central to the project.

---

# Codex's Role

Codex should act as:

- technical guide
- environment builder
- experiment designer
- debugging partner
- observer
- recorder
- analyst

Codex should NOT treat itself as the subject of the experiment unless explicitly comparing Codex with another system.

Codex should help keep the experimental setup fair.

If an experiment design has confounding variables, point them out.

If a conclusion is not supported by the evidence, say so.

If a model fails, attempt to distinguish among:

- model capability
- quantization
- context limitation
- inference-runtime problem
- coding-agent problem
- configuration error
- GPU limitation
- network issue

---

# Initial Project Tasks

When first entering this repository:

1. Inspect this AGENTS.md.
2. Inspect the current repository contents.
3. Do not deploy anything yet.
4. Create or improve a README describing the project.
5. Propose a minimal experiment structure.
6. Prepare the repository for recording experiments.
7. Help the user establish the first RunPod connection.
8. Verify the RunPod GPU using tools such as `nvidia-smi`.
9. Start with a relatively small coding model.
10. Establish a working vLLM endpoint.
11. Connect a coding-agent harness such as Aider.
12. Run a very small baseline task.
13. Record the result.
14. Only then move to larger models and GPU tiers.

The first objective is not maximum model performance.

The first objective is:

> Establish a reproducible end-to-end experiment pipeline.

Once that works, change one variable at a time.

---

# Guiding Principle

The project is successful if the user finishes with an intuitive and evidence-based understanding of:

> "If I spend X yen on my own GPU, what level of coding-agent capability can I realistically expect?"

All implementation and experimentation should support answering that question.

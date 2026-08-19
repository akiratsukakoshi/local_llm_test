# Task s2-smoke-delegated

Mode: delegated
Attempt: 1 of 3

## Objective

Implement the upstream specification: repair only slugify.py so the existing URL-slug behavior satisfies the protected unit tests.

## Acceptance criteria

- Normalize every run of whitespace or punctuation separators to one hyphen.
- Remove separators from both ends after normalization.
- Lowercase letters while preserving numeric characters.
- Do not edit test_slugify.py or add dependencies.
- The approved unittest command exits successfully.

## Enforced scope

Editable path patterns:
- `slugify.py`

Read-only path patterns:
- `test_slugify.py`

Treat this task packet as the authoritative upstream specification.
Implement it without expanding scope. Report any ambiguity instead of inventing requirements.
Do not claim completion; the upstream reviewer makes the final decision.

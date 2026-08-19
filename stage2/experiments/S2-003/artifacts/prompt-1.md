# Task s2-smoke-plan

Mode: plan
Attempt: 1 of 1

## Objective

Inspect the broken slugify implementation and propose a precise repair plan without modifying files.

## Acceptance criteria

- Identify the processing-order and separator-collapsing problems using repository evidence.
- Name the file that would change and the tests that would validate it.
- Do not modify any file.

## Enforced scope

Editable path patterns:

Read-only path patterns:
- `slugify.py`
- `test_slugify.py`

Do not edit files. Return a concrete implementation plan, risks, files likely to change, and validation steps.
The outer harness will reject any filesystem change.

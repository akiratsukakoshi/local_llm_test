# Task s2-smoke-autonomous-control

Mode: autonomous
Attempt: 1 of 3

## Objective

Repair the slugify function so that all supplied unit tests pass without changing the tests.

## Acceptance criteria

- Whitespace runs become one hyphen.
- Punctuation runs become one separator rather than repeated separators.
- Leading and trailing separators are removed.
- Letters are lowercase and numbers are preserved.
- All five tests in test_slugify.py pass unchanged.

## Enforced scope

Editable path patterns:
- `slugify.py`

Read-only path patterns:
- `test_slugify.py`

Inspect the supplied files, implement the smallest correct change, and leave verification to the outer harness.
Do not run shell commands; the outer harness runs only the tests declared in the task contract.

# Task s2-compat-autonomous

Mode: autonomous
Attempt: 1 of 3

## Objective

Repair the slugify function so that all supplied compatibility tests pass without changing the tests.

## Acceptance criteria

- Whitespace and punctuation runs normalize to one hyphen.
- Leading and trailing separators are removed.
- Existing underscore and Unicode behavior is preserved.
- Empty and punctuation-only inputs produce an empty slug.
- All tests in test_slugify.py pass unchanged.

## Enforced scope

Editable path patterns:
- `slugify.py`

Read-only path patterns:
- `test_slugify.py`

Inspect the supplied files, implement the smallest correct change, and leave verification to the outer harness.
Do not run shell commands; the outer harness runs only the tests declared in the task contract.

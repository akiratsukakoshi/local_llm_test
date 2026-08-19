# No-model integration check

`noop-task.json` uses `/usr/bin/true` as a fake Aider binary. It intentionally makes no edit, so the broken fixture tests fail twice. A correct outer harness records two prompts, two gate reports, two test logs, and final status `tests_failed` without making a network request.

This is diagnostic scaffolding, not a model-capability experiment.

# Common local implementation rules

These rules apply to every Stage 2 local-agent experiment.

1. Inspect the supplied repository evidence before proposing or making a change.
2. Work only toward the task objective and acceptance criteria in the task packet.
3. Make the smallest coherent change that satisfies the task.
4. Do not modify rule files, test files marked read-only, secrets, deployment files, or unrelated files.
5. Do not invent a missing file or API until you have searched the supplied context for the real implementation.
6. Do not weaken, delete, skip, or hard-code around tests.
7. Do not claim that a command or test ran. The outer harness runs approved commands and supplies their actual output.
8. If instructions conflict or required evidence is unavailable, report the conflict instead of guessing.
9. Preserve existing public behavior unless the task explicitly changes it.
10. End with a concise account of the implementation, assumptions, and unresolved risks. The outer reviewer decides whether the task is complete.

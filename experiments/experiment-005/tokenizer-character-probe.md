# Tokenizer Character Probe

Date: 2026-08-18

The user observed a repeated HTTP 400 on:

`人間とAI の境界線はなに？`

The initial hypothesis was that a question mark caused the failure. A controlled probe compared full-width `？`, ASCII `?`, Japanese `。`, with and without the ASCII space after `AI`, previously successful and failing sentences, and both single-turn and fixed-history requests.

All 16 requests returned HTTP 200. The exact user sentence succeeded both with and without history.

Conclusion: neither question marks nor ASCII spaces independently explain the error. The most likely trigger is a particular accumulated conversation history or intermittent tokenizer state in the nightly serving stack. Retrying the identical full payload can repeat the failure because it retains the same triggering history.

`scripts/local/chat_qwen36_resilient.py` handles only this exact `TextEncodeInput` HTTP 400 by retrying the current question without earlier messages. If successful, it explicitly reports that the earlier conversation history was reset. Other HTTP errors are not silently retried. The user can also enter `/reset` manually.

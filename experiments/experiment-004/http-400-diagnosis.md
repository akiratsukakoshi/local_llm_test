# HTTP 400 diagnosis

## Confirmed facts

- vLLM remained alive throughout the session.
- The server access log recorded the same `400 Bad Request` responses seen by the user.
- Successful requests continued before, between, and after the failures.
- No CUDA out-of-memory error, engine crash, request queue buildup, or SSH tunnel disconnect appeared in the server log.
- Therefore these were application-level API rejections, not confirmed network disconnections.

## Client limitation

`chat_qwen32.py` caught `HTTPError` under the broad connection-error handler and discarded the response body. The original session therefore did not preserve vLLM's explanatory JSON error message.

## Reproduction attempt

The exact seven-prompt sequence was resent with a diagnostic client that records HTTP response bodies. All seven requests returned HTTP 200, so the failure was intermittent and its exact validation reason could not be recovered after the fact.

## Attribution

- Exact root cause: undetermined.
- Inference server stability: degraded at the API-request level, but the engine itself did not crash.
- Network: not supported as the cause by current evidence.
- Human experience: failure regardless of attribution; four rejected prompts in one short conversation is unacceptable for interactive use.

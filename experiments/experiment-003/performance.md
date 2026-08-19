# Performance observations

- Short smoke test: 0.77 seconds for 51 prompt tokens and 20 completion tokens.
- During the three Aider turns, vLLM reported generation throughput around 20.3–21.0 tokens/second.
- The comparable 7B session logs commonly showed about 39–41 tokens/second during active generation.
- Interpretation: the 14B AWQ configuration was roughly half as fast in this small sample, but still felt interactive and completed each non-streaming Aider turn in about 7–8 seconds.
- No request queueing was observed.
- GPU KV-cache usage returned to zero after requests.

These are operational observations rather than a formal throughput benchmark. Prompt lengths and output lengths varied, so the figures should not be treated as a precise model-speed ratio.

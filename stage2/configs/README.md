# Harness configurations

- `aider-qwen38.json`: live Qwen3.8-27B configuration through the existing localhost SSH tunnel. This is the only model-capability configuration.
- `aider-noop-loopback-test.json`: no-model integration configuration used with `tests/integration/loopback_models_server.py` and `/usr/bin/true`.
- `aider-noop-test.json`: deliberately unreachable endpoint used to verify that endpoint preflight fails closed. It is not a live-run configuration.

Starting a model server or RunPod resource is always an explicit operation outside these JSON files.

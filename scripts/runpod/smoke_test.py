#!/usr/bin/env python3
import json
import time
import urllib.request

payload = {
    "model": "Qwen/Qwen2.5-Coder-7B-Instruct",
    "messages": [
        {
            "role": "user",
            "content": "Write a Python function named is_even that returns True for even integers and False otherwise. Return only the code.",
        }
    ],
    "temperature": 0,
    "max_tokens": 128,
}

request = urllib.request.Request(
    "http://127.0.0.1:8000/v1/chat/completions",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST",
)

started = time.monotonic()
with urllib.request.urlopen(request, timeout=120) as response:
    result = json.load(response)
elapsed = time.monotonic() - started

print(result["choices"][0]["message"]["content"])
print(json.dumps(result.get("usage", {}), indent=2))
print(f"elapsed_seconds={elapsed:.3f}")

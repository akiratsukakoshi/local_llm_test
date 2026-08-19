#!/usr/bin/env python3
import json
import time
import urllib.error
import urllib.request


API_URL = "http://127.0.0.1:8000/v1/chat/completions"
MODEL = "Qwen/Qwen2.5-Coder-32B-Instruct-AWQ"
PROMPTS = [
    "やあ、聞こえてる？",
    "原っぱ大学って知って る？",
    "原っぱ大学って知っている？",
    "神奈川県逗子市にある遊びの学校だよ",
    "神奈川県 逗子市にある遊びの学校だよ",
    "聞こえる？",
    "原っぱ大学は神奈川県にあるよ",
]


def main() -> None:
    messages: list[dict[str, str]] = []

    for prompt in PROMPTS:
        candidate = [*messages, {"role": "user", "content": prompt}]
        payload = {
            "model": MODEL,
            "messages": candidate,
            "temperature": 0.2,
            "max_tokens": 1024,
        }
        request = urllib.request.Request(
            API_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        started = time.monotonic()

        try:
            with urllib.request.urlopen(request, timeout=300) as response:
                result = json.load(response)
        except urllib.error.HTTPError as error:
            body = error.read().decode("utf-8", errors="replace")
            print(f"HTTP {error.code} after {time.monotonic() - started:.2f}s")
            print(f"prompt={prompt!r}")
            print(body)
            continue

        answer = result["choices"][0]["message"]["content"]
        messages = [*candidate, {"role": "assistant", "content": answer}]
        usage = result.get("usage", {})
        print(
            f"HTTP 200 after {time.monotonic() - started:.2f}s; "
            f"prompt={prompt!r}; completion={usage.get('completion_tokens')}"
        )


if __name__ == "__main__":
    main()

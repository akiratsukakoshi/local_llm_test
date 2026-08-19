#!/usr/bin/env python3
"""Probe suspected punctuation and ASCII-space tokenizer failures."""

import json
import urllib.error
import urllib.request


API_URL = "http://127.0.0.1:8000/v1/chat/completions"
MODEL = "cyankiwi/Qwen3.6-35B-A3B-AWQ-4bit"

PROMPTS = [
    "人間とAIの境界線はなに？",
    "人間とAI の境界線はなに？",
    "人間とAIの境界線はなに?",
    "人間とAI の境界線はなに?",
    "人間とAIの境界線はなに。",
    "人間とAI の境界線はなに。",
    "やほ、聞こえる？",
    "日本の神奈川県 逗子市にある遊びの学校だよ",
]


def send(messages: list[dict[str, str]]) -> tuple[int, str]:
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.6,
        "top_p": 0.95,
        "max_tokens": 1,
        "chat_template_kwargs": {"enable_thinking": False},
    }
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return response.status, ""
    except urllib.error.HTTPError as error:
        return error.code, error.read().decode("utf-8", errors="replace")


def main() -> None:
    for prompt in PROMPTS:
        status, body = send([{"role": "user", "content": prompt}])
        print(f"single {prompt!r}: HTTP {status} {body[:100]}")

    history = [
        {"role": "user", "content": "こんにちは"},
        {"role": "assistant", "content": "こんにちは！何について話しましょうか？"},
    ]
    for prompt in PROMPTS:
        status, body = send([*history, {"role": "user", "content": prompt}])
        print(f"history {prompt!r}: HTTP {status} {body[:100]}")


if __name__ == "__main__":
    main()

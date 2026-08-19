#!/usr/bin/env python3
"""Compare raw-string and structured OpenAI message content for Qwen3.6."""

import json
import urllib.error
import urllib.request


API_URL = "http://127.0.0.1:8000/v1/chat/completions"
MODEL = "cyankiwi/Qwen3.6-35B-A3B-AWQ-4bit"

MESSAGES = [
    {"role": "user", "content": "やほ、聞こえる？"},
    {
        "role": "assistant",
        "content": "はい、聞こえています！\n\n何かお手伝いできることや、お話したいことはありますか？",
    },
    {"role": "user", "content": "お、なかなか自然な回答ができるね！"},
]


def request(messages: list[dict[str, object]]) -> tuple[int, str]:
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.6,
        "top_p": 0.95,
        "max_tokens": 32,
        "chat_template_kwargs": {"enable_thinking": False},
    }
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            return response.status, response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as error:
        return error.code, error.read().decode("utf-8", errors="replace")


def structured(messages: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "role": message["role"],
            "content": [{"type": "text", "text": message["content"]}],
        }
        for message in messages
    ]


def main() -> None:
    for label, messages in (
        ("raw strings", MESSAGES),
        ("structured text", structured(MESSAGES)),
    ):
        status, body = request(messages)
        print(f"{label}: HTTP {status}")
        print(body[:500])


if __name__ == "__main__":
    main()

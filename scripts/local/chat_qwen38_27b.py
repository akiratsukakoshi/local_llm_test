#!/usr/bin/env python3
"""Interactive chat client for the Qwen3.8-27B llama.cpp experiment."""

import argparse
import json
import time
import urllib.error
import urllib.request


API_URL = "http://127.0.0.1:8000/v1/chat/completions"
MODEL = "Qwen3.8-27B-Q4_K_M"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--thinking", choices=("on", "off"), default="off")
    return parser.parse_args()


def send(payload: dict[str, object]) -> dict[str, object]:
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": "Bearer local"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=900) as response:
        return json.load(response)


def main() -> None:
    args = parse_args()
    thinking = args.thinking == "on"
    messages: list[dict[str, str]] = []
    print(
        f"Direct Qwen chat, thinking {args.thinking.upper()} ({MODEL}). "
        "Type /reset to clear history or /exit to quit."
    )

    while True:
        try:
            prompt = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if prompt in {"/exit", "/quit"}:
            break
        if prompt == "/reset":
            messages = []
            print("[conversation history reset]")
            continue
        if not prompt:
            continue

        candidate = [*messages, {"role": "user", "content": prompt}]
        payload: dict[str, object] = {
            "model": MODEL,
            "messages": candidate,
            "temperature": 0.6,
            "top_p": 0.95,
            "max_tokens": 4096,
            "chat_template_kwargs": {"enable_thinking": thinking},
        }
        started = time.monotonic()

        try:
            result = send(payload)
        except urllib.error.HTTPError as error:
            body = error.read().decode("utf-8", errors="replace")
            print(f"request error: HTTP {error.code}: {body}")
            continue
        except (urllib.error.URLError, TimeoutError) as error:
            print(f"connection error: {error}")
            continue

        message = result["choices"][0]["message"]
        answer = message.get("content") or ""
        reasoning = message.get("reasoning_content") or ""
        messages = [*candidate, {"role": "assistant", "content": answer}]

        if reasoning:
            print(f"thinking> {reasoning}")
        print(f"qwen> {answer}")

        usage = result.get("usage", {})
        elapsed = time.monotonic() - started
        print(
            f"[{elapsed:.2f}s, prompt={usage.get('prompt_tokens', '?')}, "
            f"completion={usage.get('completion_tokens', '?')}]"
        )


if __name__ == "__main__":
    main()

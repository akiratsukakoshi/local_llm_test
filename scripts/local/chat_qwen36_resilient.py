#!/usr/bin/env python3
"""Qwen3.6 chat that resets history after the known tokenizer HTTP 400."""

import argparse
import json
import time
import urllib.error
import urllib.request


API_URL = "http://127.0.0.1:8000/v1/chat/completions"
MODEL = "cyankiwi/Qwen3.6-35B-A3B-AWQ-4bit"
TOKENIZER_ERROR = "TextEncodeInput must be Union"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--thinking", choices=("on", "off"), default="off")
    return parser.parse_args()


def send(payload: dict[str, object]) -> dict[str, object]:
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=600) as response:
        return json.load(response)


def error_body(error: urllib.error.HTTPError) -> str:
    try:
        return error.read().decode("utf-8", errors="replace")
    except Exception:
        return str(error.reason)


def main() -> None:
    args = parse_args()
    thinking = args.thinking == "on"
    messages: list[dict[str, str]] = []
    print(
        f"Resilient Qwen chat, thinking {args.thinking.upper()} ({MODEL}). "
        "Type /exit to quit."
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
        result: dict[str, object] | None = None
        reset_after_error = False

        for attempt in range(2):
            try:
                result = send(payload)
                break
            except urllib.error.HTTPError as error:
                body = error_body(error)
                if attempt == 0 and error.code == 400 and TOKENIZER_ERROR in body:
                    print(
                        "history-specific tokenizer error; retrying this question "
                        "without earlier context..."
                    )
                    payload["messages"] = [{"role": "user", "content": prompt}]
                    reset_after_error = True
                    time.sleep(0.2)
                    continue
                print(f"request error: HTTP {error.code}: {body}")
                break
            except (urllib.error.URLError, TimeoutError) as error:
                print(f"connection error: {error}")
                break

        if result is None:
            continue

        choices = result["choices"]
        message = choices[0]["message"]  # type: ignore[index]
        answer = message.get("content") or ""  # type: ignore[union-attr]
        if reset_after_error:
            messages = [
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": answer},
            ]
            print("[earlier conversation history was reset]")
        else:
            messages = [*candidate, {"role": "assistant", "content": answer}]

        usage = result.get("usage", {})
        elapsed = time.monotonic() - started
        print(f"qwen> {answer}")
        print(
            f"[{elapsed:.2f}s, prompt={usage.get('prompt_tokens', '?')}, "
            f"completion={usage.get('completion_tokens', '?')}]"
        )


if __name__ == "__main__":
    main()

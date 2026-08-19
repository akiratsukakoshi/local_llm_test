#!/usr/bin/env python3
import json
import time
import urllib.error
import urllib.request


API_URL = "http://127.0.0.1:8000/v1/chat/completions"
MODEL = "cyankiwi/Qwen3.6-35B-A3B-AWQ-4bit"


def describe_http_error(error: urllib.error.HTTPError) -> str:
    try:
        body = error.read().decode("utf-8", errors="replace")
    except Exception:
        body = ""
    return f"HTTP {error.code}: {body or error.reason}"


def main() -> None:
    messages: list[dict[str, str]] = []
    print(f"Direct Qwen chat ({MODEL}). Type /exit to quit.")

    while True:
        try:
            prompt = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if prompt in {"/exit", "/quit"}:
            break
        if not prompt:
            continue

        candidate_messages = [*messages, {"role": "user", "content": prompt}]
        payload = {
            "model": MODEL,
            "messages": candidate_messages,
            "temperature": 0.6,
            "top_p": 0.95,
            "max_tokens": 4096,
            "chat_template_kwargs": {"enable_thinking": True},
        }
        request = urllib.request.Request(
            API_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        started = time.monotonic()
        try:
            with urllib.request.urlopen(request, timeout=600) as response:
                result = json.load(response)
        except urllib.error.HTTPError as error:
            print(f"request error: {describe_http_error(error)}")
            continue
        except (urllib.error.URLError, TimeoutError) as error:
            print(f"connection error: {error}")
            continue

        message = result["choices"][0]["message"]
        answer = message.get("content") or ""
        messages = [*candidate_messages, {"role": "assistant", "content": answer}]
        elapsed = time.monotonic() - started
        usage = result.get("usage", {})

        print(f"qwen> {answer}")
        print(
            f"[{elapsed:.2f}s, prompt={usage.get('prompt_tokens', '?')}, "
            f"completion={usage.get('completion_tokens', '?')}]"
        )


if __name__ == "__main__":
    main()

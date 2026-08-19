import re


def slugify(text: str) -> str:
    """Convert text into a lowercase, URL-safe slug."""
    text = re.sub(r"^[\-_]+|[\-_]+$", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"[^\w\s]", "-", text)
    return text.lower()

import re

def slugify(text: str) -> str:
    """Convert text into a lowercase, URL-safe slug."""
    # Remove leading/trailing separators
    text = re.sub(r'^[\-_]+|[\-_]+$', '', text)

    # Replace multiple consecutive whitespace characters with a single hyphen
    text = re.sub(r'\s+', '-', text)

    # Replace punctuation runs with a single hyphen
    text = re.sub(r'[^\w\s]', '-', text)

    # Convert to lowercase
    text = text.lower()

    return text

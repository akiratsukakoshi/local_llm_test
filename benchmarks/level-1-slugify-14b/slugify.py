import re

def slugify(text: str) -> str:
    """Convert text into a lowercase, URL-safe slug."""
    # Convert to lowercase
    text = text.lower()
    # Replace runs of non-word characters (except for hyphens) with a single hyphen
    text = re.sub(r'[^\w\s-]+', '-', text)
    # Collapse whitespace runs into a single hyphen
    text = re.sub(r'\s+', '-', text)
    # Collapse multiple hyphens into a single hyphen
    text = re.sub(r'-+', '-', text)
    # Remove leading and trailing separators
    text = re.sub(r'^-+|-+$', '', text)
    return text

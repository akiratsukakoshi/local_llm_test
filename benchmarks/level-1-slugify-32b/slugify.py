import re

def slugify(text: str) -> str:
    """Convert text into a lowercase, URL-safe slug."""
    # Convert to lowercase
    text = text.lower()
    # Replace punctuation with spaces
    text = re.sub(r'[^\w\s]', ' ', text)
    # Collapse multiple whitespace characters into a single hyphen
    text = re.sub(r'\s+', '-', text)
    # Remove leading and trailing hyphens
    text = text.strip('-')
    return text

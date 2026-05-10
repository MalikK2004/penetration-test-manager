import bleach
import re
from typing import Optional

# Common prompt injection phrases
INJECTION_PATTERNS = [
    r"ignore previous instructions",
    r"reveal system prompt",
    r"bypass safety",
    r"act as root",
    r"forget everything",
    r"you are now",
]

INJECTION_REGEX = re.compile('|'.join(INJECTION_PATTERNS), re.IGNORECASE)

def sanitize_input(text: str) -> str:
    """Strips HTML tags and attributes to prevent XSS."""
    if not text:
        return ""
    return bleach.clean(text, tags=[], attributes={}, strip=True)

def contains_prompt_injection(text: str) -> bool:
    """Checks if the text contains known prompt injection phrases."""
    if not text:
        return False
    return bool(INJECTION_REGEX.search(text))

def validate_and_sanitize(text: str) -> tuple[bool, Optional[str], Optional[str]]:
    """
    Validates and sanitizes input.
    Returns (is_valid, sanitized_text, error_message)
    """
    if not text or not isinstance(text, str):
        return False, None, "Input must be a non-empty string"
        
    sanitized = sanitize_input(text)
    
    if not sanitized.strip():
        return False, None, "Input cannot be empty or just whitespace"
        
    if contains_prompt_injection(sanitized):
        return False, None, "Malicious input detected"
        
    return True, sanitized, None

"""
Input Validation and Sanitization for JobShield AI Pipeline.
Enforces security constraints on untrusted user inputs before ML / rule evaluation:
1. Type checking (handles None, non-string types gracefully)
2. Character encoding, null-byte removal, and non-printable control character sanitization
3. Length bounds (minimum 20 characters, maximum 50,000 characters to prevent ReDoS / memory DoS)
4. Excessive whitespace / delimiter collapsing
"""

import re
import unicodedata
from typing import Tuple, Optional


class InputValidationError(ValueError):
    """Raised when an input cannot be processed due to validation constraints."""
    pass


MIN_JOB_LENGTH = 20
MAX_JOB_LENGTH = 50000


def validate_and_sanitize_input(raw_input: any) -> Tuple[str, dict]:
    """
    Validates and sanitizes raw job posting text.

    Returns:
        sanitized_text: The clean, safe string.
        meta: A dictionary containing validation metadata (flags, original length, etc.)
    
    Raises:
        InputValidationError: If input is null, non-string, empty, or below minimum length.
    """
    meta = {
        "is_valid": False,
        "original_length": 0,
        "sanitized_length": 0,
        "truncated": False,
        "sanitized_null_bytes": False,
        "sanitized_control_chars": False
    }

    # 1. Type check
    if raw_input is None:
        raise InputValidationError("Job posting cannot be null or None.")

    if not isinstance(raw_input, str):
        raise InputValidationError(
            f"Expected string input for job posting, received {type(raw_input).__name__}."
        )

    meta["original_length"] = len(raw_input)

    # 2. Null byte and control character sanitization
    sanitized = raw_input
    if "\x00" in sanitized:
        meta["sanitized_null_bytes"] = True
        sanitized = sanitized.replace("\x00", "")

    # Check for and strip non-printable control characters (except newline, tab, carriage return)
    cleaned_chars = []
    has_control_chars = False
    for ch in sanitized:
        if ch in ("\n", "\r", "\t"):
            cleaned_chars.append(ch)
        elif unicodedata.category(ch).startswith("C"):
            has_control_chars = True
            # Replace control char with a space
            cleaned_chars.append(" ")
        else:
            cleaned_chars.append(ch)

    if has_control_chars:
        meta["sanitized_control_chars"] = True
        sanitized = "".join(cleaned_chars)
    else:
        sanitized = "".join(cleaned_chars)

    # 3. Unicode normalization (NFKC)
    sanitized = unicodedata.normalize("NFKC", sanitized)

    # 4. Collapse excessive whitespace and newlines
    sanitized = re.sub(r"[ \t]{4,}", "   ", sanitized)
    sanitized = re.sub(r"\n{3,}", "\n\n", sanitized)
    sanitized = sanitized.strip()

    # 5. XSS Defusal / Dangerous HTML sanitization
    has_xss = False
    if (
        re.search(r"(?i)<(script|iframe|object|embed|style)[^>]*>", sanitized)
        or re.search(r"(?i)on(error|load|click|mouseover|focus)\s*=", sanitized)
        or re.search(r"(?i)javascript\s*:", sanitized)
    ):
        has_xss = True
        sanitized = re.sub(r"(?i)<(script|iframe|object|embed|style)[^>]*>.*?</\1>", "[DEFUSED_SCRIPT_BLOCK]", sanitized, flags=re.DOTALL)
        sanitized = re.sub(r"(?i)<(script|iframe|object|embed|style)[^>]*>", "[DEFUSED_TAG]", sanitized)
        sanitized = re.sub(r"(?i)on(error|load|click|mouseover|focus)\s*=", "data-defused-event=", sanitized)
        sanitized = re.sub(r"(?i)javascript\s*:", "defused_script:", sanitized)

    meta["sanitized_xss"] = has_xss

    # 6. Empty and minimum length check
    if not sanitized:
        raise InputValidationError("Job posting cannot be empty or whitespace-only.")

    if len(sanitized) < MIN_JOB_LENGTH:
        raise InputValidationError(
            f"Job posting text is too short ({len(sanitized)} characters). "
            f"A minimum of {MIN_JOB_LENGTH} characters is required for scam analysis."
        )

    # 6. Maximum length cap (DoS prevention)
    if len(sanitized) > MAX_JOB_LENGTH:
        meta["truncated"] = True
        meta["truncated_chars"] = len(sanitized) - MAX_JOB_LENGTH
        sanitized = sanitized[:MAX_JOB_LENGTH]

    meta["is_valid"] = True
    meta["sanitized_length"] = len(sanitized)

    return sanitized, meta

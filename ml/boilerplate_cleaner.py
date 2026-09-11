"""Boilerplate suppression preprocessor for JobShield AI.

Strips standardized corporate disclaimers (Equal Opportunity Employer statements,
generic compliance notices, background verification policies, benefits packages)
that dilute fraudulent signal tokens during TF-IDF vectorization.
"""

import re
from typing import List

# Patterns targeting standardized corporate boilerplate sections
BOILERPLATE_PATTERNS: List[str] = [
    # EEO / Diversity & Inclusion Boilerplates
    r"(?i)\b(?:equal\s+opportunity\s+employer|eeo\s+statement|we\s+are\s+an\s+equal\s+opportunity\s+employer)[:\s][^\n\r]*(?:\n[^\n\r]+)*",
    r"(?i)\bwe\s+are\s+committed\s+to\s+fostering\s+an\s+inclusive\s+and\s+diverse\s+work\s+environment[^\n\r]*(?:\n[^\n\r]+)*",
    r"(?i)\ball\s+qualified\s+applicants\s+will\s+receive\s+consideration\s+for\s+employment\s+without\s+regard\s+to\s+race[^\n\r]*(?:\n[^\n\r]+)*",
    r"(?i)\bwe\s+celebrate\s+diversity\s+and\s+are\s+committed\s+to\s+creating\s+an\s+inclusive\s+environment[^\n\r]*(?:\n[^\n\r]+)*",

    # Compliance & Background Verification Boilerplates
    r"(?i)\bcompliance\s*(?:&|and)\s*verification[:\s][^\n\r]*(?:\n[^\n\r]+)*",
    r"(?i)\bemployment\s+offers\s+are\s+subject\s+to\s+standard\s+professional\s+background\s+verification[^\n\r]*(?:\n[^\n\r]+)*",
    r"(?i)\bwe\s+adhere\s+to\s+rigorous\s+compliance\s+standards\s+and\s+iso\s+27001[^\n\r]*(?:\n[^\n\r]+)*",
    r"(?i)\bpre-employment\s+background\s+check\s+and\s+drug\s+screen\s+(?:is|are)\s+required[^\n\r]*(?:\n[^\n\r]+)*",

    # Standard Corporate Benefits Overviews
    r"(?i)\bcomprehensive\s+benefits\s+package[:\s][^\n\r]*(?:\n[^\n\r]+)*",
    r"(?i)\bfull-time\s+employees\s+enjoy\s+medical,\s*dental,\s*and\s*vision\s+insurance[^\n\r]*(?:\n[^\n\r]+)*",
    r"(?i)\babout\s+our\s+organization[:\s][^\n\r]*(?:\n[^\n\r]+)*",
]

_COMPILED_PATTERNS = [re.compile(pat) for pat in BOILERPLATE_PATTERNS]


def clean_boilerplate(text: str) -> str:
    """
    Strips recognized corporate boilerplate from the job description.
    Returns cleaned text. If stripping removes everything (rare), returns original text.
    """
    if not text:
        return ""

    cleaned = text
    for pattern in _COMPILED_PATTERNS:
        cleaned = pattern.sub(" ", cleaned)

    # Collapse excessive blank lines or spaces
    cleaned = re.sub(r"\n\s*\n+", "\n\n", cleaned).strip()

    return cleaned if cleaned else text

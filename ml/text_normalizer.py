"""Unicode and text canonicalization normalizer for JobShield AI.

Hardens both rule-based signal detection and ML vectorization against:
- Unicode homoglyph substitutions (e.g., Cyrillic/Greek lookalikes to Latin)
- Zero-width non-printable characters (ZWSP, ZWNJ, ZWJ, BOM, etc.)
- Confusable accented/decomposed character forms (via Unicode NFKC)
"""

import unicodedata
from typing import Dict

# Comprehensive Cyrillic, Greek, and Unicode lookalike homoglyph mapping to ASCII Latin
HOMOGLYPH_TO_LATIN: Dict[str, str] = {
    # Cyrillic lowercase
    '\u0430': 'a',  # а -> a
    '\u0441': 'c',  # с -> c
    '\u0435': 'e',  # е -> e
    '\u0456': 'i',  # і -> i
    '\u0458': 'j',  # ј -> j
    '\u043E': 'o',  # о -> o
    '\u0440': 'p',  # р -> p
    '\u0455': 's',  # ѕ -> s
    '\u0445': 'x',  # х -> x
    '\u0443': 'y',  # у -> y
    '\u0432': 'b',  # в -> b
    '\u043C': 'm',  # м -> m
    '\u043D': 'h',  # н -> h
    '\u0442': 't',  # т -> t

    # Cyrillic uppercase
    '\u0410': 'A',  # А -> A
    '\u0412': 'B',  # В -> B
    '\u0421': 'C',  # С -> C
    '\u0415': 'E',  # Е -> E
    '\u041D': 'H',  # Н -> H
    '\u0406': 'I',  # І -> I
    '\u0408': 'J',  # Ј -> J
    '\u041C': 'M',  # М -> M
    '\u041E': 'O',  # О -> O
    '\u0420': 'P',  # Р -> P
    '\u0422': 'T',  # Т -> T
    '\u0425': 'X',  # Х -> X
    '\u0423': 'Y',  # У -> Y

    # Greek lookalikes
    '\u03B1': 'a',  # α -> a
    '\u03B5': 'e',  # ε -> e
    '\u03BF': 'o',  # ο -> o
    '\u03C1': 'p',  # ρ -> p
    '\u03C5': 'u',  # υ -> u
    '\u0391': 'A',  # Α -> A
    '\u0392': 'B',  # Β -> B
    '\u0395': 'E',  # Ε -> E
    '\u0396': 'Z',  # Ζ -> Z
    '\u0397': 'H',  # Η -> H
    '\u0399': 'I',  # Ι -> I
    '\u039A': 'K',  # Κ -> K
    '\u039C': 'M',  # Μ -> M
    '\u039D': 'N',  # Ν -> N
    '\u039F': 'O',  # Ο -> O
    '\u03A1': 'P',  # Ρ -> P
    '\u03A4': 'T',  # Τ -> T
    '\u03A7': 'X',  # Χ -> X
}

# Zero-width, directional formatting, and invisible codepoints to strip
ZERO_WIDTH_CHARS = {
    '\u200B',  # Zero Width Space
    '\u200C',  # Zero Width Non-Joiner
    '\u200D',  # Zero Width Joiner
    '\u200E',  # Left-to-Right Mark
    '\u200F',  # Right-to-Left Mark
    '\u202A',  # Left-to-Right Embedding
    '\u202B',  # Right-to-Left Embedding
    '\u202C',  # Pop Directional Formatting
    '\u202D',  # Left-to-Right Override
    '\u202E',  # Right-to-Left Override
    '\u2060',  # Word Joiner
    '\uFEFF',  # Zero Width No-Break Space (BOM)
    '\u00AD',  # Soft Hyphen
}

# Build fast character translation table for homoglyphs
_HOMOGLYPH_TRANS = str.maketrans(HOMOGLYPH_TO_LATIN)
# Translation table to delete all zero-width / invisible characters
_ZERO_WIDTH_TRANS = str.maketrans('', '', ''.join(ZERO_WIDTH_CHARS))


def normalize_text(text: str) -> str:
    """
    Applies multi-stage canonical text normalization:
    1. Strips zero-width and invisible directional codepoints.
    2. Applies Unicode NFKC decomposition/composition (normalizes ligatures, fullwidth chars, compatibility forms).
    3. Translates Cyrillic/Greek homoglyphs to their visual ASCII Latin equivalents.
    """
    if not text:
        return ""

    # Step 1: Strip zero-width and non-printing format characters
    cleaned = text.translate(_ZERO_WIDTH_TRANS)

    # Step 2: Unicode NFKC normalization
    cleaned = unicodedata.normalize('NFKC', cleaned)

    # Step 3: Transliterate homoglyphs to ASCII Latin
    cleaned = cleaned.translate(_HOMOGLYPH_TRANS)

    return cleaned

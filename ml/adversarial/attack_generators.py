"""Deterministic, reproducible attack generators for JobShield AI.

Implements realistic adversarial evasion techniques across 8 categories:
1. Typos and minor spelling changes
2. Zero-width character insertion
3. Unicode / homoglyph substitutions
4. Leetspeak substitutions
5. Obfuscated contact information (Telegram, WhatsApp, email)
6. Obfuscated scam keywords (fees, crypto, wire, payment)
7. Benign camouflage (injected corporate boilerplate)
8. Sentence restructuring and clause dispersion

All mutations are seedable and maintain the readable scam intent of the posting.
"""

from dataclasses import dataclass
from enum import Enum
import random
import re
from typing import Any, Dict, List, Optional, Tuple


class AttackType(str, Enum):
    TYPOS = "typos"
    ZERO_WIDTH = "zero_width"
    HOMOGLYPHS = "unicode_homoglyphs"
    LEETSPEAK = "leetspeak"
    OBFUSCATED_CONTACTS = "obfuscated_contacts"
    OBFUSCATED_KEYWORDS = "obfuscated_keywords"
    BENIGN_CAMOUFLAGE = "benign_camouflage"
    SENTENCE_RESTRUCTURING = "sentence_restructuring"


@dataclass
class AttackResult:
    original_text: str
    attacked_text: str
    attack_type: AttackType
    mutation_metadata: Dict[str, Any]


class AdversarialAttacker:
    """Generates controlled, seedable adversarial variants of job postings."""

    # Homoglyphs mapping: Latin characters to visually identical Cyrillic/Greek glyphs
    HOMOGLYPH_MAP = {
        'a': 'а',  # Cyrillic small letter a (U+0430)
        'c': 'с',  # Cyrillic small letter es (U+0441)
        'e': 'е',  # Cyrillic small letter ie (U+0435)
        'i': 'і',  # Cyrillic small letter byelorussian-ukrainian i (U+0456)
        'j': 'ј',  # Cyrillic small letter je (U+0458)
        'o': 'о',  # Cyrillic small letter o (U+043E)
        'p': 'р',  # Cyrillic small letter er (U+0440)
        's': 'ѕ',  # Cyrillic small letter dze (U+0455)
        'x': 'х',  # Cyrillic small letter ha (U+0445)
        'y': 'у',  # Cyrillic small letter u (U+0443)
        'A': 'А',  # Cyrillic capital letter A (U+0410)
        'B': 'В',  # Cyrillic capital letter Ve (U+0412)
        'C': 'С',  # Cyrillic capital letter Es (U+0421)
        'E': 'Е',  # Cyrillic capital letter Ie (U+0415)
        'H': 'Н',  # Cyrillic capital letter En (U+041D)
        'I': 'І',  # Cyrillic capital letter Byelorussian-Ukrainian I (U+0406)
        'M': 'М',  # Cyrillic capital letter Em (U+041C)
        'O': 'О',  # Cyrillic capital letter O (U+041E)
        'P': 'Р',  # Cyrillic capital letter Er (U+0420)
        'T': 'Т',  # Cyrillic capital letter Te (U+0422)
        'X': 'Х',  # Cyrillic capital letter Ha (U+0425)
    }

    # Leetspeak substitutions
    LEET_MAP = {
        'a': '@',
        'A': '@',
        'e': '3',
        'E': '3',
        'i': '1',
        'I': '1',
        'o': '0',
        'O': '0',
        's': '$',
        'S': '$',
        't': '7',
        'T': '7',
    }

    # Zero-width codepoints: ZWSP, ZWNJ, ZWJ, BOM
    ZERO_WIDTH_CHARS = ['\u200B', '\u200C', '\u200D', '\uFEFF']

    # Keyboard layout for realistic QWERTY adjacent typos
    KEYBOARD_ADJACENT = {
        'a': ['s', 'q', 'z'],
        'b': ['v', 'g', 'h', 'n'],
        'c': ['x', 'd', 'v'],
        'd': ['s', 'e', 'r', 'f', 'c'],
        'e': ['w', 's', 'd', 'r'],
        'f': ['d', 'r', 't', 'g', 'v'],
        'g': ['f', 't', 'y', 'h', 'b'],
        'h': ['g', 'y', 'u', 'j', 'n'],
        'i': ['u', 'j', 'k', 'o'],
        'j': ['h', 'u', 'i', 'k', 'm'],
        'k': ['j', 'i', 'o', 'l'],
        'l': ['k', 'o', 'p'],
        'm': ['n', 'j', 'k'],
        'n': ['b', 'h', 'j', 'm'],
        'o': ['i', 'k', 'l', 'p'],
        'p': ['o', 'l'],
        'r': ['e', 'd', 'f', 't'],
        's': ['a', 'w', 'e', 'd', 'x'],
        't': ['r', 'f', 'g', 'y'],
        'u': ['y', 'h', 'j', 'i'],
        'v': ['c', 'f', 'g', 'b'],
        'w': ['q', 'a', 's', 'e'],
        'x': ['z', 's', 'd', 'c'],
        'y': ['t', 'g', 'h', 'u'],
        'z': ['a', 's', 'x'],
    }

    # High-value scam keywords commonly flagged by rules & transformers
    SCAM_KEYWORDS = [
        "telegram", "whatsapp", "wire transfer", "registration fee", "processing fee",
        "training fee", "equipment fee", "security deposit", "background check fee",
        "crypto", "cryptocurrency", "bitcoin", "usdt", "gift card", "immediate start",
        "no experience required", "guaranteed job", "work from home", "urgently hiring",
        "send resume to", "contact hiring manager", "direct deposit"
    ]

    # Realistic corporate benign boilerplate to camouflage scam intent
    BENIGN_BOILERPLATE = [
        (
            "\n\nEqual Opportunity Employer: We are committed to fostering an inclusive and diverse "
            "work environment. All qualified applicants will receive consideration for employment without "
            "regard to race, color, religion, sex, sexual orientation, gender identity, national origin, "
            "disability status, protected veteran status, or any other characteristic protected by law."
        ),
        (
            "\n\nComprehensive Benefits Package: Full-time employees enjoy medical, dental, and vision insurance, "
            "a 401(k) retirement savings plan with up to 6% employer matching, generous paid time off (PTO), "
            "professional development reimbursement, and wellness stipends."
        ),
        (
            "\n\nAbout Our Organization: Founded in 2012, our global technology and consulting firm provides "
            "enterprise solutions across Fortune 500 partners. We adhere to rigorous compliance standards "
            "and ISO 27001 data protection certifications across all operational branches."
        ),
        (
            "\n\nCompliance & Verification: Employment offers are subject to standard professional background "
            "verification and reference checks in accordance with local labor ordinances and federal guidelines."
        )
    ]

    def __init__(self, seed: int = 42):
        self.seed = seed

    def _get_rng(self, custom_seed: Optional[int] = None) -> random.Random:
        return random.Random(custom_seed if custom_seed is not None else self.seed)

    # ------------------------------------------------------------------------
    # 1. Typos and Minor Spelling Changes
    # ------------------------------------------------------------------------
    def attack_typos(self, text: str, typo_rate: float = 0.04, seed: Optional[int] = None) -> AttackResult:
        """Injects realistic adjacent keyboard typos, character swaps, or omitted letters."""
        rng = self._get_rng(seed)
        words = text.split()
        mutated_words: List[str] = []
        mutations_count = 0
        mutation_details: List[str] = []

        for word in words:
            # Skip very short words, urls, or special formatting
            if len(word) <= 3 or "http" in word or "@" in word or not word.isalpha():
                mutated_words.append(word)
                continue

            if rng.random() < typo_rate:
                chars = list(word)
                idx = rng.randint(0, len(chars) - 1)
                char_lower = chars[idx].lower()

                typo_type = rng.choice(["swap", "adjacent", "delete"])
                if typo_type == "swap" and idx < len(chars) - 1:
                    chars[idx], chars[idx + 1] = chars[idx + 1], chars[idx]
                    mutations_count += 1
                    mutation_details.append(f"swap in '{word}'")
                elif typo_type == "adjacent" and char_lower in self.KEYBOARD_ADJACENT:
                    replacement = rng.choice(self.KEYBOARD_ADJACENT[char_lower])
                    chars[idx] = replacement.upper() if chars[idx].isupper() else replacement
                    mutations_count += 1
                    mutation_details.append(f"adjacent typo in '{word}' ({chars[idx]} -> {replacement})")
                elif typo_type == "delete" and len(chars) > 4:
                    deleted = chars.pop(idx)
                    mutations_count += 1
                    mutation_details.append(f"deleted '{deleted}' in '{word}'")

                mutated_words.append("".join(chars))
            else:
                mutated_words.append(word)

        attacked_text = " ".join(mutated_words)
        return AttackResult(
            original_text=text,
            attacked_text=attacked_text,
            attack_type=AttackType.TYPOS,
            mutation_metadata={
                "typo_rate": typo_rate,
                "mutations_count": mutations_count,
                "mutation_details": mutation_details[:10],
            }
        )

    # ------------------------------------------------------------------------
    # 2. Zero-Width Character Insertion
    # ------------------------------------------------------------------------
    def attack_zero_width(self, text: str, insertion_rate: float = 0.5, seed: Optional[int] = None) -> AttackResult:
        """Injects invisible zero-width unicode characters inside detected or suspicious keywords."""
        rng = self._get_rng(seed)
        mutations_count = 0
        modified_words: List[str] = []

        # Target scam keywords first, otherwise target tokens containing key fraud terms
        keyword_pattern = re.compile(
            r'\b(telegram|whatsapp|fee|fees|deposit|crypto|bitcoin|usdt|wire|payment|urgent|gmail|yahoo)\b',
            re.IGNORECASE
        )

        def replace_with_zw(match: re.Match) -> str:
            nonlocal mutations_count
            word = match.group(0)
            if rng.random() < insertion_rate:
                zw_char = rng.choice(self.ZERO_WIDTH_CHARS)
                # Insert zero-width character in the middle
                split_idx = len(word) // 2
                mutations_count += 1
                return word[:split_idx] + zw_char + word[split_idx:]
            return word

        attacked_text = keyword_pattern.sub(replace_with_zw, text)

        # If no keywords matched, insert into arbitrary long words to evaluate subword splitting
        if mutations_count == 0:
            words = text.split()
            for w in words:
                if len(w) > 5 and rng.random() < 0.15:
                    zw_char = rng.choice(self.ZERO_WIDTH_CHARS)
                    idx = len(w) // 2
                    modified_words.append(w[:idx] + zw_char + w[idx:])
                    mutations_count += 1
                else:
                    modified_words.append(w)
            attacked_text = " ".join(modified_words)

        return AttackResult(
            original_text=text,
            attacked_text=attacked_text,
            attack_type=AttackType.ZERO_WIDTH,
            mutation_metadata={
                "zero_width_chars_inserted": mutations_count,
                "char_types": ["U+200B", "U+200C", "U+200D", "U+FEFF"]
            }
        )

    # ------------------------------------------------------------------------
    # 3. Unicode / Homoglyph Substitutions
    # ------------------------------------------------------------------------
    def attack_homoglyphs(self, text: str, substitution_rate: float = 0.35, seed: Optional[int] = None) -> AttackResult:
        """Substitutes Latin characters with visually indistinguishable Cyrillic/Greek homoglyphs."""
        rng = self._get_rng(seed)
        chars = list(text)
        mutations_count = 0
        substituted_pairs: List[str] = []

        # Find targets in scam keywords or general text
        for i, ch in enumerate(chars):
            if ch in self.HOMOGLYPH_MAP and rng.random() < substitution_rate:
                homoglyph = self.HOMOGLYPH_MAP[ch]
                chars[i] = homoglyph
                mutations_count += 1
                if len(substituted_pairs) < 10:
                    substituted_pairs.append(f"{ch} -> {homoglyph} (U+{ord(homoglyph):04X})")

        attacked_text = "".join(chars)
        return AttackResult(
            original_text=text,
            attacked_text=attacked_text,
            attack_type=AttackType.HOMOGLYPHS,
            mutation_metadata={
                "homoglyphs_substituted": mutations_count,
                "substitution_rate": substitution_rate,
                "sample_substitutions": substituted_pairs
            }
        )

    # ------------------------------------------------------------------------
    # 4. Leetspeak Substitutions
    # ------------------------------------------------------------------------
    def attack_leetspeak(self, text: str, substitution_rate: float = 0.4, seed: Optional[int] = None) -> AttackResult:
        """Replaces characters with common leetspeak equivalents (e.g., 'e' -> '3', 'a' -> '@', 's' -> '$')."""
        rng = self._get_rng(seed)
        # Target scam terms preferentially, or apply across text
        scam_pattern = re.compile(
            r'\b(telegram|whatsapp|payment|fee|crypto|deposit|wire|interview|urgent|contact)\b',
            re.IGNORECASE
        )

        mutations_count = 0

        def leetify_match(match: re.Match) -> str:
            nonlocal mutations_count
            word = match.group(0)
            chars = list(word)
            for i, c in enumerate(chars):
                if c in self.LEET_MAP and rng.random() < substitution_rate:
                    chars[i] = self.LEET_MAP[c]
                    mutations_count += 1
            return "".join(chars)

        attacked_text = scam_pattern.sub(leetify_match, text)

        # If few words were converted, apply to a fraction of eligible characters across text
        if mutations_count < 2:
            chars = list(text)
            for i, c in enumerate(chars):
                if c in self.LEET_MAP and rng.random() < 0.08:
                    chars[i] = self.LEET_MAP[c]
                    mutations_count += 1
            attacked_text = "".join(chars)

        return AttackResult(
            original_text=text,
            attacked_text=attacked_text,
            attack_type=AttackType.LEETSPEAK,
            mutation_metadata={
                "leetspeak_chars_replaced": mutations_count,
                "mapping_used": self.LEET_MAP
            }
        )

    # ------------------------------------------------------------------------
    # 5. Obfuscated Contact Information
    # ------------------------------------------------------------------------
    def attack_obfuscated_contacts(self, text: str, seed: Optional[int] = None) -> AttackResult:
        """Obfuscates off-platform contact channels (Telegram, WhatsApp, email) to evade regex."""
        rng = self._get_rng(seed)
        mutations: List[str] = []
        attacked = text

        # 1. Telegram variations
        telegram_replacements = [
            ("t.me/", rng.choice(["t [dot] me / ", "t[dot]me/", "t . me / ", "telegram: @"])),
            ("telegram", rng.choice(["T-e-l-e-g-r-a-m", "tele-gram", "Tele_gram", "T.e.l.e.g.r.a.m"])),
            ("@", rng.choice([" [at] ", " (at) ", " @ "]))
        ]

        # 2. WhatsApp variations
        whatsapp_replacements = [
            ("wa.me/", rng.choice(["wa [dot] me / ", "wa[dot]me/", "w.a . me / "])),
            ("whatsapp", rng.choice(["Whats-App", "W-h-a-t-s-A-p-p", "WApp", "Whats App", "What$App"])),
        ]

        # 3. Email variations
        email_patterns = [
            (r'([a-zA-Z0-9_.+-]+)@([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)',
             r'\1 [at] \2'),
            (r'\.com\b', ' [dot] com'),
            (r'\.org\b', ' [dot] org'),
            (r'\.io\b', ' [dot] io'),
        ]

        for target, repl in telegram_replacements:
            if re.search(re.escape(target), attacked, re.IGNORECASE):
                attacked = re.sub(re.escape(target), repl, attacked, flags=re.IGNORECASE)
                mutations.append(f"Obfuscated {target} -> {repl}")

        for target, repl in whatsapp_replacements:
            if re.search(re.escape(target), attacked, re.IGNORECASE):
                attacked = re.sub(re.escape(target), repl, attacked, flags=re.IGNORECASE)
                mutations.append(f"Obfuscated {target} -> {repl}")

        for pat, repl in email_patterns:
            if re.search(pat, attacked, re.IGNORECASE):
                attacked = re.sub(pat, repl, attacked, flags=re.IGNORECASE)
                mutations.append(f"Obfuscated email/domain with pattern '{pat}'")

        # If the text had no explicit telegram/whatsapp, simulate an adversarial tactic by adding
        # an obfuscated recruiter channel at the end
        if not mutations:
            synthetic_channel = rng.choice([
                "\n\nTo apply, connect with the talent coordinator on T-e-l-e-g-r-a-m: @ HR_Recruitment_Desk",
                "\n\nFor immediate interview scheduling, message on Whats-App: +1 (555) 019-2831",
                "\n\nDirect applications: submit credentials to recruitment [at] globalcareers [dot] com",
            ])
            attacked = attacked + synthetic_channel
            mutations.append(f"Appended evasive contact: '{synthetic_channel.strip()}'")

        return AttackResult(
            original_text=text,
            attacked_text=attacked,
            attack_type=AttackType.OBFUSCATED_CONTACTS,
            mutation_metadata={
                "mutations_applied": mutations,
                "mutations_count": len(mutations)
            }
        )

    # ------------------------------------------------------------------------
    # 6. Obfuscated Scam Keywords
    # ------------------------------------------------------------------------
    def attack_obfuscated_keywords(self, text: str, seed: Optional[int] = None) -> AttackResult:
        """Obfuscates fee, money, crypto, and urgency keywords that trigger regex/attention."""
        rng = self._get_rng(seed)
        mutations: List[str] = []
        attacked = text

        keyword_transforms = {
            r'\bregistration fee\b': ["r-e-g-i-s-t-r-a-t-i-o-n f-e-e", "refundable onboarding verification", "candidate enrollment deposit"],
            r'\bprocessing fee\b': ["p-r-o-c-e-s-s-i-n-g charge", "administrative file allocation clearance", "d-o-c-u-m-e-n-t fee"],
            r'\bsecurity deposit\b': ["refundable equipment assurance hold", "s-e-c-u-r-i-t-y deposit", "asset custody pledge"],
            r'\bcrypto\b': ["digital currency asset", "c-r-y-p-t-o", "web3 asset reserve"],
            r'\bbitcoin\b': ["b-i-t-c-o-i-n", "BTC token", "decentralized ledger credits"],
            r'\busdt\b': ["U-S-D-T", "stable liquid unit", "Tether credit"],
            r'\bwire transfer\b': ["direct bank wire allocation", "w-i-r-e transfer", "electronic settlement conduit"],
            r'\bgift card\b': ["prepaid electronic voucher", "retail authorization card"],
            r'\burgently hiring\b': ["priority timeline fulfillment", "expedited vacancy placement"],
            r'\bno experience required\b': ["comprehensive orientation provided", "zero prior tenure prerequisite"],
        }

        for pattern, candidates in keyword_transforms.items():
            if re.search(pattern, attacked, re.IGNORECASE):
                chosen = rng.choice(candidates)
                attacked = re.sub(pattern, chosen, attacked, flags=re.IGNORECASE)
                mutations.append(f"Obfuscated keyword '{pattern}' -> '{chosen}'")

        # If no pre-defined patterns found, check for general words like 'fee', 'deposit', 'pay'
        if not mutations:
            fallback_pattern = re.compile(r'\b(fee|fees|deposit|pay|payment)\b', re.IGNORECASE)
            def hypen_word(m: re.Match) -> str:
                w = m.group(0)
                mutations.append(f"Hyphenated '{w}'")
                return "-".join(list(w))
            attacked = fallback_pattern.sub(hypen_word, attacked)

        return AttackResult(
            original_text=text,
            attacked_text=attacked,
            attack_type=AttackType.OBFUSCATED_KEYWORDS,
            mutation_metadata={
                "keywords_obfuscated": mutations,
                "mutations_count": len(mutations)
            }
        )

    # ------------------------------------------------------------------------
    # 7. Benign Camouflage
    # ------------------------------------------------------------------------
    def attack_benign_camouflage(self, text: str, boilerplate_count: int = 2, seed: Optional[int] = None) -> AttackResult:
        """Injects extensive legitimate corporate boilerplate to dilute scam density and deceive TF-IDF/Transformers."""
        rng = self._get_rng(seed)
        selected_boilerplate = rng.sample(
            self.BENIGN_BOILERPLATE,
            min(boilerplate_count, len(self.BENIGN_BOILERPLATE))
        )

        injected_section = "".join(selected_boilerplate)
        # Position: place benign boilerplate both before and after the text to surround scam payloads
        half = len(selected_boilerplate) // 2
        prefix = "".join(selected_boilerplate[:half])
        suffix = "".join(selected_boilerplate[half:])

        attacked_text = f"{prefix.strip()}\n\n{text}\n\n{suffix.strip()}".strip()

        return AttackResult(
            original_text=text,
            attacked_text=attacked_text,
            attack_type=AttackType.BENIGN_CAMOUFLAGE,
            mutation_metadata={
                "boilerplate_sections_injected": len(selected_boilerplate),
                "injected_character_count": len(injected_section),
                "original_char_count": len(text),
                "attacked_char_count": len(attacked_text),
            }
        )

    # ------------------------------------------------------------------------
    # 8. Sentence Restructuring
    # ------------------------------------------------------------------------
    def attack_sentence_restructuring(self, text: str, seed: Optional[int] = None) -> AttackResult:
        """Disperses scam signals across clauses, reorders paragraphs, and embeds scam hooks in benefit lists."""
        rng = self._get_rng(seed)

        # Split text into paragraphs or sentences
        paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
        mutations: List[str] = []

        if len(paragraphs) > 2:
            # Preserve header/title if it looks like one, shuffle interior paragraphs
            header = paragraphs[0]
            body = paragraphs[1:]
            rng.shuffle(body)
            reordered_paragraphs = [header] + body
            attacked_text = "\n\n".join(reordered_paragraphs)
            mutations.append("Reordered interior paragraphs to disrupt structural discourse flow")
        else:
            # Sentence-level split and re-articulation
            sentences = re.split(r'(?<=[.!?])\s+', text)
            if len(sentences) > 3:
                # Rotate sentences slightly without losing core syntax
                mid = len(sentences) // 2
                restructured = sentences[mid:] + sentences[:mid]
                attacked_text = " ".join(restructured)
                mutations.append("Rotated sentence segments to separate clustered scam indicators")
            else:
                # Clause dispersion: soften imperatives into conditional clauses
                attacked_text = text.replace("You must pay", "In the event that onboarding materials necessitate, candidates provide")
                attacked_text = attacked_text.replace("Immediate start", "Subject to completion of mutual scheduling, engagement commences promptly")
                attacked_text = attacked_text.replace("Contact on Telegram", "For inquiries, candidates may optionally reach out via Telegram messaging")
                mutations.append("Softened imperative phrases into passive/conditional business clauses")

        return AttackResult(
            original_text=text,
            attacked_text=attacked_text,
            attack_type=AttackType.SENTENCE_RESTRUCTURING,
            mutation_metadata={
                "restructuring_actions": mutations,
                "mutations_count": len(mutations)
            }
        )

    # ------------------------------------------------------------------------
    # Unified Attack Dispatcher
    # ------------------------------------------------------------------------
    def generate_attack(self, text: str, attack_type: AttackType, seed: Optional[int] = None) -> AttackResult:
        """Dispatches text through the specified attack generator."""
        if attack_type == AttackType.TYPOS:
            return self.attack_typos(text, seed=seed)
        elif attack_type == AttackType.ZERO_WIDTH:
            return self.attack_zero_width(text, seed=seed)
        elif attack_type == AttackType.HOMOGLYPHS:
            return self.attack_homoglyphs(text, seed=seed)
        elif attack_type == AttackType.LEETSPEAK:
            return self.attack_leetspeak(text, seed=seed)
        elif attack_type == AttackType.OBFUSCATED_CONTACTS:
            return self.attack_obfuscated_contacts(text, seed=seed)
        elif attack_type == AttackType.OBFUSCATED_KEYWORDS:
            return self.attack_obfuscated_keywords(text, seed=seed)
        elif attack_type == AttackType.BENIGN_CAMOUFLAGE:
            return self.attack_benign_camouflage(text, seed=seed)
        elif attack_type == AttackType.SENTENCE_RESTRUCTURING:
            return self.attack_sentence_restructuring(text, seed=seed)
        else:
            raise ValueError(f"Unknown attack type: {attack_type}")


def generate_all_attacks(text: str, seed: int = 42) -> List[AttackResult]:
    """Generates all 8 adversarial variants for a given text in a deterministic manner."""
    attacker = AdversarialAttacker(seed=seed)
    results = []
    for attack_type in AttackType:
        results.append(attacker.generate_attack(text, attack_type, seed=seed))
    return results

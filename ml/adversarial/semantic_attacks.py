"""Semantic and structural adversarial generators for JobShield AI.

Implements missing realistic evasion attack vectors:
1. Synonym substitution for urgency and financial language
2. Paraphrased scam postings (formalized business rephrasing)
3. Case & intra-word spacing tricks (e.g., 'T e l e g r a m', 'u R g E n T')
"""

import random
import re
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from ml.adversarial.attack_generators import AttackResult, AttackType


# Register new attack types or distinct attack identifiers
class SemanticAttackType:
    URGENCY_SYNONYMS = "urgency_synonyms"
    PARAPHRASED_SCAM = "paraphrased_scam"
    CASE_SPACING_TRICKS = "case_spacing_tricks"


class SemanticAttacker:
    """Generates semantic and stylistic adversarial variants."""

    URGENCY_SYNONYM_MAP = {
        r"\b(urgent|urgently)\b": ["priority", "immediate start available", "accelerated consideration"],
        r"\b(act now|apply immediately|hurry)\b": ["expedited submission encouraged", "prompt consideration advised", "time-sensitive vacancy"],
        r"\b(limited positions|limited slots)\b": ["finite intake cohort", "selective candidate capacity", "defined availability"],
        r"\b(instant start|immediate hire)\b": ["direct onboarding track", "rapid cycle placement", "streamlined orientation"],
        r"\b(fast cash|quick money|easy money)\b": ["accelerated milestone remuneration", "performance-linked liquidity", "rapid compensation cycle"],
        r"\b(guaranteed income|guaranteed pay)\b": ["predictable base contract allocation", "secured baseline compensation", "established stipend framework"],
        r"\b(wire transfer|wire funds)\b": ["electronic institutional remittance", "clearing house transfer", "direct treasury conduit"],
        r"\b(cashier'?s? check)\b": ["certified commercial bank instrument", "endorsed bank draft", "institutional financial coupon"],
        r"\b(upfront payment|initial payment|upfront fee)\b": ["initial administrative allocation", "preparatory verification retainer", "onboarding provisioning clearance"],
        r"\b(no experience required|no experience needed)\b": ["foundational orientation curriculum provided", "prerequisite-free entry track", "all background levels reviewed"],
    }

    PARAPHRASE_PATTERNS = [
        (
            r"\b(earn|make)\s+\$?([0-9,]+)\s*(a|per)?\s*(week|month|day)\b",
            r"eligible for competitive compensation targeted at $\2 \3 \4 upon milestone completion"
        ),
        (
            r"\bwork from home\b",
            "remote telecommuting engagement"
        ),
        (
            r"\bdata entry clerk\b",
            "Information Processing and Records Specialist"
        ),
        (
            r"\bsend your resume to\b",
            "transmit your professional profile documentation directly to"
        ),
        (
            r"\bmust pay for equipment\b",
            "home-office hardware requisition is managed via authorized reimbursement protocol"
        ),
        (
            r"\bcheck will be mailed\b",
            "certified payment draft shall be dispatched via standard courier tracking"
        ),
    ]

    def __init__(self, seed: int = 42):
        self.seed = seed

    def _get_rng(self, seed: Optional[int] = None) -> random.Random:
        return random.Random(self.seed if seed is None else seed)

    def attack_urgency_synonyms(self, text: str, seed: Optional[int] = None) -> AttackResult:
        """Substitutes high-pressure urgency and scam keywords with business formal synonyms."""
        rng = self._get_rng(seed)
        mutations: List[str] = []
        attacked = text

        for pattern, replacements in self.URGENCY_SYNONYM_MAP.items():
            if re.search(pattern, attacked, re.IGNORECASE):
                replacement = rng.choice(replacements)
                attacked = re.sub(pattern, replacement, attacked, flags=re.IGNORECASE)
                mutations.append(f"Substituted '{pattern}' -> '{replacement}'")

        if not mutations:
            # Fallback insertion of subtle formal urgency to test evasion
            formal_urgency = " Note: Requisition scheduling prioritizes immediate cycle submissions."
            attacked = attacked + formal_urgency
            mutations.append("Appended formal time-sensitive notice")

        return AttackResult(
            original_text=text,
            attacked_text=attacked,
            attack_type=SemanticAttackType.URGENCY_SYNONYMS,
            mutation_metadata={
                "mutations": mutations,
                "count": len(mutations),
            }
        )

    def attack_paraphrase(self, text: str, seed: Optional[int] = None) -> AttackResult:
        """Paraphrases common scam phrasing into corporate vocabulary."""
        rng = self._get_rng(seed)
        mutations: List[str] = []
        attacked = text

        for pattern, repl in self.PARAPHRASE_PATTERNS:
            if re.search(pattern, attacked, re.IGNORECASE):
                attacked = re.sub(pattern, repl, attacked, flags=re.IGNORECASE)
                mutations.append(f"Paraphrased '{pattern}' -> '{repl}'")

        if not mutations:
            # Professional polishing of opening/closing
            attacked = "Corporate Requisition Brief: " + attacked + " All candidates undergo standard orientation."
            mutations.append("Wrapped in corporate styling")

        return AttackResult(
            original_text=text,
            attacked_text=attacked,
            attack_type=SemanticAttackType.PARAPHRASED_SCAM,
            mutation_metadata={
                "mutations": mutations,
                "count": len(mutations),
            }
        )

    def attack_case_spacing_tricks(self, text: str, seed: Optional[int] = None) -> AttackResult:
        """Applies intra-word spacing, alternating case, and punctuation insertion to evasive keywords."""
        rng = self._get_rng(seed)
        mutations: List[str] = []
        attacked = text

        target_words = [
            "telegram", "whatsapp", "wire", "transfer", "deposit",
            "fee", "payment", "urgent", "bitcoin", "crypto", "cashier"
        ]

        def space_trick(word: str) -> str:
            trick = rng.choice(["spaced", "dotted", "alternating_case"])
            if trick == "spaced":
                return " ".join(list(word))
            elif trick == "dotted":
                return ".".join(list(word))
            else:
                return "".join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(word))

        for w in target_words:
            pattern = rf"\b{w}\b"
            if re.search(pattern, attacked, re.IGNORECASE):
                transformed = space_trick(w)
                attacked = re.sub(pattern, transformed, attacked, flags=re.IGNORECASE)
                mutations.append(f"Obfuscated '{w}' -> '{transformed}'")

        if not mutations:
            # Inject a spaced contact to verify resistance
            injected = " Contact talent recruiter via T e l e g r a m: @HRDesk2026"
            attacked = attacked + injected
            mutations.append(f"Injected spaced contact trick: '{injected.strip()}'")

        return AttackResult(
            original_text=text,
            attacked_text=attacked,
            attack_type=SemanticAttackType.CASE_SPACING_TRICKS,
            mutation_metadata={
                "mutations": mutations,
                "count": len(mutations),
            }
        )

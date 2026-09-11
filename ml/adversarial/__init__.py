"""JobShield AI Adversarial Robustness Package.

Offline evaluation modules for testing model vulnerability to realistic evasion tactics.
"""

from ml.adversarial.attack_generators import (
    AdversarialAttacker,
    AttackResult,
    AttackType,
    generate_all_attacks,
)
from ml.adversarial.audit_reporter import AdversarialAuditReporter
from ml.adversarial.evaluator import AdversarialEvaluator, EvaluationSummary

__all__ = [
    "AttackType",
    "AttackResult",
    "AdversarialAttacker",
    "generate_all_attacks",
    "AdversarialEvaluator",
    "EvaluationSummary",
    "AdversarialAuditReporter",
]

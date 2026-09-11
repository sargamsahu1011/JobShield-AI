"""Adversarial robustness evaluation engine for JobShield AI.

Runs controlled adversarial benchmarks against the existing JobShield inference models
without modifying production files or prediction logic.
"""

from dataclasses import asdict, dataclass
import os
from typing import Any, Callable, Dict, List, Optional, Tuple

from ml.adversarial.attack_generators import (
    AdversarialAttacker,
    AttackResult,
    AttackType,
)
from ml.scam_signals import detect_scam_signals


@dataclass
class SamplePrediction:
    fraud_score: float
    prediction: str  # "Fraudulent" or "Legitimate"
    active_signals: List[str]
    signal_count: int


@dataclass
class AdversarialCaseEvaluation:
    sample_id: str
    attack_type: str
    original_text: str
    attacked_text: str
    mutation_metadata: Dict[str, Any]
    original_eval: SamplePrediction
    attacked_eval: SamplePrediction
    score_drop: float  # original_score - attacked_score
    flipped: bool      # True if originally Fraudulent and attacked is Legitimate
    dropped_signals: List[str]  # Signals present in original but lost in attacked
    new_signals: List[str]      # Signals absent in original but caught in attacked


@dataclass
class AttackTypeMetrics:
    attack_type: str
    total_evaluated: int
    originally_fraudulent: int
    flips_to_legitimate: int
    attack_success_rate: float  # flips / originally_fraudulent
    pre_attack_detection_rate: float
    post_attack_detection_rate: float
    mean_score_drop: float
    max_score_drop: float
    total_signals_original: int
    total_signals_dropped: int
    signal_dropout_rate: float


@dataclass
class EvaluationSummary:
    model_name: str
    total_samples: int
    total_evaluations: int
    overall_asr: float
    overall_flips: int
    overall_originally_fraudulent: int
    overall_pre_detection_rate: float
    overall_post_detection_rate: float
    overall_mean_score_drop: float
    overall_max_score_drop: float
    overall_signal_dropout_rate: float
    by_attack_type: Dict[str, AttackTypeMetrics]
    cases: List[AdversarialCaseEvaluation]


class AdversarialEvaluator:
    """Evaluates JobShield AI prediction robustness under controlled attacks."""

    def __init__(
        self,
        predictor_fn: Optional[Callable[[str], Tuple[float, str]]] = None,
        model_name: str = "DistilBERT",
        seed: int = 42
    ):
        """
        Args:
            predictor_fn: A callable taking a text string and returning (fraud_score, prediction).
                          If None, attempts to resolve the standard JobShield predict_job function.
            model_name: Name of the model being evaluated (e.g., 'DistilBERT' or 'TF-IDF Baseline').
            seed: Random seed for deterministic attack mutations.
        """
        self.model_name = model_name
        self.attacker = AdversarialAttacker(seed=seed)
        self.seed = seed

        if predictor_fn is not None:
            self.predictor_fn = predictor_fn
        else:
            self.predictor_fn = self._load_default_predictor()

    def _load_default_predictor(self) -> Callable[[str], Tuple[float, str]]:
        """Safely checks if DistilBERT is present, otherwise provides clear instructions."""
        model_path = "models/jobshield-distilbert-final"
        config_path = os.path.join(model_path, "threshold_config.json")

        if not os.path.exists(model_path) or not os.path.exists(config_path):
            raise FileNotFoundError(
                f"DistilBERT model directory not found at '{model_path}'.\n"
                f"As noted in the project architecture, large model weights are kept outside GitHub.\n"
                f"To evaluate DistilBERT, ensure 'models/jobshield-distilbert-final/' is present, or "
                f"run the baseline evaluator using '--baseline' in ml.run_adversarial_eval."
            )

        from ml.predict import predict_job

        def _predict(text: str) -> Tuple[float, str]:
            res = predict_job(text)
            if isinstance(res, (tuple, list)):
                score, pred_int = res[0], res[1]
                pred_str = "Fraudulent" if pred_int == 1 else "Legitimate"
                return float(score), pred_str
            return float(res["fraud_score"]), str(res["prediction"])

        return _predict

    def _evaluate_single_text(self, text: str) -> SamplePrediction:
        """Runs model inference and heuristic scam signal detection."""
        score, pred = self.predictor_fn(text)
        signal_results = detect_scam_signals(text)
        # detect_scam_signals returns Dict[str, bool]
        active_signals = [signal for signal, detected in signal_results.items() if detected]
        return SamplePrediction(
            fraud_score=score,
            prediction=pred,
            active_signals=active_signals,
            signal_count=len(active_signals)
        )

    def evaluate_sample(
        self,
        text: str,
        sample_id: str = "sample_0",
        attack_types: Optional[List[AttackType]] = None
    ) -> List[AdversarialCaseEvaluation]:
        """Evaluates all or specified attacks against a single sample."""
        if attack_types is None:
            attack_types = list(AttackType)

        original_eval = self._evaluate_single_text(text)
        results: List[AdversarialCaseEvaluation] = []

        for attack_type in attack_types:
            attack_result = self.attacker.generate_attack(text, attack_type, seed=self.seed)
            attacked_eval = self._evaluate_single_text(attack_result.attacked_text)

            score_drop = original_eval.fraud_score - attacked_eval.fraud_score
            flipped = (
                original_eval.prediction == "Fraudulent" and
                attacked_eval.prediction == "Legitimate"
            )

            # Analyze heuristic signal dropout
            orig_set = set(original_eval.active_signals)
            attack_set = set(attacked_eval.active_signals)
            dropped = sorted(list(orig_set - attack_set))
            new_sigs = sorted(list(attack_set - orig_set))

            results.append(
                AdversarialCaseEvaluation(
                    sample_id=sample_id,
                    attack_type=attack_type.value,
                    original_text=text,
                    attacked_text=attack_result.attacked_text,
                    mutation_metadata=attack_result.mutation_metadata,
                    original_eval=original_eval,
                    attacked_eval=attacked_eval,
                    score_drop=round(score_drop, 4),
                    flipped=flipped,
                    dropped_signals=dropped,
                    new_signals=new_sigs
                )
            )

        return results

    def evaluate_dataset(
        self,
        samples: List[Dict[str, Any]],
        attack_types: Optional[List[AttackType]] = None
    ) -> EvaluationSummary:
        """
        Runs evaluation on a collection of job postings.
        Expected sample dict format: {"id": str, "text": str, "label": Optional[str or int]}
        """
        all_cases: List[AdversarialCaseEvaluation] = []

        for idx, sample in enumerate(samples):
            sid = str(sample.get("id", f"sample_{idx}"))
            text = sample.get("text", "")
            if not text.strip():
                continue
            cases = self.evaluate_sample(text, sample_id=sid, attack_types=attack_types)
            all_cases.extend(cases)

        # Aggregate metrics overall and by attack category
        return self._compute_summary(all_cases)

    def _compute_summary(self, cases: List[AdversarialCaseEvaluation]) -> EvaluationSummary:
        """Computes Attack Success Rate (ASR), detection rates, drops, and dropouts."""
        by_type_cases: Dict[str, List[AdversarialCaseEvaluation]] = {}
        for c in cases:
            by_type_cases.setdefault(c.attack_type, []).append(c)

        by_attack_type_metrics: Dict[str, AttackTypeMetrics] = {}

        for atype, type_cases in by_type_cases.items():
            total = len(type_cases)
            orig_fraud = sum(1 for c in type_cases if c.original_eval.prediction == "Fraudulent")
            flips = sum(1 for c in type_cases if c.flipped)

            asr = (flips / orig_fraud) if orig_fraud > 0 else 0.0
            pre_det = (orig_fraud / total) if total > 0 else 0.0
            post_fraud = sum(1 for c in type_cases if c.attacked_eval.prediction == "Fraudulent")
            post_det = (post_fraud / total) if total > 0 else 0.0

            score_drops = [c.score_drop for c in type_cases]
            mean_drop = sum(score_drops) / len(score_drops) if score_drops else 0.0
            max_drop = max(score_drops) if score_drops else 0.0

            # Signal stats
            total_orig_signals = sum(len(c.original_eval.active_signals) for c in type_cases)
            total_dropped_signals = sum(len(c.dropped_signals) for c in type_cases)
            sig_dropout_rate = (
                (total_dropped_signals / total_orig_signals) if total_orig_signals > 0 else 0.0
            )

            by_attack_type_metrics[atype] = AttackTypeMetrics(
                attack_type=atype,
                total_evaluated=total,
                originally_fraudulent=orig_fraud,
                flips_to_legitimate=flips,
                attack_success_rate=round(asr, 4),
                pre_attack_detection_rate=round(pre_det, 4),
                post_attack_detection_rate=round(post_det, 4),
                mean_score_drop=round(mean_drop, 4),
                max_score_drop=round(max_drop, 4),
                total_signals_original=total_orig_signals,
                total_signals_dropped=total_dropped_signals,
                signal_dropout_rate=round(sig_dropout_rate, 4),
            )

        # Overall metrics
        total_evals = len(cases)
        total_orig_fraud = sum(1 for c in cases if c.original_eval.prediction == "Fraudulent")
        total_flips = sum(1 for c in cases if c.flipped)
        overall_asr = (total_flips / total_orig_fraud) if total_orig_fraud > 0 else 0.0

        all_drops = [c.score_drop for c in cases]
        overall_mean_drop = sum(all_drops) / len(all_drops) if all_drops else 0.0
        overall_max_drop = max(all_drops) if all_drops else 0.0

        total_post_fraud = sum(1 for c in cases if c.attacked_eval.prediction == "Fraudulent")
        overall_pre_det = (total_orig_fraud / total_evals) if total_evals > 0 else 0.0
        overall_post_det = (total_post_fraud / total_evals) if total_evals > 0 else 0.0

        total_orig_sigs = sum(len(c.original_eval.active_signals) for c in cases)
        total_drop_sigs = sum(len(c.dropped_signals) for c in cases)
        overall_sig_dropout = (
            (total_drop_sigs / total_orig_sigs) if total_orig_sigs > 0 else 0.0
        )

        unique_sample_ids = len(set(c.sample_id for c in cases))

        return EvaluationSummary(
            model_name=self.model_name,
            total_samples=unique_sample_ids,
            total_evaluations=total_evals,
            overall_asr=round(overall_asr, 4),
            overall_flips=total_flips,
            overall_originally_fraudulent=total_orig_fraud,
            overall_pre_detection_rate=round(overall_pre_det, 4),
            overall_post_detection_rate=round(overall_post_det, 4),
            overall_mean_score_drop=round(overall_mean_drop, 4),
            overall_max_score_drop=round(overall_max_drop, 4),
            overall_signal_dropout_rate=round(overall_sig_dropout, 4),
            by_attack_type=by_attack_type_metrics,
            cases=cases
        )

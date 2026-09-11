"""Adversarial Audit Reporter for JobShield AI.

Serializes detailed audit results into JSON and generates clean, human-readable
Markdown reports under reports/adversarial/.
"""

from dataclasses import asdict
from datetime import datetime
import json
import os
from typing import Any, Dict, Optional

from ml.adversarial.evaluator import EvaluationSummary


class AdversarialAuditReporter:
    """Handles structured JSON serialization and Markdown generation for adversarial audits."""

    def __init__(self, output_dir: str = "reports/adversarial"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def export_json(self, summary: EvaluationSummary, filename_prefix: str = "adversarial_audit") -> str:
        """Exports the complete audit structure to JSON."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_prefix}_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)

        # Convert dataclasses to dict
        data = {
            "experiment_metadata": {
                "timestamp": datetime.now().isoformat(),
                "model_evaluated": summary.model_name,
                "total_samples": summary.total_samples,
                "total_evaluations": summary.total_evaluations,
            },
            "overall_metrics": {
                "attack_success_rate": summary.overall_asr,
                "total_flips_fraud_to_legit": summary.overall_flips,
                "total_originally_fraudulent": summary.overall_originally_fraudulent,
                "pre_attack_detection_rate": summary.overall_pre_detection_rate,
                "post_attack_detection_rate": summary.overall_post_detection_rate,
                "mean_score_drop": summary.overall_mean_score_drop,
                "max_score_drop": summary.overall_max_score_drop,
                "signal_dropout_rate": summary.overall_signal_dropout_rate,
            },
            "metrics_by_attack_type": {
                k: asdict(v) for k, v in summary.by_attack_type.items()
            },
            "cases": [asdict(c) for c in summary.cases]
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return filepath

    def export_markdown(self, summary: EvaluationSummary, filename_prefix: str = "adversarial_audit") -> str:
        """Generates an executive, human-readable markdown report summarizing vulnerabilities."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_prefix}_{timestamp}.md"
        filepath = os.path.join(self.output_dir, filename)

        md = []
        md.append(f"# JobShield AI — Adversarial Robustness Audit Report")
        md.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}  ")
        md.append(f"**Target Model:** `{summary.model_name}`  ")
        md.append(f"**Samples Evaluated:** {summary.total_samples} distinct postings ({summary.total_evaluations} attack variants)  ")
        md.append("")

        md.append("## 1. Executive Summary")
        md.append(f"- **Overall Attack Success Rate (ASR):** `{summary.overall_asr * 100:.1f}%` ({summary.overall_flips}/{summary.overall_originally_fraudulent} fraudulent postings evaded detection)")
        md.append(f"- **Pre-Attack Fraud Detection Rate:** `{summary.overall_pre_detection_rate * 100:.1f}%`")
        md.append(f"- **Post-Attack Fraud Detection Rate:** `{summary.overall_post_detection_rate * 100:.1f}%` (Absolute drop: `{(summary.overall_pre_detection_rate - summary.overall_post_detection_rate) * 100:.1f}%`)")
        md.append(f"- **Mean Fraud Score Degradation:** `{-summary.overall_mean_score_drop:.4f}`")
        md.append(f"- **Maximum Observed Score Suppression:** `{summary.overall_max_score_drop:.4f}`")
        md.append(f"- **Rule-Based Heuristic Dropout Rate:** `{summary.overall_signal_dropout_rate * 100:.1f}%` of scam regex signals vanished under attack")
        md.append("")

        md.append("## 2. Vulnerability Breakdown by Attack Category")
        md.append("| Attack Type | Evaluated | Orig Fraud | Flips | ASR (%) | Pre-Det (%) | Post-Det (%) | Mean Δ Score | Max Δ Score | Signal Drop (%) |")
        md.append("| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |")

        for atype, m in sorted(summary.by_attack_type.items(), key=lambda x: x[1].attack_success_rate, reverse=True):
            md.append(
                f"| `{m.attack_type}` | {m.total_evaluated} | {m.originally_fraudulent} | {m.flips_to_legitimate} | "
                f"**{m.attack_success_rate * 100:.1f}%** | {m.pre_attack_detection_rate * 100:.1f}% | "
                f"{m.post_attack_detection_rate * 100:.1f}% | {m.mean_score_drop:+.4f} | "
                f"{m.max_score_drop:.4f} | {m.signal_dropout_rate * 100:.1f}% |"
            )
        md.append("")

        md.append("## 3. Top Evasion Cases (Fraud $\\to$ Legitimate Flips)")
        flip_cases = [c for c in summary.cases if c.flipped]
        if not flip_cases:
            md.append("*No fraudulent postings were successfully flipped in this evaluation run.*")
        else:
            for idx, c in enumerate(flip_cases[:5], 1):
                md.append(f"### Flip Example {idx}: `{c.attack_type}` (Sample: `{c.sample_id}`)")
                md.append(f"- **Score Shift:** `{c.original_eval.fraud_score:.4f}` ({c.original_eval.prediction}) $\\longrightarrow$ `{c.attacked_eval.fraud_score:.4f}` ({c.attacked_eval.prediction}) [Δ `{c.score_drop:.4f}`]")
                md.append(f"- **Dropped Signals:** `{', '.join(c.dropped_signals) if c.dropped_signals else 'None'}`")
                md.append(f"- **Original Excerpt:**")
                md.append(f"  > *\"{c.original_text[:180].strip()}...\"*")
                md.append(f"- **Attacked Excerpt:**")
                md.append(f"  > *\"{c.attacked_text[:180].strip()}...\"*")
                md.append("")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(md))

        return filepath

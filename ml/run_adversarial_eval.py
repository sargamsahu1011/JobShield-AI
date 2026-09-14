"""CLI Runner for JobShield AI Adversarial Robustness Evaluation.

Usage:
    python -m ml.run_adversarial_eval
    python -m ml.run_adversarial_eval --baseline
    python -m ml.run_adversarial_eval --max-samples 10
"""

import argparse
import os
import sys
from typing import Callable, Dict, List, Optional, Tuple

import joblib
import pandas as pd

from ml.adversarial.attack_generators import AttackType
from ml.adversarial.audit_reporter import AdversarialAuditReporter
from ml.adversarial.evaluator import AdversarialEvaluator
def _get_regression_test_cases() -> Dict[str, str]:
    """Safely extracts text samples from ml/test_cases.py without triggering uninstalled local model imports."""
    try:
        import sys
        # If running from project root and predict is available
        from ml.test_cases import TEST_CASES
        return TEST_CASES
    except Exception:
        # Fallback to direct file parsing so offline runner functions unconditionally
        test_case_path = os.path.join(os.path.dirname(__file__), "test_cases.py")
        if not os.path.exists(test_case_path):
            return {}
        cases = {}
        current_key = None
        buffer = []
        with open(test_case_path, "r", encoding="utf-8") as f:
            in_cases = False
            for line in f:
                if "TEST_CASES = {" in line:
                    in_cases = True
                    continue
                if in_cases:
                    if '"""' in line and ":" in line:
                        parts = line.split('"""')
                        key = parts[0].strip().strip('":').strip()
                        if key:
                            current_key = key
                            buffer = []
                    elif '"""' in line and current_key:
                        cases[current_key] = "\n".join(buffer).strip()
                        current_key = None
                        buffer = []
                    elif current_key:
                        buffer.append(line)
        return cases


def load_calibrated_predictor() -> Tuple[Callable[[str], Tuple[float, str]], str]:
    """Loads the deployed Calibrated TF-IDF + Platt Logistic Regression model from ml.predict."""
    from ml.predict import predict_job, MODEL_NAME, THRESHOLD

    def _predict(text: str) -> Tuple[float, str]:
        score, pred_int = predict_job(text)
        pred_str = "Fraudulent" if pred_int == 1 else "Legitimate"
        return float(score), pred_str

    return _predict, f"{MODEL_NAME} (Threshold: {THRESHOLD})"


def load_baseline_predictor() -> Tuple[Callable[[str], Tuple[float, str]], str]:
    """Loads the serialized uncalibrated TF-IDF + Logistic Regression baseline artifacts."""
    vectorizer_path = "models/tfidf_vectorizer.joblib"
    model_path = "models/tfidf_logreg.joblib"

    if not os.path.exists(vectorizer_path) or not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Baseline model artifacts not found at '{vectorizer_path}' or '{model_path}'."
        )

    vectorizer = joblib.load(vectorizer_path)
    clf = joblib.load(model_path)

    def _predict(text: str) -> Tuple[float, str]:
        vec = vectorizer.transform([text])
        prob = float(clf.predict_proba(vec)[0][1])
        pred = "Fraudulent" if prob >= 0.52 else "Legitimate"
        return prob, pred

    return _predict, "TF-IDF + Logistic Regression Baseline (Raw 0.52)"


def load_distilbert_predictor() -> Tuple[Callable[[str], Tuple[float, str]], str]:
    """Loads the DistilBERT predictor from ml.predict.

    Fails cleanly if local model weights are absent.
    """
    model_dir = "models/jobshield-distilbert-final"
    if not os.path.exists(model_dir):
        raise FileNotFoundError(
            f"DistilBERT model weights not found in '{model_dir}'.\n"
            f"NOTE: Per the repository architecture, large model weights are intentionally "
            f"excluded from git. To evaluate the baseline model instead, run:\n"
            f"    python -m ml.run_adversarial_eval --baseline"
        )

    try:
        from ml.predict import predict_job
    except ImportError as e:
        raise ImportError(f"Failed to import ml.predict: {e}")

    def _predict(text: str) -> Tuple[float, str]:
        res = predict_job(text)
        return float(res["fraud_score"]), str(res["prediction"])

    return _predict, "DistilBERT Classifier"


def load_dataset_samples(max_samples: int = 10) -> List[Dict[str, str]]:
    """Loads test samples from existing test dataset or regression test cases."""
    samples = []

    # Priority 1: Use the existing 5 regression test cases (known ground truth)
    reg_cases = _get_regression_test_cases()
    for idx, (name, text) in enumerate(reg_cases.items()):
        samples.append({
            "id": f"regression_{name}",
            "text": text,
            "label": "Fraudulent" if "fraud" in name.lower() or "scam" in name.lower() or "suspicious" in name.lower() or "entry_level_scam" in name.lower() or "phishing" in name.lower() else "Unknown"
        })

    # Priority 2: Load samples from data/processed/test.csv if available
    test_csv_path = "data/processed/test.csv"
    if os.path.exists(test_csv_path) and len(samples) < max_samples:
        try:
            df = pd.read_csv(test_csv_path)
            # Find fraudulent rows first to test evasion
            fraud_df = df[df["fraudulent"] == 1] if "fraudulent" in df.columns else df
            text_col = "combined_text" if "combined_text" in df.columns else ("description" if "description" in df.columns else None)

            if text_col:
                for idx, row in fraud_df.iterrows():
                    if len(samples) >= max_samples:
                        break
                    samples.append({
                        "id": f"dataset_{idx}",
                        "text": str(row[text_col]),
                        "label": "Fraudulent"
                    })
        except Exception as e:
            print(f"[!] Warning reading test.csv: {e}")

    return samples[:max_samples]


def main():
    parser = argparse.ArgumentParser(
        description="JobShield AI: Offline Adversarial Robustness Benchmark"
    )
    parser.add_argument(
        "--uncalibrated",
        action="store_true",
        help="Evaluate the uncalibrated TF-IDF + Logistic Regression baseline model."
    )
    parser.add_argument(
        "--baseline",
        action="store_true",
        help="Alias for --uncalibrated."
    )
    parser.add_argument(
        "--distilbert",
        action="store_true",
        help="Evaluate DistilBERT sequence classifier (if weights available)."
    )
    parser.add_argument(
        "--max-samples",
        type=int,
        default=5,
        help="Number of postings to evaluate across all 8 attack vectors (default: 5)."
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for deterministic attack mutations (default: 42)."
    )
    args = parser.parse_args()

    print("======================================================================")
    print("      JobShield AI — Adversarial Robustness Benchmark Suite           ")
    print("======================================================================")

    # 1. Resolve Predictor
    predictor_fn = None
    model_name = ""

    if args.distilbert:
        print("[*] Target model selected: DistilBERT Sequence Classifier")
        try:
            predictor_fn, model_name = load_distilbert_predictor()
        except FileNotFoundError as e:
            print(f"\n[!] DistilBERT Notice:\n{e}\n")
            print("[*] Auto-falling back to evaluating deployed Calibrated TF-IDF...")
            predictor_fn, model_name = load_calibrated_predictor()
    elif args.uncalibrated or args.baseline:
        print("[*] Target model selected: Baseline Uncalibrated TF-IDF")
        try:
            predictor_fn, model_name = load_baseline_predictor()
        except FileNotFoundError as e:
            print(f"[ERROR] {e}")
            sys.exit(1)
    else:
        print("[*] Target model selected: Deployed Calibrated TF-IDF + Platt Scaling (Production)")
        try:
            predictor_fn, model_name = load_calibrated_predictor()
        except Exception as e:
            print(f"[!] Error loading calibrated model ({e}), falling back to baseline...")
            predictor_fn, model_name = load_baseline_predictor()

    print(f"[✓] Successfully initialized inference engine: {model_name}")

    # 2. Load Evaluation Samples
    samples = load_dataset_samples(max_samples=args.max_samples)
    print(f"[*] Loaded {len(samples)} distinct target job postings for stress testing.")

    # 3. Run Benchmark
    evaluator = AdversarialEvaluator(
        predictor_fn=predictor_fn,
        model_name=model_name,
        seed=args.seed
    )

    print(f"[*] Executing {len(evaluator.ALL_ATTACK_KEYS)} adversarial attack generators on each sample (Seed: {args.seed})...")
    summary = evaluator.evaluate_dataset(samples)

    # 4. Generate Reports
    reporter = AdversarialAuditReporter()
    json_path = reporter.export_json(summary)
    md_path = reporter.export_markdown(summary)

    # 5. Display Console Summary
    print("\n" + "=" * 70)
    print(f"                ADVERSARIAL EVALUATION SUMMARY ({summary.model_name})")
    print("=" * 70)
    print(f"Total Postings Evaluated:         {summary.total_samples}")
    print(f"Postings Originally Fraudulent:   {summary.overall_originally_fraudulent} (out of {summary.total_samples} evaluated)")
    print(f"Total Attack Variants Generated:  {summary.total_evaluations}")
    print(f"Fraudulent Attack Opportunities:  {summary.fraudulent_attack_evaluations}")
    print(f"Evaded Classifications (Flips):   {summary.overall_flips}")
    print(f"Overall Attack Success Rate:      {summary.overall_asr * 100:.2f}%")
    print(f"Pre-Attack Fraud Detection Rate:  {summary.overall_pre_detection_rate * 100:.2f}%")
    print(f"Post-Attack Fraud Detection Rate: {summary.overall_post_detection_rate * 100:.2f}%")
    print(f"Mean Fraud Score Degradation:     {summary.overall_mean_score_drop:+.4f}")
    print(f"Max Fraud Score Drop Observed:    {summary.overall_max_score_drop:.4f}")
    print(f"Rule-Based Signal Dropout Rate:   {summary.overall_signal_dropout_rate * 100:.2f}%")
    print("-" * 70)
    print(f"{'Attack Type':<26} {'Eval':<6} {'Flips':<6} {'ASR (%)':<10} {'Sig Drop (%)'}")
    print("-" * 70)
    for atype, m in sorted(summary.by_attack_type.items(), key=lambda x: x[1].attack_success_rate, reverse=True):
        print(
            f"{m.attack_type:<26} {m.total_evaluated:<6} {m.flips_to_legitimate:<6} "
            f"{m.attack_success_rate * 100:>6.1f}%    {m.signal_dropout_rate * 100:>8.1f}%"
        )
    print("=" * 70)
    print(f"[✓] Structured audit log saved to: {json_path}")
    print(f"[✓] Human-readable markdown saved to: {md_path}")
    print("=" * 70)


if __name__ == "__main__":
    main()

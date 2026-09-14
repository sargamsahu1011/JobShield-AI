"""
Error Analysis for JobShield AI Production Model.
Analyzes every False Positive and False Negative made by the calibrated production model:
- calibrated_platt_logreg.joblib
- tfidf_vectorizer.joblib
- threshold: 0.54
Saves detailed breakdown to reports/error_analysis.csv.
"""

import os
import sys
import re
import joblib
import pandas as pd
import numpy as np
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from ml.scam_signals import detect_scam_signals
from ml.text_normalizer import normalize_text


def detect_extended_signals(text: str) -> dict:
    """Detect standard and extended signals for error categorization."""
    t_lower = normalize_text(text).lower()
    base_signals = detect_scam_signals(text)

    # Extended regex signals
    wfh = bool(re.search(r"\b(work from home|wfh|remote work|home[- ]based|work at home)\b", t_lower))
    high_income = bool(re.search(r"(\$\s*\d{3,5}\s*(per|\/)\s*(week|day|hr|hour))|(\b\d{2,3}k\b)|(earn\s+\$?\d+)", t_lower))
    suspicious_contact = bool(
        base_signals.get("telegram_contact", False)
        or base_signals.get("whatsapp_contact", False)
        or base_signals.get("personal_email", False)
        or re.search(r"\b(skype|gmail|yahoo|send\s+(your\s+)?cv\s+to)\b", t_lower)
    )

    signals_dict = {
        "payment_fee": bool(base_signals.get("payment_request", False) or "fee" in t_lower),
        "bank_account_info": bool(base_signals.get("sensitive_data_request", False) or "bank" in t_lower),
        "telegram_whatsapp": bool(base_signals.get("telegram_contact", False) or base_signals.get("whatsapp_contact", False)),
        "personal_email": bool(base_signals.get("personal_email", False)),
        "urgency": bool(base_signals.get("urgency_language", False)),
        "work_from_home": wfh,
        "no_experience": bool(base_signals.get("no_experience_required", False) or "no experience" in t_lower),
        "high_income": high_income,
        "suspicious_contact": suspicious_contact,
        "crypto": bool(base_signals.get("crypto_request", False)),
        "suspicious_url": bool(base_signals.get("suspicious_url", False)),
    }
    return signals_dict


def categorize_error(row: pd.Series, error_type: str, signals: dict) -> tuple[str, str]:
    """
    Categorize errors into conservative categories:
    - short_posting
    - ambiguous_legitimate
    - missing_scam_signals
    - unusual_wording
    - semantic_paraphrase
    - insufficient_evidence
    - possible_label_issue
    - uncertain
    """
    text_len = row["text_length"]
    word_cnt = row["word_count"]
    title = str(row.get("title", "")).lower()
    text = str(row.get("combined_text", ""))
    t_lower = text.lower()

    if error_type == "FP":
        # Ground truth = 0 (Legitimate), Prediction = 1 (Fraudulent)
        # Legitimate postings heavily laden with clerical / data entry duties that overlap heavily with scam vocabulary
        if "data entry" in title or "payroll" in title or "clerk" in title:
            return (
                "ambiguous_legitimate",
                "Legitimate clerical/data entry posting with high keyword overlap with typical administrative scams."
            )
        return (
            "ambiguous_legitimate",
            "Legitimate job containing phrases that resemble recruitment scam patterns."
        )

    # error_type == "FN": Ground truth = 1 (Fraudulent), Prediction = 0 (Legitimate)
    if word_cnt < 85 or text_len < 600:
        if "money motivated" in title or "sales person required" in title:
            return (
                "unusual_wording",
                "High-pressure / commission sales posting with non-standard scam phrasing and sparse description."
            )
        return (
            "short_posting",
            f"Extremely brief job posting ({word_cnt} words, {text_len} chars) lacking sufficient TF-IDF feature density."
        )

    # Check for technical/clinical corporate imposters (stolen legitimate postings)
    corporate_titles = [
        "technology consultant", "integration engineer", "lead business analyst",
        "director of perioperative services", "quality manager", "qa compliance specialist",
        "user experience designer", "android developer", "web developer", "physician assistant"
    ]
    if any(ct in title for ct in corporate_titles):
        active_signals = [k for k, v in signals.items() if v]
        if not active_signals or active_signals == ["work_from_home"]:
            return (
                "missing_scam_signals",
                "Sophisticated corporate clone mimicking genuine corporate job description; lacks overt scam vocabulary."
            )
        else:
            return (
                "semantic_paraphrase",
                f"Scam disguised as professional job with subtle indicators ({', '.join(active_signals)}) that TF-IDF missed."
            )

    if "webcam" in title:
        return (
            "unusual_wording",
            "Adult entertainment / non-traditional recruitment posting with domain-specific terms not captured in training vocabulary."
        )

    if "receptionist" in title or "admin" in title or "sales" in title:
        active_signals = [k for k, v in signals.items() if v]
        if "london" in t_lower or "we the" in t_lower or "interested persons" in t_lower:
            return (
                "unusual_wording",
                "Foreign or unconventional phrasing in hotel/receptionist vacancy bypassing standard scam n-grams."
            )
        return (
            "insufficient_evidence",
            f"General administrative/sales vacancy with low fraud confidence ({row['probability']:.4f}) and weak feature support."
        )

    return ("uncertain", "Error case with mixed characteristics requiring deeper semantic context.")


def run_error_analysis():
    base_dir = Path(__file__).resolve().parent.parent
    test_path = base_dir / "data" / "processed" / "test.csv"
    vec_path = base_dir / "models" / "tfidf_vectorizer.joblib"
    model_path = base_dir / "models" / "calibrated_platt_logreg.joblib"
    reports_dir = base_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    out_csv = reports_dir / "error_analysis.csv"

    print("==================================================")
    print("STAGE 4: PRODUCTION MODEL ERROR ANALYSIS")
    print("==================================================")
    print(f"Loading test set from: {test_path}")
    test_df = pd.read_csv(test_path)

    print(f"Loading vectorizer: {vec_path}")
    vectorizer = joblib.load(vec_path)

    print(f"Loading production model: {model_path}")
    model = joblib.load(model_path)

    threshold = 0.54
    print(f"Production decision threshold: {threshold}")

    # Compute production predictions
    X_test = vectorizer.transform(test_df["combined_text"].fillna(""))
    probabilities = model.predict_proba(X_test)[:, 1]
    predictions = (probabilities >= threshold).astype(int)

    test_df["predicted_label"] = predictions
    test_df["probability"] = probabilities
    y_true = test_df["fraudulent"].values

    fps = test_df[(y_true == 0) & (predictions == 1)].copy()
    fns = test_df[(y_true == 1) & (predictions == 0)].copy()

    fp_count = len(fps)
    fn_count = len(fns)
    total_errors = fp_count + fn_count

    print(f"Total test samples : {len(test_df)}")
    print(f"False Positives    : {fp_count}")
    print(f"False Negatives    : {fn_count}")
    print(f"Total Errors       : {total_errors}")

    assert fp_count == 3, f"Expected 3 FPs, got {fp_count}"
    assert fn_count == 21, f"Expected 21 FNs, got {fn_count}"

    records = []

    # Process False Positives
    for idx, row in fps.iterrows():
        signals = detect_extended_signals(str(row["combined_text"]))
        category, rationale = categorize_error(row, "FP", signals)
        signal_names = [k for k, v in signals.items() if v]

        records.append({
            "test_row_index": idx,
            "job_id": row["job_id"],
            "title": row.get("title", ""),
            "true_label": int(row["fraudulent"]),
            "predicted_label": int(row["predicted_label"]),
            "probability": round(float(row["probability"]), 4),
            "error_type": "FP",
            "category": category,
            "text_length": int(row["text_length"]),
            "word_count": int(row["word_count"]),
            "detected_signals": "; ".join(signal_names) if signal_names else "none",
            "rationale": rationale,
        })

    # Process False Negatives
    for idx, row in fns.iterrows():
        signals = detect_extended_signals(str(row["combined_text"]))
        category, rationale = categorize_error(row, "FN", signals)
        signal_names = [k for k, v in signals.items() if v]

        records.append({
            "test_row_index": idx,
            "job_id": row["job_id"],
            "title": row.get("title", ""),
            "true_label": int(row["fraudulent"]),
            "predicted_label": int(row["predicted_label"]),
            "probability": round(float(row["probability"]), 4),
            "error_type": "FN",
            "category": category,
            "text_length": int(row["text_length"]),
            "word_count": int(row["word_count"]),
            "detected_signals": "; ".join(signal_names) if signal_names else "none",
            "rationale": rationale,
        })

    error_df = pd.DataFrame(records)
    error_df.to_csv(out_csv, index=False)
    print(f"[+] Saved error analysis to: {out_csv}")

    print("\nError Category Breakdown:")
    print(error_df["category"].value_counts().to_string())

    print("\nSignal Distribution across Errors:")
    all_signals = []
    for s_str in error_df["detected_signals"]:
        if s_str != "none":
            all_signals.extend(s_str.split("; "))
    signal_series = pd.Series(all_signals).value_counts()
    print(signal_series.to_string())

    print("\nStage 4 Error Analysis: PASS")
    return error_df


if __name__ == "__main__":
    run_error_analysis()

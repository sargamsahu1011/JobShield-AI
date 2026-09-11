"""
Calibration module for JobShield AI primary model (TF-IDF + Logistic Regression).
Applies Platt scaling (sigmoid) and Isotonic regression to the validation split.
Computes Brier scores, Expected Calibration Error (ECE), Log Loss, and reliability curves.
Saves the calibrated model artifact and calibration metrics.
"""

import json
import os
import joblib
import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.frozen import FrozenEstimator
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    f1_score,
    log_loss,
    precision_score,
    recall_score,
    roc_auc_score,
)


def expected_calibration_error(y_true: np.ndarray, y_prob: np.ndarray, n_bins: int = 10) -> float:
    """Computes Expected Calibration Error (ECE) across uniform bins."""
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    bin_lowers = bin_boundaries[:-1]
    bin_uppers = bin_boundaries[1:]
    ece = 0.0
    for bin_lower, bin_upper in zip(bin_lowers, bin_uppers):
        if bin_upper < 1.0:
            in_bin = (y_prob >= bin_lower) & (y_prob < bin_upper)
        else:
            in_bin = (y_prob >= bin_lower) & (y_prob <= bin_upper)
        prop_in_bin = np.mean(in_bin)
        if prop_in_bin > 0:
            acc_in_bin = np.mean(y_true[in_bin])
            conf_in_bin = np.mean(y_prob[in_bin])
            ece += np.abs(conf_in_bin - acc_in_bin) * prop_in_bin
    return float(ece)


def compute_reliability_table(y_true: np.ndarray, y_prob: np.ndarray, n_bins: int = 10) -> list:
    """Generates binned reliability data for reporting."""
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    table = []
    for b_low, b_high in zip(bin_boundaries[:-1], bin_boundaries[1:]):
        if b_high < 1.0:
            cond = (y_prob >= b_low) & (y_prob < b_high)
        else:
            cond = (y_prob >= b_low) & (y_prob <= b_high)
        count = int(np.sum(cond))
        if count > 0:
            mean_pred = float(np.mean(y_prob[cond]))
            emp_pos = float(np.mean(y_true[cond]))
            err = float(abs(mean_pred - emp_pos))
        else:
            mean_pred = None
            emp_pos = None
            err = None
        table.append({
            "bin_range": [round(b_low, 2), round(b_high, 2)],
            "count": count,
            "mean_predicted": mean_pred,
            "empirical_positive_rate": emp_pos,
            "abs_error": err,
        })
    return table


def run_calibration():
    val_path = "data/processed/validation.csv"
    test_path = "data/processed/test.csv"
    vec_path = "models/tfidf_vectorizer.joblib"
    model_path = "models/tfidf_logreg.joblib"

    print("[*] Loading datasets and baseline model...")
    val_df = pd.read_csv(val_path)
    test_df = pd.read_csv(test_path)
    vectorizer = joblib.load(vec_path)
    model = joblib.load(model_path)

    X_val = vectorizer.transform(val_df["combined_text"].fillna(""))
    y_val = val_df["fraudulent"].values
    X_test = vectorizer.transform(test_df["combined_text"].fillna(""))
    y_test = test_df["fraudulent"].values

    # Uncalibrated baseline probabilities
    raw_val_probs = model.predict_proba(X_val)[:, 1]
    raw_test_probs = model.predict_proba(X_test)[:, 1]

    # Fit Platt scaling (Sigmoid) on validation set
    print("[*] Fitting Platt Scaling (Sigmoid) on validation split...")
    cal_platt = CalibratedClassifierCV(FrozenEstimator(model), method="sigmoid")
    cal_platt.fit(X_val, y_val)
    platt_val_probs = cal_platt.predict_proba(X_val)[:, 1]
    platt_test_probs = cal_platt.predict_proba(X_test)[:, 1]

    # Fit Isotonic Regression on validation set
    print("[*] Fitting Isotonic Regression on validation split...")
    cal_iso = CalibratedClassifierCV(FrozenEstimator(model), method="isotonic")
    cal_iso.fit(X_val, y_val)
    iso_val_probs = cal_iso.predict_proba(X_val)[:, 1]
    iso_test_probs = cal_iso.predict_proba(X_test)[:, 1]

    # Find optimal F1 threshold for calibrated probabilities on validation set
    best_p_thresh = 0.5
    best_f1 = 0.0
    for t in np.arange(0.01, 0.99, 0.005):
        preds = (platt_val_probs >= t).astype(int)
        f = f1_score(y_val, preds, pos_label=1, zero_division=0)
        if f > best_f1:
            best_f1 = float(f)
            best_p_thresh = float(round(t, 4))

    # Evaluate at optimal calibrated threshold
    val_cal_preds = (platt_val_probs >= best_p_thresh).astype(int)
    test_cal_preds = (platt_test_probs >= best_p_thresh).astype(int)

    metrics_summary = {
        "uncalibrated": {
            "val_brier": float(brier_score_loss(y_val, raw_val_probs)),
            "val_log_loss": float(log_loss(y_val, raw_val_probs)),
            "val_ece": expected_calibration_error(y_val, raw_val_probs),
            "test_brier": float(brier_score_loss(y_test, raw_test_probs)),
            "test_log_loss": float(log_loss(y_test, raw_test_probs)),
            "test_ece": expected_calibration_error(y_test, raw_test_probs),
            "test_pr_auc": float(average_precision_score(y_test, raw_test_probs)),
            "test_roc_auc": float(roc_auc_score(y_test, raw_test_probs)),
            "test_precision_at_0_52": float(precision_score(y_test, (raw_test_probs >= 0.52).astype(int))),
            "test_recall_at_0_52": float(recall_score(y_test, (raw_test_probs >= 0.52).astype(int))),
            "test_f1_at_0_52": float(f1_score(y_test, (raw_test_probs >= 0.52).astype(int))),
            "reliability_table_test": compute_reliability_table(y_test, raw_test_probs),
        },
        "platt_scaling": {
            "calibrated_threshold": best_p_thresh,
            "val_brier": float(brier_score_loss(y_val, platt_val_probs)),
            "val_log_loss": float(log_loss(y_val, platt_val_probs)),
            "val_ece": expected_calibration_error(y_val, platt_val_probs),
            "test_brier": float(brier_score_loss(y_test, platt_test_probs)),
            "test_log_loss": float(log_loss(y_test, platt_test_probs)),
            "test_ece": expected_calibration_error(y_test, platt_test_probs),
            "test_pr_auc": float(average_precision_score(y_test, platt_test_probs)),
            "test_roc_auc": float(roc_auc_score(y_test, platt_test_probs)),
            "val_precision": float(precision_score(y_val, val_cal_preds)),
            "val_recall": float(recall_score(y_val, val_cal_preds)),
            "val_f1": float(f1_score(y_val, val_cal_preds)),
            "test_precision": float(precision_score(y_test, test_cal_preds)),
            "test_recall": float(recall_score(y_test, test_cal_preds)),
            "test_f1": float(f1_score(y_test, test_cal_preds)),
            "reliability_table_test": compute_reliability_table(y_test, platt_test_probs),
        },
        "isotonic_regression": {
            "val_brier": float(brier_score_loss(y_val, iso_val_probs)),
            "val_log_loss": float(log_loss(y_val, iso_val_probs)),
            "val_ece": expected_calibration_error(y_val, iso_val_probs),
            "test_brier": float(brier_score_loss(y_test, iso_test_probs)),
            "test_log_loss": float(log_loss(y_test, iso_test_probs)),
            "test_ece": expected_calibration_error(y_test, iso_test_probs),
            "test_pr_auc": float(average_precision_score(y_test, iso_test_probs)),
            "test_roc_auc": float(roc_auc_score(y_test, iso_test_probs)),
            "reliability_table_test": compute_reliability_table(y_test, iso_test_probs),
        },
    }

    # Save artifacts
    cal_model_path = "models/calibrated_platt_logreg.joblib"
    metrics_path = "models/calibration_metrics.json"

    joblib.dump(cal_platt, cal_model_path)
    with open(metrics_path, "w") as f:
        json.dump(metrics_summary, f, indent=2)

    print(f"\n[+] Saved calibrated model to: {cal_model_path}")
    print(f"[+] Saved calibration metrics to: {metrics_path}")

    return metrics_summary


if __name__ == "__main__":
    run_calibration()

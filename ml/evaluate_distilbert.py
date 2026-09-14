import json
import os

import numpy as np
import pandas as pd
import torch
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    average_precision_score,
    roc_auc_score,
    confusion_matrix,
)
from transformers import AutoTokenizer, AutoModelForSequenceClassification


TEST_PATH = "data/processed/test.csv"
MODEL_DIR = "models/jobshield-distilbert-final"
OUTPUT_PRED = "models/distilbert_test_predictions.csv"
OUTPUT_METRICS = "models/distilbert_metrics.json"

MAX_LENGTH = 256


def main():
    print("Loading clean test set...")
    df = pd.read_csv(TEST_PATH)

    print(f"Test shape: {df.shape}")

    text_col = "combined_text"
    label_col = "fraudulent"

    texts = df[text_col].fillna("").astype(str).tolist()
    y_true = df[label_col].astype(int).to_numpy()

    with open(os.path.join(MODEL_DIR, "threshold_config.json"), "r") as f:
        threshold_config = json.load(f)

    threshold = float(threshold_config["final_threshold"])

    print(f"Model: {MODEL_DIR}")
    print(f"Threshold: {threshold}")
    print(f"Max sequence length: {MAX_LENGTH}")
    print(f"Rows to evaluate: {len(df)}")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
    model.to(device)
    model.eval()

    probabilities = []

    batch_size = 16

    for start in range(0, len(texts), batch_size):
        batch_texts = texts[start:start + batch_size]

        inputs = tokenizer(
            batch_texts,
            padding=True,
            truncation=True,
            max_length=MAX_LENGTH,
            return_tensors="pt",
        )

        inputs = {k: v.to(device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = model(**inputs)
            probs = torch.softmax(outputs.logits, dim=1)[:, 1]

        probabilities.extend(probs.cpu().numpy())

        print(
            f"Processed {min(start + batch_size, len(texts))}/{len(texts)}"
        )

    y_score = np.asarray(probabilities)
    y_pred = (y_score >= threshold).astype(int)

    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    pr_auc = average_precision_score(y_true, y_score)
    roc_auc = roc_auc_score(y_true, y_score)
    cm = confusion_matrix(y_true, y_pred).tolist()

    metrics = {
        "stage": "1B",
        "dataset": "clean leakage-safe test split",
        "model": "DistilBERT",
        "model_name": "distilbert-base-uncased",
        "threshold": threshold,
        "max_length": MAX_LENGTH,
        "test_rows": len(df),
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
        "pr_auc": float(pr_auc),
        "roc_auc": float(roc_auc),
        "confusion_matrix": cm,
        "device": str(device),
    }

    predictions = df.copy()
    predictions["distilbert_score"] = y_score
    predictions["distilbert_prediction"] = y_pred
    predictions.to_csv(OUTPUT_PRED, index=False)

    with open(OUTPUT_METRICS, "w") as f:
        json.dump(metrics, f, indent=2)

    print("\n=== DISTILBERT CLEAN TEST RESULTS ===")
    print(f"Precision : {precision:.4f}")
    print(f"Recall    : {recall:.4f}")
    print(f"F1        : {f1:.4f}")
    print(f"PR-AUC    : {pr_auc:.4f}")
    print(f"ROC-AUC   : {roc_auc:.4f}")
    print("Confusion Matrix:")
    print(cm)

    print(f"\nSaved: {OUTPUT_PRED}")
    print(f"Saved: {OUTPUT_METRICS}")


if __name__ == "__main__":
    main()
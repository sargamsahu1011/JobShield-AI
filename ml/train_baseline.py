import os
import json
import joblib
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    average_precision_score,
    roc_auc_score,
    precision_score,
    recall_score,
    f1_score
)


# =========================
# 1. Paths
# =========================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TRAIN_PATH = os.path.join(BASE_DIR, "data", "processed", "train.csv")
VAL_PATH = os.path.join(BASE_DIR, "data", "processed", "validation.csv")
TEST_PATH = os.path.join(BASE_DIR, "data", "processed", "test.csv")

MODEL_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODEL_DIR, exist_ok=True)


# =========================
# 2. Load datasets
# =========================

print("Loading datasets...")

train_df = pd.read_csv(TRAIN_PATH)
val_df = pd.read_csv(VAL_PATH)
test_df = pd.read_csv(TEST_PATH)

print(f"Train      : {train_df.shape}")
print(f"Validation : {val_df.shape}")
print(f"Test       : {test_df.shape}")


# =========================
# 3. Prepare text + target
# =========================

TEXT_COL = "combined_text"
TARGET_COL = "fraudulent"

X_train = train_df[TEXT_COL].fillna("")
y_train = train_df[TARGET_COL]

X_val = val_df[TEXT_COL].fillna("")
y_val = val_df[TARGET_COL]

X_test = test_df[TEXT_COL].fillna("")
y_test = test_df[TARGET_COL]


# =========================
# 4. TF-IDF
# =========================

print("\nFitting TF-IDF on TRAINING data only...")

vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),
    min_df=2,
    max_df=0.95,
    sublinear_tf=True,
    max_features=100000
)

X_train_tfidf = vectorizer.fit_transform(X_train)

# IMPORTANT:
# Validation and test are ONLY transformed.
# We do NOT fit TF-IDF on them.

X_val_tfidf = vectorizer.transform(X_val)
X_test_tfidf = vectorizer.transform(X_test)

print(f"TF-IDF train shape: {X_train_tfidf.shape}")
print(f"TF-IDF val shape  : {X_val_tfidf.shape}")
print(f"TF-IDF test shape : {X_test_tfidf.shape}")


# =========================
# 5. Logistic Regression
# =========================

print("\nTraining Logistic Regression...")

model = LogisticRegression(
    class_weight="balanced",
    max_iter=2000,
    solver="liblinear",
    random_state=42
)

model.fit(X_train_tfidf, y_train)

print("Model training completed.")


# =========================
# 6. Evaluation function
# =========================

def evaluate_model(y_true, probabilities, threshold=0.5, dataset_name="Dataset"):

    predictions = (probabilities >= threshold).astype(int)

    precision = precision_score(
        y_true,
        predictions,
        pos_label=1,
        zero_division=0
    )

    recall = recall_score(
        y_true,
        predictions,
        pos_label=1,
        zero_division=0
    )

    f1 = f1_score(
        y_true,
        predictions,
        pos_label=1,
        zero_division=0
    )

    pr_auc = average_precision_score(
        y_true,
        probabilities
    )

    roc_auc = roc_auc_score(
        y_true,
        probabilities
    )

    print("\n" + "=" * 60)
    print(f"{dataset_name} RESULTS")
    print("=" * 60)

    print(f"Threshold : {threshold:.3f}")
    print(f"Precision : {precision:.4f}")
    print(f"Recall    : {recall:.4f}")
    print(f"F1 Score  : {f1:.4f}")
    print(f"PR-AUC    : {pr_auc:.4f}")
    print(f"ROC-AUC   : {roc_auc:.4f}")

    print("\nClassification Report:")
    print(
        classification_report(
            y_true,
            predictions,
            target_names=["Legitimate", "Fraudulent"],
            digits=4,
            zero_division=0
        )
    )

    print("Confusion Matrix:")
    print(confusion_matrix(y_true, predictions))

    return {
        "threshold": threshold,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "pr_auc": pr_auc,
        "roc_auc": roc_auc
    }


# =========================
# 7. Validation prediction
# =========================

print("\nGenerating validation predictions...")

val_probabilities = model.predict_proba(X_val_tfidf)[:, 1]


# =========================
# 8. Find best threshold
# =========================

print("\nSearching for best validation F1 threshold...")

thresholds = np.arange(0.05, 0.96, 0.01)

best_threshold = 0.5
best_f1 = 0

for threshold in thresholds:

    val_predictions = (
        val_probabilities >= threshold
    ).astype(int)

    current_f1 = f1_score(
        y_val,
        val_predictions,
        pos_label=1,
        zero_division=0
    )

    if current_f1 > best_f1:
        best_f1 = current_f1
        best_threshold = threshold


print(f"Best threshold : {best_threshold:.2f}")
print(f"Best Val F1    : {best_f1:.4f}")


# =========================
# 9. Evaluate validation
# =========================

val_results = evaluate_model(
    y_val,
    val_probabilities,
    threshold=best_threshold,
    dataset_name="VALIDATION"
)


# =========================
# 10. Test prediction
# =========================

print("\nGenerating TEST predictions...")

test_probabilities = model.predict_proba(X_test_tfidf)[:, 1]

test_results = evaluate_model(
    y_test,
    test_probabilities,
    threshold=best_threshold,
    dataset_name="TEST"
)


# =========================
# 11. Save model + vectorizer
# =========================

vectorizer_path = os.path.join(
    MODEL_DIR,
    "tfidf_vectorizer.joblib"
)

model_path = os.path.join(
    MODEL_DIR,
    "tfidf_logreg.joblib"
)

joblib.dump(vectorizer, vectorizer_path)
joblib.dump(model, model_path)

print("\nSaved:")
print(vectorizer_path)
print(model_path)


# =========================
# 12. Save test predictions
# =========================

test_predictions = (
    test_probabilities >= best_threshold
).astype(int)

prediction_df = pd.DataFrame({
    "job_id": test_df["job_id"],
    "actual_label": y_test,
    "fraud_probability": test_probabilities,
    "predicted_label": test_predictions
})

prediction_path = os.path.join(
    MODEL_DIR,
    "baseline_test_predictions.csv"
)

prediction_df.to_csv(
    prediction_path,
    index=False
)

print(prediction_path)


# =========================
# 13. Save metrics
# =========================

metrics = {
    "model": "TF-IDF + Logistic Regression",
    "text_column": TEXT_COL,
    "ngram_range": [1, 2],
    "class_weight": "balanced",
    "best_threshold": float(best_threshold),
    "validation": val_results,
    "test": test_results
}

metrics_path = os.path.join(
    MODEL_DIR,
    "baseline_metrics.json"
)

with open(metrics_path, "w") as f:
    json.dump(metrics, f, indent=4)

print(metrics_path)

print("\n" + "=" * 60)
print("BASELINE COMPLETE")
print("=" * 60)
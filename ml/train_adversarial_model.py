import pandas as pd
import joblib
import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    average_precision_score,
    roc_auc_score,
    confusion_matrix
)

TRAIN = "data/processed/train_adversarial.csv"
VAL = "data/processed/validation.csv"
TEST = "data/processed/test.csv"

train = pd.read_csv(TRAIN)
val = pd.read_csv(VAL)
test = pd.read_csv(TEST)

X_train = train["combined_text"].fillna("")
y_train = train["fraudulent"]

X_val = val["combined_text"].fillna("")
y_val = val["fraudulent"]

X_test = test["combined_text"].fillna("")
y_test = test["fraudulent"]

vectorizer = TfidfVectorizer(
    max_features=100000,
    ngram_range=(1, 2),
    sublinear_tf=True
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_val_tfidf = vectorizer.transform(X_val)
X_test_tfidf = vectorizer.transform(X_test)

model = LogisticRegression(
    max_iter=2000,
    class_weight="balanced",
    random_state=42
)

model.fit(X_train_tfidf, y_train)

val_prob = model.predict_proba(X_val_tfidf)[:, 1]

best_threshold = 0.5
best_f1 = 0

for threshold in [i / 100 for i in range(1, 100)]:
    pred = (val_prob >= threshold).astype(int)
    f1 = f1_score(y_val, pred)

    if f1 > best_f1:
        best_f1 = f1
        best_threshold = threshold

test_prob = model.predict_proba(X_test_tfidf)[:, 1]
test_pred = (test_prob >= best_threshold).astype(int)

metrics = {
    "threshold": best_threshold,
    "precision": precision_score(y_test, test_pred),
    "recall": recall_score(y_test, test_pred),
    "f1": f1_score(y_test, test_pred),
    "pr_auc": average_precision_score(y_test, test_prob),
    "roc_auc": roc_auc_score(y_test, test_prob),
    "confusion_matrix": confusion_matrix(y_test, test_pred).tolist()
}

joblib.dump(
    vectorizer,
    "models/adversarial_tfidf_vectorizer.joblib"
)

joblib.dump(
    model,
    "models/adversarial_tfidf_logreg.joblib"
)

with open(
    "models/adversarial_metrics.json",
    "w"
) as f:
    json.dump(metrics, f, indent=2)

print("\n=== ADVERSARIAL-AUGMENTED MODEL ===")
print(f"Threshold : {best_threshold:.2f}")
print(f"Precision : {metrics['precision']:.4f}")
print(f"Recall    : {metrics['recall']:.4f}")
print(f"F1        : {metrics['f1']:.4f}")
print(f"PR-AUC    : {metrics['pr_auc']:.4f}")
print(f"ROC-AUC   : {metrics['roc_auc']:.4f}")
print("Confusion Matrix:")
print(confusion_matrix(y_test, test_pred))

print("\nModels saved successfully.")
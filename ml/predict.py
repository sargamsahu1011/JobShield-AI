import json
import os
import joblib

try:
    from ml.text_normalizer import normalize_text
    from ml.boilerplate_cleaner import clean_boilerplate
except ImportError:
    from text_normalizer import normalize_text
    from boilerplate_cleaner import clean_boilerplate

# Model paths
DISTILBERT_DIR = "models/jobshield-distilbert-final"
CALIBRATED_TFIDF_PATH = "models/calibrated_platt_logreg.joblib"
BASELINE_TFIDF_PATH = "models/tfidf_logreg.joblib"
VECTORIZER_PATH = "models/tfidf_vectorizer.joblib"
CALIBRATION_METRICS_PATH = "models/calibration_metrics.json"

_distilbert_available = False
_distilbert_model = None
_distilbert_tokenizer = None

# Attempt to load DistilBERT if torch and model directory exist
if os.path.exists(DISTILBERT_DIR):
    try:
        import torch
        from transformers import AutoTokenizer, AutoModelForSequenceClassification

        with open(f"{DISTILBERT_DIR}/threshold_config.json", "r") as f:
            config = json.load(f)
        THRESHOLD = config.get("final_threshold", 0.5)
        _distilbert_tokenizer = AutoTokenizer.from_pretrained(DISTILBERT_DIR)
        _distilbert_model = AutoModelForSequenceClassification.from_pretrained(DISTILBERT_DIR)
        _distilbert_model.eval()
        _distilbert_available = True
        IS_CALIBRATED = False
        MODEL_NAME = "DistilBERT Sequence Classifier"
        print(f"Loaded DistilBERT model with threshold {THRESHOLD}")
    except Exception as e:
        _distilbert_available = False

if not _distilbert_available:
    # Primary model: Calibrated TF-IDF + Logistic Regression
    if os.path.exists(CALIBRATED_TFIDF_PATH) and os.path.exists(VECTORIZER_PATH):
        vectorizer = joblib.load(VECTORIZER_PATH)
        model = joblib.load(CALIBRATED_TFIDF_PATH)
        if os.path.exists(CALIBRATION_METRICS_PATH):
            with open(CALIBRATION_METRICS_PATH, "r") as f:
                cal_data = json.load(f)
            THRESHOLD = cal_data.get("platt_scaling", {}).get("calibrated_threshold", 0.405)
        else:
            THRESHOLD = 0.405
        IS_CALIBRATED = True
        MODEL_NAME = "Calibrated TF-IDF + Logistic Regression (Platt Scaling)"
        print(f"Loaded Calibrated TF-IDF + LogReg model with threshold {THRESHOLD}")
    else:
        # Fallback to uncalibrated baseline
        vectorizer = joblib.load(VECTORIZER_PATH)
        model = joblib.load(BASELINE_TFIDF_PATH)
        THRESHOLD = 0.52
        IS_CALIBRATED = False
        MODEL_NAME = "Uncalibrated TF-IDF + Logistic Regression Baseline"
        print(f"Loaded Uncalibrated TF-IDF + LogReg model with threshold {THRESHOLD}")


def predict_job(job_text: str):
    """
    Predicts fraud risk for a given job posting text.
    Returns:
        fraud_score (float): Calibrated probability (if calibrated model loaded) or raw risk score.
        prediction (int): 1 for Fraudulent, 0 for Legitimate.
    """
    job_text = normalize_text(job_text)
    # Strip common corporate boilerplate before feature extraction to prevent dilution
    job_text = clean_boilerplate(job_text)

    if _distilbert_available:
        import torch

        inputs = _distilbert_tokenizer(
            job_text,
            return_tensors="pt",
            truncation=True,
            max_length=256
        )
        with torch.no_grad():
            outputs = _distilbert_model(**inputs)
            probabilities = torch.softmax(outputs.logits, dim=1)
        fraud_score = float(probabilities[0][1].item())
    else:
        feat = vectorizer.transform([job_text])
        fraud_score = float(model.predict_proba(feat)[0][1])

    prediction = int(fraud_score >= THRESHOLD)
    return fraud_score, prediction


if __name__ == "__main__":
    test_job = """
We are looking for a work-from-home data entry employee.
No experience required.

Earn $5000 per week.
You will receive guaranteed employment immediately.

To complete your registration, send your bank account
details and pay a small refundable processing fee.

Contact our recruiter through Telegram to continue.
"""
    fraud_prob, pred = predict_job(test_job)
    print("\n==========================================")
    print("JOBSHIELD TEST PREDICTION")
    print("==========================================")
    print(f"Model: {MODEL_NAME}")
    print(f"Score/Probability: {fraud_prob:.4f} (Calibrated: {IS_CALIBRATED})")
    print(f"Threshold: {THRESHOLD}")
    print("Prediction:", "FRAUDULENT / HIGH RISK" if pred == 1 else "LEGITIMATE / LOW RISK")

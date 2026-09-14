import json
import os
import joblib

try:
    from ml.text_normalizer import normalize_text
    from ml.boilerplate_cleaner import clean_boilerplate
except ImportError:
    from text_normalizer import normalize_text
    from boilerplate_cleaner import clean_boilerplate


# ============================================================
# MODEL PATHS
# ============================================================

DISTILBERT_DIR = "models/jobshield-distilbert-final"

CALIBRATED_TFIDF_PATH = "models/calibrated_platt_logreg.joblib"
BASELINE_TFIDF_PATH = "models/tfidf_logreg.joblib"
VECTORIZER_PATH = "models/tfidf_vectorizer.joblib"

CALIBRATION_METRICS_PATH = "models/calibration_metrics.json"


# ============================================================
# PRODUCTION CALIBRATION SETTINGS
# ============================================================

# Stage 2 selected Platt Scaling.
# Threshold was selected on the validation split.
CALIBRATION_THRESHOLD = 0.54


# ============================================================
# MODEL STATE
# ============================================================

_distilbert_available = False
_distilbert_model = None
_distilbert_tokenizer = None

vectorizer = None
model = None

THRESHOLD = CALIBRATION_THRESHOLD
IS_CALIBRATED = False
MODEL_NAME = "Not loaded"


# ============================================================
# OPTIONAL DISTILBERT LOADING
# ============================================================
# We load DistilBERT as a fallback only.
# The calibrated TF-IDF model is the primary production model.
# ============================================================

if os.path.exists(DISTILBERT_DIR):
    try:
        import torch
        from transformers import (
            AutoTokenizer,
            AutoModelForSequenceClassification
        )

        threshold_config_path = os.path.join(
            DISTILBERT_DIR,
            "threshold_config.json"
        )

        if os.path.exists(threshold_config_path):
            with open(threshold_config_path, "r") as f:
                distilbert_config = json.load(f)

            _distilbert_threshold = distilbert_config.get(
                "final_threshold",
                0.05
            )
        else:
            _distilbert_threshold = 0.05

        _distilbert_tokenizer = AutoTokenizer.from_pretrained(
            DISTILBERT_DIR
        )

        _distilbert_model = (
            AutoModelForSequenceClassification
            .from_pretrained(DISTILBERT_DIR)
        )

        _distilbert_model.eval()

        _distilbert_available = True

        print(
            f"DistilBERT fallback loaded successfully "
            f"with threshold {_distilbert_threshold}"
        )

    except Exception as e:
        _distilbert_available = False

        print(
            "DistilBERT fallback could not be loaded. "
            f"Reason: {e}"
        )


# ============================================================
# PRIMARY MODEL: CALIBRATED TF-IDF + LOGISTIC REGRESSION
# ============================================================

if (
    os.path.exists(CALIBRATED_TFIDF_PATH)
    and os.path.exists(VECTORIZER_PATH)
):
    try:
        vectorizer = joblib.load(VECTORIZER_PATH)

        model = joblib.load(
            CALIBRATED_TFIDF_PATH
        )

        # Stage 2: Platt Scaling
        THRESHOLD = CALIBRATION_THRESHOLD

        IS_CALIBRATED = True

        MODEL_NAME = (
            "Calibrated TF-IDF + Logistic Regression "
            "(Platt Scaling)"
        )

        print(
            "\nLoaded PRIMARY production model:"
        )

        print(
            f"  Model     : {MODEL_NAME}"
        )

        print(
            f"  Threshold : {THRESHOLD}"
        )

        print(
            "  Probability type: Calibrated probability"
        )

    except Exception as e:
        print(
            "\nWARNING: Calibrated TF-IDF model exists "
            f"but could not be loaded.\nReason: {e}"
        )

        vectorizer = None
        model = None


# ============================================================
# FALLBACK 1: DISTILBERT
# ============================================================

if model is None and _distilbert_available:

    THRESHOLD = _distilbert_threshold

    IS_CALIBRATED = False

    MODEL_NAME = "DistilBERT Sequence Classifier"

    print(
        "\nUsing FALLBACK model:"
    )

    print(
        f"  Model     : {MODEL_NAME}"
    )

    print(
        f"  Threshold : {THRESHOLD}"
    )


# ============================================================
# FALLBACK 2: UNCALIBRATED TF-IDF
# ============================================================

if model is None and not _distilbert_available:

    if not os.path.exists(VECTORIZER_PATH):
        raise FileNotFoundError(
            f"TF-IDF vectorizer not found: "
            f"{VECTORIZER_PATH}"
        )

    if not os.path.exists(BASELINE_TFIDF_PATH):
        raise FileNotFoundError(
            f"Baseline TF-IDF model not found: "
            f"{BASELINE_TFIDF_PATH}"
        )

    vectorizer = joblib.load(
        VECTORIZER_PATH
    )

    model = joblib.load(
        BASELINE_TFIDF_PATH
    )

    THRESHOLD = 0.52

    IS_CALIBRATED = False

    MODEL_NAME = (
        "Uncalibrated TF-IDF + "
        "Logistic Regression Baseline"
    )

    print(
        "\nUsing FINAL FALLBACK model:"
    )

    print(
        f"  Model     : {MODEL_NAME}"
    )

    print(
        f"  Threshold : {THRESHOLD}"
    )


# ============================================================
# PREDICTION FUNCTION
# ============================================================

def predict_job(job_text: str):
    """
    Predict fraud risk for a job posting.

    Parameters
    ----------
    job_text : str
        Raw job posting text.

    Returns
    -------
    fraud_score : float
        Fraud probability/risk score.

        For the primary production model this is a
        Platt-calibrated probability.

    prediction : int
        1 = Fraudulent / High Risk
        0 = Legitimate / Low Risk
    """

    if not isinstance(job_text, str):
        raise TypeError(
            "job_text must be a string."
        )

    if not job_text.strip():
        raise ValueError(
            "job_text cannot be empty."
        )

    # --------------------------------------------------------
    # TEXT PREPROCESSING
    # --------------------------------------------------------

    job_text = normalize_text(job_text)

    # Remove common corporate boilerplate before
    # feature extraction to reduce feature dilution.
    job_text = clean_boilerplate(job_text)


    # --------------------------------------------------------
    # DISTILBERT FALLBACK
    # --------------------------------------------------------

    if (
        model is None
        and _distilbert_available
    ):
        import torch

        inputs = _distilbert_tokenizer(
            job_text,
            return_tensors="pt",
            truncation=True,
            max_length=256
        )

        with torch.no_grad():
            outputs = _distilbert_model(
                **inputs
            )

            probabilities = torch.softmax(
                outputs.logits,
                dim=1
            )

        fraud_score = float(
            probabilities[0][1].item()
        )


    # --------------------------------------------------------
    # TF-IDF MODEL
    # --------------------------------------------------------

    else:

        if vectorizer is None or model is None:
            raise RuntimeError(
                "No prediction model is available."
            )

        features = vectorizer.transform(
            [job_text]
        )

        fraud_score = float(
            model.predict_proba(features)[0][1]
        )


    # --------------------------------------------------------
    # FINAL DECISION
    # --------------------------------------------------------

    prediction = int(
        fraud_score >= THRESHOLD
    )

    return fraud_score, prediction


# ============================================================
# MODEL INFORMATION
# ============================================================

def get_model_info():
    """
    Return information about the currently active model.
    """

    return {
        "model": MODEL_NAME,
        "threshold": THRESHOLD,
        "is_calibrated": IS_CALIBRATED,
        "probability_type": (
            "calibrated_probability"
            if IS_CALIBRATED
            else "risk_score"
        )
    }


# ============================================================
# TEST / COMMAND-LINE EXECUTION
# ============================================================

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


    fraud_prob, pred = predict_job(
        test_job
    )


    model_info = get_model_info()


    print("\n==========================================")
    print("        JOBSHIELD TEST PREDICTION")
    print("==========================================")

    print(
        f"Model: {model_info['model']}"
    )

    print(
        f"Score/Probability: {fraud_prob:.4f}"
    )

    print(
        f"Probability Type: "
        f"{model_info['probability_type']}"
    )

    print(
        f"Calibrated: "
        f"{model_info['is_calibrated']}"
    )

    print(
        f"Threshold: "
        f"{model_info['threshold']}"
    )

    print(
        "Prediction:",
        (
            "FRAUDULENT / HIGH RISK"
            if pred == 1
            else
            "LEGITIMATE / LOW RISK"
        )
    )

    print("==========================================")
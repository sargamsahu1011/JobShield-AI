from ml.predict import predict_job
from ml.scam_signals import detect_scam_signals
from ml.evidence_extractor import extract_evidence
from ml.gemini_explainer import generate_explanation


def analyze_job(text: str) -> dict:
    """
    Run the complete JobShield AI analysis pipeline.

    The ML model makes the fraud prediction.
    Scam signals and evidence are extracted independently.
    Gemini only explains the detected evidence.
    """

    if not text or not text.strip():
        raise ValueError("Job posting text cannot be empty.")

    text = text.strip()

    # 1. ML prediction
    # predict_job() returns:
    # (fraud_probability, prediction)
    fraud_score, prediction = predict_job(text)

    fraud_score = float(fraud_score)
    prediction = int(prediction)

    # 2. Rule-based scam signal detection
    signals = detect_scam_signals(text)

    # 3. Evidence extraction
    evidence = extract_evidence(text)

    # 4. Gemini explanation
    explanation = generate_explanation(
        fraud_score=fraud_score,
        signals=signals,
        evidence=evidence
    )

    return {
        "fraud_score": fraud_score,
        "prediction": prediction,
        "signals": signals,
        "evidence": evidence,
        "explanation": explanation
    }
from ml.predict import predict_job, IS_CALIBRATED, MODEL_NAME
from ml.scam_signals import detect_scam_signals
from ml.evidence_extractor import extract_evidence
from ml.gemini_explainer import generate_explanation
from ml.input_validator import validate_and_sanitize_input, InputValidationError


def analyze_job(text: any, include_explanation: bool = True) -> dict:
    """
    Run the complete JobShield AI analysis pipeline with security hardening:
    1. Input validation & sanitization (length caps, null bytes, encoding, type checks)
    2. ML model prediction with calibrated probabilities
    3. Rule-based scam signal detection
    4. Defensive rule-ensemble signal-floor veto
    5. Structured evidence extraction
    6. Guardrailed Gemini explanation (untrusted evidence sanitization, system-level directives)
    """

    # 1. Pipeline entry validation & sanitization
    sanitized_text, validation_meta = validate_and_sanitize_input(text)

    # 2. ML prediction
    # predict_job() returns:
    # (fraud_score, prediction)
    fraud_score, prediction = predict_job(sanitized_text)

    fraud_score = float(fraud_score)
    prediction = int(prediction)

    # 3. Rule-based scam signal detection
    signals = detect_scam_signals(sanitized_text)

    # 4. Defensive Rule-Ensemble Signal-Floor Veto (Strategy D)
    is_severe_demand = signals.get("payment_request", False) or signals.get("sensitive_data_request", False)
    has_unverified_channel = (
        signals.get("telegram_contact", False)
        or signals.get("whatsapp_contact", False)
        or signals.get("personal_email", False)
    )
    is_telegram_urgency = signals.get("telegram_contact", False) and signals.get("urgency_language", False)

    signal_veto_triggered = (is_severe_demand and has_unverified_channel) or is_telegram_urgency

    if signal_veto_triggered:
        # Enforce minimum risk floor of 0.70 and classify as Fraudulent
        fraud_score = max(fraud_score, 0.70)
        prediction = 1

    # 5. Evidence extraction
    evidence = extract_evidence(sanitized_text)

    # 6. Gemini explanation with strict guardrails
    explanation = None
    injections_detected = []
    if include_explanation:
        explanation, injections_detected = generate_explanation(
            fraud_score=fraud_score,
            signals=signals,
            evidence=evidence,
            prediction=prediction
        )

    return {
        "fraud_score": fraud_score,
        "prediction": prediction,
        "signals": signals,
        "evidence": evidence,
        "explanation": explanation,
        "is_calibrated": IS_CALIBRATED,
        "model_name": MODEL_NAME,
        "signal_veto_triggered": signal_veto_triggered,
        "input_validation": validation_meta,
        "adversarial_injections_detected": injections_detected
    }
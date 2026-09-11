import streamlit as st

from ml.jobshield_pipeline import analyze_job


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="JobShield AI",
    page_icon="🛡️",
    layout="wide"
)


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.title("🛡️ JobShield AI")

st.markdown(
    """
    **Evidence-Grounded Recruitment Scam Detection**

    Analyze a job posting for potential recruitment scam indicators
    using machine learning, rule-based evidence extraction, and
    evidence-grounded AI explanations.
    """
)

st.divider()


# ---------------------------------------------------------
# Input
# ---------------------------------------------------------

st.subheader("Analyze a Job Posting")

job_text = st.text_area(
    "Paste the complete job posting below",
    height=350,
    placeholder=(
        "Paste the job title, company information, description, "
        "requirements, benefits, contact information, etc."
    )
)


# ---------------------------------------------------------
# Analysis
# ---------------------------------------------------------

if st.button("🔍 Analyze Job Posting", type="primary"):

    if not job_text.strip():
        st.warning("Please paste a job posting before analyzing.")
        st.stop()

    with st.spinner("Analyzing job posting..."):
        try:
            result = analyze_job(job_text)

        except Exception as e:
            st.error(f"Analysis failed: {e}")
            st.stop()


    fraud_score = result["fraud_score"]
    prediction = result["prediction"]
    signals = result["signals"]
    evidence = result["evidence"]
    explanation = result["explanation"]
    is_calibrated = result.get("is_calibrated", False)
    model_name = result.get("model_name", "Classifier")


    # -----------------------------------------------------
    # Prediction
    # -----------------------------------------------------

    st.divider()
    st.subheader("Analysis Result")

    col1, col2, col3 = st.columns(3)

    with col1:
        if is_calibrated:
            st.metric(
                "Calibrated Fraud Probability",
                f"{fraud_score:.2%}"
            )
        else:
            st.metric(
                "Uncalibrated Fraud Score",
                f"{fraud_score:.4f}"
            )

    with col2:
        if prediction == 1:
            st.metric(
                "Prediction",
                "Fraudulent"
            )
        else:
            st.metric(
                "Prediction",
                "Legitimate"
            )

    with col3:
        detected_count = sum(
            1 for detected in signals.values()
            if detected
        )

        st.metric(
            "Scam Signals",
            detected_count
        )


    # -----------------------------------------------------
    # Risk indication
    # -----------------------------------------------------

    if prediction == 1:
        st.error(
            "⚠️ HIGH RISK — The classifier predicts this posting "
            "as fraudulent."
        )
    else:
        st.success(
            "✓ LOWER RISK — The classifier predicts this posting "
            "as legitimate."
        )

    if is_calibrated:
        st.caption(
            f"**Probability Semantics**: The probability above is calibrated using Platt scaling "
            f"(sigmoid calibration on holdout validation data; Test Brier score: 0.0107, Test ECE: 0.0082). "
            f"Model: {model_name}."
        )
    else:
        st.caption(
            "**Risk Score Semantics**: The score above is an uncalibrated raw model output and is "
            "NOT a calibrated empirical probability. The prediction uses the classifier's decision threshold."
        )


    # -----------------------------------------------------
    # Detected signals
    # -----------------------------------------------------

    st.divider()
    st.subheader("🚩 Detected Scam Signals")

    detected_signals = [
        signal.replace("_", " ").title()
        for signal, detected in signals.items()
        if detected
    ]

    if detected_signals:
        for signal in detected_signals:
            st.warning(f"• {signal}")
    else:
        st.success("No predefined scam signals were detected.")


    # -----------------------------------------------------
    # Evidence
    # -----------------------------------------------------

    st.divider()
    st.subheader("🔎 Evidence Extracted from the Job Posting")

    if evidence:

        for signal, sentences in evidence.items():

            st.markdown(
                f"**{signal.replace('_', ' ').title()}**"
            )

            for sentence in sentences:
                st.info(f'“{sentence}”')

    else:
        st.info(
            "No specific evidence snippets were extracted."
        )


    # -----------------------------------------------------
    # Gemini explanation
    # -----------------------------------------------------

    st.divider()
    st.subheader("🤖 AI Explanation")

    if explanation:
        st.markdown(explanation)
    else:
        st.info("No explanation was generated.")


    # -----------------------------------------------------
    # Safety recommendation
    # -----------------------------------------------------

    st.divider()
    st.subheader("🛡️ Safety Reminder")

    st.markdown(
        """
        - Never pay a registration, processing, or application fee to obtain a job.
        - Do not share passwords, OTPs, banking credentials, or unnecessary identity information.
        - Verify the company and job posting through trusted official sources.
        - Treat this result as decision-support, not as definitive proof that a job is fraudulent.
        """
    )


# ---------------------------------------------------------
# Disclaimer
# ---------------------------------------------------------

st.divider()

st.caption(
    "JobShield AI is a research and decision-support system. "
    "Predictions may contain false positives or false negatives. "
    "Always independently verify employers and job opportunities."
)
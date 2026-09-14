import sys
from pathlib import Path

import streamlit as st

# Add project root to Python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from ml.jobshield_pipeline import analyze_job


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="JobShield AI — Recruitment Scam Detection",
    page_icon="🛡️",
    layout="wide"
)


# ---------------------------------------------------------
# Header & Purpose
# ---------------------------------------------------------

st.title("🛡️ JobShield AI")

st.markdown(
    """
    **Evidence-Grounded Recruitment Scam Detection & Decision-Support System**

    Screen job postings for deceptive recruitment practices using calibrated machine learning,
    rule-based evidence extraction, and evidence-grounded AI explanations.
    """
)

st.info(
    "⚠️ **Decision-Support Notice**: JobShield AI provides probabilistic risk indicators to assist human review. "
    "Predictions are not definitive proof of fraud or legitimacy. Always conduct independent employer verification."
)

st.divider()


# ---------------------------------------------------------
# Input
# ---------------------------------------------------------

st.subheader("1. Job Posting Input")

job_text = st.text_area(
    "Paste the complete job posting text below (Title, Company, Description, Requirements, Benefits, Contact):",
    height=300,
    placeholder=(
        "Paste the job posting content here...\n\n"
        "Example:\n"
        "Title: Remote Data Entry Assistant\n"
        "Company: Example Corp\n"
        "Description: Earn $4000/week from home. No experience needed. Pay $100 registration fee to begin.\n"
        "Contact: Reach recruiter on Telegram @example_hire"
    )
)


# ---------------------------------------------------------
# Analysis Action
# ---------------------------------------------------------

if st.button("🔍 Analyze Job Posting", type="primary", use_container_width=True):

    if not job_text.strip():
        st.warning("Please paste a job posting before analyzing.")
        st.stop()

    with st.spinner("Screening job posting through calibrated ML pipeline and evidence extraction..."):
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
    threshold = result.get("threshold", 0.54)
    model_name = result.get("model_name", "Calibrated Classifier")

    # -----------------------------------------------------
    # Analysis Metrics
    # -----------------------------------------------------

    st.divider()
    st.subheader("2. Risk Assessment & Prediction")

    m_col1, m_col2, m_col3, m_col4 = st.columns(4)

    with m_col1:
        if is_calibrated:
            st.metric(
                label="Risk Probability",
                value=f"{fraud_score:.2%}",
                help="Empirically calibrated probability of fraud via Platt scaling"
            )
        else:
            st.metric(
                label="Risk Score (Uncalibrated)",
                value=f"{fraud_score:.4f}",
                help="Raw model output score"
            )

    with m_col2:
        if prediction == 1:
            st.metric(
                label="Prediction Verdict",
                value="HIGH RISK / FRAUDULENT"
            )
        else:
            st.metric(
                label="Prediction Verdict",
                value="LOW RISK / LIKELY LEGITIMATE"
            )

    with m_col3:
        st.metric(
            label="Threshold Used",
            value=f"{threshold:.2%}",
            help="Decision boundary selected on validation split for optimal F1"
        )

    with m_col4:
        st.metric(
            label="Probability Calibrated",
            value="Yes (Platt Scaling)" if is_calibrated else "No (Raw Score)",
            help="Platt scaling fitted on holdout validation data"
        )

    # -----------------------------------------------------
    # Risk Indication Banner
    # -----------------------------------------------------

    if prediction == 1:
        st.error(
            f"⚠️ **HIGH RISK / FRAUDULENT**: This job posting has been flagged with an elevated fraud probability "
            f"({fraud_score:.2%}) meeting or exceeding the production decision threshold of {threshold:.2%}."
        )
    else:
        st.success(
            f"✅ **LOW RISK / LIKELY LEGITIMATE**: The model predicts this posting is below the fraud threshold "
            f"({fraud_score:.2%} < {threshold:.2%}). No critical scam patterns were triggered."
        )

    # -----------------------------------------------------
    # Detected Signals
    # -----------------------------------------------------

    st.divider()
    st.subheader("3. Detected Scam Signals & Indicators")

    detected_signals = [
        signal.replace("_", " ").title()
        for signal, detected in signals.items()
        if detected
    ]

    if detected_signals:
        st.write(f"The rule-ensemble detected **{len(detected_signals)}** potential risk indicator(s):")
        cols = st.columns(min(len(detected_signals), 3))
        for idx, signal in enumerate(detected_signals):
            with cols[idx % len(cols)]:
                st.warning(f"🚩 **{signal}**")
    else:
        st.success("✓ No explicit heuristic scam signals (fees, personal messengers, sensitive data requests) detected.")

    # -----------------------------------------------------
    # Extracted Evidence
    # -----------------------------------------------------

    st.divider()
    st.subheader("4. Extracted Evidence from Posting")

    if evidence:
        for signal_key, sentences in evidence.items():
            st.markdown(f"**Evidence for {signal_key.replace('_', ' ').title()}**:")
            for sentence in sentences:
                st.info(f"“{sentence}”")
    else:
        st.caption("No specific verbatim risk sentences were isolated for extraction.")

    # -----------------------------------------------------
    # AI Explanation
    # -----------------------------------------------------

    st.divider()
    st.subheader("5. AI Explanation & Safety Guidance")

    if explanation:
        st.markdown(explanation)
    else:
        st.caption("AI explanation not available.")

    # -----------------------------------------------------
    # Safety Recommendations
    # -----------------------------------------------------

    st.divider()
    st.subheader("6. Job Seeker Safety Guidelines")

    st.markdown(
        """
        - **Never Pay to Work:** Legitimate employers never charge application, registration, processing, or background-check fees.
        - **Keep Communications Official:** Beware of employers insisting on Telegram, WhatsApp, or personal Gmail accounts.
        - **Protect Identity & Finances:** Never provide bank account details, credit cards, or Social Security / ID numbers prior to formal written employment offers.
        - **Verify Independently:** Check the employer's official website, verifiable phone directory, and registered domain.
        """
    )


# ---------------------------------------------------------
# Footer & Legal Disclaimer
# ---------------------------------------------------------

st.divider()

st.caption(
    "**JobShield AI Decision-Support Disclaimer**: This tool is an automated decision-support aid based on linguistic "
    "patterns and machine learning models trained on the EMSCAD benchmark dataset. It does NOT guarantee 100% scam detection "
    "accuracy (current test recall: 80.37%) and is NOT a legal determination of fraud. Users and organizations must conduct independent "
    "verification before making employment or platform enforcement decisions."
)
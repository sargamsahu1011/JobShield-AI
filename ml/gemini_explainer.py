import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


def generate_explanation(fraud_score, signals, evidence):

    detected_signals = [
        signal.replace("_", " ")
        for signal, detected in signals.items()
        if detected
    ]

    evidence_text = ""

    for signal, sentences in evidence.items():
        evidence_text += f"\n{signal.replace('_', ' ').title()}:\n"

        for sentence in sentences:
            evidence_text += f"- {sentence}\n"

    prompt = f"""
You are the explanation component of JobShield AI.

Your ONLY job is to explain the evidence already detected by
the JobShield AI system.

STRICT RULES:
1. You are NOT the fraud detector.
2. Do NOT change the fraud prediction.
3. Use ONLY the evidence explicitly provided below.
4. NEVER invent suspicious behavior, facts, URLs, company information,
   financial claims, or other evidence.
5. If evidence is not provided for a claim, DO NOT mention that claim.
6. Do not assume that a communication method is automatically fraudulent.
7. Do not treat the presence of WhatsApp, Telegram, personal email, urgency,
   or any other signal as proof of fraud by itself.
8. Describe detected signals neutrally unless the evidence explicitly indicates
   a harmful or suspicious action.
9. Clearly distinguish between "detected evidence" and general safety advice.
10. Keep the explanation concise and understandable.

Fraud score: {fraud_score:.4f}

Detected scam signals:
{", ".join(detected_signals) if detected_signals else "None"}

Evidence extracted directly from the job posting:
{evidence_text if evidence_text else "No specific evidence extracted."}

Write exactly these sections:

Why this job may be risky:
- Explain ONLY the detected evidence.
- Mention the actual suspicious text when useful.

What you should do:
- Give 2-3 practical safety recommendations.
- Do not claim that the job is definitely a scam.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text
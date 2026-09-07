import re


SIGNAL_PATTERNS = {
    "payment_request": [
        r"registration fee",
        r"processing fee",
        r"application fee",
        r"pay.*fee",
        r"payment.*required",
        r"deposit.*money",
        r"pay.*amount"
    ],

    "telegram_contact": [
        r"\btelegram\b",
        r"t\.me/"
    ],

    "whatsapp_contact": [
        r"\bwhatsapp\b",
        r"wa\.me/"
    ],

    "personal_email": [
        r"[a-zA-Z0-9._%+-]+@(gmail|yahoo|hotmail|outlook)\.(com|in|co)"
    ],

    "sensitive_data_request": [
        r"bank account",
        r"bank details",
        r"credit card",
        r"debit card",
        r"\botp\b",
        r"aadhaar",
        r"passport",
        r"social security",
        r"pan card"
    ],

    "urgency_language": [
        r"apply now",
        r"urgent",
        r"immediately",
        r"limited seats",
        r"act now",
        r"last chance",
        r"join today"
    ],

    "guaranteed_job": [
        r"guaranteed job",
        r"100% job",
        r"guaranteed placement",
        r"job guaranteed",
        r"assured job"
    ],

    "no_experience_required": [
        r"no experience required",
        r"no experience needed",
        r"anyone can apply"
    ],

    "crypto_request": [
        r"bitcoin",
        r"crypto",
        r"cryptocurrency",
        r"usdt",
        r"ethereum"
    ],

    "suspicious_url": [
        r"https?://(bit\.ly|tinyurl|t\.co|goo\.gl)"
    ]
}


def extract_evidence(text):
    """
    Extract actual sentences from a job posting
    that triggered scam signals.
    """

    # Convert line breaks into spaces so sentences aren't cut incorrectly
    cleaned_text = " ".join(text.splitlines()).strip()

    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', cleaned_text)

    evidence = {}

    for signal, patterns in SIGNAL_PATTERNS.items():

        matched_sentences = []

        for sentence in sentences:

            sentence = sentence.strip()

            if not sentence:
                continue

            sentence_lower = sentence.lower()

            if any(
                re.search(pattern, sentence_lower)
                for pattern in patterns
            ):
                matched_sentences.append(sentence)

        if matched_sentences:
            evidence[signal] = matched_sentences

    return evidence


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    test_job = """
    Work from home opportunity.
    Earn ₹80,000 per month.
    No experience required.
    Pay ₹1,500 registration fee.
    Contact us on Telegram immediately.
    """

    result = extract_evidence(test_job)

    print("\nEXTRACTED SCAM EVIDENCE")
    print("-" * 50)

    for signal, sentences in result.items():

        print(f"\n[!] {signal}")

        for sentence in sentences:
            print(f"    → {sentence}")
import re


def detect_scam_signals(text):

    text_lower = text.lower()

    signals = {}

    # 1. Payment request
    payment_patterns = [
        r"registration fee",
        r"processing fee",
        r"application fee",
        r"pay.*fee",
        r"payment.*required",
        r"deposit.*money",
        r"pay.*amount"
    ]

    signals["payment_request"] = any(
        re.search(pattern, text_lower)
        for pattern in payment_patterns
    )

    # 2. Telegram
    signals["telegram_contact"] = bool(
        re.search(r"\btelegram\b|t\.me/", text_lower)
    )

    # 3. WhatsApp
    signals["whatsapp_contact"] = bool(
        re.search(r"\bwhatsapp\b|wa\.me/", text_lower)
    )

    # 4. Personal email
    signals["personal_email"] = bool(
        re.search(
            r"[a-zA-Z0-9._%+-]+@(gmail|yahoo|hotmail|outlook)\.(com|in|co)",
            text_lower
        )
    )

    # 5. Sensitive information
    sensitive_patterns = [
        r"bank account",
        r"bank details",
        r"credit card",
        r"debit card",
        r"otp",
        r"aadhaar",
        r"passport",
        r"social security",
        r"pan card"
    ]

    signals["sensitive_data_request"] = any(
        re.search(pattern, text_lower)
        for pattern in sensitive_patterns
    )

    # 6. Urgency
    urgency_patterns = [
        r"apply now",
        r"urgent",
        r"immediately",
        r"limited seats",
        r"act now",
        r"last chance",
        r"join today"
    ]

    signals["urgency_language"] = any(
        re.search(pattern, text_lower)
        for pattern in urgency_patterns
    )

    # 7. Guaranteed job
    guaranteed_patterns = [
        r"guaranteed job",
        r"100% job",
        r"guaranteed placement",
        r"job guaranteed",
        r"assured job"
    ]

    signals["guaranteed_job"] = any(
        re.search(pattern, text_lower)
        for pattern in guaranteed_patterns
    )

    # 8. No experience
    signals["no_experience_required"] = bool(
        re.search(
            r"no experience required|no experience needed|anyone can apply",
            text_lower
        )
    )

    # 9. Crypto
    crypto_patterns = [
        r"bitcoin",
        r"crypto",
        r"cryptocurrency",
        r"usdt",
        r"ethereum"
    ]

    signals["crypto_request"] = any(
        re.search(pattern, text_lower)
        for pattern in crypto_patterns
    )

    # 10. Suspicious URL
    signals["suspicious_url"] = bool(
        re.search(
            r"https?://(bit\.ly|tinyurl|t\.co|goo\.gl)",
            text_lower
        )
    )

    return signals


if __name__ == "__main__":

    test_job = """
    Work from home opportunity.
    Earn ₹80,000 per month.
    No experience required.
    Pay ₹1,500 registration fee.
    Contact us on Telegram immediately.
    """

    result = detect_scam_signals(test_job)

    print("\nSCAM SIGNALS")
    print("-" * 40)

    for signal, detected in result.items():
        if detected:
            print(f"[!] {signal}")
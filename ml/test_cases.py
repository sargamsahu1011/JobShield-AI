from predict import predict_job
from scam_signals import detect_scam_signals
from evidence_extractor import extract_evidence


TEST_CASES = {

    "LEGITIMATE TECH JOB": """
    Software Engineer

    We are looking for a Software Engineer to join our development team.

    Responsibilities:
    - Develop and maintain web applications.
    - Work with engineers and product managers.
    - Write clean and maintainable code.

    Requirements:
    - Bachelor's degree in Computer Science or related field.
    - Experience with Python or Java.
    - Good problem-solving skills.

    Benefits:
    - Competitive salary.
    - Health insurance.
    - Paid leave.
    """,

    "OBVIOUS SCAM": """
    Work From Home Job!

    Earn ₹80,000 per month with no experience required.
    Pay ₹1,500 registration fee to secure your position.
    Contact us on Telegram immediately.
    Limited seats available. Apply now!
    """,

    "SUBTLE SCAM": """
    Online Data Entry Executive

    Earn up to ₹50,000 per month working from home.
    No prior experience required.

    Selected candidates must complete a small verification
    process before joining.

    Contact our recruitment manager through WhatsApp for
    further details.
    """,

    "LEGITIMATE REMOTE JOB": """
    Machine Learning Intern

    We are looking for a motivated Machine Learning Intern
    to work with our AI engineering team.

    Responsibilities:
    - Assist with data preprocessing and model development.
    - Conduct experiments and document results.
    - Collaborate with senior ML engineers.

    Requirements:
    - Python programming knowledge.
    - Basic understanding of machine learning.
    - Currently pursuing a degree in Computer Science,
      Data Science, or a related field.

    This is a paid internship with a three-month duration.
    Applications should be submitted through our official
    company careers portal.
    """,

    "SENSITIVE INFORMATION SCAM": """
    Customer Support Representative

    Work from home and earn ₹45,000 per month.

    To complete your employment verification, send us your
    bank account details, OTP and Aadhaar number.

    Send the information immediately to complete your joining.
    """
}


for name, job_text in TEST_CASES.items():

    print("\n" + "=" * 70)
    print(name)
    print("=" * 70)

    fraud_score, prediction = predict_job(job_text)

    signals = detect_scam_signals(job_text)

    evidence = extract_evidence(job_text)

    print(f"\nFraud Score: {fraud_score:.4f}")

    if prediction == 1:
        print("Prediction: FRAUDULENT / HIGH RISK")
    else:
        print("Prediction: LEGITIMATE / LOW RISK")

    print("\nDetected Signals:")

    detected = False

    for signal, value in signals.items():
        if value:
            print(f"  [!] {signal}")
            detected = True

    if not detected:
        print("  None")

    print("\nEvidence:")

    if evidence:
        for signal, sentences in evidence.items():
            print(f"\n  {signal}:")
            for sentence in sentences:
                print(f"    → {sentence}")
    else:
        print("  None")
"""JobShield AI — Canonical Protected Regression Test Suite

This file is the single, authoritative source of truth for the five protected
regression tests.

Protected Tests:
1. Obvious scam (Fraudulent, expected ~0.9987; signals: payment_request, telegram_contact, urgency_language, no_experience_required)
2. Legitimate internship (Legitimate, expected ~0.0018; signals: None)
3. Legitimate job with WhatsApp (Legitimate, expected ~0.0013; signals: whatsapp_contact ONLY — must NOT trip veto-floor)
4. Legitimate, high salary + no experience (Legitimate, expected ~0.0035; documents no_experience_required regex gap)
5. Sophisticated scam (Fraudulent, expected ~0.9943; signals: telegram_contact, sensitive_data_request, urgency_language; NO payment_request)
"""

CANONICAL_PROTECTED_TESTS = {
    "Obvious scam": {
        "text": """Work From Home Data Entry Assistant!
Earn $4,500 every week with no experience required.
All equipment will be provided.
To secure your position, submit a $150 registration fee via wire transfer or gift cards.
Contact our hiring manager immediately on Telegram: @quick_career_support.
Hurry, only 2 positions remaining! Apply now!""",
        "expected_prediction": "FRAUDULENT",
        "expected_prob_range": (0.95, 1.0),
        "expected_approx_prob": 0.9987,
        "expected_signals": ["payment_request", "telegram_contact", "urgency_language", "no_experience_required"],
        "forbidden_signals": [],
        "description": "Standard obvious scam with fee, off-platform Telegram, high urgency, and no experience hook."
    },
    "Legitimate internship": {
        "text": """Machine Learning Research Intern
We are seeking a summer Machine Learning Research Intern to join our NLP engineering group.

Responsibilities:
- Collaborate with research scientists to implement baseline transformer models.
- Assist in data cleaning, evaluation scripting, and statistical significance testing.
- Document experimental methodologies and present findings at internal lab meetings.

Qualifications:
- Currently enrolled in a B.S., M.S., or Ph.D. program in Computer Science, Statistics, or related field.
- Working proficiency in Python and familiarity with PyTorch or JAX.
- Solid foundational understanding of linear algebra and probability.

Benefits:
- Competitive hourly compensation ($45/hr).
- Mentorship from senior research scientists.
- Office lunch stipend and transit pass.

Applications must be submitted exclusively through our official corporate careers portal at https://careers.example-tech.com/jobs/ml-intern-2026.""",
        "expected_prediction": "LEGITIMATE",
        "expected_prob_range": (0.0, 0.05),
        "expected_approx_prob": 0.0018,
        "expected_signals": [],
        "forbidden_signals": ["payment_request", "telegram_contact", "whatsapp_contact", "sensitive_data_request"],
        "description": "Clean, legitimate university internship with zero scam signals."
    },
    "Legitimate job with WhatsApp": {
        "text": """Customer Logistics Field Supervisor (Latin America Region)
Global Freight Solutions is hiring an on-site Logistics Field Supervisor based in Miami, FL to coordinate regional transport routes.

Key Responsibilities:
- Oversee day-to-day dispatch communication with regional trucking partners.
- Resolve supply chain bottlenecks and track delivery milestones.
- Coordinate with bilingual cross-border carriers across North and South America.

Requirements:
- 3+ years experience in freight forwarding, fleet dispatch, or transport operations.
- Fluent in English and Spanish.
- Strong organizational and crisis-management abilities.

Compensation:
- Annual base salary: $68,000 - $75,000 depending on experience.
- Full medical, dental, and 401(k) matching.

For expedited initial dispatch coordination queries, contact our regional operations recruiter via WhatsApp at wa.me/13055550189. Formal applications and CVs must be submitted via our official site.""",
        "expected_prediction": "LEGITIMATE",
        "expected_prob_range": (0.0, 0.05),
        "expected_approx_prob": 0.0013,
        "expected_signals": ["whatsapp_contact"],
        "forbidden_signals": ["payment_request", "sensitive_data_request", "telegram_contact"],
        "must_not_trigger_veto": True,
        "description": "Legitimate enterprise posting utilizing WhatsApp strictly for recruiter routing. Must NOT trip veto floor."
    },
    "Legitimate, high salary + no experience": {
        "text": """Junior Executive Sales Trainee — Real Estate Development
Prestige Properties Group is launching our annual Executive Sales Trainee cohort in Chicago, IL.

Position Overview:
We train ambitious individuals from the ground up to represent multi-million-dollar commercial and luxury residential properties.
No prior professional experience is required — comprehensive 12-week paid corporate mentorship provided.

What We Offer:
- First-year target compensation: $120,000 - $140,000 ($60,000 guaranteed base + uncapped performance commissions).
- Comprehensive health, dental, and life insurance.
- Continuous leadership development program.

Requirements:
- Bachelor's degree preferred or equivalent military/customer-facing background.
- Exceptional verbal communication, persistence, and coachability.
- Valid driver's license.

To apply, please submit your resume through LinkedIn or our official careers portal.""",
        "expected_prediction": "LEGITIMATE",
        "expected_prob_range": (0.0, 0.05),
        "expected_approx_prob": 0.0035,
        "expected_signals": [],
        "regex_gap_notes": "Note: regex tests 'no experience required' exactly. Text says 'No prior professional experience is required'. Documents the known phrasing gap.",
        "description": "High-paying legitimate trainee posting with 'No prior professional experience is required'. Documents regex gap."
    },
    "Sophisticated scam": {
        "text": """Executive Communications Specialist — Global Strategy Office
International Advisory Partners seeks a remote Executive Communications Specialist to support C-suite executive briefings.

Role & Responsibilities:
- Draft confidential executive summaries, speech materials, and internal corporate advisories.
- Manage sensitive stakeholder communication across European and Asian market divisions.
- Maintain utmost discretion handling proprietary strategic agendas.

Requirements:
- Proven written fluency in corporate affairs or business journalism.
- Ability to synthesize high-level strategic intelligence under tight turnarounds.

Immediate Onboarding Procedure:
Due to high application volume, our executive assessment team is conducting onboarding screenings immediately.
Candidates must connect with our Senior Partner on Telegram at https://t.me/IAP_Executive_Advisory.
To issue your security credentials and secure corporate laptop, you must provide your SSN, banking verification routing, and national ID document scan within 24 hours. Failure to submit immediately will result in disqualification.""",
        "expected_prediction": "FRAUDULENT",
        "expected_prob_range": (0.95, 1.0),
        "expected_approx_prob": 0.9943,
        "expected_signals": ["telegram_contact", "sensitive_data_request", "urgency_language"],
        "forbidden_signals": ["payment_request"],
        "description": "Sophisticated phishing scam requesting sensitive credentials via Telegram with urgent deadlines; NO payment_request."
    }
}

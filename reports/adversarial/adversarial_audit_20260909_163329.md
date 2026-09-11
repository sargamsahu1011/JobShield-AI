# JobShield AI — Adversarial Robustness Audit Report
**Generated:** 2026-09-09 16:33:29 UTC  
**Target Model:** `TF-IDF + Logistic Regression Baseline`  
**Samples Evaluated:** 5 distinct postings (40 attack variants)  

## 1. Executive Summary
- **Overall Attack Success Rate (ASR):** `16.7%` (4/24 fraudulent postings evaded detection)
- **Pre-Attack Fraud Detection Rate:** `60.0%`
- **Post-Attack Fraud Detection Rate:** `50.0%` (Absolute drop: `10.0%`)
- **Mean Fraud Score Degradation:** `-0.0623`
- **Maximum Observed Score Suppression:** `0.5280`
- **Rule-Based Heuristic Dropout Rate:** `25.0%` of scam regex signals vanished under attack

## 2. Vulnerability Breakdown by Attack Category
| Attack Type | Evaluated | Orig Fraud | Flips | ASR (%) | Pre-Det (%) | Post-Det (%) | Mean Δ Score | Max Δ Score | Signal Drop (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `benign_camouflage` | 5 | 3 | 3 | **100.0%** | 60.0% | 0.0% | +0.2903 | 0.5079 | 0.0% |
| `unicode_homoglyphs` | 5 | 3 | 1 | **33.3%** | 60.0% | 40.0% | +0.1315 | 0.5280 | 85.7% |
| `typos` | 5 | 3 | 0 | **0.0%** | 60.0% | 60.0% | +0.0303 | 0.0969 | 0.0% |
| `zero_width` | 5 | 3 | 0 | **0.0%** | 60.0% | 60.0% | -0.0001 | 0.0225 | 14.3% |
| `leetspeak` | 5 | 3 | 0 | **0.0%** | 60.0% | 60.0% | +0.0222 | 0.1320 | 42.9% |
| `obfuscated_contacts` | 5 | 3 | 0 | **0.0%** | 60.0% | 60.0% | -0.0042 | 0.0098 | 28.6% |
| `obfuscated_keywords` | 5 | 3 | 0 | **0.0%** | 60.0% | 60.0% | +0.0266 | 0.1332 | 28.6% |
| `sentence_restructuring` | 5 | 3 | 0 | **0.0%** | 60.0% | 60.0% | +0.0017 | 0.0083 | 0.0% |

## 3. Top Evasion Cases (Fraud $\to$ Legitimate Flips)
### Flip Example 1: `unicode_homoglyphs` (Sample: `regression_OBVIOUS SCAM`)
- **Score Shift:** `0.8518` (Fraudulent) $\longrightarrow$ `0.3237` (Legitimate) [Δ `0.5280`]
- **Dropped Signals:** `no_experience_required, payment_request, telegram_contact, urgency_language`
- **Original Excerpt:**
  > *"Work From Home Job!



    Earn ₹80,000 per month with no experience required.

    Pay ₹1,500 registration fee to secure your position.

    Contact us on Telegram immediately...."*
- **Attacked Excerpt:**
  > *"Work Frоm Ноme Job!



    Eаrn ₹80,000 pеr mоnth with nо еxpеrienсe requіrеd.

    Pау ₹1,500 rеgistration fee to secure yоur роѕіtіоn.

    Contaсt uѕ on Telеgram іmmediately...."*

### Flip Example 2: `benign_camouflage` (Sample: `regression_OBVIOUS SCAM`)
- **Score Shift:** `0.8518` (Fraudulent) $\longrightarrow$ `0.3439` (Legitimate) [Δ `0.5079`]
- **Dropped Signals:** `None`
- **Original Excerpt:**
  > *"Work From Home Job!



    Earn ₹80,000 per month with no experience required.

    Pay ₹1,500 registration fee to secure your position.

    Contact us on Telegram immediately...."*
- **Attacked Excerpt:**
  > *"Equal Opportunity Employer: We are committed to fostering an inclusive and diverse work environment. All qualified applicants will receive consideration for employment without rega..."*

### Flip Example 3: `benign_camouflage` (Sample: `regression_SUBTLE SCAM`)
- **Score Shift:** `0.7443` (Fraudulent) $\longrightarrow$ `0.3051` (Legitimate) [Δ `0.4392`]
- **Dropped Signals:** `None`
- **Original Excerpt:**
  > *"Online Data Entry Executive



    Earn up to ₹50,000 per month working from home.

    No prior experience required.



    Selected candidates must complete a small verification..."*
- **Attacked Excerpt:**
  > *"Equal Opportunity Employer: We are committed to fostering an inclusive and diverse work environment. All qualified applicants will receive consideration for employment without rega..."*

### Flip Example 4: `benign_camouflage` (Sample: `regression_SENSITIVE INFORMATION SCAM`)
- **Score Shift:** `0.6594` (Fraudulent) $\longrightarrow$ `0.2828` (Legitimate) [Δ `0.3766`]
- **Dropped Signals:** `None`
- **Original Excerpt:**
  > *"Customer Support Representative



    Work from home and earn ₹45,000 per month.



    To complete your employment verification, send us your

    bank account details, OTP and A..."*
- **Attacked Excerpt:**
  > *"Equal Opportunity Employer: We are committed to fostering an inclusive and diverse work environment. All qualified applicants will receive consideration for employment without rega..."*

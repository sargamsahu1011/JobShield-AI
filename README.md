# 🛡️ JobShield AI — Evidence-Grounded Recruitment Scam Detection

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![scikit-learn](https://img.shields.io/badge/ML-scikit--learn-F7931E.svg)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**JobShield AI** is a machine-learning-powered recruitment scam detection system that analyzes job postings for fraudulent patterns, produces a calibrated risk score, identifies specific scam signals, and generates evidence-grounded explanations.

The system combines a **TF-IDF + Logistic Regression classifier**, rule-based scam-signal detection, input-security defenses, and an **LLM explanation layer** to provide transparent decision support for job seekers and recruitment analysts.

> **JobShield AI is a decision-support system, not definitive proof that a job posting is fraudulent.**

---

## ⭐ Key Results

| Metric          | Clean Test Performance |
| --------------- | ---------------------: |
| **Precision**   |             **96.63%** |
| **Recall**      |             **80.37%** |
| **F1-Score**    |             **87.76%** |
| **PR-AUC**      |             **90.96%** |
| **ROC-AUC**     |             **98.65%** |
| **Brier Score** |             **0.0124** |
| **ECE**         |             **0.0076** |

**Clean independent test set:** 1,736 job postings

**Prompt-injection security tests:** 8/8 passed  
**Regression tests:** 8/8 passed  
**Adversarial robustness:** 6/9 attacks detected

---

## 🎯 Problem

Online recruitment scams increasingly imitate legitimate job advertisements while attempting to:

- Request upfront payments or "verification" fees
- Move applicants to unofficial communication channels
- Collect sensitive financial or identity information
- Create artificial urgency
- Promise unrealistic guarantees
- Exploit inexperienced job seekers

Keyword-only detection can miss sophisticated scams, while an unexplained ML probability does not tell users **why** a posting appears suspicious.

JobShield AI addresses this by combining:

1. **Machine-learning classification**
2. **Explicit scam-signal extraction**
3. **Probability calibration**
4. **Security and prompt-injection defenses**
5. **Evidence-grounded explanations**

---

## ✨ Features

### 🔍 ML-Based Scam Detection

- TF-IDF representation using word and phrase-level features
- Logistic Regression classifier with balanced class weights
- Leakage-safe train/validation/test splitting
- Probability calibration using Platt Scaling
- Validation-tuned production threshold

### 🚨 Scam Signal Detection

The system explicitly checks for signals such as:

- Upfront payment or registration fees
- Verification or onboarding fees
- Telegram / WhatsApp routing
- Sensitive banking or identity information requests
- False urgency
- Unrealistic guarantees
- No-experience-required patterns
- Other suspicious recruitment language

### 🧾 Evidence-Grounded Explanations

The explanation layer receives extracted evidence rather than unrestricted control over the classification process.

It explains:

- Why a posting was flagged
- Which signals were detected
- Which text evidence supports those signals
- Recommended safety actions

### 🛡️ Security Defenses

JobShield AI includes defenses against malicious job-posting content attempting to manipulate the AI system.

Examples include:

- Prompt-injection detection
- Fake system-instruction detection
- Persona-hijacking detection
- Input sanitization
- Null-byte stripping
- Input length limits
- XSS defusal
- Quoted-material handling

Most importantly:

> **The LLM does not determine or override the underlying ML verdict.**

The production classifier determines the risk score. The LLM is restricted to explaining extracted evidence.

---

## 📸 Application Screenshots

### 🚨 Scam Detection — High-Risk Job

JobShield AI identifies suspicious job postings and provides a calibrated fraud probability, production threshold, and final risk verdict.

![Scam Risk Assessment](reports/screenshots/01-scam-risk.png)

### 🔍 Scam Signals Detected

The rule-based signal layer provides interpretable indicators alongside the ML prediction.

![Detected Scam Signals](reports/screenshots/02-scam-signals.png)

### 🧾 Evidence Extraction

JobShield AI extracts the exact text responsible for each detected scam signal, making the prediction easier to audit.

![Extracted Scam Evidence](reports/screenshots/03-scam-evidence.png)

### ✅ Legitimate Job Detection

The system also handles legitimate job postings and produces a low-risk prediction when scam patterns are absent.

![Legitimate Job Risk Assessment](reports/screenshots/04-legitimate-risk.png)

### 🛡️ Prompt-Injection Security Test

The application remains focused on fraud detection even when the input contains instructions attempting to manipulate the AI explanation layer.

![Security Test Risk Assessment](reports/screenshots/05-security-risk.png)

### 🔐 Security Signals

The security test correctly identifies the underlying scam indicators instead of following the injected instructions.

![Security Test Signals](reports/screenshots/06-security-signals.png)

### 🤖 AI Explanation & Safety Guidance

The explanation layer provides risk reasoning and actionable safety guidance based on the detected evidence.

![AI Explanation and Safety Guidance](reports/screenshots/07-security-explanation.png)

# 🏗️ System Architecture

```text
                    Job Posting Text
                           │
                           ▼
              ┌─────────────────────────┐
              │ Input Validation &       │
              │ Sanitization             │
              │                         │
              │ • Length limits         │
              │ • Null-byte stripping   │
              │ • XSS defusal           │
              └────────────┬────────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │ Text Normalization      │
              │                         │
              │ • Character mapping     │
              │ • Text preprocessing     │
              └────────────┬────────────┘
                           │
            ┌──────────────┼──────────────┐
            │              │              │
            ▼              ▼              ▼
      ┌──────────┐   ┌────────────┐  ┌──────────────┐
      │ TF-IDF   │   │ Scam Signal│  │ Prompt        │
      │ Features │   │ Detector   │  │ Injection     │
      │          │   │            │  │ Guard         │
      └────┬─────┘   └──────┬─────┘  └──────────────┘
           │                │
           ▼                │
   ┌────────────────┐       │
   │ Logistic       │       │
   │ Regression     │       │
   │                │       │
   │ Platt Scaling  │       │
   └───────┬────────┘       │
           │                │
           └────────┬───────┘
                    ▼
          ┌─────────────────────┐
          │ Risk Decision Layer │
          │                     │
          │ Threshold = 0.54    │
          │ Signal-based checks │
          └──────────┬──────────┘
                     │
                     ▼
          ┌─────────────────────┐
          │ Evidence-Grounded   │
          │ Explanation Layer   │
          │                     │
          │ Google Gemini Flash │
          └──────────┬──────────┘
                     │
                     ▼
          ┌─────────────────────┐
          │ Streamlit Analyst   │
          │ UI                  │
          └─────────────────────┘
```

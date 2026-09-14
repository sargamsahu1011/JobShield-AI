# 🛡️ JobShield AI — Evidence-Grounded Recruitment Scam Detection

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Streamlit UI](https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg)](frontend/app.py)

**JobShield AI** is a machine learning and AI-assisted platform designed to detect fraudulent job postings, identify specific recruitment scam signals, and generate transparent, evidence-grounded risk assessments for job seekers and career analysts.

---

## 🎯 Purpose & Intended Use
- **Purpose:** Provide an evidence-grounded decision-support tool that flags suspicious recruitment postings, highlights deceptive patterns (e.g., upfront payment demands, off-platform messaging, credential phishing), and provides actionable safety recommendations.
- **Intended Use:** Triage and risk analysis for job seekers, university career centers, job boards, and fraud analysts.
- **Decision-Support Disclaimer:** JobShield AI is **not** definitive proof of fraud. It provides probabilistic risk scoring and evidence indicators to assist human judgment.

---

## 🏗️ System Architecture

```
Raw Job Posting Text
        │
        ▼
[Input Validation & Sanitization] (Null-byte stripping, length capping, XSS defusal)
        │
        ├────────────────────────────────────────┬────────────────────────────────────────┐
        ▼                                        ▼                                        ▼
[Text Normalization & TF-IDF]         [Rule-Based Signal Detector]             [Prompt Injection Guard]
- Canonical character mapping         - Upfront payment / fees                 - Direct override scans
- Sublinear TF-IDF (1,2 n-grams)      - Telegram / WhatsApp routing            - Persona hijacking defusal
        │                             - Sensitive banking / SSN requests       - Fake system tag detection
        ▼                             - False urgency & guarantees                        │
[Calibrated Logistic Regression]                 │                                        │
- Platt Scaling (Sigmoid)                        │                                        │
- Threshold: 0.54                                │                                        │
        │                                        │                                        │
        └────────────────────────────────────────┼────────────────────────────────────────┘
                                                 ▼
                              [Defensive Floor & Signal Veto]
                              - Checks severe scam signals & overrides
                              - Ensures fraud score >= 0.70 if critical risk
                                                 │
                                                 ▼
                              [Evidence-Grounded Explainer]
                              - Google Gemini 3.5 / 3.6 Flash
                              - Strictly bounded system instructions
                              - Explains only factual extracted evidence
                                                 │
                                                 ▼
                                     [Streamlit Analyst UI]
```

---

## 📊 Production Model & Benchmark

- **Model:** Calibrated TF-IDF + Logistic Regression (Platt Scaling)
- **Vectorization:** Sublinear TF-IDF (1, 2 n-grams, min_df=2, max_df=0.95, 100k features)
- **Decision Threshold:** `0.54` (tuned on held-out validation split)
- **Data Splitting:** Leakage-safe `GroupShuffleSplit` (`random_state=42`) grouping identical text

### Clean Test Benchmark Results
Evaluated on the independent test set (`data/processed/test.csv`, $N = 1,736$):

| Metric | Clean Test Score |
| :--- | :--- |
| **Precision** | **96.63%** (`0.9663`) |
| **Recall** | **80.37%** (`0.8037`) |
| **F1-Score** | **87.76%** (`0.8776`) |
| **PR-AUC** | **90.96%** (`0.9096`) |
| **ROC-AUC** | **98.65%** (`0.9865`) |

### Confusion Matrix
```
                    Predicted Legitimate    Predicted Fraudulent
Actual Legitimate           1626                     3  (FP)
Actual Fraudulent             21                    86  (TP)
```
- **Total Test Errors:** 24 (3 False Positives, 21 False Negatives) out of 1,736 samples.

### DistilBERT Control Comparison (Stage 1B)
During Stage 1B, a transformer benchmark (`distilbert-base-uncased`, max length 256, threshold 0.05) was evaluated on the identical clean test split:
- **DistilBERT Results:** Precision: 92.38% (`0.9238`), Recall: 90.65% (`0.9065`), F1-Score: 91.51% (`0.9151`), PR-AUC: 96.16% (`0.9616`), ROC-AUC: 99.28% (`0.9928`), Confusion Matrix: `[[1621, 8], [10, 97]]`.
- **Production Choice Rationale:** Although DistilBERT achieves higher recall, Calibrated TF-IDF + Logistic Regression delivers significantly higher precision (96.63% vs 92.38%) with only 3 False Positives compared to DistilBERT's 8. In job scam detection, minimizing false positives on legitimate employers is paramount. Furthermore, Calibrated TF-IDF provides deterministic linear feature explainability, sub-millisecond inference on CPU without GPU overhead, and minimal operational complexity. DistilBERT remains retained as an optional fallback classifier.

---

## 🛡️ Robustness & Security Summary

### Stage 3: Adversarial Robustness
- **Attack Detection Rate:** 66.67% (6/9 attacks detected).
- **Surface Obfuscation:** Passed strongly (character substitution, punctuation, spacing, and case manipulation are effectively resolved by the text normalizer).
- **Known Weakness:** **Semantic paraphrasing** (rewriting scam concepts using clean, professional vocabulary without keyword triggers) evades n-gram representation.

### Stage 4: Error Analysis
- **False Positives (3):** Legitimate data-entry and payroll clerk postings with vocabulary that closely overlaps with administrative job scams (`ambiguous_legitimate`).
- **False Negatives (21):**
  - Stolen corporate postings / clones lacking explicit scam text (`missing_scam_signals`: 7)
  - Ultra-short postings under 85 words lacking feature mass (`short_posting`: 6)
  - Subtle scams with paraphrased language (`semantic_paraphrase`: 3)
  - Vague administrative vacancies (`insufficient_evidence`: 3)
  - Non-standard phrasing (`unusual_wording`: 2)

### Stage 5: Security & Prompt-Injection Resilience
- **Score:** 8/8 test cases passed (100%).
- **Defense Mechanism:** Input sanitization, immutable ML classification, prompt-injection regex defusal, and strictly bounded Gemini system instructions that prevent instructions in job text from overriding review verdicts.

---

## 🚀 Quickstart & Reproduction

### 1. Installation
```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 2. Environment Configuration
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Run Verification Tests
```powershell
# Run regression test suite (8 operational requirements)
.venv\Scripts\python.exe ml\test_regression_suite.py

# Run security & prompt-injection suite
.venv\Scripts\python.exe ml\test_security_injections.py

# Run error analysis on the clean test split
.venv\Scripts\python.exe ml\error_analysis.py
```

### 4. Launch Application
```powershell
.venv\Scripts\streamlit.exe run frontend\app.py
```

---

## ⚠️ Known Limitations & Ethical Use
1. **Decision Support Only:** This system is an automated risk screening tool, not definitive proof of criminality.
2. **Semantic Paraphrasing:** Scammers employing creative vocabulary or corporate impersonation without surface signals may be missed.
3. **Cloned Corporate Job Descriptions:** If a scammer copies a legitimate Fortune 500 job description verbatim and conducts fraud off-platform, text analysis alone cannot detect it without domain and URL verification.
4. **Human Review Required:** Adverse employment or platform moderation actions must never be taken based solely on automated scores.

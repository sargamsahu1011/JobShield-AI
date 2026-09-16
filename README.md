# 🛡️ JobShield AI

### Evidence-Grounded Recruitment Scam Detection

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/Frontend-React-61DAFB.svg)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Build-Vite-646CFF.svg)](https://vite.dev/)
[![Flask](https://img.shields.io/badge/API-Flask-000000.svg)](https://flask.palletsprojects.com/)
[![scikit-learn](https://img.shields.io/badge/ML-scikit--learn-F7931E.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **JobShield AI is an end-to-end machine-learning system for detecting suspicious recruitment postings, producing calibrated risk estimates, identifying interpretable scam signals, extracting supporting evidence, and generating constrained AI explanations.**

It combines **NLP-based classification, probability calibration, rule-based detection, evidence extraction, adversarial-input defenses, REST API engineering, and a production web interface** into a single system.

> ⚠️ **Important:** JobShield AI is a decision-support system. A model prediction is not definitive proof that a job posting is fraudulent or legitimate. Users should independently verify employers, domains, recruiters, and application channels.

---

## 🚀 Live Application

JobShield AI is deployed as a production web application with a separate frontend and backend.

**Architecture:**

```text
React + Vite
     │
     ▼
  Vercel
     │
     │ HTTPS
     ▼
 Flask REST API
     │
     ▼
 JobShield ML Pipeline
     │
     ├── TF-IDF + Logistic Regression
     ├── Platt Calibration
     ├── Scam Signal Detection
     ├── Evidence Extraction
     ├── Input Validation
     └── Prompt-Injection Detection
              │
              ▼
       Gemini Explanation
```

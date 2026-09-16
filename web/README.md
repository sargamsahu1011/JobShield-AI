# JobShield AI — Web Frontend

The web frontend for **JobShield AI**, an evidence-grounded recruitment scam detection system.

The application provides a user-friendly interface for analyzing job postings and displaying:

- Fraud probability
- Risk classification
- Detected scam signals
- Supporting evidence
- Model information
- Security/safety guidance
- AI-generated explanation

## Tech Stack

- React
- Vite
- JavaScript
- CSS
- Fetch API
- Vercel for production deployment

## Architecture

```text
User
  │
  ▼
React + Vite Frontend
  │
  │ POST /api/analyze
  ▼
JobShield AI Flask API
  │
  ├── Input Validation
  ├── TF-IDF + Logistic Regression
  ├── Platt Calibration
  ├── Scam Signal Detection
  ├── Evidence Extraction
  ├── Prompt-Injection Detection
  └── Gemini Explanation Layer
  │
  ▼
Structured Analysis
  │
  ▼
React UI
```

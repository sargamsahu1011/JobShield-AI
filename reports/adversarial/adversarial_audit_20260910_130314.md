# JobShield AI — Adversarial Robustness Audit Report
**Generated:** 2026-09-10 13:03:14 UTC  
**Target Model:** `Calibrated TF-IDF + Logistic Regression (Platt Scaling) (Threshold: 0.405)`  
**Samples Evaluated:** 5 distinct postings (40 attack variants)  

## 1. Executive Summary
- **Overall Attack Success Rate (ASR):** `4.2%` (1/24 fraudulent postings evaded detection)
- **Pre-Attack Fraud Detection Rate:** `60.0%`
- **Post-Attack Fraud Detection Rate:** `57.5%` (Absolute drop: `2.5%`)
- **Mean Fraud Score Degradation:** `-0.0191`
- **Maximum Observed Score Suppression:** `0.2552`
- **Rule-Based Heuristic Dropout Rate:** `12.5%` of scam regex signals vanished under attack

## 2. Vulnerability Breakdown by Attack Category
| Attack Type | Evaluated | Orig Fraud | Flips | ASR (%) | Pre-Det (%) | Post-Det (%) | Mean Δ Score | Max Δ Score | Signal Drop (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `leetspeak` | 5 | 3 | 1 | **33.3%** | 60.0% | 40.0% | +0.0539 | 0.2314 | 42.9% |
| `typos` | 5 | 3 | 0 | **0.0%** | 60.0% | 60.0% | +0.0511 | 0.2014 | 0.0% |
| `zero_width` | 5 | 3 | 0 | **0.0%** | 60.0% | 60.0% | +0.0000 | 0.0000 | 0.0% |
| `unicode_homoglyphs` | 5 | 3 | 0 | **0.0%** | 60.0% | 60.0% | +0.0000 | 0.0000 | 0.0% |
| `obfuscated_contacts` | 5 | 3 | 0 | **0.0%** | 60.0% | 60.0% | -0.0014 | 0.0197 | 28.6% |
| `obfuscated_keywords` | 5 | 3 | 0 | **0.0%** | 60.0% | 60.0% | +0.0510 | 0.2552 | 28.6% |
| `benign_camouflage` | 5 | 3 | 0 | **0.0%** | 60.0% | 60.0% | +0.0000 | 0.0000 | 0.0% |
| `sentence_restructuring` | 5 | 3 | 0 | **0.0%** | 60.0% | 60.0% | -0.0020 | 0.0021 | 0.0% |

## 3. Top Evasion Cases (Fraud $\to$ Legitimate Flips)
### Flip Example 1: `leetspeak` (Sample: `regression_SENSITIVE INFORMATION SCAM`)
- **Score Shift:** `0.5000` (Fraudulent) $\longrightarrow$ `0.2686` (Legitimate) [Δ `0.2314`]
- **Dropped Signals:** `None`
- **Original Excerpt:**
  > *"Customer Support Representative

    Work from home and earn ₹45,000 per month.

    To complete your employment verification, send us your
    bank account details, OTP and A..."*
- **Attacked Excerpt:**
  > *"Cus7omer Support Repre$ent@tive

    Work from hom3 and earn ₹45,000 per month.

    To complete your employment verifica7ion, $end us your
    bank account details, OTP and A..."*

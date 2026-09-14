# JobShield AI — Adversarial Robustness Audit Report
**Generated:** 2026-09-14 12:18:23 UTC  
**Target Model:** `Calibrated TF-IDF + Logistic Regression (Platt Scaling) (Threshold: 0.655)`  
**Samples Evaluated:** 10 distinct postings (110 attack variants)  

## 1. Executive Summary
- **Overall Attack Success Rate (ASR):** `0.0%` (0/4 fraudulent postings evaded detection)
- **Pre-Attack Fraud Detection Rate:** `40.0%`
- **Post-Attack Fraud Detection Rate:** `40.0%` (Absolute drop: `0.0%`)
- **Mean Fraud Score Degradation:** `-0.0013`
- **Maximum Observed Score Suppression:** `0.0818`
- **Rule-Based Heuristic Dropout Rate:** `10.4%` of scam regex signals vanished under attack

## 2. Vulnerability Breakdown by Attack Category
| Attack Type | Evaluated | Orig Fraud | Flips | ASR (%) | Pre-Det (%) | Post-Det (%) | Mean Δ Score | Max Δ Score | Signal Drop (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `typos` | 10 | 4 | 0 | **0.0%** | 40.0% | 40.0% | +0.0045 | 0.0230 | 0.0% |
| `zero_width` | 10 | 4 | 0 | **0.0%** | 40.0% | 40.0% | +0.0000 | 0.0000 | 0.0% |
| `unicode_homoglyphs` | 10 | 4 | 0 | **0.0%** | 40.0% | 40.0% | +0.0000 | 0.0000 | 0.0% |
| `leetspeak` | 10 | 4 | 0 | **0.0%** | 40.0% | 40.0% | +0.0074 | 0.0593 | 28.6% |
| `obfuscated_contacts` | 10 | 4 | 0 | **0.0%** | 40.0% | 40.0% | -0.0001 | 0.0014 | 42.9% |
| `obfuscated_keywords` | 10 | 4 | 0 | **0.0%** | 40.0% | 40.0% | +0.0082 | 0.0818 | 28.6% |
| `benign_camouflage` | 10 | 4 | 0 | **0.0%** | 40.0% | 40.0% | +0.0000 | 0.0000 | 0.0% |
| `sentence_restructuring` | 10 | 4 | 0 | **0.0%** | 40.0% | 40.0% | -0.0061 | 0.0002 | 0.0% |
| `urgency_synonyms` | 10 | 4 | 0 | **0.0%** | 40.0% | 40.0% | -0.0007 | 0.0430 | 14.3% |
| `paraphrased_scam` | 10 | 4 | 0 | **0.0%** | 40.0% | 40.0% | +0.0024 | 0.0671 | 0.0% |
| `case_spacing_tricks` | 10 | 4 | 0 | **0.0%** | 40.0% | 40.0% | -0.0017 | 0.0001 | 0.0% |

## 3. Top Evasion Cases (Fraud $\to$ Legitimate Flips)
*No fraudulent postings were successfully flipped in this evaluation run.*
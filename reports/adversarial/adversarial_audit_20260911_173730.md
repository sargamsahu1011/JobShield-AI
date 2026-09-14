# JobShield AI — Adversarial Robustness Audit Report
**Generated:** 2026-09-11 17:37:30 UTC  
**Target Model:** `Calibrated TF-IDF + Logistic Regression (Platt Scaling) (Threshold: 0.655)`  
**Samples Evaluated:** 5 distinct postings (40 attack variants)  

## 1. Executive Summary
- **Overall Attack Success Rate (ASR):** `0.0%` (0/8 fraudulent postings evaded detection)
- **Pre-Attack Fraud Detection Rate:** `20.0%`
- **Post-Attack Fraud Detection Rate:** `20.0%` (Absolute drop: `0.0%`)
- **Mean Fraud Score Degradation:** `-0.0017`
- **Maximum Observed Score Suppression:** `0.0818`
- **Rule-Based Heuristic Dropout Rate:** `12.5%` of scam regex signals vanished under attack

## 2. Vulnerability Breakdown by Attack Category
| Attack Type | Evaluated | Orig Fraud | Flips | ASR (%) | Pre-Det (%) | Post-Det (%) | Mean Δ Score | Max Δ Score | Signal Drop (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `typos` | 5 | 1 | 0 | **0.0%** | 20.0% | 20.0% | +0.0060 | 0.0230 | 0.0% |
| `zero_width` | 5 | 1 | 0 | **0.0%** | 20.0% | 20.0% | +0.0000 | 0.0000 | 0.0% |
| `unicode_homoglyphs` | 5 | 1 | 0 | **0.0%** | 20.0% | 20.0% | +0.0000 | 0.0000 | 0.0% |
| `leetspeak` | 5 | 1 | 0 | **0.0%** | 20.0% | 20.0% | +0.0028 | 0.0089 | 28.6% |
| `obfuscated_contacts` | 5 | 1 | 0 | **0.0%** | 20.0% | 20.0% | +0.0003 | 0.0014 | 42.9% |
| `obfuscated_keywords` | 5 | 1 | 0 | **0.0%** | 20.0% | 20.0% | +0.0164 | 0.0818 | 28.6% |
| `benign_camouflage` | 5 | 1 | 0 | **0.0%** | 20.0% | 20.0% | +0.0000 | 0.0000 | 0.0% |
| `sentence_restructuring` | 5 | 1 | 0 | **0.0%** | 20.0% | 20.0% | -0.0121 | 0.0002 | 0.0% |

## 3. Top Evasion Cases (Fraud $\to$ Legitimate Flips)
*No fraudulent postings were successfully flipped in this evaluation run.*
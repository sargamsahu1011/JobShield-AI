# JobShield AI — Adversarial Robustness Audit Report
**Generated:** 2026-09-09 15:50:14 UTC  
**Target Model:** `MockBaseline`  
**Samples Evaluated:** 1 distinct postings (8 attack variants)  

## 1. Executive Summary
- **Overall Attack Success Rate (ASR):** `37.5%` (3/8 fraudulent postings evaded detection)
- **Pre-Attack Fraud Detection Rate:** `100.0%`
- **Post-Attack Fraud Detection Rate:** `62.5%` (Absolute drop: `37.5%`)
- **Mean Fraud Score Degradation:** `-0.2850`
- **Maximum Observed Score Suppression:** `0.7600`
- **Rule-Based Heuristic Dropout Rate:** `33.3%` of scam regex signals vanished under attack

## 2. Vulnerability Breakdown by Attack Category
| Attack Type | Evaluated | Orig Fraud | Flips | ASR (%) | Pre-Det (%) | Post-Det (%) | Mean Δ Score | Max Δ Score | Signal Drop (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `zero_width` | 1 | 1 | 1 | **100.0%** | 100.0% | 0.0% | +0.7600 | 0.7600 | 33.3% |
| `unicode_homoglyphs` | 1 | 1 | 1 | **100.0%** | 100.0% | 0.0% | +0.7600 | 0.7600 | 100.0% |
| `obfuscated_keywords` | 1 | 1 | 1 | **100.0%** | 100.0% | 0.0% | +0.7600 | 0.7600 | 66.7% |
| `typos` | 1 | 1 | 0 | **0.0%** | 100.0% | 100.0% | +0.0000 | 0.0000 | 0.0% |
| `leetspeak` | 1 | 1 | 0 | **0.0%** | 100.0% | 100.0% | +0.0000 | 0.0000 | 66.7% |
| `obfuscated_contacts` | 1 | 1 | 0 | **0.0%** | 100.0% | 100.0% | +0.0000 | 0.0000 | 0.0% |
| `benign_camouflage` | 1 | 1 | 0 | **0.0%** | 100.0% | 100.0% | +0.0000 | 0.0000 | 0.0% |
| `sentence_restructuring` | 1 | 1 | 0 | **0.0%** | 100.0% | 100.0% | +0.0000 | 0.0000 | 0.0% |

## 3. Top Evasion Cases (Fraud $\to$ Legitimate Flips)
### Flip Example 1: `zero_width` (Sample: `sample_1`)
- **Score Shift:** `0.8800` (Fraudulent) $\longrightarrow$ `0.1200` (Legitimate) [Δ `0.7600`]
- **Dropped Signals:** `payment_request`
- **Original Excerpt:**
  > *"URGENT: Pay registration fee via crypto USDT...."*
- **Attacked Excerpt:**
  > *"URGENT: Pay registration f‍ee via cry‌pto USDT...."*

### Flip Example 2: `unicode_homoglyphs` (Sample: `sample_1`)
- **Score Shift:** `0.8800` (Fraudulent) $\longrightarrow$ `0.1200` (Legitimate) [Δ `0.7600`]
- **Dropped Signals:** `crypto_request, payment_request, urgency_language`
- **Original Excerpt:**
  > *"URGENT: Pay registration fee via crypto USDT...."*
- **Attacked Excerpt:**
  > *"URGENТ: Раy regiѕtratіоn feе vіa crуpto USDТ...."*

### Flip Example 3: `obfuscated_keywords` (Sample: `sample_1`)
- **Score Shift:** `0.8800` (Fraudulent) $\longrightarrow$ `0.1200` (Legitimate) [Δ `0.7600`]
- **Dropped Signals:** `crypto_request, payment_request`
- **Original Excerpt:**
  > *"URGENT: Pay registration fee via crypto USDT...."*
- **Attacked Excerpt:**
  > *"URGENT: Pay candidate enrollment deposit via digital currency asset U-S-D-T...."*

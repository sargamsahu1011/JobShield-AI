# JobShield AI — Adversarial Robustness Audit Report
**Generated:** 2026-09-14 12:18:32 UTC  
**Target Model:** `TF-IDF + Logistic Regression Baseline (Raw 0.52)`  
**Samples Evaluated:** 30 distinct postings (330 attack variants)  

## 1. Executive Summary
- **Overall Attack Success Rate (ASR):** `4.3%` (11/23 fraudulent postings evaded detection)
- **Pre-Attack Fraud Detection Rate:** `76.7%`
- **Post-Attack Fraud Detection Rate:** `73.3%` (Absolute drop: `3.3%`)
- **Mean Fraud Score Degradation:** `-0.0408`
- **Maximum Observed Score Suppression:** `0.5790`
- **Rule-Based Heuristic Dropout Rate:** `10.2%` of scam regex signals vanished under attack

## 2. Vulnerability Breakdown by Attack Category
| Attack Type | Evaluated | Orig Fraud | Flips | ASR (%) | Pre-Det (%) | Post-Det (%) | Mean Δ Score | Max Δ Score | Signal Drop (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `unicode_homoglyphs` | 30 | 23 | 10 | **43.5%** | 76.7% | 43.3% | +0.2345 | 0.5790 | 0.0% |
| `benign_camouflage` | 30 | 23 | 1 | **4.3%** | 76.7% | 73.3% | +0.1295 | 0.3540 | 0.0% |
| `typos` | 30 | 23 | 0 | **0.0%** | 76.7% | 76.7% | +0.0083 | 0.0470 | 0.0% |
| `zero_width` | 30 | 23 | 0 | **0.0%** | 76.7% | 76.7% | +0.0179 | 0.0573 | 0.0% |
| `leetspeak` | 30 | 23 | 0 | **0.0%** | 76.7% | 76.7% | +0.0683 | 0.1141 | 37.5% |
| `obfuscated_contacts` | 30 | 23 | 0 | **0.0%** | 76.7% | 76.7% | -0.0011 | 0.0059 | 37.5% |
| `obfuscated_keywords` | 30 | 23 | 0 | **0.0%** | 76.7% | 76.7% | +0.0027 | 0.0791 | 25.0% |
| `sentence_restructuring` | 30 | 23 | 0 | **0.0%** | 76.7% | 76.7% | -0.0026 | 0.0023 | 0.0% |
| `urgency_synonyms` | 30 | 23 | 0 | **0.0%** | 76.7% | 76.7% | -0.0081 | 0.0499 | 12.5% |
| `paraphrased_scam` | 30 | 23 | 0 | **0.0%** | 76.7% | 76.7% | +0.0015 | 0.0689 | 0.0% |
| `case_spacing_tricks` | 30 | 23 | 0 | **0.0%** | 76.7% | 76.7% | -0.0024 | 0.0001 | 0.0% |

## 3. Top Evasion Cases (Fraud $\to$ Legitimate Flips)
### Flip Example 1: `unicode_homoglyphs` (Sample: `regression_Obvious scam`)
- **Score Shift:** `0.8973` (Fraudulent) $\longrightarrow$ `0.4191` (Legitimate) [Δ `0.4782`]
- **Dropped Signals:** `None`
- **Original Excerpt:**
  > *"Work From Home Data Entry Assistant!
Earn $4,500 every week with no experience required.
All equipment will be provided.
To secure your position, submit a $150 registration fee via..."*
- **Attacked Excerpt:**
  > *"Work Frоm Ноme Data Еntry Аѕsіѕtant!
Eаrn $4,500 everу week wіth nо eхреrience required.
All equipment will bе рrоvіdеd.
То securе уour poѕitіon, submit a $150 registrаtіоn fее via..."*

### Flip Example 2: `unicode_homoglyphs` (Sample: `dataset_178`)
- **Score Shift:** `0.8963` (Fraudulent) $\longrightarrow$ `0.3173` (Legitimate) [Δ `0.5790`]
- **Dropped Signals:** `None`
- **Original Excerpt:**
  > *"TITLE: Customer Service Representative DESCRIPTION: Experienced, reliable team members are needed for our Customer Service Representative needed! We are currently searching for can..."*
- **Attacked Excerpt:**
  > *"TІТLЕ: Customеr Servісe Rерresеntativе DESCRІРTІОN: Еxperienced, reliable team mеmbеrѕ аrе nееded for our Сuѕtomer Servіcе Representativе nееdеd! Wе are сurrently seаrсhing fоr can..."*

### Flip Example 3: `unicode_homoglyphs` (Sample: `dataset_273`)
- **Score Shift:** `0.9130` (Fraudulent) $\longrightarrow$ `0.5108` (Legitimate) [Δ `0.4022`]
- **Dropped Signals:** `None`
- **Original Excerpt:**
  > *"TITLE: Assistant Accountant/immediate start DESCRIPTION: Our organisation is seeking students / graduates with a finance, business or commerce related degree qualifications. We wan..."*
- **Attacked Excerpt:**
  > *"TІТLЕ: Assіstаnt Аcсоuntant/immеdiatе start DЕSСRIРТІON: Our organisation is seеkіng ѕtudеntѕ / grаduаtes with а fіnance, buѕinеss or commercе rеlаtеd dеgree quаlificatіоns. Wе wan..."*

### Flip Example 4: `unicode_homoglyphs` (Sample: `dataset_312`)
- **Score Shift:** `0.8162` (Fraudulent) $\longrightarrow$ `0.3729` (Legitimate) [Δ `0.4433`]
- **Dropped Signals:** `None`
- **Original Excerpt:**
  > *"TITLE: Payroll Data Coordinator Positions - Earn $100-$200 Daily DESCRIPTION: We are a full-service marketing and staffing firm, serving companies ranging from Fortune 100 to new s..."*
- **Attacked Excerpt:**
  > *"TІТLЕ: Payrоll Datа Сoоrdіnator Рosіtionѕ - Еarn $100-$200 Dаіlу DESCRIPTION: We are a full-servісе mаrkеtіng аnd staffing fіrm, ѕerving cоmpаnies ranging from Fortunе 100 tо nеw ѕ..."*

### Flip Example 5: `unicode_homoglyphs` (Sample: `dataset_313`)
- **Score Shift:** `0.8162` (Fraudulent) $\longrightarrow$ `0.3729` (Legitimate) [Δ `0.4433`]
- **Dropped Signals:** `None`
- **Original Excerpt:**
  > *"TITLE: Payroll Data Coordinator Positions - Earn $100-$200 Daily DESCRIPTION: We are a full-service marketing and staffing firm, serving companies ranging from Fortune 100 to new s..."*
- **Attacked Excerpt:**
  > *"TІТLЕ: Payrоll Datа Сoоrdіnator Рosіtionѕ - Еarn $100-$200 Dаіlу DESCRIPTION: We are a full-servісе mаrkеtіng аnd staffing fіrm, ѕerving cоmpаnies ranging from Fortunе 100 tо nеw ѕ..."*

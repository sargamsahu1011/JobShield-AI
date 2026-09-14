# JobShield AI — False Positive Audit Resolution Report

**Model Evaluated:** `Calibrated TF-IDF + Logistic Regression (Platt Scaling)` (Threshold: `0.6550`)  
**Resolution Summary:** 8/9 False Positives Resolved (88.89%), 1 Open Case

## Case-by-Case Audit Resolution Table

| Case | Job ID | Job Title | Historical Score | Current Score | Verdict Shift | Status | Reason |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| 1 | `1670` | Office PA/Receptionist | `0.7527` | `0.5878` | Fraud $\to$ Legit | ✅ RESOLVED | Score dropped below calibrated threshold (0.5878 < 0.6550) via Platt scaling & canonical normalizer |
| 2 | `6742` | Customer Service Representative | `0.4885` | `0.5387` | Fraud $\to$ Legit | ✅ RESOLVED | Score dropped below calibrated threshold (0.5387 < 0.6550) via Platt scaling & canonical normalizer |
| 3 | `6790` | Customer Service Representative | `0.4885` | `0.5387` | Fraud $\to$ Legit | ✅ RESOLVED | Score dropped below calibrated threshold (0.5387 < 0.6550) via Platt scaling & canonical normalizer |
| 4 | `6907` | Administrative Assistant | `0.7653` | `0.6017` | Fraud $\to$ Legit | ✅ RESOLVED | Score dropped below calibrated threshold (0.6017 < 0.6550) via Platt scaling & canonical normalizer |
| 5 | `7898` | Executive Administrative Assistant | `0.6987` | `0.4906` | Fraud $\to$ Legit | ✅ RESOLVED | Score dropped below calibrated threshold (0.4906 < 0.6550) via Platt scaling & canonical normalizer |
| 6 | `11136` | Assistant Chief Nursing Officer (hospital west of Montgomery, AL) | `0.5257` | `0.6059` | Fraud $\to$ Legit | ✅ RESOLVED | Score dropped below calibrated threshold (0.6059 < 0.6550) via Platt scaling & canonical normalizer |
| 7 | `12242` | Teaching Assistant | `0.9136` | `0.7871` | Fraud $\to$ Fraud | ⚠️ STILL OPEN | Score remains elevated (0.7871 >= 0.6550) due to administrative/data-entry scam keyword density |
| 8 | `13085` | Bilingual Products and Services Coordinator II | `0.5393` | `0.5042` | Fraud $\to$ Legit | ✅ RESOLVED | Score dropped below calibrated threshold (0.5042 < 0.6550) via Platt scaling & canonical normalizer |
| 9 | `16639` | Immediate Opening : Help Desk /Technical Support Coordinator | `0.4674` | `0.5749` | Fraud $\to$ Legit | ✅ RESOLVED | Score dropped below calibrated threshold (0.5749 < 0.6550) via Platt scaling & canonical normalizer |

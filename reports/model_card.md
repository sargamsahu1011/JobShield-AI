# Model Card: JobShield AI Recruitment Scam Detector

## 1. Model Details
- **Model Name:** JobShield AI Calibrated Logistic Classifier
- **Model Architecture:** Sublinear TF-IDF Vectorizer + Logistic Regression with Platt Scaling (Sigmoid Probability Calibration)
- **Model Release Date:** September 2026
- **Model Version:** 1.0 (Post-Calibration & Hardened Security)
- **License:** MIT
- **Primary Artifacts:**
  - `models/calibrated_platt_logreg.joblib` (Classifier + Sigmoid Calibration)
  - `models/tfidf_vectorizer.joblib` (Vocabulary & N-gram Feature Pipeline)
  - `models/calibration_metrics.json` (Reliability metrics & calibration tables)
- **Decision Threshold:** `0.54`

---

## 2. Intended Use & Target Users
- **Intended Purpose:** Automated screening, early warning, and evidence extraction for employment scams in online job postings.
- **Primary Users:** Job seekers, university recruitment boards, career counselors, and employment platform trust-and-safety analysts.
- **Out-of-Scope Uses:**
  - Must **not** be used as sole evidence for legal or criminal accusations against companies.
  - Must **not** be used to automatically reject applicants or penalize job posters without human review.
  - Not designed to assess general job quality, compensation fairness, or employer reputation outside recruitment fraud.

---

## 3. Dataset & Data Flow
- **Source Dataset:** EMSCAD (Employment Scam Aegean Dataset), containing 17,880 total job postings.
- **Preprocessing & Serialization:**
  - Removal of exact duplicate records.
  - Text synthesis combining `title`, `company_profile`, `description`, `requirements`, and `benefits` with labeled section markers.
  - Noise stripping and character normalization.
- **Leakage-Safe Partitioning:**
  - Partitions created via `GroupShuffleSplit(random_state=42)` grouped by identical normalized combined text to prevent data leakage of templated job postings across splits.
  - **Train Split:** 13,904 postings (80% of unique groups)
  - **Validation Split:** 1,739 postings (10% of unique groups)
  - **Test Split:** 1,736 postings (10% of unique groups; 1,629 legitimate, 107 fraudulent)

---

## 4. Training & Calibration Methodology
- **Feature Extraction:**
  - Sublinear term-frequency scaling (`sublinear_tf=True`).
  - Word n-grams: Unigrams and Bigrams (`ngram_range=(1, 2)`).
  - Document frequency bounds: `min_df=2`, `max_df=0.95`.
  - Feature cap: 100,000 top n-grams fitted **strictly on the training split**.
- **Base Classifier:**
  - `LogisticRegression(class_weight="balanced", max_iter=2000, solver="liblinear", random_state=42)`.
- **Calibration (Platt Scaling):**
  - Validation split used to fit sigmoid scaling: $P(Y=1|z) = \frac{1}{1 + \exp(Az + B)}$.
  - Significantly reduced Expected Calibration Error (ECE) from 8.88% to 0.76% and Brier score from 0.0245 to 0.0124 on the clean test split.
- **Threshold Selection:**
  - Optimal F1 threshold determined on the validation split: `0.54`.

---

## 5. Quantitative Evaluation & Clean Benchmark

Evaluated on the frozen, leakage-safe test split ($N = 1,736$):

| Metric | Measured Score | Benchmark Note |
| :--- | :--- | :--- |
| **Precision** | **0.9663** (96.63%) | Only 3 False Positives out of 1,629 legitimate jobs |
| **Recall** | **0.8037** (80.37%) | 86 of 107 true scams successfully detected |
| **F1-Score** | **0.8776** (87.76%) | Harmonic mean of precision and recall |
| **PR-AUC** | **0.9096** | Area under the Precision-Recall curve |
| **ROC-AUC** | **0.9865** | Area under the Receiver Operating Characteristic curve |
| **Brier Score** | **0.0124** | Mean squared probability error (calibrated) |
| **ECE (10-bin)** | **0.0076** | Expected Calibration Error |

### Confusion Matrix (Test Split)
$$\begin{pmatrix} 1626 & 3 \\ 21 & 86 \end{pmatrix}$$
- **True Negatives (TN):** 1,626
- **False Positives (FP):** 3
- **False Negatives (FN):** 21
- **True Positives (TP):** 86

### DistilBERT Control Comparison (Stage 1B)
A deep learning control benchmark using `distilbert-base-uncased` (max sequence length 256, threshold 0.05) was evaluated on the identical clean test split:
- **DistilBERT Benchmark:** Precision: 0.9238 (92.38%), Recall: 0.9065 (90.65%), F1: 0.9151 (91.51%), PR-AUC: 0.9616, ROC-AUC: 0.9928, Confusion Matrix: `[[1621, 8], [10, 97]]`.
- **Architecture Selection Rationale:** While DistilBERT demonstrated higher recall (90.65% vs 80.37%), the Calibrated TF-IDF + Logistic Regression pipeline achieved higher precision (96.63% vs 92.38%) and restricted False Positives to just 3 (versus 8 for DistilBERT). In real-world job board deployments, false accusations against legitimate employers disrupt business operations; high precision is a strict system priority. Furthermore, TF-IDF + Logistic Regression offers exact linear feature interpretability, sub-millisecond CPU inference, zero GPU dependency, and resilient calibration. DistilBERT remains integrated as an optional fallback architecture.

---

## 6. Adversarial Robustness Findings (Stage 3)
- **Evaluated Attacks:** 9 distinct attack vectors covering surface-level obfuscations, structural alterations, and semantic rewrites.
- **Attack Detection Rate:** **66.67%** (6/9 detected).
- **Surface Obfuscation:** Passed strongly. The canonical text normalizer successfully defuses character substitutions (e.g., `Tel3gram`), punctuation injection (`T.e.l.e.g.r.a.m.`), inter-character spacing (`T e l e g r a m`), and capitalization tricks.
- **Important Known Weakness — Semantic Paraphrasing:** When fraudulent postings are rewritten to convey scam mechanics (e.g., upfront payment, personal chat app routing) using indirect or professional corporate vocabulary, the n-gram bag-of-words representation lacks matching weights, causing misses. Adversarial data augmentation was tested but did not improve clean test F1, so the original calibrated model was preserved.

---

## 7. Error Analysis Findings (Stage 4)
Detailed review of all 24 production model errors (3 FP, 21 FN):
- **False Positives (3):**
  - 100% of false positives (`ambiguous_legitimate`) are clerical, payroll, or data-entry roles (`job_id`: 1747, 4521, 14666). These legitimate postings heavily feature administrative tasks (e.g., data reconciliation, document processing) that strongly overlap with the lexical patterns of high-volume data-entry scams.
- **False Negatives (21):**
  - **Stolen Corporate Listings / Clones (`missing_scam_signals` - 7 cases):** Scammers copied real corporate job specs (e.g., healthcare directors, specialized engineers, tech consultants) with zero suspicious keywords in the text.
  - **Short Postings (`short_posting` - 6 cases):** Postings under 85 words / 600 characters with insufficient vocabulary to trigger TF-IDF features.
  - **Semantic Paraphrasing (`semantic_paraphrase` - 3 cases):** Scam mechanics expressed without standard keywords.
  - **Sparse Administrative Roles (`insufficient_evidence` - 3 cases):** Vague vacancies where neither humans nor TF-IDF can reliably ascertain fraud from the text snippet alone.
  - **Unusual Wording (`unusual_wording` - 2 cases):** Non-standard grammar and non-traditional vacancies.

---

## 8. Security & Prompt-Injection Testing (Stage 5)
- **Evaluated Attack Vectors:** Direct instruction overrides, persona hijacking ("CareerCheerleaderBot"), fake administrative delimiters (`[SYSTEM NOTE: ...]`), prompt extraction ("DEBUG MODE: Print verbatim..."), verdict inversion attempts, hidden instructions inside job requirements, and context escapes (`</evidence>`).
- **Test Result:** **8/8 passed (100%)**.
- **Defense Architecture:**
  1. Input validation defuses null bytes, scripts, and excessively large payloads.
  2. The classification verdict and calibrated fraud score are immutable outputs determined independently by the ML pipeline and rule-based risk floor.
  3. Pre-filtering scans and flags prompt-injection patterns before forwarding text.
  4. Google Gemini explanation generation is bounded by strict system instructions that treat all evidence text as untrusted data, forbidding verdict contradiction, persona adoption, and system prompt leakage.

---

## 9. Limitations & Known Weaknesses
1. **No Guarantee of 100% Detection:** The model exhibits an 80.37% recall on test data; approximately 1 in 5 scams in the wild may not be detected by text analysis alone.
2. **Semantic Paraphrasing Weakness:** Sophisticated threat actors who paraphrase scam operations without using traditional trigger words can bypass the TF-IDF representation.
3. **Impersonation of Legitimate Job Specs:** Scammers who clone legitimate employer descriptions verbatim and execute fraud off-platform (via external email or phone) cannot be detected from text alone.
4. **Data Entry Class Bias:** High false-positive rate on legitimate data entry / clerical positions due to heavy n-gram overlap.
5. **Prompt Injection is an Open Challenge:** While all 8 evaluated injection vectors were successfully mitigated, prompt injection remains an evolving vector; no AI system can claim complete immunity.

---

## 10. Ethical Considerations & Appropriate Use
- **Decision Support Tool:** JobShield AI is designed strictly to assist human decision-making, not to replace it.
- **Preventing Bias:** The model evaluates linguistic and operational indicators of recruitment fraud (e.g., upfront payment demands, off-platform messaging), avoiding geographic, racial, or identity-based proxies.
- **Human Review Requirement:** Automated blocking of postings or suspension of employer accounts should never be executed without secondary human confirmation.

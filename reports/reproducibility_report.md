# JobShield AI — Reproducibility Report

## 1. Executive Summary & Environment
This document details the exact environment, data flow, deterministic seeds, artifact locations, and execution commands required to reproduce the clean test benchmark for the JobShield AI production model.

- **OS / Platform:** Windows (x86_64)
- **Python Version:** 3.12 (via virtual environment `.venv\Scripts\python.exe`)
- **Key Dependencies (Pinned in `requirements.txt`):**
  - `scikit-learn==1.9.0`
  - `joblib==1.6.0`
  - `pandas==3.0.5`
  - `numpy==2.5.2`
  - `google-genai==2.22.0`
  - `streamlit==1.63.0`
  - `torch==2.14.0`
  - `transformers==5.16.1`

---

## 2. Data Flow & Leakage-Safe Splitting
The dataset pipeline strictly isolates training, validation, and test partitions to eliminate data leakage across identical postings:

1. **Raw Ingestion:** `data/raw/fake_job_postings.csv` (17,880 rows).
2. **Deduplication & Serialization (`ml/preprocessing.py`):**
   - Exact duplicate rows dropped.
   - Text fields (`title`, `company_profile`, `description`, `requirements`, `benefits`) formatted into `combined_text` with semantic field tags (`TITLE:`, `COMPANY:`, `DESCRIPTION:`, `REQUIREMENTS:`, `BENEFITS:`).
   - Saved to `data/processed/jobshield_clean.csv`.
3. **Grouped Leakage-Safe Splitting (`ml/split_dataset.py`):**
   - `GroupShuffleSplit` groups rows by identical `combined_text`.
   - Split 1 (80% Train, 20% Temp): `random_state=42`.
   - Split 2 (50% Validation, 50% Test of Temp): `random_state=42`.
   - Partition sizes:
     - Train: `data/processed/train.csv` (13,904 rows)
     - Validation: `data/processed/validation.csv` (1,739 rows)
     - Test: `data/processed/test.csv` (1,736 rows)

---

## 3. Production Model Architecture & Calibration
- **Feature Extraction:** TF-IDF (`ngram_range=(1, 2)`, `min_df=2`, `max_df=0.95`, `sublinear_tf=True`, `max_features=100000`), fit ONLY on `train.csv`. Saved as `models/tfidf_vectorizer.joblib`.
- **Base Classifier:** `LogisticRegression(class_weight="balanced", max_iter=2000, solver="liblinear", random_state=42)`. Saved as `models/tfidf_logreg.joblib`.
- **Probability Calibration:**
  - Platt Scaling (`method="sigmoid"`) fitted on validation set using `CalibratedClassifierCV(FrozenEstimator(model), method="sigmoid")`.
  - Saved as `models/calibrated_platt_logreg.joblib`.
- **Decision Threshold:** `0.54` (tuned on the validation split for optimal F1).

---

## 4. Benchmark Verification Target
Evaluating `models/calibrated_platt_logreg.joblib` with `models/tfidf_vectorizer.joblib` on `data/processed/test.csv` at threshold `0.54` strictly yields:

| Metric | Target Value |
| :--- | :--- |
| **Precision** | `0.9663` (96.63%) |
| **Recall** | `0.8037` (80.37%) |
| **F1-Score** | `0.8776` (87.76%) |
| **PR-AUC** | `0.9096` |
| **ROC-AUC** | `0.9865` |
| **Confusion Matrix** | `[[1626, 3], [21, 86]]` |
| **False Positives** | 3 |
| **False Negatives** | 21 |
| **Total Test Samples** | 1,736 |

---

## 5. Step-by-Step Reproduction Commands

### Step A: Setup Virtual Environment & Install Dependencies
```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Step B: (Optional) Data Preprocessing & Leakage-Safe Splitting
*(Existing splits in `data/processed/` are already preserved and must NOT be regenerated unnecessarily)*:
```powershell
# Only if rebuilding from scratch:
.venv\Scripts\python.exe ml\preprocessing.py
.venv\Scripts\python.exe ml\split_dataset.py
```

### Step C: Baseline Model Training & Vectorization
```powershell
.venv\Scripts\python.exe ml\train_baseline.py
```

### Step D: Probability Calibration (Platt Scaling)
```powershell
.venv\Scripts\python.exe ml\calibrate_model.py
```

### Step E: Verify Production Model Benchmark & Error Analysis
```powershell
.venv\Scripts\python.exe ml\error_analysis.py
```

### Step F: Run Regression & Security Tests
```powershell
.venv\Scripts\python.exe ml\test_security_injections.py
.venv\Scripts\python.exe ml\test_comprehensive_security.py
```

### Step G: Launch Application
```powershell
.venv\Scripts\streamlit.exe run frontend\app.py
```

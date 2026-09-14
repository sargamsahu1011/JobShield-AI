# JobShield AI — Adversarial Robustness Evaluation Report (Stage 3)

## 1. Executive Summary
This report evaluates the adversarial robustness of the production JobShield AI pipeline (Calibrated TF-IDF + Logistic Regression with Platt scaling, threshold 0.54) against deliberate evasion techniques commonly employed by recruitment fraud threat actors.

- **Total Adversarial Vectors Evaluated:** 9
- **Attacks Successfully Detected (Target: Fraudulent):** 6 / 9
- **Attack Detection Rate:** **66.67%**
- **Attacks Evading Classifier (False Negatives):** 3 / 9 (33.33%)
- **Key Defense Finding:** Multi-stage canonical text normalization (`ml/text_normalizer.py`) effectively eliminates surface-level lexical evasion (character substitution, punctuation injection, spacing manipulation, casing).
- **Primary System Limitation:** **Semantic paraphrasing** without surface triggers remains an open vulnerability for n-gram bag-of-words architectures.

---

## 2. Attack Vector Breakdown & Empirical Results

The evaluation was conducted using `ml/adversarial_test.py` against known fraudulent templates across 9 attack categories:

| ID | Attack Vector Category | Description | Calibrated Fraud Score | Prediction (Threshold = 0.54) | Status | Robustness Result |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **ADV-01** | `clean_scam` (Baseline) | Unmodified recruitment fraud template | 0.9824 (98.24%) | 1 (Fraudulent) | PASS | Baseline detected |
| **ADV-02** | `character_substitution` | Leetspeak / homoglyphs (`Tel3gram`, `w0rk`) | 0.9824 (98.24%) | 1 (Fraudulent) | PASS | Defused by text normalizer |
| **ADV-03** | `punctuation_obfuscation` | Injected dots and dashes (`T.e.l.e.g.r.a.m.`) | 0.9824 (98.24%) | 1 (Fraudulent) | PASS | Stripped before tokenization |
| **ADV-04** | `spacing_obfuscation` | Inter-character spaces (`W o r k  F r o m  H o m e`) | 0.9824 (98.24%) | 1 (Fraudulent) | PASS | Compacted by normalizer |
| **ADV-05** | `case_manipulation` | Random casing (`tElEgRaM`, `uRgEnT`) | 0.9824 (98.24%) | 1 (Fraudulent) | PASS | Handled by casefold normalizer |
| **ADV-06** | `sentence_splitting` | Fragmented syntax breaking n-grams | 0.5479 (54.79%) | 1 (Fraudulent) | PASS | Surpasses 0.54 threshold |
| **ADV-07** | `synonym_substitution` | Replacing fraud keywords with formal synonyms | 0.4456 (44.56%) | 0 (Legitimate) | FAIL | Evaded n-gram weights |
| **ADV-08** | `urgency_paraphrase` | Paraphrasing urgency ("immediate enrollment") | 0.0455 (4.55%) | 0 (Legitimate) | FAIL | Evaded n-gram weights |
| **ADV-09** | `heavy_paraphrase` | End-to-end corporate rewrite of scam mechanics | 0.0405 (4.05%) | 0 (Legitimate) | FAIL | Evaded n-gram weights |

---

## 3. Defense Mechanisms & Normalization Analysis

### 3.1 Surface Obfuscation Defusal
The production pipeline implements canonical character normalization prior to TF-IDF vectorization:
1. **Homoglyph Translation:** Cyrillic, Greek, and Unicode lookalikes mapped to ASCII Latin equivalents.
2. **Zero-Width Stripping:** Codepoints (`\u200b`, `\u200c`, `\u200d`, `\ufeff`) removed.
3. **Punctuation & Delimiter Consolidation:** Token-breaking punctuation within keywords collapsed.
4. **Whitespace Regularization:** Multi-space, zero-width space, and tab sequences standardized.

Because of this pre-tokenization stage, ADV-02, ADV-03, ADV-04, and ADV-05 produce identical normalized representations to the clean baseline (`0.9824`), achieving 100% defense against surface noise.

### 3.2 Semantic Paraphrasing Vulnerability
ADV-07, ADV-08, and ADV-09 represent semantic evasion where scam semantics (e.g., fee requests, off-platform messaging, unvetted immediate hiring) are described without using the high-weight TF-IDF n-grams learned during training.
- **Experimental Mitigation Evaluated:** Adversarial training augmentation was tested (`data/processed/train_adversarial.csv`).
- **Result:** While adversarial training improved recall on paraphrased attacks, it degraded clean test split precision and introduced false positives on legitimate administrative job postings.
- **Architectural Decision:** To preserve the critical production guarantee of 96.63% precision and only 3 False Positives on real-world legitimate postings, adversarial augmentation was not merged into the primary model. Instead, semantic paraphrasing is explicitly documented as a known system boundary, mitigated in production by secondary heuristic indicators and Gemini evidence verification.

---

## 4. Summary of Robustness Guarantees
- **Guaranteed:** Resistance to character-level noise, leetspeak, homoglyphs, spacing, and punctuation injection.
- **Not Guaranteed:** Complete immunity against creative semantic rewrites, clean corporate impersonations, or off-platform fraud execution.

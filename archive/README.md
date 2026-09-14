# Archive Directory

This directory contains intermediate and exploratory test scripts developed during Stage 5 and earlier evaluation cycles. They have been archived to preserve audit history while keeping the root directory clean.

## Archived Files

1. `test_gemini.py`: Ad-hoc exploratory test script for testing raw Gemini API SDK calls, superseded by production module `ml/gemini_explainer.py`.
2. `test_stage5_evaluation.py`: Intermediate Stage 5 evaluation script, superseded by the canonical `ml/test_comprehensive_security.py` and `ml/run_adversarial_eval.py`.
3. `test_stage5_injections.py`: Exploratory injection generation script, integrated into `ml/test_comprehensive_security.py`.
4. `test_targeted_injections.py`: Exploratory targeted prompt injection test harness, superseded by `ml/test_comprehensive_security.py`.

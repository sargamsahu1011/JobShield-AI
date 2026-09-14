"""NON-CANONICAL DEMO TEST CASES

WARNING: This file is NON-CANONICAL and preserved solely for legacy/interactive sandbox testing.
For the official, binding protected regression tests, refer exclusively to:
    ml/protected_regression_tests.py
"""

# Re-export from the single canonical source of truth
from ml.protected_regression_tests import CANONICAL_PROTECTED_TESTS

# Retain mapping for backwards compatibility with any legacy script runners
TEST_CASES = {name: data["text"] for name, data in CANONICAL_PROTECTED_TESTS.items()}

if __name__ == "__main__":
    print("WARNING: ml/test_cases.py is non-canonical. Use ml/protected_regression_tests.py.")

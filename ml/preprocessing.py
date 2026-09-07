import pandas as pd
from pathlib import Path


# ==============================
# 1. PATHS
# ==============================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "fake_job_postings.csv"
PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "jobshield_clean.csv"


# ==============================
# 2. LOAD DATA
# ==============================

print("Loading dataset...")

df = pd.read_csv(RAW_DATA_PATH)

print(f"Dataset loaded successfully!")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")


# ==============================
# 3. REMOVE DUPLICATES
# ==============================

before = len(df)

df = df.drop_duplicates()

after = len(df)

print(f"Duplicates removed: {before - after}")


# ==============================
# 4. HANDLE MISSING VALUES
# ==============================

text_columns = [
    "title",
    "company_profile",
    "description",
    "requirements",
    "benefits"
]

categorical_columns = [
    "location",
    "department",
    "employment_type",
    "required_experience",
    "required_education",
    "industry",
    "function",
    "salary_range"
]


# Text fields → empty string
for column in text_columns:
    df[column] = df[column].fillna("")


# Categorical fields → Unknown
for column in categorical_columns:
    df[column] = df[column].fillna("Unknown")


# ==============================
# 5. CREATE COMBINED TEXT
# ==============================

df["combined_text"] = (
    "TITLE: " + df["title"] +
    " COMPANY: " + df["company_profile"] +
    " DESCRIPTION: " + df["description"] +
    " REQUIREMENTS: " + df["requirements"] +
    " BENEFITS: " + df["benefits"]
)


# ==============================
# 6. BASIC TEXT FEATURES
# ==============================

df["text_length"] = df["combined_text"].str.len()

df["word_count"] = (
    df["combined_text"]
    .str.split()
    .str.len()
)


# ==============================
# 7. SAVE PROCESSED DATA
# ==============================

PROCESSED_DATA_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(PROCESSED_DATA_PATH, index=False)

print("\nPreprocessing completed successfully!")

print(f"Final rows: {len(df)}")
print(f"Final columns: {len(df.columns)}")

print(f"\nSaved to:")
print(PROCESSED_DATA_PATH)
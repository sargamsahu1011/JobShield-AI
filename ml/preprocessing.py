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


def serialize_job_posting(row) -> str:
    """
    Serialize job posting fields into labeled text for modeling.
    Empty/NaN fields are omitted entirely so empty labeled headers
    (e.g., 'COMPANY: DESCRIPTION:') are never emitted.
    """
    parts = []
    field_labels = [
        ("title", "TITLE:"),
        ("company_profile", "COMPANY:"),
        ("description", "DESCRIPTION:"),
        ("requirements", "REQUIREMENTS:"),
        ("benefits", "BENEFITS:"),
    ]
    for col, label in field_labels:
        val = row.get(col, "")
        if pd.notna(val):
            val_str = str(val).strip()
            if val_str and val_str.lower() != "nan" and val_str.lower() != "unknown":
                parts.append(f"{label} {val_str}")
    return " ".join(parts).strip()


# ==============================
# 5. CREATE COMBINED TEXT
# ==============================

df["combined_text"] = df.apply(serialize_job_posting, axis=1)


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
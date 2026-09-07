import pandas as pd
import re
from pathlib import Path

# -----------------------------------
# Paths
# -----------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "jobshield_clean.csv"

# -----------------------------------
# Load data
# -----------------------------------
df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("JOBSHIELD DATA QUALITY AUDIT")
print("=" * 60)

print(f"\nDataset shape: {df.shape}")

# -----------------------------------
# Text columns
# -----------------------------------
text_columns = [
    "title",
    "company_profile",
    "description",
    "requirements",
    "benefits",
    "combined_text"
]

# -----------------------------------
# 1. Empty text
# -----------------------------------
print("\n" + "=" * 60)
print("1. EMPTY TEXT CHECK")
print("=" * 60)

for col in text_columns:
    empty_count = (
        df[col]
        .fillna("")
        .astype(str)
        .str.strip()
        .eq("")
        .sum()
    )

    print(f"{col:20} : {empty_count}")

# -----------------------------------
# 2. Very short postings
# -----------------------------------
print("\n" + "=" * 60)
print("2. VERY SHORT JOB POSTINGS")
print("=" * 60)

short_jobs = df[df["combined_text"].str.len() < 100]

print(f"Jobs with <100 characters: {len(short_jobs)}")

if len(short_jobs) > 0:
    print("\nExamples:")
    print(
        short_jobs[
            ["job_id", "title", "combined_text", "fraudulent"]
        ].head(5).to_string(index=False)
    )

# -----------------------------------
# 3. HTML detection
# -----------------------------------
print("\n" + "=" * 60)
print("3. HTML DETECTION")
print("=" * 60)

html_pattern = r"<[^>]+>"

html_count = (
    df["combined_text"]
    .fillna("")
    .astype(str)
    .str.contains(html_pattern, regex=True)
    .sum()
)

print(f"Jobs containing HTML tags: {html_count}")

# -----------------------------------
# 4. URL detection
# -----------------------------------
print("\n" + "=" * 60)
print("4. URL DETECTION")
print("=" * 60)

url_pattern = r"(https?://|www\.)\S+"

url_count = (
    df["combined_text"]
    .fillna("")
    .astype(str)
    .str.contains(url_pattern, regex=True)
    .sum()
)

print(f"Jobs containing URLs: {url_count}")

# -----------------------------------
# 5. Email detection
# -----------------------------------
print("\n" + "=" * 60)
print("5. EMAIL DETECTION")
print("=" * 60)

email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"

email_count = (
    df["combined_text"]
    .fillna("")
    .astype(str)
    .str.contains(email_pattern, regex=True)
    .sum()
)

print(f"Jobs containing email addresses: {email_count}")

# -----------------------------------
# 6. Phone number detection
# -----------------------------------
print("\n" + "=" * 60)
print("6. PHONE NUMBER DETECTION")
print("=" * 60)

phone_pattern = r"(?<!\d)(?:\+?\d[\d\s().-]{8,}\d)(?!\d)"

phone_count = (
    df["combined_text"]
    .fillna("")
    .astype(str)
    .str.contains(phone_pattern, regex=True)
    .sum()
)

print(f"Jobs containing possible phone numbers: {phone_count}")

# -----------------------------------
# 7. Excessive punctuation
# -----------------------------------
print("\n" + "=" * 60)
print("7. EXCESSIVE PUNCTUATION")
print("=" * 60)

exclamation_count = (
    df["combined_text"]
    .fillna("")
    .astype(str)
    .str.count("!")
)

print(f"Jobs with 5+ exclamation marks: {(exclamation_count >= 5).sum()}")

# -----------------------------------
# 8. Fraud distribution
# -----------------------------------
print("\n" + "=" * 60)
print("8. TARGET DISTRIBUTION")
print("=" * 60)

print(df["fraudulent"].value_counts())

print("\nPercentage:")
print(
    (df["fraudulent"].value_counts(normalize=True) * 100)
    .round(2)
)

print("\n" + "=" * 60)
print("AUDIT COMPLETED")
print("=" * 60)
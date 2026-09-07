import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# -----------------------------------
# Paths
# -----------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "jobshield_clean.csv"


# -----------------------------------
# Load dataset
# -----------------------------------
print("Loading dataset...")

df = pd.read_csv(DATA_PATH)

print(f"Dataset shape: {df.shape}")


# -----------------------------------
# Exact duplicate check
# -----------------------------------
print("\n" + "=" * 60)
print("1. EXACT DUPLICATE CHECK")
print("=" * 60)

duplicate_text = df["combined_text"].duplicated().sum()

print(f"Duplicate combined_text values: {duplicate_text}")


# -----------------------------------
# Duplicate descriptions
# -----------------------------------
print("\n" + "=" * 60)
print("2. DUPLICATE DESCRIPTION CHECK")
print("=" * 60)

duplicate_description = (
    df["description"]
    .fillna("")
    .duplicated()
    .sum()
)

print(f"Duplicate descriptions: {duplicate_description}")


# -----------------------------------
# Duplicate company + description
# -----------------------------------
print("\n" + "=" * 60)
print("3. COMPANY + DESCRIPTION DUPLICATES")
print("=" * 60)

company_description = (
    df["company_profile"].fillna("").astype(str)
    + " || "
    + df["description"].fillna("").astype(str)
)

duplicate_company_description = company_description.duplicated().sum()

print(
    f"Duplicate company-profile + description combinations: "
    f"{duplicate_company_description}"
)


# -----------------------------------
# Near-duplicate analysis
# -----------------------------------
print("\n" + "=" * 60)
print("4. NEAR-DUPLICATE TEXT ANALYSIS")
print("=" * 60)

# Use a sample so the pairwise calculation remains manageable.
sample_size = min(3000, len(df))

sample_df = df.sample(
    n=sample_size,
    random_state=42
).reset_index(drop=True)

vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english",
    max_features=10000,
    ngram_range=(1, 2)
)

tfidf_matrix = vectorizer.fit_transform(
    sample_df["combined_text"]
)

similarity_matrix = cosine_similarity(tfidf_matrix)


# Remove self-similarity
import numpy as np

np.fill_diagonal(similarity_matrix, 0)


# -----------------------------------
# Similarity thresholds
# -----------------------------------
thresholds = [0.90, 0.95, 0.98]

for threshold in thresholds:

    count = np.sum(similarity_matrix >= threshold)

    # Each pair appears twice (A-B and B-A)
    pair_count = count // 2

    print(
        f"Pairs with cosine similarity >= {threshold}: "
        f"{pair_count}"
    )


# -----------------------------------
# Show highly similar examples
# -----------------------------------
threshold = 0.95

rows, cols = np.where(similarity_matrix >= threshold)

pairs = []

for i, j in zip(rows, cols):

    if i < j:

        pairs.append(
            (
                i,
                j,
                similarity_matrix[i, j]
            )
        )


pairs = sorted(
    pairs,
    key=lambda x: x[2],
    reverse=True
)


print("\nTop near-duplicate pairs:")

for i, j, similarity in pairs[:10]:

    print("\n" + "-" * 60)

    print(f"Similarity: {similarity:.4f}")

    print(
        f"Job 1 ID: {sample_df.iloc[i]['job_id']}"
    )

    print(
        f"Job 2 ID: {sample_df.iloc[j]['job_id']}"
    )

    print(
        f"Job 1 label: {sample_df.iloc[i]['fraudulent']}"
    )

    print(
        f"Job 2 label: {sample_df.iloc[j]['fraudulent']}"
    )

    print(
        f"Job 1 title: {sample_df.iloc[i]['title']}"
    )

    print(
        f"Job 2 title: {sample_df.iloc[j]['title']}"
    )


print("\n" + "=" * 60)
print("DUPLICATE AUDIT COMPLETED")
print("=" * 60)
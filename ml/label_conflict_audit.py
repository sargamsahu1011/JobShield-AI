import pandas as pd

print("Loading dataset...")

df = pd.read_csv("data/processed/jobshield_clean.csv")

print("Dataset shape:", df.shape)

# ============================================================
# 1. EXACT TEXT DUPLICATES WITH DIFFERENT LABELS
# ============================================================

print("\n" + "=" * 60)
print("1. EXACT DUPLICATES WITH CONFLICTING LABELS")
print("=" * 60)

conflicts = (
    df.groupby("combined_text")["fraudulent"]
    .nunique()
)

conflicting_groups = conflicts[conflicts > 1]

print("Conflicting duplicate groups:", len(conflicting_groups))

if len(conflicting_groups) > 0:
    print("\nExamples:")

    for text in conflicting_groups.index[:10]:

        rows = df[df["combined_text"] == text][
            ["job_id", "title", "fraudulent"]
        ]

        print("\n" + "-" * 50)
        print(rows.to_string(index=False))


# ============================================================
# 2. DUPLICATE DESCRIPTIONS WITH DIFFERENT LABELS
# ============================================================

print("\n" + "=" * 60)
print("2. DUPLICATE DESCRIPTIONS WITH CONFLICTING LABELS")
print("=" * 60)

description_conflicts = (
    df.groupby("description")["fraudulent"]
    .nunique()
)

description_conflicting_groups = description_conflicts[
    description_conflicts > 1
]

print(
    "Conflicting description groups:",
    len(description_conflicting_groups)
)

if len(description_conflicting_groups) > 0:

    print("\nExamples:")

    for description in description_conflicting_groups.index[:10]:

        rows = df[df["description"] == description][
            ["job_id", "title", "fraudulent"]
        ]

        print("\n" + "-" * 50)
        print(rows.to_string(index=False))


# ============================================================
# 3. COMPANY + DESCRIPTION CONFLICTS
# ============================================================

print("\n" + "=" * 60)
print("3. COMPANY + DESCRIPTION CONFLICTS")
print("=" * 60)

company_desc_conflicts = (
    df.groupby(["company_profile", "description"])["fraudulent"]
    .nunique()
)

company_desc_conflicting_groups = company_desc_conflicts[
    company_desc_conflicts > 1
]

print(
    "Conflicting company + description groups:",
    len(company_desc_conflicting_groups)
)


# ============================================================
# 4. SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("CONFLICT AUDIT SUMMARY")
print("=" * 60)

print("Exact-text conflicting groups:",
      len(conflicting_groups))

print("Description conflicting groups:",
      len(description_conflicting_groups))

print("Company + description conflicting groups:",
      len(company_desc_conflicting_groups))

print("\nAUDIT COMPLETED")
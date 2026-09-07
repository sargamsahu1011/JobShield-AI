import pandas as pd
from sklearn.model_selection import GroupShuffleSplit

print("=" * 60)
print("JOBSHIELD LEAKAGE-SAFE DATA SPLIT")
print("=" * 60)

# ------------------------------------------------------------
# 1. LOAD DATA
# ------------------------------------------------------------

INPUT_FILE = "data/processed/jobshield_clean.csv"

df = pd.read_csv(INPUT_FILE)

print("\nDataset shape:", df.shape)

# ------------------------------------------------------------
# 2. CREATE GROUPS
# ------------------------------------------------------------
# Identical combined_text values belong to the same group.
# This prevents duplicate postings from appearing in
# different train/validation/test sets.

df["group_id"] = (
    df["combined_text"]
    .fillna("")
    .astype(str)
    .str.strip()
    .factorize()[0]
)

print("Unique text groups:", df["group_id"].nunique())

# ------------------------------------------------------------
# 3. FIRST SPLIT
# ------------------------------------------------------------
# 80% TRAIN
# 20% TEMPORARY
#
# GroupShuffleSplit ensures that one group cannot be
# distributed across both sets.

gss1 = GroupShuffleSplit(
    n_splits=1,
    test_size=0.20,
    random_state=42
)

train_idx, temp_idx = next(
    gss1.split(
        df,
        y=df["fraudulent"],
        groups=df["group_id"]
    )
)

train_df = df.iloc[train_idx].copy()
temp_df = df.iloc[temp_idx].copy()

# ------------------------------------------------------------
# 4. SECOND SPLIT
# ------------------------------------------------------------
# Temporary set:
# 10% VALIDATION
# 10% TEST
#
# Therefore split temp 50/50.

gss2 = GroupShuffleSplit(
    n_splits=1,
    test_size=0.50,
    random_state=42
)

val_idx, test_idx = next(
    gss2.split(
        temp_df,
        y=temp_df["fraudulent"],
        groups=temp_df["group_id"]
    )
)

val_df = temp_df.iloc[val_idx].copy()
test_df = temp_df.iloc[test_idx].copy()

# ------------------------------------------------------------
# 5. REMOVE INTERNAL GROUP COLUMN
# ------------------------------------------------------------

train_df = train_df.drop(columns=["group_id"])
val_df = val_df.drop(columns=["group_id"])
test_df = test_df.drop(columns=["group_id"])

# ------------------------------------------------------------
# 6. SAVE SPLITS
# ------------------------------------------------------------

train_df.to_csv(
    "data/processed/train.csv",
    index=False
)

val_df.to_csv(
    "data/processed/validation.csv",
    index=False
)

test_df.to_csv(
    "data/processed/test.csv",
    index=False
)

# ------------------------------------------------------------
# 7. DISPLAY RESULTS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("SPLIT SIZES")
print("=" * 60)

print("Train      :", train_df.shape)
print("Validation :", val_df.shape)
print("Test       :", test_df.shape)

# ------------------------------------------------------------
# 8. TARGET DISTRIBUTION
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("TARGET DISTRIBUTION")
print("=" * 60)

for name, data in [
    ("TRAIN", train_df),
    ("VALIDATION", val_df),
    ("TEST", test_df)
]:

    counts = data["fraudulent"].value_counts()
    percentages = data["fraudulent"].value_counts(
        normalize=True
    ) * 100

    print(f"\n{name}")

    print(
        pd.DataFrame({
            "count": counts,
            "percentage": percentages.round(2)
        })
    )

# ------------------------------------------------------------
# 9. VERIFY DUPLICATE GROUP LEAKAGE
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("LEAKAGE CHECK")
print("=" * 60)

# Recreate group IDs from the original dataset
# and check whether any exact combined_text appears
# across different splits.

def get_groups(data):
    return set(
        data["combined_text"]
        .fillna("")
        .astype(str)
        .str.strip()
    )


train_groups = get_groups(train_df)
val_groups = get_groups(val_df)
test_groups = get_groups(test_df)

train_val_overlap = train_groups & val_groups
train_test_overlap = train_groups & test_groups
val_test_overlap = val_groups & test_groups

print("Train ↔ Validation overlap:",
      len(train_val_overlap))

print("Train ↔ Test overlap:",
      len(train_test_overlap))

print("Validation ↔ Test overlap:",
      len(val_test_overlap))

# ------------------------------------------------------------
# 10. FINAL STATUS
# ------------------------------------------------------------

if (
    len(train_val_overlap) == 0
    and len(train_test_overlap) == 0
    and len(val_test_overlap) == 0
):
    print("\n✅ NO EXACT TEXT LEAKAGE DETECTED")
else:
    print("\n⚠️ TEXT LEAKAGE DETECTED")

print("\nFiles created:")
print("  data/processed/train.csv")
print("  data/processed/validation.csv")
print("  data/processed/test.csv")

print("\n" + "=" * 60)
print("SPLIT COMPLETED")
print("=" * 60)
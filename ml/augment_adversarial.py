import pandas as pd
import os

TRAIN = "data/processed/train.csv"
OUTPUT = "data/processed/train_adversarial.csv"

df = pd.read_csv(TRAIN)

fraud = df[df["fraudulent"] == 1].copy()

variants = []

for _, row in fraud.iterrows():
    text = str(row["combined_text"])

    # Semantic/lexical transformations
    v1 = text.replace("urgent", "immediate")
    v2 = text.replace("telegram", "messaging application")
    v3 = text.replace("pay", "submit a payment")
    v4 = text.replace("fee", "registration charge")
    v5 = text.replace("bank account", "financial account")
    v6 = text.replace("no experience", "previous experience is unnecessary")

    for variant in [v1, v2, v3, v4, v5, v6]:
        if variant != text:
            new_row = row.copy()
            new_row["combined_text"] = variant
            variants.append(new_row)

augmented = pd.DataFrame(variants)

# Avoid accidental duplicates
augmented = augmented.drop_duplicates(
    subset=["combined_text"]
)

final_df = pd.concat(
    [df, augmented],
    ignore_index=True
)

final_df.to_csv(
    OUTPUT,
    index=False
)

print("Original training rows :", len(df))
print("Original fraud rows    :", len(fraud))
print("Adversarial rows added :", len(augmented))
print("Final training rows    :", len(final_df))
print("Final fraud rows       :", final_df["fraudulent"].sum())
print("Saved                  :", OUTPUT)
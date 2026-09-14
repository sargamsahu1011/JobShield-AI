import json
import os
import matplotlib.pyplot as plt
import numpy as np

METRICS_PATH = "models/calibration_metrics.json"
OUTPUT_PATH = "reports/calibration_reliability.png"


def extract_curve(table):
    x = []
    y = []

    for row in table:
        if row["count"] > 0:
            x.append(row["mean_predicted"])
            y.append(row["empirical_positive_rate"])

    return np.array(x), np.array(y)


with open(METRICS_PATH, "r") as f:
    metrics = json.load(f)

uncal_x, uncal_y = extract_curve(
    metrics["uncalibrated"]["reliability_table_test"]
)

platt_x, platt_y = extract_curve(
    metrics["platt_scaling"]["reliability_table_test"]
)

iso_x, iso_y = extract_curve(
    metrics["isotonic_regression"]["reliability_table_test"]
)

plt.figure(figsize=(8, 6))

plt.plot([0, 1], [0, 1], "--", label="Perfect calibration")
plt.plot(
    uncal_x,
    uncal_y,
    marker="o",
    label="Uncalibrated TF-IDF"
)
plt.plot(
    platt_x,
    platt_y,
    marker="o",
    label="Platt scaling"
)
plt.plot(
    iso_x,
    iso_y,
    marker="o",
    label="Isotonic regression"
)

plt.xlabel("Mean predicted probability")
plt.ylabel("Empirical fraud rate")
plt.title("JobShield AI — Calibration Reliability Diagram")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

os.makedirs("reports", exist_ok=True)
plt.savefig(OUTPUT_PATH, dpi=200)
plt.close()

print(f"[+] Saved reliability diagram to: {OUTPUT_PATH}")
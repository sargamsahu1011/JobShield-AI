import json
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


# ==========================================
# PATHS
# ==========================================

MODEL_PATH = "models/jobshield-distilbert-final"


# ==========================================
# LOAD THRESHOLD
# ==========================================

with open(f"{MODEL_PATH}/threshold_config.json", "r") as f:
    config = json.load(f)

THRESHOLD = config["final_threshold"]

print("Threshold:", THRESHOLD)


# ==========================================
# LOAD TOKENIZER
# ==========================================

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

print("Tokenizer loaded successfully!")


# ==========================================
# LOAD MODEL
# ==========================================

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_PATH
)

model.eval()

print("Model loaded successfully!")


# ==========================================
# PREDICTION FUNCTION
# ==========================================

def predict_job(job_text):

    inputs = tokenizer(
        job_text,
        return_tensors="pt",
        truncation=True,
        max_length=256
    )

    with torch.no_grad():

        outputs = model(**inputs)

        probabilities = torch.softmax(
            outputs.logits,
            dim=1
        )

    fraud_probability = probabilities[0][1].item()

    prediction = int(fraud_probability >= THRESHOLD)

    return fraud_probability, prediction


# ==========================================
# TEST JOB
# ==========================================

test_job = """
We are looking for a work-from-home data entry employee.
No experience required.

Earn $5000 per week.
You will receive guaranteed employment immediately.

To complete your registration, send your bank account
details and pay a small refundable processing fee.

Contact our recruiter through Telegram to continue.
"""


fraud_probability, prediction = predict_job(test_job)


print("\n==========================================")
print("JOBSHIELD TEST PREDICTION")
print("==========================================")

print("Fraud Probability:", round(fraud_probability, 4))
print("Threshold:", THRESHOLD)

if prediction == 1:
    print("Prediction: FRAUDULENT / HIGH RISK")
else:
    print("Prediction: LEGITIMATE / LOW RISK")
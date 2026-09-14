import sys
import os
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml.predict import predict_job


ATTACKS = [
    {
        "id": "clean_scam",
        "category": "baseline",
        "text": """
        Work from home data entry job.
        Earn $5000 per week.
        No experience required.
        Pay a refundable registration fee to begin.
        Send your bank account details to complete verification.
        Contact our recruiter through Telegram.
        """
    },

    {
        "id": "character_substitution",
        "category": "obfuscation",
        "text": """
        Work from home data entry job.
        Earn $5000 per week.
        No experience required.
        Pay a refundable registration fee to begin.
        Send your bank account details to complete verification.
        Contact our recruiter through Tel3gram.
        """
    },

    {
        "id": "punctuation_obfuscation",
        "category": "obfuscation",
        "text": """
        Work from home data entry job.
        Earn $5000 per week.
        No experience required.
        Pay a refundable registration fee to begin.
        Send your bank account details to complete verification.
        Contact our recruiter through T.e.l.e.g.r.a.m.
        """
    },

    {
        "id": "spacing_obfuscation",
        "category": "obfuscation",
        "text": """
        Work from home data entry job.
        Earn $5000 per week.
        No experience required.
        Pay a refundable registration fee to begin.
        Send your bank account details to complete verification.
        Contact our recruiter through T e l e g r a m.
        """
    },

    {
        "id": "case_manipulation",
        "category": "case",
        "text": """
        WORK FROM HOME DATA ENTRY JOB.
        EARN $5000 PER WEEK.
        NO EXPERIENCE REQUIRED.
        PAY A REFUNDABLE REGISTRATION FEE TO BEGIN.
        SEND YOUR BANK ACCOUNT DETAILS TO COMPLETE VERIFICATION.
        CONTACT OUR RECRUITER THROUGH TELEGRAM.
        """
    },

    {
        "id": "sentence_splitting",
        "category": "sentence_split",
        "text": """
        This is a work from home opportunity.
        You can earn $5000 per week.
        There is no experience requirement.
        To complete registration you should pay a small fee.
        Your bank information will be required for verification.
        Our recruiter will continue the conversation through Telegram.
        """
    },

    {
        "id": "synonym_substitution",
        "category": "synonym",
        "text": """
        Remote data entry opportunity.
        Receive $5000 every week.
        Previous experience is unnecessary.
        Submit a small refundable registration payment.
        Provide your banking information for identity confirmation.
        Message our hiring representative on Telegram.
        """
    },

    {
        "id": "urgency_paraphrase",
        "category": "paraphrase",
        "text": """
        Remote employment opportunity.
        Immediate hiring with unusually high weekly compensation.
        Applicants can start without prior experience.
        Complete the onboarding process by making a refundable payment.
        Provide financial account information for verification.
        Continue the recruitment process through Telegram.
        """
    },

    {
        "id": "heavy_paraphrase",
        "category": "paraphrase",
        "text": """
        A remote position is available for people interested in simple
        online administrative work. The company claims that selected
        applicants can make several thousand dollars each week without
        previous employment experience.

        Before starting, applicants are instructed to transfer a small
        amount of money as part of the registration process and provide
        personal banking information.

        Further communication with the supposed recruiter takes place
        using an external messaging application.
        """
    }
]


def main():
    results = []

    print("=" * 70)
    print("JOBSHIELD — ADVERSARIAL ROBUSTNESS TEST")
    print("=" * 70)

    for attack in ATTACKS:
        try:
            probability, prediction = predict_job(attack["text"])

            results.append({
                "id": attack["id"],
                "category": attack["category"],
                "probability": probability,
                "prediction": prediction,
                "correct": prediction == 1
            })

            label = (
                "FRAUDULENT"
                if prediction == 1
                else
                "LEGITIMATE"
            )

            status = (
                "PASS"
                if prediction == 1
                else
                "FAIL"
            )

            print(
                f"\n[{status}] "
                f"{attack['id']}"
            )
            print(
                f"Category    : {attack['category']}"
            )
            print(
                f"Probability : {probability:.4f}"
            )
            print(
                f"Prediction  : {label}"
            )

        except Exception as e:
            print(
                f"\n[ERROR] {attack['id']}: {e}"
            )

    results_df = pd.DataFrame(results)

    os.makedirs("reports", exist_ok=True)

    output_path = (
        "reports/adversarial_results.csv"
    )

    results_df.to_csv(
        output_path,
        index=False
    )

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    if len(results_df) > 0:
        passed = results_df["correct"].sum()
        total = len(results_df)

        print(
            f"Detected correctly : "
            f"{passed}/{total}"
        )

        print(
            f"Attack detection rate : "
            f"{passed / total:.2%}"
        )

        print("\nResults by category:")

        category_summary = (
            results_df
            .groupby("category")["correct"]
            .agg(["count", "sum"])
        )

        category_summary["detection_rate"] = (
            category_summary["sum"]
            / category_summary["count"]
        )

        print(category_summary)

    print(
        f"\nSaved results to: {output_path}"
    )


if __name__ == "__main__":
    main()
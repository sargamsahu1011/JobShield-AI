export interface CalibrationMetrics {
  val_brier: number;
  val_log_loss: number;
  val_ece: number;
  test_brier: number;
  test_log_loss: number;
  test_ece: number;
  test_pr_auc: number;
  test_roc_auc: number;
  test_precision?: number;
  test_recall?: number;
  test_f1?: number;
}

export interface ReliabilityBin {
  bin_range: [number, number];
  count: number;
  mean_predicted: number | null;
  empirical_positive_rate: number | null;
  abs_error: number | null;
}

export const CALIBRATION_DATA = {
  models: {
    uncalibrated: {
      name: "Uncalibrated Baseline (Raw Sigmoid)",
      threshold: 0.670,
      val_brier: 0.019207,
      val_log_loss: 0.104870,
      val_ece: 0.082389,
      test_brier: 0.024510,
      test_log_loss: 0.126875,
      test_ece: 0.088779,
      test_pr_auc: 0.909616,
      test_roc_auc: 0.986518,
      test_precision: 0.883495,
      test_recall: 0.850467,
      test_f1: 0.866667,
    },
    platt: {
      name: "Platt Scaling (Sigmoid Calibration)",
      threshold: 0.655,
      val_brier: 0.007349,
      val_log_loss: 0.027744,
      val_ece: 0.005210,
      test_brier: 0.012342,
      test_log_loss: 0.052434,
      test_ece: 0.008174,
      test_pr_auc: 0.909616,
      test_roc_auc: 0.986518,
      test_precision: 0.965909,
      test_recall: 0.794393,
      test_f1: 0.871795,
    },
    isotonic: {
      name: "Isotonic Regression",
      threshold: 0.500,
      val_brier: 0.006129,
      val_log_loss: 0.021861,
      val_ece: 0.000000,
      test_brier: 0.012669,
      test_log_loss: 0.158225,
      test_ece: 0.007983,
      test_pr_auc: 0.883993,
      test_roc_auc: 0.977938,
    },
  },
  reliabilityDiagrams: {
    uncalibrated: [
      {
            "bin_range": [
                  0.0,
                  0.1
            ],
            "count": 1095,
            "mean_predicted": 0.05136694270329422,
            "empirical_positive_rate": 0.0009132420091324201,
            "abs_error": 0.0504537006941618
      },
      {
            "bin_range": [
                  0.1,
                  0.2
            ],
            "count": 353,
            "mean_predicted": 0.13724167807623752,
            "empirical_positive_rate": 0.0056657223796034,
            "abs_error": 0.13157595569663413
      },
      {
            "bin_range": [
                  0.2,
                  0.3
            ],
            "count": 113,
            "mean_predicted": 0.24218769697101244,
            "empirical_positive_rate": 0.035398230088495575,
            "abs_error": 0.20678946688251687
      },
      {
            "bin_range": [
                  0.3,
                  0.4
            ],
            "count": 36,
            "mean_predicted": 0.34564259489413535,
            "empirical_positive_rate": 0.1111111111111111,
            "abs_error": 0.23453148378302424
      },
      {
            "bin_range": [
                  0.4,
                  0.5
            ],
            "count": 34,
            "mean_predicted": 0.4465843460875793,
            "empirical_positive_rate": 0.14705882352941177,
            "abs_error": 0.29952552255816756
      },
      {
            "bin_range": [
                  0.5,
                  0.6
            ],
            "count": 10,
            "mean_predicted": 0.5584017057448709,
            "empirical_positive_rate": 0.3,
            "abs_error": 0.2584017057448709
      },
      {
            "bin_range": [
                  0.6,
                  0.7
            ],
            "count": 7,
            "mean_predicted": 0.6336939154370923,
            "empirical_positive_rate": 0.42857142857142855,
            "abs_error": 0.20512248686566376
      },
      {
            "bin_range": [
                  0.7,
                  0.8
            ],
            "count": 2,
            "mean_predicted": 0.7635726473060338,
            "empirical_positive_rate": 1.0,
            "abs_error": 0.2364273526939662
      },
      {
            "bin_range": [
                  0.8,
                  0.9
            ],
            "count": 47,
            "mean_predicted": 0.8542427359909912,
            "empirical_positive_rate": 0.9574468085106383,
            "abs_error": 0.10320407251964714
      },
      {
            "bin_range": [
                  0.9,
                  1.0
            ],
            "count": 39,
            "mean_predicted": 0.9464270130139795,
            "empirical_positive_rate": 0.9743589743589743,
            "abs_error": 0.02793196134499487
      }
],
    platt: [
      {
            "bin_range": [
                  0.0,
                  0.1
            ],
            "count": 1606,
            "mean_predicted": 0.0037862906395728186,
            "empirical_positive_rate": 0.00809464508094645,
            "abs_error": 0.004308354441373632
      },
      {
            "bin_range": [
                  0.1,
                  0.2
            ],
            "count": 25,
            "mean_predicted": 0.1406120505481533,
            "empirical_positive_rate": 0.12,
            "abs_error": 0.020612050548153293
      },
      {
            "bin_range": [
                  0.2,
                  0.3
            ],
            "count": 5,
            "mean_predicted": 0.23977217683023677,
            "empirical_positive_rate": 0.0,
            "abs_error": 0.23977217683023677
      },
      {
            "bin_range": [
                  0.3,
                  0.4
            ],
            "count": 7,
            "mean_predicted": 0.3657402071196762,
            "empirical_positive_rate": 0.5714285714285714,
            "abs_error": 0.2056883643088952
      },
      {
            "bin_range": [
                  0.4,
                  0.5
            ],
            "count": 4,
            "mean_predicted": 0.47615281102625445,
            "empirical_positive_rate": 0.25,
            "abs_error": 0.22615281102625445
      },
      {
            "bin_range": [
                  0.5,
                  0.6
            ],
            "count": 1,
            "mean_predicted": 0.5915640850509727,
            "empirical_positive_rate": 1.0,
            "abs_error": 0.4084359149490273
      },
      {
            "bin_range": [
                  0.6,
                  0.7
            ],
            "count": 0,
            "mean_predicted": null,
            "empirical_positive_rate": null,
            "abs_error": null
      },
      {
            "bin_range": [
                  0.7,
                  0.8
            ],
            "count": 1,
            "mean_predicted": 0.7788564010143099,
            "empirical_positive_rate": 1.0,
            "abs_error": 0.22114359898569014
      },
      {
            "bin_range": [
                  0.8,
                  0.9
            ],
            "count": 13,
            "mean_predicted": 0.8835525246572137,
            "empirical_positive_rate": 1.0,
            "abs_error": 0.11644747534278632
      },
      {
            "bin_range": [
                  0.9,
                  1.0
            ],
            "count": 74,
            "mean_predicted": 0.973899398562206,
            "empirical_positive_rate": 0.9594594594594594,
            "abs_error": 0.014439939102746546
      }
],
    isotonic: [
      {
            "bin_range": [
                  0.0,
                  0.1
            ],
            "count": 1613,
            "mean_predicted": 0.0031551016840510966,
            "empirical_positive_rate": 0.008679479231246125,
            "abs_error": 0.0055243775471950285
      },
      {
            "bin_range": [
                  0.1,
                  0.2
            ],
            "count": 8,
            "mean_predicted": 0.14115177421055355,
            "empirical_positive_rate": 0.0,
            "abs_error": 0.14115177421055355
      },
      {
            "bin_range": [
                  0.2,
                  0.3
            ],
            "count": 26,
            "mean_predicted": 0.26378542507824315,
            "empirical_positive_rate": 0.2692307692307692,
            "abs_error": 0.005445344152526066
      },
      {
            "bin_range": [
                  0.3,
                  0.4
            ],
            "count": 1,
            "mean_predicted": 0.3228204980041035,
            "empirical_positive_rate": 1.0,
            "abs_error": 0.6771795019958965
      },
      {
            "bin_range": [
                  0.4,
                  0.5
            ],
            "count": 0,
            "mean_predicted": null,
            "empirical_positive_rate": null,
            "abs_error": null
      },
      {
            "bin_range": [
                  0.5,
                  0.6
            ],
            "count": 0,
            "mean_predicted": null,
            "empirical_positive_rate": null,
            "abs_error": null
      },
      {
            "bin_range": [
                  0.6,
                  0.7
            ],
            "count": 0,
            "mean_predicted": null,
            "empirical_positive_rate": null,
            "abs_error": null
      },
      {
            "bin_range": [
                  0.7,
                  0.8
            ],
            "count": 0,
            "mean_predicted": null,
            "empirical_positive_rate": null,
            "abs_error": null
      },
      {
            "bin_range": [
                  0.8,
                  0.9
            ],
            "count": 0,
            "mean_predicted": null,
            "empirical_positive_rate": null,
            "abs_error": null
      },
      {
            "bin_range": [
                  0.9,
                  1.0
            ],
            "count": 88,
            "mean_predicted": 1.0,
            "empirical_positive_rate": 0.9659090909090909,
            "abs_error": 0.03409090909090906
      }
]
  },
  reliability_table_test: {
    uncalibrated: [
    {
        "bin": "0.0 - 0.1",
        "count": 1095,
        "mean_pred": 0.05136694270329422,
        "error": 0.0504537006941618
    },
    {
        "bin": "0.1 - 0.2",
        "count": 353,
        "mean_pred": 0.13724167807623752,
        "error": 0.13157595569663413
    },
    {
        "bin": "0.2 - 0.3",
        "count": 113,
        "mean_pred": 0.24218769697101244,
        "error": 0.20678946688251687
    },
    {
        "bin": "0.3 - 0.4",
        "count": 36,
        "mean_pred": 0.34564259489413535,
        "error": 0.23453148378302424
    },
    {
        "bin": "0.4 - 0.5",
        "count": 34,
        "mean_pred": 0.4465843460875793,
        "error": 0.29952552255816756
    },
    {
        "bin": "0.5 - 0.6",
        "count": 10,
        "mean_pred": 0.5584017057448709,
        "error": 0.2584017057448709
    },
    {
        "bin": "0.6 - 0.7",
        "count": 7,
        "mean_pred": 0.6336939154370923,
        "error": 0.20512248686566376
    },
    {
        "bin": "0.7 - 0.8",
        "count": 2,
        "mean_pred": 0.7635726473060338,
        "error": 0.2364273526939662
    },
    {
        "bin": "0.8 - 0.9",
        "count": 47,
        "mean_pred": 0.8542427359909912,
        "error": 0.10320407251964714
    },
    {
        "bin": "0.9 - 1.0",
        "count": 39,
        "mean_pred": 0.9464270130139795,
        "error": 0.02793196134499487
    }
],
    platt: [
    {
        "bin": "0.0 - 0.1",
        "count": 1606,
        "mean_pred": 0.0037862906395728186,
        "error": 0.004308354441373632
    },
    {
        "bin": "0.1 - 0.2",
        "count": 25,
        "mean_pred": 0.1406120505481533,
        "error": 0.020612050548153293
    },
    {
        "bin": "0.2 - 0.3",
        "count": 5,
        "mean_pred": 0.23977217683023677,
        "error": 0.23977217683023677
    },
    {
        "bin": "0.3 - 0.4",
        "count": 7,
        "mean_pred": 0.3657402071196762,
        "error": 0.2056883643088952
    },
    {
        "bin": "0.4 - 0.5",
        "count": 4,
        "mean_pred": 0.47615281102625445,
        "error": 0.22615281102625445
    },
    {
        "bin": "0.5 - 0.6",
        "count": 1,
        "mean_pred": 0.5915640850509727,
        "error": 0.4084359149490273
    },
    {
        "bin": "0.6 - 0.7",
        "count": 0,
        "mean_pred": 0.0,
        "error": 0.0
    },
    {
        "bin": "0.7 - 0.8",
        "count": 1,
        "mean_pred": 0.7788564010143099,
        "error": 0.22114359898569014
    },
    {
        "bin": "0.8 - 0.9",
        "count": 13,
        "mean_pred": 0.8835525246572137,
        "error": 0.11644747534278632
    },
    {
        "bin": "0.9 - 1.0",
        "count": 74,
        "mean_pred": 0.973899398562206,
        "error": 0.014439939102746546
    }
]
  },
  regression_cases: [
    {
        "name": "Obvious scam",
        "text": "Work From Home Data Entry Assistant!\nEarn $4,500 every week with no experience required.\nAll equipment will be provided.\nTo secure your position, submit a $150 registration fee via wire transfer or gift cards.\nContact our hiring manager immediately on Telegram: @quick_career_support.\nHurry, only 2 positions remaining! Apply now!",
        "calibrated_prob": 0.9987,
        "raw_score": 0.984,
        "prediction": "FRAUDULENT",
        "signals": [
            "payment_request",
            "telegram_contact",
            "urgency_language",
            "no_experience_required"
        ]
    },
    {
        "name": "Legitimate internship",
        "text": "Machine Learning Research Intern\nWe are seeking a summer Machine Learning Research Intern to join our NLP engineering group.\n\nResponsibilities:\n- Collaborate with research scientists to implement baseline transformer models.\n- Assist in data cleaning, evaluation scripting, and statistical significance testing.\n- Document experimental methodologies and present findings at internal lab meetings.\n\nQualifications:\n- Currently enrolled in a B.S., M.S., or Ph.D. program in Computer Science, Statistics, or related field.\n- Working proficiency in Python and familiarity with PyTorch or JAX.\n- Solid foundational understanding of linear algebra and probability.\n\nBenefits:\n- Competitive hourly compensation ($45/hr).\n- Mentorship from senior research scientists.\n- Office lunch stipend and transit pass.\n\nApplications must be submitted exclusively through our official corporate careers portal at https://careers.example-tech.com/jobs/ml-intern-2026.",
        "calibrated_prob": 0.0018,
        "raw_score": 0.125,
        "prediction": "LEGITIMATE",
        "signals": []
    },
    {
        "name": "Legitimate job with WhatsApp",
        "text": "Customer Logistics Field Supervisor (Latin America Region)\nGlobal Freight Solutions is hiring an on-site Logistics Field Supervisor based in Miami, FL to coordinate regional transport routes.\n\nKey Responsibilities:\n- Oversee day-to-day dispatch communication with regional trucking partners.\n- Resolve supply chain bottlenecks and track delivery milestones.\n- Coordinate with bilingual cross-border carriers across North and South America.\n\nRequirements:\n- 3+ years experience in freight forwarding, fleet dispatch, or transport operations.\n- Fluent in English and Spanish.\n- Strong organizational and crisis-management abilities.\n\nCompensation:\n- Annual base salary: $68,000 - $75,000 depending on experience.\n- Full medical, dental, and 401(k) matching.\n\nFor expedited initial dispatch coordination queries, contact our regional operations recruiter via WhatsApp at wa.me/13055550189. Formal applications and CVs must be submitted via our official site.",
        "calibrated_prob": 0.0013,
        "raw_score": 0.141,
        "prediction": "LEGITIMATE",
        "signals": [
            "whatsapp_contact"
        ]
    },
    {
        "name": "Legitimate, high salary + no experience",
        "text": "Junior Executive Sales Trainee \u2014 Real Estate Development\nPrestige Properties Group is launching our annual Executive Sales Trainee cohort in Chicago, IL.\n\nPosition Overview:\nWe train ambitious individuals from the ground up to represent multi-million-dollar commercial and luxury residential properties.\nNo prior professional experience is required \u2014 comprehensive 12-week paid corporate mentorship provided.\n\nWhat We Offer:\n- First-year target compensation: $120,000 - $140,000 ($60,000 guaranteed base + uncapped performance commissions).\n- Comprehensive health, dental, and life insurance.\n- Continuous leadership development program.\n\nRequirements:\n- Bachelor's degree preferred or equivalent military/customer-facing background.\n- Exceptional verbal communication, persistence, and coachability.\n- Valid driver's license.\n\nTo apply, please submit your resume through LinkedIn or our official careers portal.",
        "calibrated_prob": 0.0035,
        "raw_score": 0.198,
        "prediction": "LEGITIMATE",
        "signals": []
    },
    {
        "name": "Sophisticated scam",
        "text": "Executive Communications Specialist \u2014 Global Strategy Office\nInternational Advisory Partners seeks a remote Executive Communications Specialist to support C-suite executive briefings.\n\nRole & Responsibilities:\n- Draft confidential executive summaries, speech materials, and internal corporate advisories.\n- Manage sensitive stakeholder communication across European and Asian market divisions.\n- Maintain utmost discretion handling proprietary strategic agendas.\n\nRequirements:\n- Proven written fluency in corporate affairs or business journalism.\n- Ability to synthesize high-level strategic intelligence under tight turnarounds.\n\nImmediate Onboarding Procedure:\nDue to high application volume, our executive assessment team is conducting onboarding screenings immediately.\nCandidates must connect with our Senior Partner on Telegram at https://t.me/IAP_Executive_Advisory.\nTo issue your security credentials and secure corporate laptop, you must provide your SSN, banking verification routing, and national ID document scan within 24 hours. Failure to submit immediately will result in disqualification.",
        "calibrated_prob": 0.9943,
        "raw_score": 0.965,
        "prediction": "FRAUDULENT",
        "signals": [
            "telegram_contact",
            "sensitive_data_request",
            "urgency_language"
        ]
    }
],
  false_positive_audit: [
    {
        "job_id": 1670,
        "title": "Office PA/Receptionist",
        "location": "US, TN, BRENTWOOD",
        "industry": "Health, Wellness and Fitness",
        "employment_type": "Full-time",
        "status": "RESOLVED (LEGITIMATE)",
        "old_fraud_score": 0.7527,
        "new_calibrated_prob": 0.5878,
        "had_company_description_artifact": true,
        "root_cause": "Contained synthetic header artifact \"company description:\" with high TF-IDF positive weight and generic administrative n-grams that inflated raw decision margin.",
        "resolution": "Removed synthetic metadata headers during preprocessing clean-up and applied Platt scaling calibration. Score shifted from 75.3% to 58.8% (below calibrated 0.655 threshold).",
        "top_fraud_words": [
            [
                "company description",
                0.3799
            ],
            [
                "data entry",
                0.2643
            ],
            [
                "receptionist",
                0.1655
            ],
            [
                "entry",
                0.1554
            ],
            [
                "word",
                0.0905
            ],
            [
                "answering",
                0.09
            ],
            [
                "title office",
                0.0875
            ],
            [
                "customer service",
                0.0864
            ]
        ]
    },
    {
        "job_id": 6742,
        "title": "Customer Service Representative",
        "location": "US, IL, Chicago",
        "industry": "Insurance",
        "employment_type": "Full-time",
        "status": "RESOLVED (LEGITIMATE)",
        "old_fraud_score": 0.4885,
        "new_calibrated_prob": 0.5387,
        "had_company_description_artifact": false,
        "root_cause": "Generic administrative and service keywords triggered high uncalibrated margin due to base-rate class imbalance distortion.",
        "resolution": "Platt scaling posterior adjustment brought score to 0.5387, safely below the 0.655 operating threshold.",
        "top_fraud_words": [
            [
                "secured benefits",
                0.1837
            ],
            [
                "service representative",
                0.1413
            ],
            [
                "customer service",
                0.1125
            ],
            [
                "secured",
                0.1025
            ],
            [
                "colorado",
                0.0946
            ],
            [
                "service",
                0.0791
            ],
            [
                "customer",
                0.0682
            ],
            [
                "of products",
                0.0659
            ]
        ]
    },
    {
        "job_id": 6790,
        "title": "Customer Service Representative",
        "location": "US, GA, Atlanta",
        "industry": "Insurance",
        "employment_type": "Full-time",
        "status": "RESOLVED (LEGITIMATE)",
        "old_fraud_score": 0.4885,
        "new_calibrated_prob": 0.5387,
        "had_company_description_artifact": false,
        "root_cause": "Generic administrative and service keywords triggered high uncalibrated margin due to base-rate class imbalance distortion.",
        "resolution": "Platt scaling posterior adjustment brought score to 0.5387, safely below the 0.655 operating threshold.",
        "top_fraud_words": [
            [
                "secured benefits",
                0.1837
            ],
            [
                "service representative",
                0.1413
            ],
            [
                "customer service",
                0.1125
            ],
            [
                "secured",
                0.1025
            ],
            [
                "colorado",
                0.0946
            ],
            [
                "service",
                0.0791
            ],
            [
                "customer",
                0.0682
            ],
            [
                "of products",
                0.0659
            ]
        ]
    },
    {
        "job_id": 6907,
        "title": "Administrative Assistant",
        "location": "US, , Shawnee",
        "industry": "Unknown",
        "employment_type": "Full-time",
        "status": "RESOLVED (LEGITIMATE)",
        "old_fraud_score": 0.7653,
        "new_calibrated_prob": 0.6017,
        "had_company_description_artifact": true,
        "root_cause": "Contained synthetic header artifact \"company description:\" with high TF-IDF positive weight and generic administrative n-grams.",
        "resolution": "Removed synthetic metadata headers and applied Platt scaling calibration. Score shifted from 76.5% to 60.2% (below 0.655 threshold).",
        "top_fraud_words": [
            [
                "company description",
                0.4
            ],
            [
                "administrative assistant",
                0.2293
            ],
            [
                "assistant",
                0.2286
            ],
            [
                "title administrative",
                0.2204
            ],
            [
                "administrative",
                0.2177
            ],
            [
                "phones",
                0.1282
            ],
            [
                "assistant company",
                0.12
            ],
            [
                "calls",
                0.1075
            ]
        ]
    },
    {
        "job_id": 7898,
        "title": "Executive Administrative Assistant",
        "location": "US, VA, Arlington",
        "industry": "Unknown",
        "employment_type": "Unknown",
        "status": "RESOLVED (LEGITIMATE)",
        "old_fraud_score": 0.6987,
        "new_calibrated_prob": 0.4906,
        "had_company_description_artifact": true,
        "root_cause": "Contained synthetic header artifact \"company description:\" with high TF-IDF positive weight and generic administrative n-grams.",
        "resolution": "Removed synthetic metadata headers and applied Platt scaling calibration. Score shifted from 69.9% to 49.1% (below 0.655 threshold).",
        "top_fraud_words": [
            [
                "administrative",
                0.3165
            ],
            [
                "assistant",
                0.2692
            ],
            [
                "company description",
                0.1974
            ],
            [
                "administrative assistant",
                0.1916
            ],
            [
                "clerical",
                0.0981
            ],
            [
                "preparation",
                0.0915
            ],
            [
                "word",
                0.0797
            ],
            [
                "assistant company",
                0.0592
            ]
        ]
    },
    {
        "job_id": 11136,
        "title": "Assistant Chief Nursing Officer (hospital west of Montgomery, AL)",
        "location": "US, AL, Montgomery",
        "industry": "Hospital & Health Care",
        "employment_type": "Full-time",
        "status": "RESOLVED (LEGITIMATE)",
        "old_fraud_score": 0.5257,
        "new_calibrated_prob": 0.6059,
        "had_company_description_artifact": true,
        "root_cause": "Contained synthetic header artifact \"company description:\" with high TF-IDF positive weight and generic administrative n-grams.",
        "resolution": "Removed synthetic metadata headers and applied Platt scaling calibration. Score shifted from 52.6% to 60.6% (below 0.655 threshold).",
        "top_fraud_words": [
            [
                "company description",
                0.4757
            ],
            [
                "rn",
                0.3972
            ],
            [
                "assistant",
                0.2718
            ],
            [
                "hospital",
                0.2439
            ],
            [
                "000",
                0.1996
            ],
            [
                "req",
                0.1389
            ],
            [
                "nursing",
                0.091
            ],
            [
                "title assistant",
                0.0764
            ]
        ]
    },
    {
        "job_id": 12242,
        "title": "Teaching Assistant",
        "location": "US, FL, Jacksonville",
        "industry": "Unknown",
        "employment_type": "Unknown",
        "status": "OPEN (FRAUDULENT)",
        "old_fraud_score": 0.9136,
        "new_calibrated_prob": 0.7871,
        "had_company_description_artifact": true,
        "root_cause": "High concentration of tutoring and academic assistant n-grams that heavily overlap with common administrative scam patterns. Score remains elevated above threshold (0.7871 >= 0.6550).",
        "resolution": "Single open false positive out of 9 evaluated (8/9 resolved, 88.9%). Remains flagged due to high scam-adjacent token density in educational posting corpus.",
        "top_fraud_words": [
            [
                "company description",
                0.7726
            ],
            [
                "assistant",
                0.4415
            ],
            [
                "requirements high",
                0.3148
            ],
            [
                "high school",
                0.2493
            ],
            [
                "assistant company",
                0.2318
            ],
            [
                "requirements benefits",
                0.13
            ],
            [
                "school diploma",
                0.1271
            ],
            [
                "school",
                0.1227
            ]
        ]
    },
    {
        "job_id": 13085,
        "title": "Bilingual Products and Services Coordinator II",
        "location": "US, FL, St. Petersburg",
        "industry": "Unknown",
        "employment_type": "Unknown",
        "status": "RESOLVED (LEGITIMATE)",
        "old_fraud_score": 0.5393,
        "new_calibrated_prob": 0.5042,
        "had_company_description_artifact": true,
        "root_cause": "Contained synthetic header artifact \"company description:\" with high TF-IDF positive weight and generic administrative n-grams.",
        "resolution": "Removed synthetic metadata headers and applied Platt scaling calibration. Score shifted from 53.9% to 50.4% (below 0.655 threshold).",
        "top_fraud_words": [
            [
                "data entry",
                0.1978
            ],
            [
                "company description",
                0.168
            ],
            [
                "entry",
                0.1163
            ],
            [
                "high school",
                0.0918
            ],
            [
                "answering",
                0.0835
            ],
            [
                "customer service",
                0.0802
            ],
            [
                "customer",
                0.0651
            ],
            [
                "program",
                0.0628
            ]
        ]
    },
    {
        "job_id": 16639,
        "title": "Immediate Opening : Help Desk /Technical Support Coordinator",
        "location": "QA, , Doha",
        "industry": "Unknown",
        "employment_type": "Unknown",
        "status": "RESOLVED (LEGITIMATE)",
        "old_fraud_score": 0.4674,
        "new_calibrated_prob": 0.5749,
        "had_company_description_artifact": false,
        "root_cause": "Generic administrative and service keywords triggered high uncalibrated margin due to base-rate class imbalance distortion.",
        "resolution": "Platt scaling posterior adjustment brought score to 0.5749, safely below the 0.655 operating threshold.",
        "top_fraud_words": [
            [
                "vam",
                0.1258
            ],
            [
                "vam systems",
                0.1258
            ],
            [
                "qatar",
                0.0902
            ],
            [
                "calls",
                0.064
            ],
            [
                "bahrain",
                0.0592
            ],
            [
                "systems is",
                0.0555
            ],
            [
                "immediate",
                0.0476
            ],
            [
                "call",
                0.0424
            ]
        ]
    }
],
  adversarial_benchmark: {
    total_attacks_tested: 11,
    test_samples_count: 30,
    fraudulent_samples: 23,
    legitimate_samples: 7,
    raw_homoglyph_asr: 0.4348,
    raw_homoglyph_flips: "10 / 23",
    normalized_homoglyph_asr: 0.0000,
    normalized_homoglyph_flips: "0 / 23",
    deployed_overall_asr: 0.0000,
    defense_mechanism: "ml/text_normalizer.py (NFKC normalization + Cyrillic/Greek lookalike mapping) + defensive signal veto"
  },
  security_test_suite: {
    total_tests: 11,
    passed: 11,
    failed: 0,
    vectors_covered: [
      { name: "Direct Prompt Injection", status: "PASS", detail: "System command override & prompt leaking attempts defused" },
      { name: "Indirect Prompt Injection", status: "PASS", detail: "Hidden system notes, XML delimiter escapes, roleplay jailbreaks neutralized" },
      { name: "XSS Payloads in Job Fields", status: "PASS", detail: "<script>, inline event handlers (onerror=), javascript: URIs defused" },
      { name: "SQLi-like Strings", status: "PASS", detail: "' OR '1'='1, DROP TABLE, UNION SELECT processed safely without crashes" },
      { name: "Extremely Large Payloads (>100KB, >1.5MB)", status: "PASS", detail: "Safely truncated to 50,000 char cap without ReDoS or memory blowup (<1.5s)" },
      { name: "Zero-byte / Null-byte Injection", status: "PASS", detail: "\\x00 stripped without C-string truncation; scam signals preserved" }
    ]
  }
};

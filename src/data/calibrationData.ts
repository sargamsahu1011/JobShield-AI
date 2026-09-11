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
      threshold: 0.52,
      val_brier: 0.019296,
      val_log_loss: 0.102635,
      val_ece: 0.070058,
      test_brier: 0.022270,
      test_log_loss: 0.115945,
      test_ece: 0.084639,
      test_pr_auc: 0.930775,
      test_roc_auc: 0.993132,
      test_precision: 0.831461,
      test_recall: 0.840909,
      test_f1: 0.836158,
    },
    platt: {
      name: "Platt Scaling (Sigmoid Calibration)",
      threshold: 0.405,
      val_brier: 0.010407,
      val_log_loss: 0.043242,
      val_ece: 0.003504,
      test_brier: 0.010720,
      test_log_loss: 0.040692,
      test_ece: 0.008175,
      test_pr_auc: 0.930775,
      test_roc_auc: 0.993132,
      test_precision: 0.890244,
      test_recall: 0.829545,
      test_f1: 0.858824,
    },
    isotonic: {
      name: "Isotonic Regression",
      threshold: 0.500,
      val_brier: 0.009139,
      val_log_loss: 0.037526,
      val_ece: 0.000000,
      test_brier: 0.011593,
      test_log_loss: 0.042368,
      test_ece: 0.003449,
      test_pr_auc: 0.910490,
      test_roc_auc: 0.992586,
      test_precision: 0.8659,
      test_recall: 0.8068,
      test_f1: 0.8353,
    },
  },
  reliability_table_test: {
    uncalibrated: [
      { bin: "0.0 - 0.1", count: 1196, mean_pred: 0.0469, empirical: 0.0000, error: 0.0469 },
      { bin: "0.1 - 0.2", count: 321, mean_pred: 0.1383, empirical: 0.0062, error: 0.1321 },
      { bin: "0.2 - 0.3", count: 96, mean_pred: 0.2471, empirical: 0.0208, error: 0.2263 },
      { bin: "0.3 - 0.4", count: 53, mean_pred: 0.3475, empirical: 0.0377, error: 0.3098 },
      { bin: "0.4 - 0.5", count: 26, mean_pred: 0.4430, empirical: 0.3077, error: 0.1353 },
      { bin: "0.5 - 0.6", count: 9, mean_pred: 0.5416, empirical: 0.1111, error: 0.4305 },
      { bin: "0.6 - 0.7", count: 12, mean_pred: 0.6481, empirical: 0.5000, error: 0.1481 },
      { bin: "0.7 - 0.8", count: 7, mean_pred: 0.7810, empirical: 0.5714, error: 0.2096 },
      { bin: "0.8 - 0.9", count: 17, mean_pred: 0.8596, empirical: 0.9412, error: 0.0816 },
      { bin: "0.9 - 1.0", count: 47, mean_pred: 0.9492, empirical: 1.0000, error: 0.0508 },
    ],
    platt: [
      { bin: "0.0 - 0.1", count: 1647, mean_pred: 0.0072, empirical: 0.0030, error: 0.0041 },
      { bin: "0.1 - 0.2", count: 42, mean_pred: 0.1378, empirical: 0.1905, error: 0.0527 },
      { bin: "0.2 - 0.3", count: 9, mean_pred: 0.2392, empirical: 0.2222, error: 0.0170 },
      { bin: "0.3 - 0.4", count: 4, mean_pred: 0.3797, empirical: 0.0000, error: 0.3797 },
      { bin: "0.4 - 0.5", count: 7, mean_pred: 0.4610, empirical: 0.5714, error: 0.1104 },
      { bin: "0.5 - 0.6", count: 4, mean_pred: 0.5287, empirical: 0.5000, error: 0.0287 },
      { bin: "0.6 - 0.7", count: 1, mean_pred: 0.6987, empirical: 0.0000, error: 0.6987 },
      { bin: "0.7 - 0.8", count: 6, mean_pred: 0.7609, empirical: 0.6667, error: 0.0943 },
      { bin: "0.8 - 0.9", count: 9, mean_pred: 0.8572, empirical: 1.0000, error: 0.1428 },
      { bin: "0.9 - 1.0", count: 55, mean_pred: 0.9738, empirical: 0.9818, error: 0.0081 },
    ],
  },
  regression_cases: [
    {
      name: "LEGITIMATE TECH JOB",
      raw_score: 0.1324,
      calibrated_prob: 0.0097,
      prediction: "LEGITIMATE",
      signals: [],
      text: `Software Engineer\n\nWe are looking for a Software Engineer to join our development team.\n\nResponsibilities:\n- Develop and maintain web applications.\n- Work with engineers and product managers.\n- Write clean and maintainable code.\n\nRequirements:\n- Bachelor's degree in Computer Science or related field.\n- Experience with Python or Java.\n- Good problem-solving skills.\n\nBenefits:\n- Competitive salary.\n- Health insurance.\n- Paid leave.`,
    },
    {
      name: "OBVIOUS SCAM",
      raw_score: 0.8518,
      calibrated_prob: 0.8786,
      prediction: "FRAUDULENT",
      signals: ["payment_request", "telegram_contact", "urgency_language", "no_experience_required"],
      text: `Work From Home Job!\n\nEarn ₹80,000 per month with no experience required.\nSimple online data entry tasks.\n\nRequirements:\n- Basic mobile or computer usage.\n- Work 1-2 hours per day.\n\nPay ₹1,500 registration fee to secure your position.\nContact us on Telegram immediately. Limited seats available. Apply now!`,
    },
    {
      name: "SUBTLE SCAM",
      raw_score: 0.7443,
      calibrated_prob: 0.6775,
      prediction: "FRAUDULENT",
      signals: ["whatsapp_contact"],
      text: `Customer Support Executive (Remote)\n\nWe are hiring Remote Customer Support Executives for global clients.\n\nResponsibilities:\n- Handle customer inquiries via email and chat.\n- Maintain customer records.\n\nBenefits:\n- Work from home.\n- Flexible hours.\n\nContact our recruitment manager through WhatsApp for further details.`,
    },
    {
      name: "LEGITIMATE REMOTE JOB",
      raw_score: 0.1994,
      calibrated_prob: 0.0234,
      prediction: "LEGITIMATE",
      signals: [],
      text: `Remote Content Writer\n\nDigital Marketing Agency looking for a freelance Content Writer.\n\nRequirements:\n- Strong portfolio of published articles.\n- Experience writing tech blogs.\n- Good research and editing skills.\n\nApply with your resume and portfolio links.`,
    },
    {
      name: "SENSITIVE INFORMATION SCAM",
      raw_score: 0.6594,
      calibrated_prob: 0.5000,
      prediction: "FRAUDULENT",
      signals: ["sensitive_data_request", "urgency_language"],
      text: `Immediate Hiring: Administrative Assistant\n\nUrgent requirement for Administrative Assistant.\n\nTo complete your employment verification, send us your bank account details, OTP and Aadhaar number.\n\nSend the information immediately to complete your joining.`,
    },
  ],
};

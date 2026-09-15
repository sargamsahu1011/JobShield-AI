import { useState } from "react";
import ReactMarkdown from "react-markdown";
import "./App.css";

const API_URL = "http://127.0.0.1:5000";

function App() {
  const [jobText, setJobText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyzeJob = async () => {
    if (!jobText.trim()) {
      setError("Please enter a job posting first.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(`${API_URL}/api/analyze`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: jobText,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Analysis failed.");
      }

      setResult(data);
    } catch (err) {
      setError(
        err.message ||
          "Unable to connect to the JobShield AI backend."
      );
    } finally {
      setLoading(false);
    }
  };

  const probability = result
    ? (result.fraud_score * 100).toFixed(2)
    : null;

  const isFraud = result?.prediction === 1 || result?.fraud_score >= result?.threshold;

  return (
    <div className="app">
      <header className="navbar">
        <div className="brand">
          <div className="brand-icon">🛡️</div>
          <div>
            <h1>JobShield AI</h1>
            <span>AI-Powered Job Scam Detection</span>
          </div>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          AI Engine Online
        </div>
      </header>

      <main className="container">
        <section className="hero">
          <span className="eyebrow">SMARTER JOB SAFETY</span>

          <h2>
            Detect suspicious job postings
            <br />
            <span>before they cost you.</span>
          </h2>

          <p>
            Analyze job descriptions using machine learning, scam-signal
            detection, evidence extraction, and AI-powered reasoning.
          </p>
        </section>

        <section className="analysis-card">
          <div className="card-header">
            <div>
              <h3>Job Posting Analysis</h3>
              <p>Paste the complete job description below.</p>
            </div>

            <span className="model-badge">
              TF-IDF + Logistic Regression
            </span>
          </div>

          <textarea
            value={jobText}
            onChange={(e) => setJobText(e.target.value)}
            placeholder="Paste a job posting here...

Example:
We are hiring a Data Entry Executive.
No experience required. Work from home.
A refundable registration fee is required before onboarding..."
          />

          <div className="action-row">
            <span className="character-count">
              {jobText.length} characters
            </span>

            <button
              onClick={analyzeJob}
              disabled={loading}
              className="analyze-button"
            >
              {loading ? "Analyzing..." : "Analyze Job →"}
            </button>
          </div>
        </section>

        {error && (
          <div className="error-box">
            ⚠️ {error}
          </div>
        )}

        {result && (
          <section className="results">
            <div className="result-header">
              <div>
                <span className="eyebrow">ANALYSIS COMPLETE</span>
                <h2>Risk Assessment</h2>
              </div>

              <div className={`verdict ${isFraud ? "danger" : "safe"}`}>
                {isFraud ? "HIGH RISK" : "LOW RISK"}
              </div>
            </div>

            <div className="risk-grid">
              <div className="risk-card main-risk">
                <span>Fraud Probability</span>

                <strong>{probability}%</strong>

                <div className="progress">
                  <div
                    className={`progress-fill ${
                      isFraud ? "danger-fill" : "safe-fill"
                    }`}
                    style={{
                      width: `${Math.min(Number(probability), 100)}%`,
                    }}
                  ></div>
                </div>

                <p>
                  Production threshold:{" "}
                  {(result.threshold * 100).toFixed(2)}%
                </p>
              </div>

              <div className="risk-card">
                <span>Model</span>
                <strong className="small-value">
                  Calibrated ML
                </strong>
                <p>
                  {result.is_calibrated
                    ? "Platt calibrated probability"
                    : "Uncalibrated probability"}
                </p>
              </div>

              <div className="risk-card">
                <span>Detection Engine</span>
                <strong className="small-value">
                  Production
                </strong>
                <p>{result.model_name}</p>
              </div>
            </div>

            <div className="result-section">
              <div className="section-title">
                <span>🔍</span>
                <h3>Scam Signals</h3>
              </div>

              <div className="signals">
                {Object.entries(result.signals || {}).map(
                  ([key, value]) =>
                    value && (
                      <div className="signal" key={key}>
                        <span>⚠</span>
                        {key
                          .replaceAll("_", " ")
                          .replace(/\b\w/g, (c) => c.toUpperCase())}
                      </div>
                    )
                )}

                {!Object.values(result.signals || {}).some(Boolean) && (
                  <div className="no-signals">
                    ✓ No explicit scam signals detected.
                  </div>
                )}
              </div>
            </div>

            <div className="result-section">
              <div className="section-title">
                <span>🧾</span>
                <h3>Evidence</h3>
              </div>

              {result.evidence &&
              Object.keys(result.evidence).length > 0 ? (
                <div className="evidence-list">
                  {Object.entries(result.evidence).map(
                    ([key, value]) => (
                      <div className="evidence-item" key={key}>
                        <strong>
                          {key
                            .replaceAll("_", " ")
                            .replace(/\b\w/g, (c) => c.toUpperCase())}
                        </strong>
                        <p>
                          {Array.isArray(value)
                            ? value.join(" ")
                            : String(value)}
                        </p>
                      </div>
                    )
                  )}
                </div>
              ) : (
                <div className="no-signals">
                  No specific evidence extracted.
                </div>
              )}
            </div>

            {result.explanation && (
            <div className="result-section explanation">
             <div className="section-title">
             <span>🤖</span>
            <h3>AI Explanation</h3>
            </div>

    <ReactMarkdown>{result.explanation}</ReactMarkdown>
  </div>
)}
            {result.signal_veto_triggered && (
              <div className="security-notice">
                🛡️ <strong>Safety override activated.</strong>
                <br />
                High-risk scam indicators triggered the defensive
                rule-ensemble protection.
              </div>
            )}
          </section>
        )}

        <footer>
          <p>
            JobShield AI provides risk assessment and should not be treated
            as a definitive judgment about an employer.
          </p>
        </footer>
      </main>
    </div>
  );
}

export default App;
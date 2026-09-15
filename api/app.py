import sys
from pathlib import Path

from flask import Flask, request, jsonify
from flask_cors import CORS

# Add project root to Python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from ml.jobshield_pipeline import analyze_job
from ml.input_validator import InputValidationError


app = Flask(__name__)
CORS(app)
@app.get("/")
def root():
    return jsonify({
        "status": "ok",
        "service": "JobShield AI API",
        "health": "/api/health",
        "analyze": "/api/analyze"
    })

@app.get("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "JobShield AI API"
    })


@app.post("/api/analyze")
def analyze():
    try:
        data = request.get_json(silent=True)

        if not data or "text" not in data:
            return jsonify({
                "error": "Missing 'text' in request body"
            }), 400

        text = data["text"]

        result = analyze_job(
            text=text,
            include_explanation=True
        )

        return jsonify(result), 200

    except InputValidationError as e:
        return jsonify({
            "error": str(e)
        }), 400

    except Exception as e:
        print(f"API error: {e}")

        return jsonify({
            "error": "Internal server error"
        }), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
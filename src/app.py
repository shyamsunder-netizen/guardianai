from flask import Flask, render_template, request
import pandas as pd
import joblib
import os
from urllib.parse import urlparse

from feature_extractor import extract_features
from threat_engine import calculate_threat_score
from hosting_detector import is_suspicious_hosting
from entropy_utils import calculate_entropy
from brand_similarity import detect_brand_similarity

app = Flask(__name__)

# ✅ Correct model loading for:
# GuardianAI/src/app.py
# GuardianAI/models/phishing_model.pkl

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "..", "models", "phishing_model.pkl")

model = joblib.load(model_path)


@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        try:
            url = request.form["url"]

            if not url.startswith("http"):
                url = "http://" + url

            parsed = urlparse(url)
            domain = parsed.netloc.lower().split(":")[0]

            # -------- Feature Extraction --------
            features = extract_features(url)
            X = pd.DataFrame([features])

            ml_prediction = model.predict(X)[0]
            ml_confidence = round(
                model.predict_proba(X)[0][ml_prediction] * 100, 2
            )

            entropy = calculate_entropy(domain)
            suspicious_hosting = is_suspicious_hosting(url)

            # -------- Brand Similarity --------
            brand_flag, detected_brand, distance = detect_brand_similarity(domain)

            password_detected = 0
            external_form = 0
            domain_age = 0

            score, reasons = calculate_threat_score(
                ml_prediction,
                ml_confidence,
                entropy,
                domain_age,
                brand_flag,
                suspicious_hosting,
                password_detected,
                external_form
            )

            explanation = {
                "ML Prediction": "Phishing" if ml_prediction == 1 else "Safe",
                "ML Confidence (%)": ml_confidence,
                "Domain Entropy": round(entropy, 3),
                "Brand Similarity": detected_brand if brand_flag else "None",
                "Unicode Spoof": features.get("unicode_spoof", 0),
                "Base64 Payload": features.get("base64_detected", 0)
            }

            if score >= 70:
                risk = "HIGH"
            elif score >= 40:
                risk = "MEDIUM"
            else:
                risk = "LOW"

            result = {
                "url": url,
                "score": score,
                "risk": risk,
                "confidence": ml_confidence,
                "reasons": reasons,
                "explanation": explanation
            }

        except Exception as e:
            result = {
                "url": url if "url" in locals() else "Unknown",
                "score": 0,
                "risk": "ERROR",
                "confidence": 0,
                "reasons": [str(e)],
                "explanation": {}
            }

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
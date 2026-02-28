import pandas as pd
import joblib
from urllib.parse import urlparse

from feature_extractor import extract_features
from brand_detector import detect_brand_impersonation
from headless_analyzer import analyze_dynamic_content
from threat_engine import calculate_threat_score


print("🛡️ GuardianAI - Advanced Threat Detection Engine")
print("------------------------------------------------")

model = joblib.load("../models/phishing_model.pkl")


# Suspicious hosting services
SUSPICIOUS_HOSTING = [
    "ngrok", "trycloudflare", "serveo",
    "localtunnel", "herokuapp",
    "vercel", "onrender", "firebaseapp"
]


while True:
    url = input("\nEnter URL to check (or type 'exit'): ")

    if url.lower() == "exit":
        print("Exiting GuardianAI. Stay safe online.")
        break

    # =========================
    # 1️⃣ ML FEATURE EXTRACTION
    # =========================
    features = extract_features(url, use_whois=True)
    X = pd.DataFrame([features])

    prediction = model.predict(X)[0]
    probability = model.predict_proba(X)[0][prediction]
    confidence = round(probability * 100, 2)

    entropy = features["domain_entropy"]
    domain_age_days = features["domain_age_days"]

    # =========================
    # 2️⃣ BRAND DETECTION
    # =========================
    brand_flag, brand, _ = detect_brand_impersonation(url)

    # =========================
    # 3️⃣ SUSPICIOUS HOSTING
    # =========================
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    suspicious_hosting = any(service in domain for service in SUSPICIOUS_HOSTING)

    # =========================
    # 4️⃣ HEADLESS BEHAVIOR ANALYSIS
    # =========================
    dynamic_results = analyze_dynamic_content(url)
    password_detected = dynamic_results["has_password_field"]
    external_form = dynamic_results["external_form_action"]

    # =========================
    # 5️⃣ THREAT SCORE CALCULATION
    # =========================
    threat_score, reasons = calculate_threat_score(
        ml_prediction=prediction,
        ml_confidence=confidence,
        entropy=entropy,
        domain_age_days=domain_age_days,
        brand_flag=brand_flag,
        suspicious_hosting=suspicious_hosting,
        password_detected=password_detected,
        external_form=external_form
    )

    # =========================
    # 6️⃣ FINAL OUTPUT
    # =========================
    print("\n===== Threat Analysis Report =====")
    print(f"Threat Score: {round(threat_score, 2)} / 100")

    if threat_score >= 70:
        level = "HIGH"
    elif threat_score >= 40:
        level = "MEDIUM"
    else:
        level = "LOW"

    print(f"Risk Level: {level}")

    print("\nReasons:")
    if reasons:
        for reason in reasons:
            print(f"- {reason}")
    else:
        print("- No major threat indicators detected")

    print("\nTechnical Details:")
    print(f"- ML Confidence: {confidence}%")
    print(f"- Domain Entropy: {round(entropy, 3)}")
    print(f"- Domain Age (days): {domain_age_days}")
    print(f"- Password Field Detected: {password_detected}")
    print(f"- External Form Submission: {external_form}")
def calculate_threat_score(
    ml_prediction,
    ml_confidence,
    entropy,
    domain_age,
    brand_flag,
    suspicious_hosting,
    password_detected,
    external_form
):

    score = 0
    reasons = []

    # ML Layer
    if ml_prediction == 1:
        score += ml_confidence * 0.6
        reasons.append("ML model indicates phishing")

    # High Entropy
    if entropy > 3.8:
        score += 15
        reasons.append("High domain randomness detected")

    # Suspicious hosting
    if suspicious_hosting:
        score += 15
        reasons.append("Suspicious hosting provider")

    # Brand impersonation
    if brand_flag:
        score += 25
        reasons.append("Brand impersonation similarity detected")

    # Stealth phishing detection
    if ml_prediction == 0 and entropy > 3.8 and suspicious_hosting:
        score += 20
        reasons.append("Stealth phishing behavior pattern")

    if score > 100:
        score = 100

    return int(score), reasons
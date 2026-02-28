from urllib.parse import urlparse
import re
import math
from collections import Counter
import unicodedata

# =========================
# ENTROPY CALCULATION
# =========================
def calculate_entropy(text):
    if not text:
        return 0
    counter = Counter(text)
    length = len(text)
    entropy = 0
    for count in counter.values():
        probability = count / length
        entropy -= probability * math.log2(probability)
    return entropy


# =========================
# UNICODE SPOOF DETECTION
# =========================
def has_unicode_spoof(domain):
    for char in domain:
        if ord(char) > 127:
            return 1
    return 0


# =========================
# BASE64 DETECTION
# =========================
def detect_base64(text):
    return 1 if re.search(r'[A-Za-z0-9+/=]{20,}', text) else 0


# =========================
# MAIN FEATURE EXTRACTION
# =========================
def extract_features(url):
    features = {}

    url_lower = url.lower()
    parsed = urlparse(url_lower)
    domain = parsed.netloc.split(":")[0]

    # ---------------- BASIC FEATURES ----------------
    features['url_length'] = len(url)
    features['num_dots'] = url.count('.')
    features['num_hyphens'] = url.count('-')
    features['num_digits'] = sum(c.isdigit() for c in url)
    features['has_https'] = 1 if parsed.scheme == "https" else 0
    features['has_at_symbol'] = 1 if '@' in url else 0
    features['uses_ip'] = 1 if re.match(r"^\d+\.\d+\.\d+\.\d+", domain) else 0

    # Suspicious words
    suspicious_words = [
        'login','verify','secure','update',
        'account','bank','confirm','password'
    ]
    features['suspicious_words'] = sum(word in url_lower for word in suspicious_words)

    # Suspicious TLD
    suspicious_tlds = ['.xyz','.tk','.top','.gq','.ml','.cf']
    features['suspicious_tld'] = 1 if any(domain.endswith(tld) for tld in suspicious_tlds) else 0

    features['subdomain_count'] = domain.count('.')
    features['special_char_count'] = len(re.findall(r"[!@#$%^&*(),?\":{}|<>]", url))
    features['has_port'] = 1 if ':' in parsed.netloc else 0

    # ---------------- ADVANCED BEHAVIORAL FEATURES ----------------
    features['path_length'] = len(parsed.path)
    features['query_length'] = len(parsed.query)
    features['query_entropy'] = calculate_entropy(parsed.query)
    features['base64_detected'] = detect_base64(parsed.query)

    # ---------------- DOMAIN ENTROPY ----------------
    clean_domain = domain.replace(".", "")
    features['domain_entropy'] = calculate_entropy(clean_domain)

    # ---------------- UNICODE SPOOF ----------------
    features['unicode_spoof'] = has_unicode_spoof(domain)

    # ---------------- DOMAIN AGE DISABLED ----------------
    features['domain_age_days'] = 0
    features['is_new_domain'] = 0

    return features
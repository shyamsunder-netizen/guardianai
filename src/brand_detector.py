import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

KNOWN_BRANDS = {
    "paypal": "paypal.com",
    "google": "google.com",
    "amazon": "amazon.com",
    "facebook": "facebook.com",
    "microsoft": "microsoft.com",
    "apple": "apple.com",
    "netflix": "netflix.com",
    "instagram": "instagram.com",
    "linkedin": "linkedin.com",
    "github": "github.com"
}

def detect_brand_impersonation(url):
    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    # Remove port
    domain = domain.split(":")[0]

    # --- DOMAIN LEVEL CHECK ---
    for brand, official_domain in KNOWN_BRANDS.items():
        if brand in domain and official_domain not in domain:
            return True, brand, "Domain-level impersonation detected"

    # --- WEBSITE TITLE CHECK ---
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, timeout=5, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string.lower() if soup.title and soup.title.string else ""

        for brand, official_domain in KNOWN_BRANDS.items():
            if brand in title and official_domain not in domain:
                return True, brand, title

        return False, None, title

    except Exception:
        # If fetch fails, rely only on domain logic
        return False, None, None
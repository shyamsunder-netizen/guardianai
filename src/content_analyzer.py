import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def analyze_page_content(url):
    results = {
        "has_password_field": 0,
        "has_login_form": 0,
        "external_form_action": 0
    }

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, timeout=5, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        forms = soup.find_all("form")

        for form in forms:
            # Check password input
            password_inputs = form.find_all("input", {"type": "password"})
            if password_inputs:
                results["has_password_field"] = 1

            # Check if form action posts to different domain
            action = form.get("action")
            if action:
                if action.startswith("http"):
                    action_domain = urlparse(action).netloc.lower()
                    if action_domain and action_domain != domain:
                        results["external_form_action"] = 1

            # Basic login detection
            if "login" in form.text.lower():
                results["has_login_form"] = 1

        return results

    except Exception:
        return results
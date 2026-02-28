from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from urllib.parse import urlparse
import time


def analyze_dynamic_content(url):
    results = {
        "has_password_field": 0,
        "external_form_action": 0
    }

    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        driver.get(url)

        # Wait for JS to load
        time.sleep(5)

        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        # Detect password fields
        password_fields = driver.find_elements(By.XPATH, "//input[@type='password']")
        if password_fields:
            results["has_password_field"] = 1

        # Detect forms posting to external domain
        forms = driver.find_elements(By.TAG_NAME, "form")
        for form in forms:
            action = form.get_attribute("action")
            if action and action.startswith("http"):
                action_domain = urlparse(action).netloc.lower()
                if action_domain and action_domain != domain:
                    results["external_form_action"] = 1

        driver.quit()
        return results

    except Exception as e:
        return results
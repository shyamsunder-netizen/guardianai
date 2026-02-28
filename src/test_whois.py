import whois

try:
    domain = "google.com"
    info = whois.whois(domain)
    print("WHOIS lookup successful!")
    print("Domain name:", info.domain_name)
    print("Creation date:", info.creation_date)
except Exception as e:
    print("WHOIS lookup failed.")
    print("Error:", e)
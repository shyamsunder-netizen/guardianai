def is_suspicious_hosting(url):
    suspicious_hosts = [
        "ngrok",
        "trycloudflare",
        "localtunnel",
        "herokuapp",
        "onrender",
        "vercel",
        "firebaseapp",
        "serveo",
        "duckdns",
        "000webhost"
    ]

    url_lower = url.lower()

    for host in suspicious_hosts:
        if host in url_lower:
            return True

    return False
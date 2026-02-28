import pandas as pd
import random


def load_legitimate_domains(filepath, limit=5000):
    df = pd.read_csv(filepath, header=None)
    domains = df[1].head(limit).tolist()
    urls = ["https://www." + domain for domain in domains]
    return pd.DataFrame({"url": urls, "label": 0})


def load_phishing_feed(filepath, limit=5000):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    urls = lines[:limit]
    return pd.DataFrame({"url": urls, "label": 1})


def generate_synthetic_phishing(domains, count=3000):
    suspicious_words = ["login", "verify", "secure", "update", "account", "confirm"]
    tlds = [".xyz", ".top", ".tk", ".ml", ".cf"]

    fake_urls = []

    for _ in range(count):
        domain = random.choice(domains)
        word = random.choice(suspicious_words)
        tld = random.choice(tlds)

        fake = f"http://{domain}-{word}{tld}"
        fake_urls.append(fake)

    return pd.DataFrame({"url": fake_urls, "label": 1})


def build_dataset():
    legit_df = load_legitimate_domains("../data/tranco.csv")
    phishing_df = load_phishing_feed("../data/openphish.txt")

    synthetic_df = generate_synthetic_phishing(
        legit_df["url"].str.replace("https://www.", "", regex=False).tolist()
    )

    final_df = pd.concat([legit_df, phishing_df, synthetic_df])
    final_df = final_df.sample(frac=1).reset_index(drop=True)

    final_df.to_csv("../data/guardianai_large_dataset.csv", index=False)

    print("Dataset created successfully!")
    print("Total samples:", len(final_df))


if __name__ == "__main__":
    build_dataset()
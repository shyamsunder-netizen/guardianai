from headless_analyzer import analyze_dynamic_content

url = input("Enter URL: ")

results = analyze_dynamic_content(url)

print("\n--- Headless Analysis ---")
for key, value in results.items():
    print(f"{key}: {value}")

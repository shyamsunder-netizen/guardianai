from content_analyzer import analyze_page_content

url = input("Enter URL: ")

results = analyze_page_content(url)

print("\n--- Content Analysis ---")
for key, value in results.items():
    print(f"{key}: {value}")
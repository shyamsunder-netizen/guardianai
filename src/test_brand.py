from brand_detector import detect_brand_impersonation

url = input("Enter URL: ")

flag, brand, title = detect_brand_impersonation(url)

if flag:
    print(f"⚠️ Brand impersonation detected!")
    print(f"Brand: {brand}")
    print(f"Page title: {title}")
else:
    print("No impersonation detected.")
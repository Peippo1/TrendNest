# test_https.py
import requests
r = requests.get("https://finance.yahoo.com")
print("Status Code:", r.status_code)
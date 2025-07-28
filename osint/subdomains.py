# File: osint/subdomains.py
import requests

def enumerate_subdomains(domain):
    print(f"[Subdomains] Searching for: {domain}")
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    try:
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            subs = set()
            for entry in data:
                name = entry['name_value']
                for sub in name.splitlines():
                    subs.add(sub)
            for s in subs:
                print(" -", s)
        else:
            print("[Subdomains] No data found.")
    except Exception as e:
        print(f"[Subdomains] Error: {e}")

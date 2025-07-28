# File: osint/whois_lookup.py
import whois

def perform_whois(domain):
    try:
        print(f"[WHOIS] Gathering info for: {domain}")
        result = whois.whois(domain)
        print(result)
    except Exception as e:
        print(f"[WHOIS] Error: {e}")

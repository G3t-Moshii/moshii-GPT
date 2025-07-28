# File: osint/dns_lookup.py
import dns.resolver

def perform_dns_lookup(domain):
    print(f"[DNS] Resolving: {domain}")
    try:
        for record_type in ["A", "MX", "NS"]:
            answers = dns.resolver.resolve(domain, record_type)
            print(f"[{record_type}] Records:")
            for r in answers:
                print(" -", r.to_text())
    except Exception as e:
        print(f"[DNS] Error: {e}")

# File: osint/os_detection.py
import nmap

def detect_os(ip):
    print(f"[OS Detection] Scanning {ip} ...")
    scanner = nmap.PortScanner()
    try:
        scanner.scan(ip, arguments="-O")
        if ip in scanner.all_hosts():
            osmatch = scanner[ip].get('osmatch', [])
            if osmatch:
                print(f"[+] OS Detected: {osmatch[0]['name']}")
            else:
                print("[-] OS not detected.")
        else:
            print("[-] No host found.")
    except Exception as e:
        print(f"[OS Detection] Error: {e}")

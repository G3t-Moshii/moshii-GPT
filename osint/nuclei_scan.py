# osint/nuclei_scan.py

import subprocess

def run_nuclei_scan(target):
    try:
        print(f"[Nuclei] Scanning target: {target}")
        result = subprocess.run(["nuclei", "-u", target], capture_output=True, text=True)
        print(result.stdout)
    except Exception as e:
        print(f"[!] Nuclei scan failed: {str(e)}")

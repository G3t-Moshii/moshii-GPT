import requests

def color(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

def check_virustotal(indicator, api_key):
    print(f"[VT] Checking: {indicator}")
    
    url = f"https://www.virustotal.com/api/v3/search?query={indicator}"
    headers = {"x-apikey": api_key}

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()

        if "data" not in data or len(data["data"]) == 0:
            print(color("[-] No results found.", "33"))
            return

        item = data["data"][0]
        type_ = item.get("type", "unknown")
        id_ = item.get("id", "N/A")
        print(f"→ Type: {type_}, ID: {id_}")

        # Get full report using the ID
        report_url = f"https://www.virustotal.com/api/v3/{type_}s/{id_}"
        r2 = requests.get(report_url, headers=headers)
        r2.raise_for_status()
        report = r2.json()

        stats = report["data"]["attributes"]["last_analysis_stats"]
        harmless = stats.get("harmless", 0)
        malicious = stats.get("malicious", 0)
        suspicious = stats.get("suspicious", 0)
        undetected = stats.get("undetected", 0)

        if malicious > 0 or suspicious > 0:
            mal_color = "91"  # Red
        else:
            mal_color = "92"  # Green

        print(color(f"[+] Harmless: {harmless}", "92"))
        print(color(f"[+] Malicious: {malicious}", mal_color))
        print(color(f"[+] Suspicious: {suspicious}", mal_color))
        print(color(f"[+] Undetected: {undetected}", "90"))

        gui_link = f"https://www.virustotal.com/gui/{type_}/{id_}"
        print(color(f"[🔗] VT GUI Link: {gui_link}", "94"))

    except requests.exceptions.HTTPError as errh:
        print(color(f"[HTTP Error] {errh}", "91"))
    except requests.exceptions.ConnectionError:
        print(color("[!] Connection error. Check internet.", "91"))
    except Exception as e:
        print(color(f"[!] Unexpected error: {str(e)}", "91"))

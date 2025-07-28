import os
import json

API_FILE = os.path.join(os.path.dirname(__file__), "apikeys.json")

def load_api_keys():
    if os.path.exists(API_FILE):
        with open(API_FILE, "r") as f:
            return json.load(f)
    else:
        return ask_and_save_api_keys()

def ask_and_save_api_keys():
    print("[🔐] Enter your API keys (they'll be saved for future use):\n")
    chatgpt_key = input("🔑 OpenAI API key: ").strip()
    deepseek_key = input("🔑 DeepSeek API key (leave blank if not used): ").strip()
    vt_key = input("🔑 VirusTotal API key: ").strip()

    keys = {
        "chatgpt": chatgpt_key,
        "deepseek": deepseek_key,
        "virustotal": vt_key
    }

    with open(API_FILE, "w") as f:
        json.dump(keys, f, indent=2)

    print("\n✅ API keys saved.")
    return keys

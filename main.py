# main.py

import os
import sys
import readline
import atexit
from config import load_api_keys
from utils.banner import show_banner
from osint.whois_lookup import perform_whois
from osint.dns_lookup import perform_dns_lookup
from osint.subdomains import enumerate_subdomains
from osint.os_detection import detect_os
from osint.virus_total import check_virustotal
from osint.nuclei_scan import run_nuclei_scan
from smart_shell import interpret_and_run, handle_chat_mode

HISTORY_FILE = os.path.expanduser("~/.moshiigpt_history")
if os.path.exists(HISTORY_FILE):
    readline.read_history_file(HISTORY_FILE)
atexit.register(readline.write_history_file, HISTORY_FILE)

def show_help():
    print("""
MoshiiGPT Usage:
  moshiigpt [command] [args]

OSINT Commands:
  osint <target>         Run OSINT scan on a domain or IP
  detect-os <ip>         Detect operating system of a target IP
  vt <indicator>         Scan hash, domain, URL or IP via VirusTotal
  nuclei <target>        Run nuclei scanner on a target

Smart Shell Commands:
  ask <command>          Interpret and execute a smart shell command
  listen <iface> <port>  Start a netcat listener on interface and port
  start record <ip> [proto...]   Record traffic with optional protocol filter
  stop record <ip>       Stop recording for a specific IP
  stop all recordings    Stop all active recordings
  show recordings        Show all currently active recordings

AI Assistant:
  evade <goal>           Ask AI to generate AV-evasive code
  chat                   Start interactive AI chat mode
  chat --<provider> <question>  Ask a question to a specific AI provider

General:
  help                   Show this help message
  exit / quit            Exit the tool
""")

def main():
    show_banner()
    apis = load_api_keys()

    if len(sys.argv) > 1:
        cmd = " ".join(sys.argv[1:]).strip()
    else:
        cmd = input(f"\033[91m[moshii\033[0m@GPT]$ ").strip()

    while True:
        try:
            if not cmd:
                cmd = input(f"\033[91m[moshii\033[0m@GPT]$ ").strip()
                continue

            if cmd.startswith("osint "):
                target = cmd.split(" ")[1]
                perform_whois(target)
                perform_dns_lookup(target)
                enumerate_subdomains(target)

            elif cmd.startswith("detect-os "):
                ip = cmd.split(" ")[1]
                detect_os(ip)

            elif cmd.startswith("vt "):
                indicator = cmd.split(" ")[1]
                check_virustotal(indicator, apis['virustotal'])

            elif cmd.startswith("nuclei "):
                target = cmd.split(" ")[1]
                run_nuclei_scan(target)

            elif cmd.startswith("evade "):
                from ask_ai import ask_ai
                goal = cmd[6:].strip()
                prompt = f"Generate AV-evasive code to: {goal}. Use polymorphic or obfuscated techniques."
                try:
                    print(f"[🤖 Chatgpt]", ask_ai(prompt, apis, provider="chatgpt"))
                except Exception as e:
                    print("[🤖 ChatGPT] [AI ERROR]", str(e))

            elif cmd.startswith("chat"):
                provider = "chatgpt"
                query = ""

                if cmd.startswith("chat --"):
                    try:
                        _, flag, query = cmd.split(None, 2)
                        provider = flag.replace("--", "")
                    except ValueError:
                        print("[!] Invalid chat syntax. Use: chat --provider <question>")
                        cmd = input(f"\033[91m[moshii\033[0m@GPT]$ ").strip()
                        continue

                handle_chat_mode(apis, provider, query)

            elif cmd.startswith("ask"):
                output = interpret_and_run(cmd[3:].strip(), apis)
                print(output)

            elif cmd.startswith("listen") or cmd.startswith("start record") or cmd.startswith("stop record") or cmd in ["stop all recordings", "show recordings"]:
                output = interpret_and_run(cmd, apis)
                print(output)

            elif cmd in ["help", "--help", "-h"]:
                show_help()

            elif cmd in ["exit", "quit"]:
                print("[+] Exiting... Bye! ..See You :)")
                break

            else:
                print("[-] Unknown command. Try 'moshiigpt --help'")

            cmd = input(f"\033[91m[moshii\033[0m@GPT]$ ").strip()

        except KeyboardInterrupt:
            print("\n[+] Session interrupted. Type 'exit' to quit.")
            cmd = input(f"\033[91m[moshii\033[0m@GPT]$ ").strip()

if __name__ == "__main__":
    main()

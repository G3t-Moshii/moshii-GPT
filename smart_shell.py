# smart_shell.py

import subprocess
import os
import re
from ask_ai import ask_ai

recordings = {}

def interpret_and_run(command, apis):
    command = command.strip()

    if command.startswith("listen"):
        return handle_listen(command)
    elif command.startswith("start record"):
        return handle_start_record(command)
    elif command.startswith("stop record"):
        return handle_stop_record(command)
    elif command == "stop all recordings":
        return stop_all_recordings()
    elif command == "show recordings":
        return show_active_recordings()
    else:
        return f"[SmartShell] Sorry, I don't recognize that command yet."

def get_ip_of_interface(interface):
    try:
        output = subprocess.getoutput(f"ip -4 addr show {interface}")
        match = re.search(r"inet (\d+\.\d+\.\d+\.\d+)", output)
        return match.group(1) if match else None
    except:
        return None

def handle_listen(command):
    parts = command.split()
    if len(parts) != 3:
        return "Usage: listen <interface> <port>"
    interface, port = parts[1], parts[2]

    ip = get_ip_of_interface(interface)
    if not ip:
        return f"[-] Could not find IP for interface {interface}"

    print(f"Listening with: nc -nlvp {port} -s {ip}\nPress Ctrl+C to stop.")
    subprocess.call(["x-terminal-emulator", "-e", f"nc -nlvp {port} -s {ip}"])
    return ""

def handle_start_record(command):
    parts = command.split()
    if len(parts) < 3:
        return "Usage: start record <ip> [protocols...]"

    ip = parts[2]
    protocols = parts[3:]

    print("Select interface to capture on:")
    interfaces = get_interfaces()
    for idx, iface in enumerate(interfaces):
        print(f"{idx}. {iface}")
    selected = input("Choose interface number: ")
    try:
        iface = interfaces[int(selected)]
    except:
        return "Invalid selection."

    proto_filter = " or ".join(protocols) if protocols else ""
    filename = f"logs/{ip.replace('.', '_')}.pcap"
    os.makedirs("logs", exist_ok=True)

    cmd = ["tcpdump", "-i", iface, "host", ip, "-w", filename]
    if proto_filter:
        cmd += ["and", proto_filter]

    proc = subprocess.Popen(cmd)
    recordings[ip] = proc
    return f"[+] Started recording traffic to {filename} on {iface}"

def handle_stop_record(command):
    parts = command.split()
    if len(parts) != 3:
        return "Usage: stop record <ip>"
    ip = parts[2]
    proc = recordings.get(ip)
    if proc:
        proc.terminate()
        del recordings[ip]
        return f"[+] Stopped recording for {ip}"
    else:
        return f"[-] No active recording found for {ip}"

def stop_all_recordings():
    for ip, proc in recordings.items():
        proc.terminate()
    recordings.clear()
    return "[+] All recordings stopped."

def show_active_recordings():
    if not recordings:
        return "[+] No active recordings."
    return "\n".join([f"[*] {ip}" for ip in recordings])

def get_interfaces():
    output = subprocess.getoutput("ip -o link show | awk -F': ' '{print $2}'")
    return output.strip().split('\n')

def handle_chat_mode(apis, provider="chatgpt", initial_prompt=""):
    print("[Chat Mode] Started. Type your questions. Type 'exit' to leave chat mode.")
    while True:
        try:
            query = initial_prompt or input("\033[91m[moshii\033[0m@GPT]$ ").strip()

            if not query:
                continue
            if query.lower() == "exit":
                print("[+] Exiting Chat Mode.")
                break

            if query.startswith("chat --"):
                try:
                    parts = query.split(None, 2)
                    _, flag, message = parts
                    prov = flag.replace("--", "").strip()
                    if prov in apis:
                        provider = prov
                        query = message
                    else:
                        print(f"[!] Unknown provider '{prov}'")
                        continue
                except ValueError:
                    print("[!] Invalid chat syntax. Use: chat --provider <your question>")
                    continue

            try:
                response = ask_ai(query, apis, provider)
                print(f"[🤖 {provider.capitalize()}]", response)
            except Exception as e:
                print(f"[🤖 {provider.capitalize()}] [AI ERROR]", str(e))

            initial_prompt = ""
        except KeyboardInterrupt:
            print("\n[+] Exiting Chat Mode.")
            break

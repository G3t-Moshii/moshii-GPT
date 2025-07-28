# shell_core.py
import subprocess
import os
from datetime import datetime

recordings = {}  # Store active tcpdump processes

SUPPORTED_PROTOCOLS = {
    "http": "port 80",
    "https": "port 443",
    "dns": "port 53",
    "ftp": "port 21",
    "ssh": "port 22",
    "smtp": "port 25",
    "pop3": "port 110",
    "imap": "port 143"
}

def interpret_and_run(query: str) -> str:
    query = query.strip().lower()

    try:
        if query.startswith("listen"):
            parts = query.split()
            if len(parts) == 2:
                port = parts[1]
                return start_listener("0.0.0.0", port)
            elif len(parts) == 3:
                ip, port = parts[1], parts[2]
                return start_listener(ip, port)
            else:
                return "Usage: listen [ip] <port>"

        elif query.startswith("record"):
            return start_recording(query)

        elif query.startswith("stop all"):
            return stop_all_recordings()

        elif query.startswith("stop"):
            return stop_recording(query)

        elif query.startswith("show"):
            return show_recordings()

        else:
            return f"[SmartShell] Sorry, I don't recognize that command yet."

    except Exception as e:
        return f"[SmartShell ERROR] {str(e)}"

def start_listener(ip: str, port: str) -> str:
    try:
        cmd = ["nc", "-lvnp", port, "-s", ip]
        subprocess.Popen(cmd)
        return f"[+] Listening on {ip}:{port} using netcat..."
    except Exception as e:
        return f"[Netcat ERROR] {str(e)}"

def start_recording(command: str) -> str:
    parts = command.split()
    if len(parts) < 2:
        return "Usage: record <target_ip> [protocol1] [protocol2] ..."

    target_ip = parts[1]
    protocols = parts[2:] if len(parts) > 2 else []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    log_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(log_dir, exist_ok=True)

    filename = f"capture_{target_ip.replace('.', '_')}_{timestamp}.pcap"
    filepath = os.path.join(log_dir, filename)

    if protocols:
        filters = [SUPPORTED_PROTOCOLS.get(proto, f"port {proto}") for proto in protocols]
        filter_str = f"host {target_ip} and (" + " or ".join(filters) + ")"
    else:
        filter_str = f"host {target_ip}"

    try:
        proc = subprocess.Popen(["tcpdump", "-i", "any", "-w", filepath, filter_str],
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
        recordings[target_ip] = {"proc": proc, "file": filepath}
        return f"[+] Recording started for {target_ip} → File: {filepath}"
    except Exception as e:
        return f"[tcpdump ERROR] {str(e)}"

def stop_recording(command: str) -> str:
    parts = command.split()
    if len(parts) < 2:
        return "Usage: stop <target_ip>"

    target_ip = parts[1]
    rec = recordings.get(target_ip)
    if rec:
        rec["proc"].terminate()
        del recordings[target_ip]
        return f"[+] Recording for {target_ip} stopped. Saved to {rec['file']}"
    return f"[-] No active recording found for {target_ip}"

def stop_all_recordings() -> str:
    results = []
    for ip, rec in list(recordings.items()):
        rec["proc"].terminate()
        results.append(f"[+] Stopped {ip}, saved to {rec['file']}")
        del recordings[ip]
    return "\n".join(results) if results else "[-] No active recordings."

def show_recordings() -> str:
    if not recordings:
        return "[-] No active recordings."
    return "\n".join([f"[*] {ip} → {info['file']}" for ip, info in recordings.items()])

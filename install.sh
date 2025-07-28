#!/bin/bash

echo "[+] Starting installation..."

# Ensure running as root
if [ "$EUID" -ne 0 ]; then
  echo "[-] Please run as root"
  exit 1
fi

# --------- Install system tools ---------
TOOLS=("nmap" "netcat-openbsd" "tcpdump" "iproute2" "iputils-ping" "nano" "curl")

echo "[+] Installing required system tools..."
for tool in "${TOOLS[@]}"; do
  if ! dpkg -s "$tool" &>/dev/null; then
    echo "[*] Installing $tool..."
    apt-get install -y "$tool"
  else
    echo "[✓] $tool already installed."
  fi
done

# --------- Install Python packages ---------
echo "[+] Installing Python requirements..."
if [ -f requirements.txt ]; then
  pip3 install --no-cache-dir -r requirements.txt
else
  echo "[-] requirements.txt not found!"
  exit 1
fi

# --------- Make 'moshiigpt' globally accessible ---------
echo "[+] Making 'moshiigpt' command available..."
chmod +x moshiigpt
ln -sf "$(pwd)/moshiigpt" /usr/local/bin/moshiigpt

# --------- Create logs directory ---------
mkdir -p logs

echo "[✓] Installation complete! You can now run 'moshiigpt'"

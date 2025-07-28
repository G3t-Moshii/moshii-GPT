<h1 align="center">
  بــــسم الـلـه الرحــمــن الرحــيـم
</h1>
<h1 align="center">
  🚀 MoshiiGPT — CyberShell Assistant 🧠
</h1>

<p align="center">
  <img src="moshii-GPT" width="600" alt="Cyber GPT Animation"/>
</p>

<p align="center">
  <b>MoshiiGPT</b> is a sleek AI-powered cybersecurity shell assistant — 
  combining <code>OpenAI</code>, <code>DeepSeek</code>, and <code>Together AI</code> 
  into a beautiful terminal UI for OSINT, packet recording, scanning, and more!
</p>

---
🎯 Contribution & Roadmap

Multi-provider AI chat

Packet capture and real-time listening

OSINT collection with subdomain extraction
---
## ✨ Features

- 🔥 AI Chat Mode (ChatGPT, DeepSeek, Together.AI)
- 🕵️‍♂️ OSINT Gathering (WHOIS, DNS, Subdomains)
- 🎧 Packet Recording with `tcpdump`
- 👂 Listening on custom interfaces using `netcat`
- 📁 Logs saved in organized folders per target
- 🛡️ Works offline for passive recon
- 🤖 Smart shell interface: `[moshii@GPT]$` with command recall

---

## ⚙️ Installation
└─# git clone https://github.com/G3t-Moshii/moshii-GPT.git

└─# cd moshii-GPT

└─# pip install -r requirements.txt

└─# chmod +x moshiigpt

└─# ./moshiigpt
---
### 🔧 Prerequisites

- Python 3.9+
- `nmap`, `tcpdump`, `netcat`, `curl`, `nuclei`, etc.

---
Set your API keys in apikeys.json:

{
  "chatgpt": "sk-...",
  "deepseek": "sk-...",
  "together": "sk-...",
  "virustotal": "VT-..."
}
---


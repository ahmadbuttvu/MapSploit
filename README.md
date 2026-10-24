# MapSploit Framework 🛡️

An automated, non-intrusive vulnerability mapping tool that bridges Nmap reconnaissance with the Metasploit RPC to safely identify exploit modules without executing active payloads.

## 🚀 Features
*   **Smart Nmap Parsing:** Automatically runs version detection (`-sV`) and extracts open ports, services, and product versions.
*   **Context-Aware Mapping:** Connects seamlessly to a background `msfrpcd` (Metasploit RPC server) to find exploits.
*   **Advanced Scoring Engine:** Ranks exploits based on their reliability and filters out false positives by matching OS and vendor details.
*   **Safe & Non-Intrusive:** Does not fire active exploits, making it safe for enterprise-level auditing and portfolio demonstration.
*   **HTML Reporting:** Generates clean, professional HTML vulnerability reports.

## 🛠️ Prerequisites
*   Kali Linux (or any Linux distro with Metasploit Framework)
*   Python 3.x
*   Nmap
*   PostgreSQL (for Metasploit Database)

## 📦 Installation
```bash
# Clone the repository
git clone [https://github.com/ahmadbuttvu/MapSploit.git](https://github.com/ahmadbuttvu/MapSploit.git)
cd MapSploit

# Install required Python libraries
sudo pip install -r requirements.txt --break-system-packages

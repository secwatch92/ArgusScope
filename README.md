# ArgusScope

🔍 **ArgusScope** is a modular CLI tool for domain and subdomain enumeration, leveraging Python and MongoDB. Inspired by the all-seeing Argus, it offers pre-auth detection, passive and active discovery, and structured data storage. Ideal for penetration testers and red teamers in lab environments.

---

## ⚙️ Features

- **Pre-authenticated detection** of vulnerable FortiWeb versions
- **Reverse shell** (bash) via `/cgi-bin/shell.sh`
- **Encrypted data exfiltration** to `/tmp/exfil.txt` (Base64-encoded)
- **Persistence via cron job** (`/etc/cron.d/sys`)
- **Full cleanup** after use (removes shell, cron, and SQL traces)
- **Active only** while listener runs and cleanup is triggered

---

## 📋 Requirements

- Python 3.6+
- `requests` library: `pip install requests`

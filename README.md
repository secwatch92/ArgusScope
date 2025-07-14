# ArgusScope

🔍 ArgusScope is a modular CLI tool for domain and subdomain enumeration using Python and MongoDB. Inspired by the all‑seeing Argus, it offers passive & active discovery, structured storage, and export features. Ideal for pentesting labs.

---

## 🧰 Features

- Modular CLI commands (`program`, `domain`, `subdomain`, `url`, `ip`, `import`, `export`, `convert`)
- MongoDB-backed structured storage
- JSON/BSON import-export and CSV/XML conversion
- Designed for recon workflows (pentesting, bug bounty)

---

## 📋 Requirements

- Python 3.8+
- `pymongo` library: `pip install pymongo`
- [MongoDB](https://www.mongodb.com) (at least version 4.x)

---

## 🚀 Getting Started

```bash
git clone https://github.com/youruser/ArgusScope.git
cd ArgusScope
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python ssm.py --help


Then run commands like:

```bash
python ssm.py domain add example.com
python ssm.py subdomain list example.com
```

***

## 🗺️ Roadmap

* ✅ Core CLI commands implemented

* 🕵️ Add passive recon plugins (crt.sh, Amass, Sublist3r)

* 🔄 Add scanning modules (Nuclei, Nikto)

* 🤖 Add CI/CD with tests, linting, Docker image

* 🛠️ Add authentication and logging enhancements

***

## 🏷 Topics

`argusscope`, `pentesting`, `recon`, `osint`, `domain-enumeration`, `subdomain-enumeration`, `mongo`, `python`, `cli-tool`

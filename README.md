
# 🛡️ Vulnerable Web Applications Collection

> **⚠️ SECURITY WARNING**: This repository contains intentionally vulnerable applications for **educational and testing purposes only**. **DO NOT** expose any app to the internet or use in production environments.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/akintunero/vulnerable-web-apps)](https://github.com/akintunero/vulnerable-web-apps/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/akintunero/vulnerable-web-apps)](https://github.com/akintunero/vulnerable-web-apps/issues)

---

## 📚 Table of Contents

- [Overview](#overview)
- [Educational Value](#educational-value)
- [Projects](#projects)
  - [ConfusedCloud](#confusedcloud)
  - [CyberMart](#cybermart)
  - [FakeCrypto](#fakecrypto)
  - [HRLeaks](#hrleaks)
  - [SkyHack](#skyhack)
  - [VoteVault](#votevault)
- [Getting Started](#getting-started)
  - [Docker Setup (Recommended)](#docker-setup-recommended)
  - [Manual Setup (Python)](#manual-setup-python)
- [Usage](#usage)
- [Security Features](#security-features)
- [Contribution Guide](#contribution-guide)
- [Support](#support)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## 🧠 Overview

This repository contains a curated set of **intentionally vulnerable web applications** designed for:

- Ethical Hacking Practice
- Capture The Flag (CTF) Events
- Security Training Workshops
- Red Team Labs & Student Labs

Each app targets real-world vulnerabilities in a controlled, isolated environment.

---

## 🎓 Educational Value

- 🔐 Learn common web app security flaws
- 🧪 Practice hands-on penetration testing
- 🎯 Train for bug bounty & CTFs
- 👩🏽‍🏫 Deliver instructor-led workshops
- 🛠️ Understand defensive best practices

---

## 🚀 Projects

> ✅ Each app is self-contained and Docker-ready.

### 🔧 ConfusedCloud
- **Type**: Cloud Management Panel  
- **Vulnerabilities**: SQLi, XSS, CSRF, Auth Bypass  
- **Stack**: Flask, SQLite, Docker  
- **[View App →](./ConfusedCloud/)**

### 🛒 CyberMart
- **Type**: E-commerce Store  
- **Vulnerabilities**: NoSQLi, Command Injection, Unsafe Deserialization  
- **Stack**: Flask, MongoDB, Docker  
- **[View App →](./CyberMart/)**

### 💰 FakeCrypto
- **Type**: Cryptocurrency Exchange  
- **Vulnerabilities**: SSRF, XXE, Session Hijacking, Log Injection  
- **Stack**: Flask, SQLite, Web3  
- **[View App →](./FakeCrypto/)**

### 👥 HRLeaks
- **Type**: HR Management System  
- **Vulnerabilities**: Insecure Direct Object Reference (IDOR), Data Exposure  
- **Stack**: Flask, SQLite, File Uploads  
- **[View App →](./HRLeaks/)**

### ✈️ SkyHack
- **Type**: Airline Booking Portal  
- **Vulnerabilities**: JWT Tampering, API Abuse, Authorization Bypass  
- **Stack**: Flask, SQLite, JWT Auth  
- **[View App →](./SkyHack/)**

### 🗳️ VoteVault
- **Type**: Voting System  
- **Vulnerabilities**: Vote Manipulation, Auth Flaws, Blockchain Integrity  
- **Stack**: Flask, SQLite, Blockchain Concepts  
- **[View App →](./VoteVault/)**

---

## ⚙️ Getting Started

### ✅ Prerequisites

- [Docker](https://www.docker.com/)
- [Python 3.8+](https://www.python.org/downloads/)
- Git CLI

💡 If you're new to Docker, refer to [Docker Getting Started Guide](https://docs.docker.com/get-started/).

---

### 🐳 Docker Setup (Recommended)

```bash
git clone https://github.com/akintunero/vulnerable-web-apps.git
cd vulnerable-web-apps/ConfusedCloud   # Replace with desired project

docker-compose up -d
```

Then visit `http://localhost:5000` (or as specified).

---


## 🎮 Usage

You can run apps independently. Default ports:

Each project can be run independently using the provided `start.sh` scripts:

```bash
# ConfusedCloud
cd ConfusedCloud
./start.sh
# Access at http://localhost:8001

# CyberMart
cd CyberMart
./start.sh
# Access at http://localhost:5002

# FakeCrypto
cd FakeCrypto
./start.sh
# Access at http://localhost:7004

# HRLeaks
cd HRLeaks
./start.sh
# Access at http://localhost:8000

# SkyHack
cd SkyHack
./start.sh
# Access at http://localhost:8080

# VoteVault
cd VoteVault
./start.sh
# Access at http://localhost:5003
```

**Alternative Methods:**
- Use `docker-compose up -d` directly in each project directory
- CyberMart also has `./run.sh` for advanced management features


## 🤝 Contribution Guide

We welcome contributions! Follow the steps:

1. Fork the repository  
2. Create a feature branch  
3. Commit & push your changes  
4. Open a Pull Request

### 🧷 Guidelines

- Keep vulnerabilities educational, not destructive
- Include proper documentation
- Add test cases or proof-of-concept
- Use clean and readable code

### 🤖 Code of Conduct

We follow the [Contributor Covenant Code of Conduct](./CODE_OF_CONDUCT.md).

---

## 🆘 Support

- 📖 **Docs**: See individual app README files
- 🐞 **Issues**: [Submit an Issue](https://github.com/akintunero/vulnerable-web-apps/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/akintunero/vulnerable-web-apps/discussions)
- 📧 **Email**: akintunero101@gmail.com

---

## 📄 License

This project is licensed under the MIT License.  
See [LICENSE](./LICENSE) for full details.

---

## 🙏 Acknowledgments

Thanks to:

- The open-source security community
- Educators and security trainers
- Contributors and bug hunters
- Tools and libraries powering these apps

---

<div align="center">

**Made for the cybersecurity community. Practice responsibly.**

[![GitHub](https://img.shields.io/badge/GitHub-akintunero-181717?style=for-the-badge&logo=github)](https://github.com/akintunero)  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-olumayowaa-0077B5?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/olumayowaa)  
[![Twitter](https://img.shields.io/badge/Twitter-@akintunero-1DA1F2?style=for-the-badge&logo=twitter)](https://twitter.com/akintunero)

</div>

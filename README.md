
# 🛡️ Web Application Security Training Platform

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
  - [EnterpriseHR](#enterprisehr)
  - [SkyHack](#skyhack)
  - [VoteVault](#votevault)
- [Getting Started](#getting-started)
  - [Docker Setup (Recommended)](#docker-setup-recommended)
  - [Manual Setup (Python)](#manual-setup-python)
- [Usage](#usage)
- [Security Training](#security-training)
- [Contribution Guide](#contribution-guide)
- [Support](#support)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## 🧠 Overview

This repository contains a curated set of **web applications** designed for:

- Security Research and Testing
- Capture The Flag (CTF) Events
- Security Training Workshops
- Red Team Labs & Student Labs

Each application provides a controlled environment for learning web application security concepts.

---

## 🎓 Educational Value

- 🔐 Learn web application security concepts
- 🧪 Practice hands-on security testing
- 🎯 Train for security assessments
- 👩🏽‍🏫 Deliver instructor-led workshops
- 🛠️ Understand defensive best practices

---

## 🚀 Projects

> ✅ Each application is self-contained and Docker-ready.

### 🔧 ConfusedCloud
- **Type**: Cloud Management Panel  
- **Technology**: Flask, SQLite, Docker  
- **Purpose**: Cloud infrastructure management simulation
- **[View App →](./ConfusedCloud/)**

### 🛒 CyberMart
- **Type**: E-commerce Store  
- **Technology**: Flask, MongoDB, Docker  
- **Purpose**: Online retail platform simulation
- **[View App →](./CyberMart/)**

### 💰 FakeCrypto
- **Type**: Cryptocurrency Exchange  
- **Technology**: Flask, SQLite, Web3  
- **Purpose**: Digital asset trading simulation
- **[View App →](./FakeCrypto/)**

### 👥 EnterpriseHR
- **Type**: HR Management System  
- **Technology**: Flask, SQLite, File Uploads  
- **Purpose**: Human resources management simulation
- **[View App →](./EnterpriseHR/)**

### ✈️ SkyHack
- **Type**: Airline Booking Portal  
- **Technology**: Flask, SQLite, JWT Auth  
- **Purpose**: Travel booking system simulation
- **[View App →](./SkyHack/)**

### 🗳️ VoteVault
- **Type**: Voting System  
- **Technology**: Flask, SQLite, Blockchain Concepts  
- **Purpose**: Digital voting platform simulation
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

### 🐍 Manual Setup (Python) - (Not Recommended)

```bash
git clone https://github.com/akintunero/vulnerable-web-apps.git
cd vulnerable-web-apps/ConfusedCloud   # Replace with desired project

pip install -r requirements.txt
python app.py
```

---

## 🎮 Usage

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

# EnterpriseHR
cd EnterpriseHR
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

---

## 🔒 Security Training

These applications are designed for educational purposes and contain various security concepts for learning. Users are encouraged to:

- Practice in isolated environments
- Follow responsible disclosure practices
- Use only for authorized testing
- Respect the educational nature of these applications

---

## 🤝 Contribution Guide

We welcome contributions! Follow the steps:

1. Fork the repository  
2. Create a feature branch  
3. Commit & push your changes  
4. Open a Pull Request

### 🧷 Guidelines

- Keep applications educational and professional
- Include proper documentation
- Add test cases where appropriate
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
- Contributors and researchers
- Tools and libraries powering these applications

---

<div align="center">

**Made for the cybersecurity community. Practice responsibly.**

[![GitHub](https://img.shields.io/badge/GitHub-akintunero-181717?style=for-the-badge&logo=github)](https://github.com/akintunero)  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-olumayowaa-0077B5?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/olumayowaa)  
[![Twitter](https://img.shields.io/badge/Twitter-@akintunero-1DA1F2?style=for-the-badge&logo=twitter)](https://twitter.com/akintunero)

</div>

# 🛡️ Vulnerable Web Applications Collection

> **⚠️ SECURITY WARNING**: This repository contains intentionally vulnerable web applications for educational and testing purposes only. **DO NOT** deploy these applications in production environments or expose them to the internet.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/akintunero/vulnerable-web-apps)](https://github.com/akintunero/vulnerable-web-apps/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/akintunero/vulnerable-web-apps)](https://github.com/akintunero/vulnerable-web-apps/network)
[![GitHub issues](https://img.shields.io/github/issues/akintunero/vulnerable-web-apps)](https://github.com/akintunero/vulnerable-web-apps/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/akintunero/vulnerable-web-apps)](https://github.com/akintunero/vulnerable-web-apps/pulls)

## 📋 Table of Contents

- [Overview](#overview)
- [Projects](#projects)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [Security Features](#security-features)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## 🎯 Overview

This repository contains a comprehensive collection of intentionally vulnerable web applications designed for **educational purposes**, **security research**, and **penetration testing practice**. Each application demonstrates different types of web vulnerabilities and security flaws in a controlled environment.

### 🎓 Educational Value

- **Learn Security Concepts**: Understand common web vulnerabilities
- **Practice Penetration Testing**: Develop ethical hacking skills
- **Security Research**: Study attack vectors and defense mechanisms
- **CTF Challenges**: Use for Capture The Flag competitions
- **Security Training**: Perfect for security workshops and training sessions

## 🚀 Projects

### [🔧 ConfusedCloud](./ConfusedCloud/)
**Cloud Management Platform** | *Oct 17, 2024 - Jan 16, 2025*
- **Vulnerabilities**: SQL Injection, XSS, CSRF, Authentication Bypass
- **Features**: Multi-tenant cloud management, resource provisioning, billing system
- **Tech Stack**: Python Flask, SQLite, Docker
- **Difficulty**: ⭐⭐⭐

### [🛒 CyberMart](./CyberMart/)
**E-commerce Platform** | *Jan 2, 2025 - Jul 19, 2025*
- **Vulnerabilities**: NoSQL Injection, Command Injection, Deserialization
- **Features**: Shopping cart, payment processing, admin panel, product management
- **Tech Stack**: Python Flask, MongoDB, Docker
- **Difficulty**: ⭐⭐⭐⭐

### [💰 FakeCrypto](./FakeCrypto/)
**Cryptocurrency Exchange** | *Dec 13, 2024 - Apr 2, 2025*
- **Vulnerabilities**: SSRF, XXE, Log Injection, Session Management
- **Features**: Trading platform, wallet management, NFT marketplace, order book
- **Tech Stack**: Python Flask, SQLite, Web3 integration
- **Difficulty**: ⭐⭐⭐⭐⭐

### [👥 HRLeaks](./HRLeaks/)
**HR Management System** | *Jan 2, 2025 - Apr 15, 2025*
- **Vulnerabilities**: Information Disclosure, Access Control, Data Exposure
- **Features**: Employee management, payroll system, resume uploads, audit logs
- **Tech Stack**: Python Flask, SQLite, File upload handling
- **Difficulty**: ⭐⭐

### [✈️ SkyHack](./SkyHack/)
**Airline Booking System** | *Dec 22, 2024 - Apr 12, 2025*
- **Vulnerabilities**: JWT Manipulation, IDOR, API Security, Honeypot
- **Features**: Flight booking, boarding passes, check-in system, admin panel
- **Tech Stack**: Python Flask, SQLite, JWT authentication
- **Difficulty**: ⭐⭐⭐⭐

### [🗳️ VoteVault](./VoteVault/)
**Voting Platform** | *May 29, 2025 - Aug 15, 2025*
- **Vulnerabilities**: Vote Manipulation, Authentication Flaws, Data Integrity
- **Features**: Secure voting, result verification, admin dashboard, audit trails
- **Tech Stack**: Python Flask, SQLite, Blockchain concepts
- **Difficulty**: ⭐⭐⭐

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.8+
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/akintunero/vulnerable-web-apps.git
cd vulnerable-web-apps

# Choose a project to run
cd ConfusedCloud  # or any other project

# Start with Docker
docker-compose up -d

# Or run locally
pip install -r requirements.txt
python app.py
```

## 📦 Installation

### Method 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/akintunero/vulnerable-web-apps.git
cd vulnerable-web-apps

# Run any project
cd ConfusedCloud
docker-compose up -d
```

### Method 2: Local Development

```bash
# Clone the repository
git clone https://github.com/akintunero/vulnerable-web-apps.git
cd vulnerable-web-apps

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies for specific project
cd ConfusedCloud
pip install -r requirements.txt

# Run the application
python app.py
```

## 🎮 Usage

### Running Individual Projects

Each project can be run independently:

```bash
# ConfusedCloud
cd ConfusedCloud
docker-compose up -d
# Access at http://localhost:5000

# CyberMart
cd CyberMart
docker-compose up -d
# Access at http://localhost:5001

# FakeCrypto
cd FakeCrypto
docker-compose up -d
# Access at http://localhost:5002

# HRLeaks
cd HRLeaks
docker-compose up -d
# Access at http://localhost:5003

# SkyHack
cd SkyHack
docker-compose up -d
# Access at http://localhost:5004

# VoteVault
cd VoteVault
docker-compose up -d
# Access at http://localhost:5005
```

### Default Credentials

Most applications include default test accounts:

- **Username**: `admin` / **Password**: `admin`
- **Username**: `user` / **Password**: `password`
- **Username**: `test` / **Password**: `test123`

## 🛡️ Security Features

### Vulnerability Categories

| Category | Description | Projects |
|----------|-------------|----------|
| **SQL Injection** | Database query manipulation | ConfusedCloud, CyberMart |
| **XSS** | Cross-site scripting attacks | ConfusedCloud, HRLeaks |
| **CSRF** | Cross-site request forgery | ConfusedCloud, CyberMart |
| **Authentication** | Login bypass, session management | All projects |
| **Authorization** | Access control bypass | HRLeaks, SkyHack |
| **File Upload** | Malicious file uploads | FakeCrypto, HRLeaks |
| **API Security** | API endpoint vulnerabilities | SkyHack, VoteVault |
| **Cryptography** | Weak encryption, JWT manipulation | SkyHack, FakeCrypto |

### Learning Path

1. **Beginner**: Start with HRLeaks and VoteVault
2. **Intermediate**: Try ConfusedCloud and CyberMart
3. **Advanced**: Challenge yourself with FakeCrypto and SkyHack

## 🤝 Contributing

We welcome contributions! Please read our contributing guidelines.

### How to Contribute

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Contribution Guidelines

- 🔒 **Security First**: Ensure vulnerabilities are educational, not exploitable
- 📚 **Documentation**: Add clear documentation for new features
- 🧪 **Testing**: Include test cases for new vulnerabilities
- 🎯 **Educational Value**: Focus on learning and skill development

### Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Olumayowa Akinkuehinmi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🆘 Support

### Getting Help

- 📖 **Documentation**: Check individual project README files
- 🐛 **Issues**: Report bugs via [GitHub Issues](https://github.com/akintunero/vulnerable-web-apps/issues)
- 💬 **Discussions**: Join conversations in [GitHub Discussions](https://github.com/akintunero/vulnerable-web-apps/discussions)
- 📧 **Email**: Contact at akintunero101@gmail.com

### Community

- 🌟 **Star** this repository if you find it helpful
- 🔄 **Fork** to contribute or create your own version
- 📢 **Share** with security enthusiasts and learners
- 🐛 **Report** issues and suggest improvements

## 🙏 Acknowledgments

- **Security Researchers**: For identifying and documenting vulnerabilities
- **Open Source Community**: For tools and frameworks used
- **Educational Institutions**: For supporting security education
- **Contributors**: Everyone who helps improve this project

## 📊 Repository Statistics

- **Total Projects**: 6
- **Total Commits**: 287+
- **Lines of Code**: 50,000+
- **Vulnerability Types**: 15+
- **Supported Platforms**: Linux, macOS, Windows

---

<div align="center">

**Made with ❤️ for the security community**

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/akintunero)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/akintunero)
[![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/akintunero)

</div> 
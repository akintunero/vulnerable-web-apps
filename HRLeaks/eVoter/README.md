# E-VoteNow 🗳️

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Security](https://img.shields.io/badge/Security-Vulnerable%20Demo-red.svg)](SECURITY.md)

> **⚠️ SECURITY WARNING**: This is a deliberately vulnerable online voting platform designed for educational purposes. DO NOT use in production environments.

A modern, feature-rich online voting platform built with FastAPI, Jinja2, and Tailwind CSS. This project demonstrates various web security vulnerabilities for educational and testing purposes.

## 📋 Table of Contents

- [Features](#-features)
- [Security Vulnerabilities](#-security-vulnerabilities)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Architecture](#-architecture)
- [Contributing](#-contributing)
- [Security](#-security)
- [License](#-license)
- [Author](#-author)

## ✨ Features

### 🎯 Core Functionality
- **User Registration & Authentication** - Secure login system with session management
- **Real-time Voting** - Live vote casting with confirmation dialogs
- **Live Results** - Real-time election results with animated charts
- **Candidate Profiles** - Detailed candidate information and policies
- **Election Timer** - Countdown to election end with live updates
- **Geographic Results** - Regional voting breakdown by location
- **Export Functionality** - Download results in CSV/JSON formats

### 🎨 User Experience
- **Responsive Design** - Mobile-first approach with Tailwind CSS
- **Loading States** - Professional loading indicators and animations
- **Toast Notifications** - User feedback system
- **Vote Confirmation** - Two-step voting process
- **Real-time Updates** - Auto-refresh every 30 seconds
- **Accessibility** - Screen reader and keyboard navigation support

### 📊 Analytics & Insights
- **Voter Turnout** - Live percentage calculations
- **Regional Breakdown** - Geographic voting patterns
- **Voting Trends** - Early voting vs election day statistics
- **Audit Trail** - Complete vote logging for verification

## 🔒 Security Vulnerabilities

This platform intentionally contains multiple security vulnerabilities for educational purposes:

### 🚨 Critical Vulnerabilities
- **Weak Password Hashing** - MD5 instead of bcrypt/Argon2
- **No CSRF Protection** - Vulnerable to cross-site request forgery
- **SQL Injection** - Multiple endpoints vulnerable to SQL injection
- **Template Injection** - Server-side template injection (CVE-2019-16759)
- **Broken Cryptography** - Weak encryption keys and algorithms
- **Session Management** - Insecure session handling
- **Rate Limiting** - Minimal protection against vote spam

### 🕵️ Hidden Vulnerabilities
- **Backdoor Accounts** - Hardcoded admin credentials
- **Path Traversal** - Directory traversal vulnerabilities
- **SSRF** - Server-side request forgery
- **Command Injection** - OS command injection via user input
- **Header Injection** - HTTP header manipulation
- **Time-based Blind SQLi** - Advanced SQL injection techniques

### 🎯 Educational Value
- Perfect for learning web security concepts
- Ideal for penetration testing practice
- Great for security training workshops
- Demonstrates real-world vulnerability patterns

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### One-Command Setup
```bash
git clone https://github.com/akintunero/evoting-system.git
cd evoting-system
docker-compose up --build
```

Visit `http://localhost:8000` to access the application.

## 📦 Installation

### Option 1: Docker (Recommended)
```bash
# Clone the repository
git clone https://github.com/akintunero/evoting-system.git
cd evoting-system

# Build and run with Docker Compose
docker-compose up --build

# Access the application
open http://localhost:8000
```

### Option 2: Local Development
```bash
# Clone the repository
git clone https://github.com/akintunero/evoting-system.git
cd evoting-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 🎮 Usage



### Basic Workflow
1. **Register/Login** - Create an account
2. **View Candidates** - Learn about each candidate's policies
3. **Cast Vote** - Select your preferred candidate and confirm
4. **View Results** - Monitor live election results
5. **Export Data** - Download results in various formats

### Key Pages
- **Home** (`/`) - Landing page with election timer
- **Dashboard** (`/dashboard`) - Main voting interface
- **Candidates** (`/candidates`) - Candidate profiles and policies
- **Results** (`/results`) - Live election results
- **FAQ** (`/faq`) - Frequently asked questions

## 📚 API Documentation

### Core Endpoints
- `GET /` - Home page
- `GET /dashboard` - Voting dashboard
- `GET /results` - Election results
- `GET /candidates` - Candidate information
- `GET /faq` - FAQ page

### API Endpoints
- `GET /api/election-status` - Election timer and statistics
- `GET /api/geographic-results` - Regional voting data
- `GET /api/export-results` - Export results (CSV/JSON)

### Authentication Endpoints
- `GET /login` - Login page
- `POST /login` - Authenticate user
- `GET /register` - Registration page
- `POST /register` - Create new account
- `GET /logout` - End session

## 🔒 Educational Endpoints

Some endpoints are intentionally vulnerable and may not be linked from the UI. For a full list of educational/CTF endpoints, see [docs/vulnerabilities.md](docs/vulnerabilities.md).

## 🏗️ Architecture

### Tech Stack
- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: Jinja2 templates with Tailwind CSS
- **Database**: In-memory storage (for demo purposes)
- **Containerization**: Docker & Docker Compose
- **Security**: Intentionally vulnerable for education

### Project Structure
```
evoting-system/
├── app/
│   ├── main.py              # FastAPI application
│   ├── static/              # Static assets
│   └── templates/           # Jinja2 templates
├── docker-compose.yml       # Docker configuration
├── Dockerfile              # Container definition
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

### Key Components
- **Voting System** - Core voting logic and validation
- **User Management** - Registration, authentication, sessions
- **Results Engine** - Vote counting and statistics
- **Security Layer** - Intentionally vulnerable security measures
- **UI Components** - Responsive templates and styling

## 🤝 Contributing

We welcome contributions! Please read our contributing guidelines.

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/evoting-system.git
cd evoting-system

# Set up development environment
docker-compose up --build

# Make changes and test
# Submit pull request
```

### Code Style
- Follow PEP 8 for Python code
- Use meaningful commit messages
- Add tests for new features
- Update documentation as needed

## 🔒 Security

### Educational Purpose
This project is designed for educational purposes only. It contains intentional vulnerabilities to help students and security professionals learn about web security.

### Responsible Disclosure
If you discover a vulnerability not intentionally included for educational purposes, please report it responsibly:

1. **DO NOT** create public issues for security vulnerabilities
2. **DO** email security details to: akintunero10@gmail.com
3. **DO** include detailed reproduction steps
4. **DO** allow reasonable time for response

### Security Best Practices
For production voting systems, ensure:
- Strong password hashing (bcrypt, Argon2)
- CSRF protection on all forms
- Input validation and sanitization
- Proper session management
- Rate limiting and DDoS protection
- Regular security audits
- Compliance with election regulations

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Olúmáyòwá

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

## 👨‍💻 Author

**Olúmáyòwá**

- **Email**: akintunero10@gmail.com
- **GitHub**: [@akintunero](https://github.com/akintunero)
- **Project**: [E-VoteNow](https://github.com/akintunero/evoting-system)

### Acknowledgments
- FastAPI community for the excellent framework
- Tailwind CSS for the beautiful styling
- Security researchers who inspire educational projects
- Open source contributors worldwide

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

**🔒 Remember: This is for educational purposes only.**

**📧 Questions? Contact: akintunero10@gmail.com**

</div> 
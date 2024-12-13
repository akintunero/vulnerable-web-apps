# 🪙 FakeCrypto - Vulnerable Cryptocurrency Trading Platform

A deliberately vulnerable cryptocurrency trading platform designed for security research and penetration testing practice. This application demonstrates various web application vulnerabilities in a controlled, educational environment.

## ⚠️ **SECURITY WARNING**

**This application contains intentional vulnerabilities and should ONLY be run in isolated Docker containers. Never deploy to production or expose to public networks.**

## 🎯 Overview

FakeCrypto is a vulnerable cryptocurrency trading platform that simulates a real-world crypto exchange with multiple security flaws. It's designed to help security researchers, penetration testers, and students learn about web application security vulnerabilities.

### Key Features:
- 💰 Cryptocurrency trading simulation
- 🔐 Authentication vulnerabilities
- 💳 Payment processing flaws
- 📊 Data manipulation vulnerabilities
- 🎨 NFT marketplace with security issues

## 🚀 Quick Start

### Prerequisites
- Docker
- Docker Compose

### Installation & Setup

```bash
# Clone the repository
git clone git@github.com:akintunero/vulnerable-web-apps.git
cd vulnerable-web-apps/OpenSource/FakeCrypto

# Start the application
docker-compose up -d

# Access the application
# URL: http://localhost:5000
```

## 🏗️ Architecture

### Components
- **Frontend**: HTML/CSS/JavaScript with Tailwind CSS
- **Backend**: Python Flask application
- **Database**: SQLite with JSON data files
- **Container**: Docker with Python 3.9

### Directory Structure
```
FakeCrypto/
├── app.py              # Main Flask application
├── data_manager.py     # Data management utilities
├── templates/          # HTML templates
├── static/            # CSS, JS, images
├── data/              # JSON data files
├── logs/              # Application logs
├── docker-compose.yml # Docker configuration
├── Dockerfile         # Container definition
└── requirements.txt   # Python dependencies
```

## 🎓 Learning Objectives

### Vulnerability Categories
1. **SQL Injection**
   - Login form injection
   - Search functionality injection
   - Data retrieval vulnerabilities

2. **Cross-Site Scripting (XSS)**
   - Reflected XSS in search
   - Stored XSS in comments
   - DOM-based XSS

3. **Cross-Site Request Forgery (CSRF)**
   - Transaction manipulation
   - Account settings modification
   - Payment processing flaws

4. **Authentication Flaws**
   - Weak password policies
   - Session management issues
   - Privilege escalation

5. **Business Logic Vulnerabilities**
   - Price manipulation
   - Transaction race conditions
   - Balance manipulation

## 🔍 Vulnerability Guide

### 1. SQL Injection
- **Location**: Login and search forms
- **Technique**: SQL injection in input fields
- **Impact**: Unauthorized access and data extraction

### 2. Cross-Site Scripting (XSS)
- **Location**: Search functionality and user input
- **Technique**: Script injection in search queries
- **Impact**: Session hijacking and data theft

### 3. CSRF Vulnerabilities
- **Location**: Transaction and account forms
- **Technique**: Cross-site request forgery
- **Impact**: Unauthorized transactions and account modification

### 4. Authentication Bypass
- **Location**: Login system
- **Technique**: Various authentication bypass methods
- **Impact**: Unauthorized access to accounts

### 5. Business Logic Flaws
- **Location**: Trading and payment systems
- **Technique**: Price manipulation and race conditions
- **Impact**: Financial exploitation

## 🛠️ Development

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run locally (NOT recommended for production)
python app.py
```

### Docker Development
```bash
# Build and run
docker-compose up --build

# View logs
docker-compose logs -f

# Stop application
docker-compose down
```

## 📊 Features

### Trading Platform
- Real-time cryptocurrency prices
- Buy/sell functionality
- Portfolio management
- Transaction history

### NFT Marketplace
- NFT creation and trading
- Marketplace functionality
- Digital asset management

### User Management
- User registration and login
- Profile management
- Account settings
- Security preferences

### Admin Panel
- User management
- System monitoring
- Transaction oversight
- Security settings

## 🔧 Configuration

### Environment Variables
```bash
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///fakecrypto.db
```

### Docker Configuration
```yaml
version: '3.8'
services:
  fakecrypto:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    environment:
      - FLASK_ENV=development
```

## 🎯 Use Cases

### Security Research
- Study cryptocurrency platform vulnerabilities
- Practice financial application security testing
- Learn about trading platform security

### Educational Purposes
- Security training programs
- University cybersecurity courses
- Capture-the-flag (CTF) challenges

### Testing Environments
- Security tool testing
- Vulnerability scanner validation
- Security assessment practice

## 📈 Trading Features

### Supported Cryptocurrencies
- Bitcoin (BTC)
- Ethereum (ETH)
- Cardano (ADA)
- Dogecoin (DOGE)

### Trading Functions
- Real-time price updates
- Buy/sell orders
- Portfolio tracking
- Transaction history

### NFT Marketplace
- NFT creation
- Marketplace trading
- Digital asset management
- Collection browsing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add new vulnerabilities or improvements
4. Ensure Docker compatibility
5. Update documentation
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 📞 Contact

**Author:** Olúmáyòwá Akinkuehinmi  
**Email:** akintunero101@gmail.com  
**GitHub:** [@akintunero](https://github.com/akintunero)

---

**⚠️ Remember: This application contains intentional vulnerabilities. Use only in controlled, educational environments!** 
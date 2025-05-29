# 🗳️ VoteVault - Vulnerable Digital Voting System

A deliberately vulnerable digital voting system designed for security research and penetration testing practice. This application demonstrates various web application vulnerabilities in a controlled, educational environment.

## ⚠️ **SECURITY WARNING**

**This application contains intentional vulnerabilities and should ONLY be run in isolated Docker containers. Never deploy to production or expose to public networks.**

## 🎯 Overview

VoteVault is a vulnerable digital voting system that simulates a real-world electronic voting platform with multiple security flaws. It's designed to help security researchers, penetration testers, and students learn about web application security vulnerabilities.

### Key Features:
- 🗳️ Digital voting functionality
- 👥 Voter registration system
- 📊 Election results management
- 🔐 Authentication vulnerabilities
- 📈 Data manipulation flaws

## 🚀 Quick Start

### Prerequisites
- Docker
- Docker Compose

### Installation & Setup

```bash
# Clone the repository
git clone git@github.com:akintunero/vulnerable-web-apps.git
cd vulnerable-web-apps/OpenSource/VoteVault

# Start the application
docker-compose up -d

# Access the application
# URL: http://localhost:5000
```

## 🏗️ Architecture

### Components
- **Frontend**: HTML/CSS/JavaScript with Bootstrap
- **Backend**: Python Flask application
- **Database**: SQLite with JSON data files
- **Container**: Docker with Python 3.9

### Directory Structure
```
VoteVault/
├── backend/
│   ├── app.py          # Main Flask application
│   ├── templates/      # HTML templates
│   ├── static/         # CSS, JS, images
│   └── uploads/        # File uploads
├── docker-compose.yml  # Docker configuration
├── Dockerfile          # Container definition
└── requirements.txt    # Python dependencies
```

## 🎓 Learning Objectives

### Vulnerability Categories
1. **Vote Manipulation**
   - Vote tampering
   - Ballot stuffing
   - Result manipulation

2. **Authentication Flaws**
   - Weak password policies
   - Session management issues
   - Privilege escalation

3. **Data Exposure**
   - Voter information leakage
   - Election data exposure
   - Result disclosure

4. **Business Logic Vulnerabilities**
   - Access control flaws
   - Vote validation bypass
   - Election manipulation

5. **Information Disclosure**
   - Error message exposure
   - Debug information leakage
   - System information disclosure

## 🔍 Vulnerability Guide

### 1. Vote Manipulation
- **Location**: Voting interface
- **Technique**: Parameter manipulation
- **Impact**: Unauthorized vote modification

### 2. Authentication Bypass
- **Location**: Login system
- **Technique**: Various authentication bypass methods
- **Impact**: Unauthorized access to voting functions

### 3. Data Exposure
- **Location**: Election results and voter data
- **Technique**: Direct object reference
- **Impact**: Unauthorized access to sensitive data

### 4. Business Logic Flaws
- **Location**: Vote validation system
- **Technique**: Logic bypass and manipulation
- **Impact**: Vote tampering and result manipulation

### 5. Information Disclosure
- **Location**: Error pages and debug endpoints
- **Technique**: Error message analysis
- **Impact**: System information leakage

## 🛠️ Development

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run locally (NOT recommended for production)
python backend/app.py
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

### Voting System
- Voter registration
- Ballot creation
- Vote casting
- Result tabulation

### Election Management
- Election creation
- Candidate management
- Voter registration
- Result monitoring

### Administrative Functions
- User management
- Election oversight
- Result verification
- Security settings

### Voter Interface
- Voter authentication
- Ballot display
- Vote submission
- Result viewing

## 🔧 Configuration

### Environment Variables
```bash
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///votevault.db
```

### Docker Configuration
```yaml
version: '3.8'
services:
  votevault:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./uploads:/app/uploads
    environment:
      - FLASK_ENV=development
```

## 🎯 Use Cases

### Security Research
- Study voting system vulnerabilities
- Practice election security testing
- Learn about democracy protection

### Educational Purposes
- Security training programs
- University cybersecurity courses
- Capture-the-flag (CTF) challenges

### Testing Environments
- Security tool testing
- Vulnerability scanner validation
- Security assessment practice

## 📈 Voting Features

### Election Management
- Election creation
- Candidate registration
- Voter eligibility
- Result tabulation

### Voter Functions
- Voter registration
- Ballot access
- Vote casting
- Result viewing

### Administrative Functions
- User management
- Election oversight
- Result verification
- Security monitoring

### Security Features
- Vote verification
- Audit logging
- Result integrity
- Access control

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
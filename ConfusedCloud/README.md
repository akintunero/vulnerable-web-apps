# ☁️ ConfusedCloud - Vulnerable Cloud Management Platform

A deliberately vulnerable cloud management platform designed for security research and penetration testing practice. This application demonstrates various web application vulnerabilities in a controlled, educational environment.

## ⚠️ **SECURITY WARNING**

**This application contains intentional vulnerabilities and should ONLY be run in isolated Docker containers. Never deploy to production or expose to public networks.**

## 🎯 Overview

ConfusedCloud is a vulnerable cloud management platform that simulates a real-world cloud service with multiple security flaws. It's designed to help security researchers, penetration testers, and students learn about web application security vulnerabilities.

### Key Features:
- 🔐 Authentication bypass vulnerabilities
- 👥 Privilege escalation flaws
- 📊 Data exposure vulnerabilities
- 🔍 Information disclosure issues
- 🛡️ Security misconfigurations

## 🚀 Quick Start

### Prerequisites
- Docker
- Docker Compose

### Installation & Setup

```bash
# Clone the repository
git clone git@github.com:akintunero/vulnerable-web-apps.git
cd vulnerable-web-apps/OpenSource/ConfusedCloud

# Start the application
docker-compose up -d

# Access the application
# URL: http://localhost:5000
```

## 🏗️ Architecture

### Components
- **Frontend**: HTML/CSS/JavaScript with Bootstrap
- **Backend**: Python Flask application
- **Database**: SQLite (for simplicity)
- **Container**: Docker with Python 3.9

### Directory Structure
```
ConfusedCloud/
├── app/
│   ├── main.py          # Main Flask application
│   ├── data.py          # Data management
│   ├── static/          # CSS, JS, images
│   └── templates/       # HTML templates
├── data/                # JSON data files
├── docker-compose.yml   # Docker configuration
├── Dockerfile          # Container definition
└── requirements.txt    # Python dependencies
```

## 🎓 Learning Objectives

### Vulnerability Categories
1. **Authentication Bypass**
   - Weak password policies
   - Session management flaws
   - Authentication bypass techniques

2. **Privilege Escalation**
   - Role-based access control flaws
   - Admin panel access vulnerabilities
   - Permission bypass methods

3. **Data Exposure**
   - Sensitive data disclosure
   - API endpoint exposure
   - Configuration file access

4. **Information Disclosure**
   - Error message exposure
   - Debug information leakage
   - System information disclosure

## 🔍 Vulnerability Guide

### 1. Authentication Bypass
- **Location**: Login page
- **Technique**: SQL injection in login form
- **Impact**: Unauthorized access to admin panel

### 2. Privilege Escalation
- **Location**: User dashboard
- **Technique**: Parameter manipulation
- **Impact**: Access to admin functions

### 3. Data Exposure
- **Location**: API endpoints
- **Technique**: Directory traversal
- **Impact**: Access to sensitive configuration files

### 4. Information Disclosure
- **Location**: Error pages
- **Technique**: Error message analysis
- **Impact**: System information leakage

## 🛠️ Development

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run locally (NOT recommended for production)
python app/main.py
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

## 📊 API Endpoints

### Public Endpoints
- `GET /` - Home page
- `GET /login` - Login page
- `GET /register` - Registration page
- `GET /dashboard` - User dashboard

### Admin Endpoints
- `GET /admin` - Admin panel
- `GET /admin/users` - User management
- `GET /admin/settings` - System settings

### API Endpoints
- `GET /api/v1/users` - User data
- `GET /api/v1/settings` - System settings
- `POST /api/v1/admin` - Admin operations

## 🔧 Configuration

### Environment Variables
```bash
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///confusedcloud.db
```

### Docker Configuration
```yaml
version: '3.8'
services:
  confusedcloud:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
    environment:
      - FLASK_ENV=development
```

## 🎯 Use Cases

### Security Research
- Study vulnerability patterns
- Practice penetration testing
- Learn about web application security

### Educational Purposes
- Security training programs
- University cybersecurity courses
- Capture-the-flag (CTF) challenges

### Testing Environments
- Security tool testing
- Vulnerability scanner validation
- Security assessment practice

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
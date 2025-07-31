# Vulnerable Web Applications Collection

A comprehensive collection of intentionally vulnerable web applications designed for security testing, penetration testing practice, and educational purposes.

## 🚨 **IMPORTANT SECURITY WARNING**

⚠️ **These applications contain intentional security vulnerabilities and should NEVER be deployed in production environments or exposed to the internet.**

⚠️ **Use only in isolated, controlled environments for educational and testing purposes.**

## 📁 Project Structure

This repository contains multiple vulnerable web applications, each designed to demonstrate different types of security vulnerabilities:

### 🏗️ **ConfusedCloud** - Cloud Management Platform
- **Vulnerabilities**: SQL Injection, XSS, CSRF, Authentication Bypass
- **Technology**: Flask, Python
- **Features**: Cloud service management, billing, user dashboard
- **Educational Value**: Real-world cloud platform vulnerabilities

### 🛒 **CyberMart** - E-commerce Platform  
- **Vulnerabilities**: Command Injection, Deserialization, SSRF, XXE
- **Technology**: Flask, Python
- **Features**: Product catalog, shopping cart, admin panel
- **Educational Value**: E-commerce security testing scenarios

### 💰 **FakeCrypto** - Cryptocurrency Exchange
- **Vulnerabilities**: Session Management, Input Validation, Authorization Flaws
- **Technology**: Flask, Python
- **Features**: Trading platform, wallet management, NFT marketplace
- **Educational Value**: Financial application security testing

### 👥 **HRLeaks** - Human Resources System
- **Vulnerabilities**: Data Exposure, Access Control, Information Disclosure
- **Technology**: Flask, Python
- **Features**: Employee management, payroll, resume handling
- **Educational Value**: HR system security and data privacy

### ✈️ **SkyHack** - Airline Booking System
- **Vulnerabilities**: JWT Manipulation, API Security, Session Hijacking
- **Technology**: Flask, Python
- **Features**: Flight booking, check-in, frequent flyer program
- **Educational Value**: Travel industry security testing

### 🗳️ **VoteVault** - Voting System
- **Vulnerabilities**: Election Security, Vote Manipulation, Audit Trail
- **Technology**: Flask, Python
- **Features**: Digital voting, result verification, admin controls
- **Educational Value**: Critical infrastructure security

## 🛠️ Setup Instructions

### Prerequisites
- Docker and Docker Compose
- Python 3.8+
- Git

### Quick Start
```bash
# Clone the repository
git clone git@github.com:akintunero/vulnerable-web-apps.git
cd vulnerable-web-apps

# Choose a project to run
cd ConfusedCloud  # or any other project

# Start with Docker
docker-compose up -d

# Or run locally
pip install -r requirements.txt
python app.py
```

## 🎯 Learning Objectives

Each application is designed to teach specific security concepts:

- **OWASP Top 10** vulnerabilities
- **Web Application Security** testing methodologies
- **Penetration Testing** techniques
- **Secure Coding** practices
- **Security Assessment** frameworks

## 📚 Educational Resources

### Recommended Learning Path
1. **Start with ConfusedCloud** - Basic web vulnerabilities
2. **Progress to CyberMart** - E-commerce security
3. **Explore FakeCrypto** - Financial application security
4. **Study HRLeaks** - Data privacy and access control
5. **Master SkyHack** - API and session security
6. **Challenge with VoteVault** - Critical infrastructure security

### Security Testing Tools
- **Burp Suite** - Web application security testing
- **OWASP ZAP** - Automated security scanning
- **SQLMap** - SQL injection testing
- **Nikto** - Web server vulnerability scanner

## 🔒 Security Categories Covered

### Injection Attacks
- SQL Injection
- NoSQL Injection
- Command Injection
- LDAP Injection

### Cross-Site Attacks
- Cross-Site Scripting (XSS)
- Cross-Site Request Forgery (CSRF)
- Cross-Origin Resource Sharing (CORS)

### Authentication & Authorization
- Session Management
- JWT Security
- Access Control
- Privilege Escalation

### Data Security
- Input Validation
- Output Encoding
- Data Encryption
- Secure Communication

## 🚀 Contributing

We welcome contributions to improve the educational value of these applications:

1. **Fork** the repository
2. **Create** a feature branch
3. **Add** new vulnerabilities or improve existing ones
4. **Submit** a pull request

### Contribution Guidelines
- Ensure vulnerabilities are clearly documented
- Include educational materials and walkthroughs
- Maintain realistic application scenarios
- Follow secure coding practices for the framework code

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚖️ Disclaimer

This software is provided for educational purposes only. The authors are not responsible for any misuse of these applications. Users are responsible for ensuring they comply with applicable laws and regulations.

## 🤝 Support

For questions, issues, or contributions:
- **Issues**: Use GitHub Issues
- **Discussions**: Use GitHub Discussions
- **Security**: Report security issues privately

---

**Remember**: These applications are intentionally vulnerable. Use responsibly and only in controlled environments for learning and testing purposes. 
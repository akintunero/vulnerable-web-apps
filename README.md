# 🚀 Vulnerable Web Applications Collection

A comprehensive collection of intentionally vulnerable web applications designed for security research, penetration testing practice, and educational purposes. **All applications are containerized with Docker for safe isolation.**

## ⚠️ **IMPORTANT SECURITY NOTICE**

**These applications contain intentional vulnerabilities and should ONLY be run in isolated Docker containers. Never deploy these applications in production environments or on public-facing servers.**

## 📋 Table of Contents

- [Overview](#overview)
- [Projects](#projects)
- [Quick Start](#quick-start)
- [Security Guidelines](#security-guidelines)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## 🎯 Overview

This repository contains a curated collection of vulnerable web applications, each designed to demonstrate specific security vulnerabilities in a controlled, educational environment. All applications are Dockerized to ensure safe isolation and easy deployment.

### Key Features:
- 🔒 **Docker Isolation**: All apps run in isolated containers
- 🎓 **Educational Focus**: Designed for learning security concepts
- 🛡️ **Controlled Environment**: Safe for security research
- 📚 **Comprehensive Documentation**: Detailed setup and vulnerability guides

## 🏗️ Projects

### [ConfusedCloud](ConfusedCloud/) - Cloud Management Platform
A vulnerable cloud management platform demonstrating various web application vulnerabilities including authentication bypass, privilege escalation, and data exposure.

### [FakeCrypto](FakeCrypto/) - Cryptocurrency Trading Platform
A vulnerable cryptocurrency trading platform featuring SQL injection, XSS, CSRF, and other common web vulnerabilities.

### [HRLeaks](HRLeaks/) - Human Resources Management System
A vulnerable HR management system showcasing data exposure, authentication flaws, and business logic vulnerabilities.

### [VoteVault](VoteVault/) - Digital Voting System
A vulnerable digital voting platform demonstrating election security vulnerabilities and data integrity issues.

### [SkyHack](SkyHack/) - Airline Booking System
A vulnerable airline booking system featuring authentication bypass, data manipulation, and session management flaws.

### [CyberMart](CyberMart/) - E-commerce Shopping Cart
A vulnerable e-commerce platform demonstrating payment processing vulnerabilities, cart manipulation, and checkout race conditions.

## 🚀 Quick Start

### Prerequisites
- Docker
- Docker Compose
- Git

### Installation
```bash
# Clone the repository
git clone git@github.com:akintunero/vulnerable-web-apps.git
cd vulnerable-web-apps

# Navigate to any project directory
cd OpenSource/[project-name]

# Start the application
docker-compose up -d
```

### Example: Starting ConfusedCloud
```bash
cd OpenSource/ConfusedCloud
docker-compose up -d
# Access at http://localhost:5000
```

## 🛡️ Security Guidelines

### **CRITICAL RULES:**
1. **NEVER** deploy these applications in production
2. **ALWAYS** run in isolated Docker containers
3. **NEVER** expose to public networks
4. **ONLY** use for educational purposes
5. **ALWAYS** use strong passwords for admin accounts

### Safe Usage:
- ✅ Run in Docker containers
- ✅ Use on isolated networks
- ✅ Use for security research
- ✅ Use for educational purposes
- ✅ Use for penetration testing practice

### Unsafe Usage:
- ❌ Deploy to production
- ❌ Expose to public internet
- ❌ Use with real data
- ❌ Use for actual business operations

## 🎓 Educational Use Cases

- **Security Research**: Study vulnerability patterns
- **Penetration Testing**: Practice ethical hacking
- **Security Training**: Learn about web application security
- **CTF Challenges**: Create capture-the-flag scenarios
- **Security Auditing**: Practice security assessments

## 🤝 Contributing

We welcome contributions! Please read our contributing guidelines:

1. **Fork** the repository
2. **Create** a feature branch
3. **Add** your vulnerable application
4. **Ensure** Docker containerization
5. **Document** vulnerabilities clearly
6. **Submit** a pull request

### Adding New Projects
When adding a new vulnerable application:

1. Create a new directory under `OpenSource/`
2. Include `Dockerfile` and `docker-compose.yml`
3. Add comprehensive `README.md`
4. Document all vulnerabilities
5. Include setup instructions
6. Add security warnings

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

**Author:** Olúmáyòwá Akinkuehinmi  
**Email:** akintunero101@gmail.com  
**GitHub:** [@akintunero](https://github.com/akintunero)

## 🙏 Acknowledgments

- Security researchers and penetration testers
- Open source security community
- Educational institutions using these applications
- Contributors and maintainers

---

**⚠️ Remember: These applications contain intentional vulnerabilities. Use responsibly and only in controlled environments!** 
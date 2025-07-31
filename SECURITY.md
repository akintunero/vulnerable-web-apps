# Security Policy

## Supported Versions

Use this section to tell people about which versions of your project are currently being supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

### ⚠️ Important Notice

This repository contains **intentionally vulnerable web applications** designed for educational purposes. These applications are meant to be run in controlled, isolated environments for:

- Security education and training
- Penetration testing practice
- Security research and development
- Capture The Flag (CTF) competitions

### 🚨 Security Reporting

If you discover a **real security vulnerability** (not an intentional educational vulnerability) in our applications, please report it responsibly:

#### How to Report

1. **Email**: Send detailed information to akintunero101@gmail.com
2. **Subject Line**: Use "SECURITY VULNERABILITY: [Brief Description]"
3. **Include**:
   - Detailed description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if applicable)

#### What to Include

```
Subject: SECURITY VULNERABILITY: [Brief Description]

Description:
[Detailed description of the vulnerability]

Steps to Reproduce:
1. [Step 1]
2. [Step 2]
3. [Step 3]

Impact:
[Description of potential impact]

Suggested Fix:
[Optional: Your suggested solution]

Environment:
- OS: [Your operating system]
- Python Version: [Your Python version]
- Browser: [Your browser and version]
```

### 🛡️ Vulnerability Types

#### Intentional Educational Vulnerabilities

These are **expected and documented**:

- SQL Injection vulnerabilities
- Cross-Site Scripting (XSS)
- Cross-Site Request Forgery (CSRF)
- Authentication bypasses
- File upload vulnerabilities
- Command injection
- Deserialization vulnerabilities

#### Real Security Issues

These should be **reported immediately**:

- Remote code execution (RCE)
- Server-side request forgery (SSRF)
- Critical authentication bypasses
- Data exposure vulnerabilities
- Docker escape vulnerabilities
- Network security issues

### 🔒 Responsible Disclosure

We follow responsible disclosure practices:

1. **Acknowledge**: We will acknowledge receipt within 48 hours
2. **Investigate**: We will investigate and validate the report
3. **Fix**: We will develop and test a fix
4. **Disclose**: We will disclose the vulnerability appropriately
5. **Credit**: We will credit the reporter (if desired)

### 📅 Disclosure Timeline

- **48 hours**: Initial response and acknowledgment
- **7 days**: Status update and investigation results
- **30 days**: Fix development and testing
- **60 days**: Public disclosure (if applicable)

### 🎯 Scope

#### In Scope

- Security vulnerabilities in application code
- Docker configuration issues
- Deployment security problems
- Documentation security concerns

#### Out of Scope

- Intentional educational vulnerabilities
- Issues in dependencies (report to upstream)
- General security best practices
- Feature requests or enhancements

### 🏆 Recognition

Security researchers who responsibly report vulnerabilities will be:

- **Credited**: In security advisories and documentation
- **Thanked**: Publicly acknowledged for their contribution
- **Listed**: Added to our security researchers hall of fame

### 📞 Contact Information

**Primary Contact**: akintunero101@gmail.com

**Alternative Contact**: GitHub Issues (for non-sensitive reports)

**PGP Key**: Available upon request for sensitive communications

### 🔐 Security Best Practices

#### For Users

1. **Isolated Environment**: Always run applications in isolated containers
2. **No Production Use**: Never deploy these applications in production
3. **Network Isolation**: Use isolated networks or VPNs
4. **Regular Updates**: Keep dependencies updated
5. **Monitoring**: Monitor for unexpected behavior

#### For Contributors

1. **Educational Focus**: Ensure vulnerabilities are for learning
2. **Clear Documentation**: Document all security issues
3. **Safe Defaults**: Use secure configurations by default
4. **Testing**: Thoroughly test all security features
5. **Review**: Have security features reviewed by peers

### 📋 Security Checklist

Before contributing security-related code:

- [ ] Vulnerability is educational, not exploitable
- [ ] Clear documentation of the security issue
- [ ] Safe default configurations
- [ ] Proper error handling
- [ ] Input validation where appropriate
- [ ] Security warnings in documentation
- [ ] Test cases for the vulnerability
- [ ] No sensitive data in code or logs

### 🚨 Emergency Contacts

For critical security issues requiring immediate attention:

- **Email**: akintunero101@gmail.com
- **Subject**: "URGENT: Critical Security Issue"
- **Response Time**: Within 24 hours

### 📊 Security Metrics

We track and report on:

- Number of security reports received
- Average time to fix vulnerabilities
- Types of vulnerabilities reported
- Security researcher contributions

### 🔄 Security Updates

- **Monthly**: Security dependency updates
- **Quarterly**: Security review of applications
- **Annually**: Comprehensive security audit

---

**Remember**: These applications are for educational purposes only. Always use them responsibly and in controlled environments. 
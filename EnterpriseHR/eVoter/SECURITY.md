# Security Policy

## Supported Versions

This project is designed for educational purposes and contains intentional vulnerabilities. Use only in controlled, isolated environments.

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

### ⚠️ Important Notice

This project **intentionally contains multiple security vulnerabilities** for educational purposes. These vulnerabilities are part of the learning experience and are not bugs to be fixed.

### What to Report

**DO report:**
- Vulnerabilities not intentionally included for educational purposes
- Issues with the documentation or setup process
- Bugs in the user interface or functionality
- Performance issues

**DO NOT report:**
- Intentional vulnerabilities (SQL injection, XSS, etc.)
- Weak password hashing (MD5)
- Missing CSRF protection
- Insecure session management
- Any other deliberately vulnerable features

### How to Report

If you discover a legitimate security issue:

1. **DO NOT** create a public GitHub issue
2. **DO** email security details to: **akintunero10@gmail.com**
3. **DO** include:
   - Detailed description of the vulnerability
   - Step-by-step reproduction instructions
   - Potential impact assessment
   - Suggested fix (if applicable)
4. **DO** allow reasonable time for response (typically 48-72 hours)

### Responsible Disclosure Timeline

- **Initial Response**: Within 48 hours
- **Assessment**: Within 1 week
- **Fix Development**: Within 2 weeks (if applicable)
- **Public Disclosure**: After fix is deployed

## Known Vulnerabilities

This section documents the intentional vulnerabilities for educational purposes:

### Critical Vulnerabilities

| Vulnerability | Description | Educational Value |
|---------------|-------------|-------------------|
| SQL Injection | Multiple endpoints vulnerable | Learn SQL injection techniques |
| Template Injection | Jinja2 template injection | Understand SSTI attacks |
| Weak Password Hashing | MD5 instead of bcrypt | Password security importance |
| No CSRF Protection | Forms vulnerable to CSRF | Cross-site request forgery |
| Session Management | Insecure session handling | Session security best practices |
| Rate Limiting | Minimal protection | DDoS and brute force attacks |

### Hidden Vulnerabilities

| Vulnerability | Description | Location |
|---------------|-------------|----------|
| Backdoor Accounts | Hardcoded credentials | Multiple admin accounts |
| Path Traversal | Directory traversal | File access endpoints |
| SSRF | Server-side request forgery | URL processing |
| Command Injection | OS command injection | User input processing |
| Header Injection | HTTP header manipulation | Response headers |
| XSS | Cross-site scripting | User input display |

### Educational Use Cases

1. **Penetration Testing Practice**
   - Learn common web vulnerabilities
   - Practice exploitation techniques
   - Understand attack vectors

2. **Security Training**
   - CTF (Capture The Flag) challenges
   - Security workshops
   - Code review exercises

3. **Research and Development**
   - Security tool testing
   - Vulnerability scanner validation
   - Security framework development

## Security Best Practices

### For Production Voting Systems

If you're building a real voting system, ensure:

- **Strong Authentication**
  - Use bcrypt, Argon2, or PBKDF2 for password hashing
  - Implement multi-factor authentication
  - Use secure session management

- **Input Validation**
  - Validate and sanitize all user inputs
  - Use parameterized queries for database operations
  - Implement proper CSRF protection

- **Access Control**
  - Implement role-based access control
  - Use principle of least privilege
  - Regular access reviews

- **Data Protection**
  - Encrypt sensitive data at rest and in transit
  - Implement proper key management
  - Regular security audits

- **Monitoring and Logging**
  - Comprehensive audit trails
  - Real-time security monitoring
  - Incident response procedures

### For Educational Use

When using this project for learning:

1. **Isolated Environment**
   - Use Docker containers
   - Never expose to public internet
   - Use virtual machines if needed

2. **Controlled Access**
   - Limit access to authorized users only
   - Monitor usage and activities
   - Regular environment resets

3. **Documentation**
   - Document learning objectives
   - Track vulnerability discoveries
   - Share findings responsibly

## Contact Information

**Security Contact**: akintunero10@gmail.com

**Response Time**: 48-72 hours for initial response

**Encryption**: PGP key available upon request

---

**Remember**: This project is for educational purposes only. Never use in production environments or with real data. 
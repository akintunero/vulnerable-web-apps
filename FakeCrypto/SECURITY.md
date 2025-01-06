# Security Policy

## Supported Versions

This project is designed for educational purposes and contains intentional vulnerabilities. However, we take security seriously and will address any unintended security issues.

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |

## Reporting a Vulnerability

**Important**: This application contains intentional vulnerabilities for educational purposes. Before reporting, please ensure you're reporting an unintended security issue, not one of the documented intentional vulnerabilities.

### How to Report

If you discover a security vulnerability, please follow these steps:

1. **Do not create a public GitHub issue** for security vulnerabilities
2. **Email us directly** at akintunero10@gmail.com with the subject line: `[SECURITY] Vulnerability Report`
3. **Include detailed information** about the vulnerability:
   - Description of the issue
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)
   - Your contact information

### What to Include in Your Report

- **Clear description** of the vulnerability
- **Proof of concept** or steps to reproduce
- **Impact assessment** (what could an attacker do?)
- **Environment details** (Docker version, OS, etc.)
- **Timeline** for disclosure (if you have preferences)

### Response Timeline

- **Initial response**: Within 48 hours
- **Status update**: Within 1 week
- **Resolution**: Depends on complexity, typically 2-4 weeks

### Responsible Disclosure

We follow responsible disclosure practices:

1. **Private reporting** - We'll work with you privately
2. **Timely response** - We'll acknowledge and investigate promptly
3. **Coordinated disclosure** - We'll coordinate public disclosure
4. **Credit acknowledgment** - We'll credit you in our security advisories

## Intentional Vulnerabilities

This application contains the following **intentional vulnerabilities** for educational purposes:

- Private key exposure
- Logic flaws in token transfers
- Open redirect vulnerabilities
- Hardcoded credentials
- Plain text password storage
- Input validation bypasses
- And others throughout the application

**These are NOT security bugs** - they are part of the educational design.

## Security Best Practices

When using this application:

1. **Never use real credentials** or private keys
2. **Run only in isolated environments** (Docker containers)
3. **Do not deploy to production** or public-facing servers
4. **Use only for educational purposes** and security research
5. **Follow responsible disclosure** for any unintended issues

## Security Features

This application includes several security measures:

- **Container isolation** - All vulnerabilities are contained within Docker
- **Non-root user** - Application runs as non-privileged user
- **Resource limits** - Memory and CPU limits prevent abuse
- **Read-only filesystem** - Except for necessary data volumes
- **Network isolation** - Custom Docker network

## Contact Information

- **Security Email**: akintunero10@gmail.com
- **Maintainer**: Olúmáyòwá (@akintunero)
- **GitHub**: https://github.com/akintunero/fakecryptox

## Acknowledgments

We appreciate security researchers who responsibly report vulnerabilities. Contributors will be acknowledged in:

- Security advisories
- Release notes
- Project documentation

Thank you for helping make FakeCryptoX more secure for educational use! 
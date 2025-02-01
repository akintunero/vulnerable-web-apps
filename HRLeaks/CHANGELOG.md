# Changelog

All notable changes to HRLeaks will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-XX

### 🎉 **Initial Release**

#### ✨ **Added**
- Complete HR management system with FastAPI backend
- Jinja2 templates with Tailwind CSS frontend
- Docker containerization with docker-compose
- Employee management (CRUD operations)
- Payroll processing and management
- Resume/CV storage and management
- Audit logging system
- User authentication and authorization
- Mock data with realistic UK-based information
- Professional UI without security warnings

#### 🔒 **Security Features (Intentional Vulnerabilities)**
- **26 total vulnerabilities** implemented:
  - 12 real CVE implementations
  - 14 additional vulnerability types
- Cross-Site Scripting (XSS) vulnerabilities
- SQL Injection vulnerabilities
- Command Injection vulnerabilities
- Path Traversal vulnerabilities
- XML External Entity (XXE) vulnerabilities
- Insecure Deserialization
- Server-Side Template Injection (SSTI)
- Insecure File Upload
- Information Disclosure
- Insecure Random Generation
- Buffer Overflow simulation
- Insecure eval usage
- Log4Shell variants (CVE-2021-44228)
- Insecure PDF viewer (CVE-2023-25690)

#### 🌍 **Localization**
- UK-based data and currency (GBP £)
- UK address formats and phone numbers
- British English spelling and terminology
- UK-specific company information

#### 🐳 **Infrastructure**
- Docker containerization
- Docker Compose setup
- Volume persistence for data
- Health check endpoints
- Environment variable configuration

#### 📚 **Documentation**
- Comprehensive README.md
- MIT License
- Contributing guidelines
- Security policy
- Changelog
- Open-source standard documentation

#### 🧪 **Testing Features**
- Mock pages for demonstration
- Multiple access methods
- Realistic test scenarios
- Educational vulnerability examples
- Safe testing environment

#### 🔧 **Technical Features**
- Session-based authentication
- Cookie management
- JSON data persistence
- File upload handling
- PDF generation and viewing
- Audit trail logging
- Role-based access control

### 🐛 **Fixed**
- Route conflicts with "new" being parsed as integer
- Missing CRUD functionality for employees, resumes, and payroll
- Jinja2 template strftime filter issues
- Missing LDAP libraries in Docker build
- Internal server errors on login due to missing email field
- Template rendering issues

### 🔄 **Changed**
- Removed security warnings from UI for professional appearance
- Updated navigation structure
- Improved error handling
- Enhanced data validation
- Streamlined user experience

### 🗑️ **Removed**
- Security testing section from navigation
- Demo credentials from login page
- Detailed vulnerability information from public pages
- Unnecessary security notices

---

## [Unreleased]

### 🚧 **Planned Features**
- Additional vulnerability types
- Enhanced testing scenarios
- More realistic data sets
- Advanced exploitation techniques
- Mobile-responsive design improvements
- API documentation
- Automated testing suite

### 🔮 **Future Enhancements**
- Multi-language support
- Advanced reporting features
- Integration with security tools
- Educational content expansion
- Community features
- Enterprise features

---

## Version History

- **1.0.0** - Initial release with complete HR system and 26 vulnerabilities
- **Unreleased** - Future enhancements and improvements

---

## Release Notes

### Version 1.0.0
This is the initial release of HRLeaks, providing a comprehensive vulnerable HR management system for security testing and educational purposes. The application includes a full-featured HR system with 26 intentional vulnerabilities, professional UI, UK localization, and complete Docker deployment.

**Key Highlights:**
- Complete HR functionality with realistic data
- 26 intentional vulnerabilities for testing
- Professional appearance without security warnings
- UK-based localization and currency
- Docker containerization for easy deployment
- Comprehensive documentation

**Target Audience:**
- Security professionals
- Penetration testers
- Security students
- Educational institutions
- Security researchers

---

## Support

For support, questions, or contributions:
- **Issues**: [GitHub Issues](https://github.com/akintunero/HRLeaks/issues)
- **Discussions**: [GitHub Discussions](https://github.com/akintunero/HRLeaks/discussions)
- **Email**: akintunero101@gmail.com

---

**⚠️ Remember**: This application is intentionally vulnerable. Use only in controlled, isolated environments for educational purposes. 
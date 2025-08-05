# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive open-source documentation
- Security policy and responsible disclosure guidelines
- Contributing guidelines and code of conduct
- MIT license for open-source distribution

## [1.0.0] - 2024-11-17

### Added
- **Core Voting System**
  - User registration and authentication
  - Real-time vote casting with confirmation
  - Live election results with animated charts
  - Candidate profiles and policy information

- **User Interface**
  - Modern responsive design with Tailwind CSS
  - Mobile-first approach
  - Loading states and animations
  - Toast notifications system
  - Real-time updates every 30 seconds

- **Educational Features**
  - Multiple intentional security vulnerabilities
  - SQL injection endpoints
  - Template injection demonstrations
  - XSS vulnerability examples
  - Path traversal vulnerabilities
  - Command injection scenarios
  - SSRF demonstrations
  - Hidden backdoor accounts

- **Analytics & Insights**
  - Voter turnout calculations
  - Geographic voting breakdown
  - Export functionality (CSV/JSON)
  - Real-time poll results
  - Election countdown timer

- **Security Vulnerabilities (Educational)**
  - Weak password hashing (MD5)
  - No CSRF protection
  - Broken cryptography
  - Insecure session management
  - Rate limiting bypasses
  - Hidden API endpoints
  - Sensitive data exposure
  - Time-based blind SQL injection

### Technical Features
- **Backend**: FastAPI with Python 3.11+
- **Frontend**: Jinja2 templates with Tailwind CSS
- **Database**: In-memory storage for demo purposes
- **Containerization**: Docker and Docker Compose
- **Security**: Intentionally vulnerable for education



### Key Pages
- Home page with election timer
- Dashboard for voting interface
- Candidates page with profiles
- Results page with live updates
- FAQ page with information
- Admin panel (vulnerable)
- Various vulnerable endpoints

### Educational Value
- Perfect for web security learning
- Ideal for penetration testing practice
- Great for CTF challenges
- Demonstrates real-world vulnerability patterns
- Provides hands-on security training

## [0.9.0] - 2024-11-04

### Added
- Initial project setup
- Basic FastAPI application structure
- Docker configuration
- Core voting functionality
- Basic UI templates

### Changed
- Multiple iterations of vulnerability implementations
- UI/UX improvements
- Security feature additions

### Fixed
- Runtime errors and template issues
- Docker build problems
- Jinja2 filter compatibility

---

## Version History

### Version 1.0.0
- **Release Date**: November 2024
- **Status**: Current stable release
- **Purpose**: Educational security platform
- **Target Audience**: Security students, researchers, and professionals

### Version 0.9.0
- **Release Date**: November 2024
- **Status**: Development version
- **Purpose**: Initial development and testing
- **Target Audience**: Internal development and testing

---

## Future Releases

### Planned Features
- Additional vulnerability types
- More complex CTF challenges
- Enhanced educational materials
- Improved UI/UX components
- Better documentation and guides

### Roadmap
- **v1.1.0**: Additional educational content
- **v1.2.0**: Enhanced UI/UX improvements
- **v2.0.0**: Major feature additions

---

## Contributing to Changelog

When adding entries to this changelog, please follow these guidelines:

1. **Use the existing format** - Follow the established structure
2. **Be descriptive** - Explain what changed and why
3. **Categorize changes** - Use Added, Changed, Deprecated, Removed, Fixed, Security
4. **Include version numbers** - Always specify the version
5. **Add dates** - Include release dates when known

### Change Categories

- **Added** - New features
- **Changed** - Changes in existing functionality
- **Deprecated** - Soon-to-be removed features
- **Removed** - Removed features
- **Fixed** - Bug fixes
- **Security** - Security-related changes

---

**Note**: This changelog is maintained for educational purposes. All vulnerabilities are intentional and part of the learning experience. 
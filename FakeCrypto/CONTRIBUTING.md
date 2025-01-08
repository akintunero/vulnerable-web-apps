# Contributing to FakeCryptoX

Thank you for your interest in contributing to FakeCryptoX! This project is designed for educational purposes and security research.

## 🎯 Project Goals

- Provide a realistic cryptocurrency exchange simulation
- Demonstrate common web application vulnerabilities
- Support security education and penetration testing practice
- Maintain educational value while improving realism

## 🚀 Getting Started

### Prerequisites
- Docker and Docker Compose
- Basic understanding of web security
- Python knowledge (for backend contributions)

### Development Setup

1. Fork and clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/fakecryptox.git
cd fakecryptox
```

2. Build and run the application:
```bash
docker-compose up --build
```

3. Access the application at http://localhost:8080

## 📋 Contribution Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Keep functions focused and concise
- Add type hints where appropriate

### Security Considerations
- **Never remove intentional vulnerabilities** - they're part of the educational purpose
- Ensure new vulnerabilities are properly contained within Docker
- Test that vulnerabilities don't escape the container
- Document any new vulnerabilities added

### Testing
- Test all new features thoroughly
- Ensure the application builds and runs correctly
- Verify that data persistence works as expected
- Test vulnerability containment

## 🐛 Bug Reports

When reporting bugs, please include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (Docker version, OS, etc.)

## 💡 Feature Requests

We welcome feature requests that:
- Enhance educational value
- Improve realism of the crypto exchange
- Add new vulnerability types
- Improve user experience

## 🔧 Development Workflow

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Follow the coding guidelines
   - Test thoroughly
   - Update documentation if needed

3. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add: brief description of changes"
   ```

4. **Push and create a Pull Request**:
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Message Format
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters
- Reference issues and pull requests after the first line

## 📁 Project Structure

```
FakeCryptoX/
├── app.py                 # Main FastAPI application
├── data_manager.py        # Data persistence layer
├── templates/            # Jinja2 HTML templates
├── data/                # Persistent data storage
├── logs/                # Application logs
├── docker-compose.yml   # Docker orchestration
├── Dockerfile          # Container configuration
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
├── CONTRIBUTING.md    # This file
├── LICENSE           # MIT License
└── PROJECT_SUMMARY.md # Technical overview
```

## 🛡️ Security Guidelines

### Adding Vulnerabilities
- Ensure vulnerabilities are educational and realistic
- Contain all vulnerabilities within the Docker environment
- Test that vulnerabilities can be exploited safely
- Document any new vulnerabilities added

### Vulnerability Types We're Interested In
- Authentication and authorization flaws
- Input validation and injection attacks
- Cryptographic weaknesses
- Business logic flaws
- Data exposure vulnerabilities
- Web3/blockchain specific vulnerabilities

## 🧪 Testing

### Manual Testing
- Test all user flows
- Verify vulnerability exploitation
- Check data persistence
- Test container isolation

### Automated Testing
- Add unit tests for new features
- Test vulnerability containment
- Verify Docker build process

## 📚 Documentation

### Code Documentation
- Add docstrings for new functions
- Update README.md for new features
- Document new vulnerabilities
- Update API documentation if needed

### Educational Documentation
- Explain how to exploit new vulnerabilities
- Provide learning objectives
- Include real-world examples

## 🤝 Community Guidelines

- Be respectful and inclusive
- Help others learn and grow
- Share knowledge and experiences
- Report security issues responsibly

## 📞 Getting Help

- Open an issue for bugs or questions
- Join discussions in pull requests
- Check existing documentation first

## 🎉 Recognition

Contributors will be recognized in:
- Project README.md
- Release notes
- Contributor hall of fame

Thank you for contributing to FakeCryptoX! Your efforts help make security education more accessible and effective. 
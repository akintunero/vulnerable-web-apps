# Contributing to HRLeaks

Thank you for your interest in contributing to HRLeaks! This document provides guidelines and information for contributors.

## 🤝 **How to Contribute**

We welcome contributions from the community! Here are the main ways you can contribute:

### 🐛 **Reporting Bugs**
- Use the [GitHub Issues](https://github.com/akintunero/HRLeaks/issues) page
- Provide detailed information about the bug
- Include steps to reproduce the issue
- Mention your environment (OS, Python version, etc.)

### 💡 **Suggesting Features**
- Open a [GitHub Discussion](https://github.com/akintunero/HRLeaks/discussions)
- Describe the feature and its benefits
- Consider the educational value for security testing

### 🔧 **Code Contributions**
- Fork the repository
- Create a feature branch
- Make your changes
- Add tests if applicable
- Submit a pull request

## 🛠️ **Development Setup**

### Prerequisites
- Python 3.9+
- Docker and Docker Compose
- Git

### Local Development

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/HRLeaks.git
   cd HRLeaks
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

### Docker Development

```bash
docker compose up --build
```

## 📝 **Code Style Guidelines**

### Python
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings for functions and classes
- Keep functions small and focused

### HTML/Templates
- Use consistent indentation
- Follow Jinja2 best practices
- Maintain semantic HTML structure

### CSS
- Follow Tailwind CSS conventions
- Use utility classes when possible
- Keep custom CSS minimal

## 🧪 **Testing**

### Running Tests
```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=main
```

### Adding Tests
- Create test files in a `tests/` directory
- Use descriptive test names
- Test both positive and negative cases
- Mock external dependencies

## 🔒 **Security Considerations**

### Adding Vulnerabilities
- Document the vulnerability clearly
- Include educational comments
- Ensure it's safe for testing environments
- Add appropriate warnings

### Vulnerability Documentation
- Describe the vulnerability type
- Explain the attack vector
- Provide remediation guidance
- Include CVE references when applicable

## 📋 **Pull Request Process**

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clear commit messages
   - Test your changes thoroughly
   - Update documentation if needed

3. **Submit a pull request**
   - Provide a clear description
   - Reference any related issues
   - Include screenshots for UI changes

4. **Code review**
   - Address feedback promptly
   - Make requested changes
   - Ensure all tests pass

## 📚 **Documentation**

### Updating Documentation
- Keep README.md current
- Update API documentation
- Add inline code comments
- Create tutorials for new features

### Documentation Standards
- Use clear, concise language
- Include code examples
- Provide step-by-step instructions
- Add screenshots when helpful

## 🏷️ **Issue Labels**

We use the following labels to categorize issues:

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Improvements to documentation
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention is needed
- `security` - Security-related issues
- `vulnerability` - New vulnerability to add

## 🎯 **Project Goals**

When contributing, keep in mind our project goals:

1. **Educational Value** - Help people learn about security
2. **Realistic Scenarios** - Provide authentic testing environments
3. **Safety** - Ensure vulnerabilities are contained
4. **Accessibility** - Make security testing accessible to all

## 📞 **Getting Help**

- **Issues**: [GitHub Issues](https://github.com/akintunero/HRLeaks/issues)
- **Discussions**: [GitHub Discussions](https://github.com/akintunero/HRLeaks/discussions)
- **Email**: akintunero101@gmail.com

## 🙏 **Acknowledgments**

Thank you to all contributors who help make HRLeaks a valuable educational tool for the security community!

---

**Remember**: This project is for educational purposes. Always use in controlled, isolated environments. 
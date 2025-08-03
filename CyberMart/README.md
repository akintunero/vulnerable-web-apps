# 🛒 CyberMart - Vulnerable E-commerce Platform

A deliberately vulnerable e-commerce platform designed for security research and penetration testing practice. This application demonstrates various web application vulnerabilities in a realistic e-commerce environment.

## ⚠️ **SECURITY WARNING**

**This application contains intentional vulnerabilities and should ONLY be run in isolated Docker containers. Never deploy to production or expose to public networks.**

## 🎯 Overview

CyberMart is a vulnerable e-commerce platform that simulates a real-world online store with multiple security flaws. It's designed to help security researchers, penetration testers, and students learn about web application security vulnerabilities in an e-commerce context.

### Key Features:
- 🛍️ Complete e-commerce functionality
- 👥 User account management
- 📦 Product catalog with categories
- 🛒 Shopping cart and wishlist
- 💳 Checkout and payment processing
- 📋 Order management and tracking
- 💰 Discount code system
- 📄 PDF invoice generation
- 📧 Email notifications
- ⭐ Product reviews and ratings
- 🔧 Admin panel for management

## 🚀 Quick Start

### Prerequisites
- Docker
- Docker Compose

### Installation & Setup

```bash
# Clone the repository
git clone git@github.com:akintunero/vulnerable-web-apps.git
cd vulnerable-web-apps/CyberMart

# Start the application
./start.sh

# Access the application
# URL: http://localhost:5002
```

## 🏗️ Architecture

### Components
- **Frontend**: HTML/CSS/JavaScript with Bootstrap
- **Backend**: Python Flask application
- **Database**: SQLite (primary), MongoDB (NoSQL injection testing)
- **Cache**: Redis (rate limiting)
- **Container**: Docker with Python 3.9

### Directory Structure
```
CyberMart/
├── app.py                 # Main Flask application
├── templates/             # HTML templates
├── static/               # CSS, JS, images
├── uploads/              # File uploads
├── docker-compose.yml    # Docker configuration
├── Dockerfile           # Container definition
├── requirements.txt     # Python dependencies
└── start.sh            # Startup script
```

## 🎓 Learning Objectives

### Vulnerability Categories
1. **NoSQL Injection**
   - MongoDB query injection
   - Parameter manipulation
   - Data extraction techniques

2. **Command Injection**
   - Unsafe user input to shell
   - System command execution
   - Privilege escalation

3. **Unsafe Deserialization**
   - Pickle deserialization
   - JSON deserialization
   - Code execution via deserialization

4. **Parameter Tampering**
   - Price manipulation
   - Quantity manipulation
   - Discount code abuse

5. **IDOR (Insecure Direct Object Reference)**
   - Order access without authorization
   - Invoice access bypass
   - User data exposure

6. **XSS (Cross-Site Scripting)**
   - Cart field injection
   - Product review injection
   - Stored XSS in user content

7. **Unvalidated Redirects**
   - Checkout flow manipulation
   - Open redirect vulnerabilities
   - Phishing attack simulation

8. **Local File Inclusion**
   - Path traversal attacks
   - File download vulnerabilities
   - System file access

9. **CSRF (Cross-Site Request Forgery)**
   - Checkout form manipulation
   - Order form attacks
   - Admin action bypass

10. **Weak Password Policies**
    - Short password acceptance
    - Common password allowance
    - Brute force vulnerability

11. **Open Redirects**
    - Email redirect manipulation
    - URL parameter injection
    - Phishing simulation

12. **Insufficient Rate Limiting**
    - API brute force vulnerability
    - Login attempt bypass
    - Resource exhaustion

## 🔍 Vulnerability Guide

### 1. NoSQL Injection
- **Location**: `/api/products/search`
- **Technique**: MongoDB query injection
- **Impact**: Data extraction and manipulation

### 2. Command Injection
- **Location**: `/api/command`
- **Technique**: Shell command injection
- **Impact**: System command execution

### 3. Parameter Tampering
- **Location**: `/api/cart/add`, `/api/checkout`
- **Technique**: Price/quantity manipulation
- **Impact**: Financial fraud

### 4. IDOR
- **Location**: `/api/invoice/{id}`, `/order/{id}`
- **Technique**: Direct object access
- **Impact**: Unauthorized data access

### 5. XSS
- **Location**: `/api/reviews/add`, cart fields
- **Technique**: Stored XSS in user content
- **Impact**: Session hijacking, data theft

### 6. CSRF
- **Location**: `/api/checkout`, order forms
- **Technique**: Cross-site request forgery
- **Impact**: Unauthorized actions

## 🛠️ Testing with Burp Suite

### Setup
1. Configure Burp Suite proxy to `127.0.0.1:8080`
2. Set browser proxy settings
3. Install Burp CA certificate in browser

### Test Cases

#### NoSQL Injection
```bash
# Test MongoDB injection
curl "http://localhost:5002/api/products/search?q=test"
curl "http://localhost:5002/api/products/search?q={\"\$ne\":null}"
```

#### Command Injection
```bash
# Test command injection
curl -X POST "http://localhost:5002/api/command" \
  -H "Content-Type: application/json" \
  -d '{"command":"ls -la"}'
```

#### Parameter Tampering
```bash
# Test price manipulation
curl -X POST "http://localhost:5002/api/cart/add" \
  -H "Content-Type: application/json" \
  -d '{"product_id":1,"quantity":1,"price":-10.00}'
```

#### IDOR Testing
```bash
# Test invoice access
curl "http://localhost:5002/api/invoice/1"
curl "http://localhost:5002/api/invoice/999"
```

## 📊 Features

### E-commerce Functionality
- **Product Catalog**: Categories, search, filtering
- **Shopping Cart**: Add/remove items, quantity management
- **Wishlist**: Save products for later
- **User Accounts**: Registration, login, profile management
- **Checkout Process**: Address, payment, discount codes
- **Order Management**: History, tracking, status updates
- **Reviews & Ratings**: Product feedback system
- **Admin Panel**: Product, order, user management
- **PDF Invoices**: Downloadable order invoices
- **Email Notifications**: Order confirmations, status updates

### Security Testing Features
- **Stealthy Vulnerabilities**: No obvious vulnerability hints
- **Realistic Interface**: Professional e-commerce appearance
- **Multiple Attack Vectors**: Various vulnerability types
- **Educational Value**: Clear learning objectives
- **Burp Suite Compatible**: Full proxy testing support

## 🔧 Configuration

### Environment Variables
```bash
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your-secret-key
```

### Database Setup
```bash
# Initialize database
python3 -c "from app import init_db; init_db()"
```

## 📝 Usage

### Starting the Application
```bash
./start.sh
```

### Accessing the Application
- **Main Site**: http://localhost:5002
- **Admin Panel**: http://localhost:5002/admin
- **API Endpoints**: http://localhost:5002/api/*

### Default Accounts
- **Admin**: admin@cybermart.com / admin123
- **User**: user@cybermart.com / password123

## 🛡️ Security Notes

- All vulnerabilities are intentionally implemented
- No real payment processing
- Mock data for testing
- Isolated Docker environment
- Educational purposes only

## 📚 Educational Resources

- OWASP Top 10
- Web Application Security Testing
- E-commerce Security Best Practices
- Vulnerability Assessment Methodologies

## 🤝 Contributing

This project is designed for educational purposes. Contributions should focus on:
- Adding new vulnerability types
- Improving educational content
- Enhancing testing scenarios
- Documentation improvements

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Remember**: This application is for educational purposes only. Never use these techniques on real systems without proper authorization. 
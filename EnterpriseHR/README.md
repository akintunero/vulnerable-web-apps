# 👥 EnterpriseHR - Human Resources Management System

A comprehensive human resources management system designed for security research and testing practice. This application demonstrates various web application concepts in a controlled, educational environment.

## ⚠️ **SECURITY WARNING**

**This application is designed for educational purposes and should ONLY be run in isolated Docker containers. Never deploy to production or expose to public networks.**

## 🎯 Overview

EnterpriseHR is an HR management system that simulates a real-world human resources platform. It's designed to help security researchers, penetration testers, and students learn about web application security concepts.

### Key Features:
- 👤 Employee management system
- 📊 Payroll processing
- 📝 Resume management
- 🔐 Authentication systems
- 📈 Data management

## 🚀 Quick Start

### Prerequisites
- Docker
- Docker Compose

### Installation & Setup

```bash
# Clone the repository
git clone git@github.com:akintunero/vulnerable-web-apps.git
cd vulnerable-web-apps/OpenSource/HRLeaks

# Start the application
docker-compose up -d

# Access the application
# URL: http://localhost:8000
```

## 🏗️ Architecture

### Components
- **Frontend**: HTML/CSS/JavaScript with Bootstrap
- **Backend**: Python Flask application
- **Database**: SQLite with JSON data files
- **Container**: Docker with Python 3.9

### Directory Structure
```
HRLeaks/
├── main.py              # Main Flask application
├── templates/           # HTML templates
├── static/             # CSS, JS, images
├── uploads/            # File uploads
├── temp/               # Temporary files
├── docker-compose.yml  # Docker configuration
├── Dockerfile          # Container definition
└── requirements.txt    # Python dependencies
```

## 🎓 Learning Objectives

This application is designed to help users understand:

1. **Web Application Security Concepts**
   - Input validation and sanitization
   - Authentication and authorization
   - Session management
   - Data protection

2. **Security Testing Methodologies**
   - Manual testing approaches
   - Automated testing tools
   - Security assessment frameworks

3. **Defensive Programming**
   - Secure coding practices
   - Security best practices
   - Risk mitigation strategies

## 🔍 Application Features

### 1. HR Management
- Employee directory and profiles
- Payroll processing and management
- Leave request handling
- Performance review system

### 2. User Management
- Employee registration and authentication
- Role-based access control
- Session management
- Profile administration

### 3. Administrative Functions
- Employee administration
- Payroll management
- System monitoring
- Data management

### 3. File Upload Vulnerabilities
- **Location**: Resume upload functionality
- **Technique**: Malicious file upload
- **Impact**: Server compromise and data theft

### 4. Business Logic Flaws
- **Location**: Employee management system
- **Technique**: Parameter manipulation
- **Impact**: Unauthorized data access and modification

### 5. Information Disclosure
- **Location**: Error pages and debug endpoints
- **Technique**: Error message analysis
- **Impact**: System information leakage

## 🛠️ Development

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run locally (NOT recommended for production)
python main.py
```

### Docker Development
```bash
# Build and run
docker-compose up --build

# View logs
docker-compose logs -f

# Stop application
docker-compose down
```

## 📊 Features

### Employee Management
- Employee profiles
- Contact information
- Employment history
- Performance reviews

### Payroll System
- Salary information
- Payment processing
- Tax calculations
- Benefits management

### Resume Management
- Resume uploads
- Document storage
- File management
- Access control

### HR Functions
- Employee onboarding
- Performance tracking
- Leave management
- Policy administration

## 🔧 Configuration

### Environment Variables
```bash
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///hrleaks.db
UPLOAD_FOLDER=./uploads
PORT=8000
```

## 📡 API Endpoints

### Authentication
- `POST /login` - Employee authentication
- `POST /register` - Employee registration
- `GET /logout` - User logout

### Employee Management
- `GET /api/employees` - Get all employees
- `GET /api/employees/<id>` - Get employee details
- `POST /api/employees` - Add new employee
- `PUT /api/employees/<id>` - Update employee

### Payroll
- `GET /api/payroll` - Get payroll data
- `GET /api/payroll/<employee_id>` - Get employee payroll
- `POST /api/payroll/export` - Export payroll data

### Leave Management
- `GET /api/leave` - Get leave requests
- `POST /api/leave` - Submit leave request
- `PUT /api/leave/<id>` - Update leave request
- `GET /api/leave/<id>` - Get leave details

### File Management
- `POST /api/upload` - Upload documents
- `GET /api/files` - Get uploaded files
- `GET /api/files/<id>` - Download file

### Admin Functions
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/employees` - Employee management
- `GET /admin/payroll` - Payroll management
- `GET /admin/reports` - Report generation

### Docker Configuration
```yaml
version: '3.8'
services:
  hrleaks:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./uploads:/app/uploads
      - ./temp:/app/temp
    environment:
      - FLASK_ENV=development
```

## 🎯 Use Cases

### Security Research
- Study HR system vulnerabilities
- Practice data protection testing
- Learn about business logic flaws

### Educational Purposes
- Security training programs
- University cybersecurity courses
- Capture-the-flag (CTF) challenges

### Testing Environments
- Security tool testing
- Vulnerability scanner validation
- Security assessment practice

## 📈 HR Features

### Employee Management
- Employee profiles
- Contact information
- Employment history
- Performance tracking

### Payroll Processing
- Salary management
- Payment processing
- Tax calculations
- Benefits administration

### Document Management
- Resume storage
- Policy documents
- Performance reviews
- Employment contracts

### Administrative Functions
- User management
- System configuration
- Audit logging
- Security settings

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add new vulnerabilities or improvements
4. Ensure Docker compatibility
5. Update documentation
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 📞 Contact

**Author:** Olúmáyòwá Akinkuehinmi  
**Email:** akintunero101@gmail.com  
**GitHub:** [@akintunero](https://github.com/akintunero)

---

**⚠️ Remember: This application contains intentional vulnerabilities. Use only in controlled, educational environments!** 
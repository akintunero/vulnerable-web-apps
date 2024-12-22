# 🚨 VULNERABLE AIRLINE WEB APPLICATION 🚨

## ⚠️ DISCLAIMER ⚠️

**THIS APPLICATION IS INTENTIONALLY VULNERABLE AND SHOULD ONLY BE USED FOR:**

- Educational purposes
- Ethical hacking training
- CTF (Capture The Flag) challenges
- Security research in controlled environments
- Penetration testing practice

**DO NOT DEPLOY THIS APPLICATION IN PRODUCTION OR ON PUBLIC NETWORKS.**

**THE DEVELOPERS ARE NOT RESPONSIBLE FOR ANY MISUSE OF THIS APPLICATION.**

## ⚠️ Security Warning

> **This application is intentionally vulnerable. For your safety, always run it inside Docker.**
>
> - **Never run on your host system or a public network.**
> - **Use only in isolated, controlled environments.**
> - **The developers are not responsible for misuse or data loss.**

---

## 🛩️ SkyHack Airlines - Vulnerable Web Application

A deliberately vulnerable airline booking system built with Flask to demonstrate common web application security vulnerabilities.

## 🎯 Features (With Intentional Vulnerabilities)

### ✈️ Core Systems
- **Flight Booking System** - SQL Injection, XSS vulnerabilities
- **Check-In System** - IDOR vulnerabilities
- **Admin Panel** - Default credentials, RCE via file upload
- **Frequent Flyer Portal** - IDOR, CSRF vulnerabilities
- **Mock Payment System** - Insecure payment logic, hardcoded bypasses
- **Mobile API** - JWT token leakage, weak authentication

### 🔓 Documented Vulnerabilities

#### 1. SQL Injection (CVE-2024-1234)
- **Location**: Flight search functionality
- **Impact**: Database compromise, data exfiltration
- **Payload**: `' UNION SELECT * FROM users --`

#### 2. Cross-Site Scripting (CVE-2024-5678)
- **Location**: Passenger name input
- **Impact**: Session hijacking, credential theft
- **Payload**: `<script>alert('XSS')</script>`

#### 3. Insecure Direct Object Reference (CVE-2024-9012)
- **Location**: Check-in system, frequent flyer portal
- **Impact**: Unauthorized access to other users' data
- **Exploit**: Change booking ID parameter

#### 4. Remote Code Execution (CVE-2024-3456)
- **Location**: Admin file upload
- **Impact**: Server compromise
- **Payload**: Upload malicious Python file

#### 5. Cross-Site Request Forgery (CVE-2024-7890)
- **Location**: Points transfer functionality
- **Impact**: Unauthorized actions on behalf of user
- **Exploit**: Malicious form submission

#### 6. JWT Token Weakness (CVE-2024-2345)
- **Location**: Mobile API authentication
- **Impact**: Token forgery, session hijacking
- **Exploit**: Weak secret key

#### 7. Hardcoded Credentials (CVE-2024-6789)
- **Location**: Admin panel
- **Impact**: Unauthorized admin access
- **Credentials**: admin@airline.co:admin123

#### 8. Insecure File Upload (CVE-2024-0123)
- **Location**: Admin manifest upload
- **Impact**: Malicious file execution
- **Exploit**: Upload executable files

#### 9. Weak Password Policy (CVE-2024-4567)
- **Location**: User registration
- **Impact**: Account compromise
- **Exploit**: Use weak passwords

#### 10. Information Disclosure (CVE-2024-8901)
- **Location**: Error pages
- **Impact**: System information leakage
- **Exploit**: Trigger errors to see stack traces

#### 11. Session Fixation (CVE-2024-2345)
- **Location**: Login system
- **Impact**: Session hijacking
- **Exploit**: Predictable session IDs

#### 12. Directory Traversal (CVE-2024-5678)
- **Location**: File access endpoints
- **Impact**: Unauthorized file access
- **Exploit**: `../../../etc/passwd`

#### 13. XML External Entity (CVE-2024-9012)
- **Location**: Flight data parsing
- **Impact**: Server-side request forgery
- **Exploit**: XXE payload in XML input

#### 14. Server-Side Template Injection (CVE-2024-3456)
- **Location**: Email templates
- **Impact**: Remote code execution
- **Exploit**: Template injection payloads

#### 15. Insecure Deserialization (CVE-2024-7890)
- **Location**: Session management
- **Impact**: Remote code execution
- **Exploit**: Malicious pickle objects

## New Features & Vulnerabilities

- Decoy endpoints: `/admin/secure`, `/api/siem`, `/api/fake-status`, `/api/audit-log`
- Decoy admin account: `decoy_admin@airline.co` triggers fake SIEM alert
- Loyalty tier endpoints: `/loyalty-status`, `/upgrade-tier`, `/api/loyalty/tiers` (with logic flaws)
- Vulnerable file download: `/download` (path traversal)
- Race condition: `/checkin` (double check-in possible)
- Fake rate limiting headers (not enforced)
- Boarding pass endpoint: `/boarding-pass/<booking_id>` (IDOR)
- Flight status API: `/api/flight-status` (data exposure)

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd vuln-airline

# Build and run with Docker Compose (all setup is automatic)
docker compose up --build

# Access the application
open http://localhost:8080
```

> **Note:** All dependencies are installed, the database is initialized, and the app runs automatically inside the container. No manual setup is required!

### Manual Setup (For Developers)

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py

# Run the application
python app.py
```

## 🎮 Usage

### Default Credentials
- **Admin**: admin@airline.co / admin123
- **Test User**: user@secf0rtress.com / password123

### Sample Vulnerable Endpoints
- `/search` - SQL Injection
- `/checkin` - IDOR
- `/admin` - Default credentials
- `/api/checkin` - JWT issues
- `/frequent-flyer` - CSRF

## 📁 Project Structure

```
vuln-airline/
├── app.py                 # Main Flask application
├── init_db.py            # Database initialization
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose setup
├── static/              # Static files (CSS, JS, images)
├── templates/           # Jinja2 templates
├── logs/               # Fake application logs
├── uploads/            # File upload directory
└── database/           # SQLite database files
```

## 🛡️ Security Notes

This application contains multiple intentional vulnerabilities for educational purposes:

1. **Never use in production**
2. **Isolate in controlled environment**
3. **Use only for authorized testing**
4. **Follow responsible disclosure if finding new issues**

## 📚 Learning Resources

- OWASP Top 10
- Web Application Security Testing
- Ethical Hacking Fundamentals
- CTF Challenges

## 🤝 Contributing

This is an educational project. Contributions should focus on:
- Adding new vulnerability types
- Improving documentation
- Enhancing educational value
- Fixing non-security bugs

## 📄 License

This project is for educational use only. Use at your own risk.

---

**Remember: This application is intentionally vulnerable. Use responsibly!** 
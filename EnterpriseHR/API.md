# API Documentation

## 🔌 **HRLeaks API Reference**

This document provides comprehensive API documentation for the HRLeaks application. All endpoints are designed for educational purposes and contain intentional vulnerabilities.

## 📋 **Base Information**

- **Base URL**: `http://localhost:8000`
- **Content Type**: `application/json`
- **Authentication**: Session-based (cookies)
- **Status**: Educational/Testing Environment

## 🔐 **Authentication Endpoints**

### POST `/login`
Authenticate a user and create a session.

**Request Body:**
```json
{
  "email": "admin@hrleaks.co.uk",
  "password": "hr123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "user": {
    "id": 1,
    "email": "admin@hrleaks.co.uk",
    "role": "admin"
  }
}
```

**Vulnerabilities:**
- SQL Injection in email field
- Weak password validation
- Session fixation

### POST `/logout`
Logout and destroy session.

**Response:**
```json
{
  "success": true,
  "message": "Logout successful"
}
```

## 👥 **Employee Management**

### GET `/employees`
Get all employees (requires authentication).

**Query Parameters:**
- `search` (optional): Search by name or email
- `department` (optional): Filter by department
- `sort` (optional): Sort field (name, email, department)

**Response:**
```json
{
  "employees": [
    {
      "id": 1,
      "name": "John Smith",
      "email": "john.smith@hrleaks.co.uk",
      "department": "IT",
      "position": "Software Engineer",
      "salary": 45000,
      "hire_date": "2023-01-15"
    }
  ]
}
```

**Vulnerabilities:**
- SQL Injection in search parameter
- Information disclosure
- XSS in employee names

### GET `/employees/{id}`
Get employee details by ID.

**Path Parameters:**
- `id`: Employee ID (integer)

**Response:**
```json
{
  "id": 1,
  "name": "John Smith",
  "email": "john.smith@hrleaks.co.uk",
  "phone": "+44 20 7123 4567",
  "address": "123 Baker Street, London, UK",
  "department": "IT",
  "position": "Software Engineer",
  "salary": 45000,
  "hire_date": "2023-01-15",
  "manager": "Jane Doe"
}
```

**Vulnerabilities:**
- IDOR (Insecure Direct Object Reference)
- Path traversal in ID parameter
- Information disclosure

### POST `/employees`
Create a new employee.

**Request Body:**
```json
{
  "name": "New Employee",
  "email": "new.employee@hrleaks.co.uk",
  "phone": "+44 20 7123 4568",
  "address": "456 Oxford Street, London, UK",
  "department": "HR",
  "position": "HR Assistant",
  "salary": 35000
}
```

**Response:**
```json
{
  "success": true,
  "message": "Employee created successfully",
  "employee_id": 11
}
```

**Vulnerabilities:**
- XSS in name and address fields
- SQL Injection in all fields
- Insecure file upload

### PUT `/employees/{id}`
Update employee information.

**Path Parameters:**
- `id`: Employee ID (integer)

**Request Body:**
```json
{
  "name": "Updated Name",
  "email": "updated@hrleaks.co.uk",
  "salary": 50000
}
```

**Vulnerabilities:**
- IDOR
- XSS
- SQL Injection

### DELETE `/employees/{id}`
Delete an employee.

**Path Parameters:**
- `id`: Employee ID (integer)

**Response:**
```json
{
  "success": true,
  "message": "Employee deleted successfully"
}
```

**Vulnerabilities:**
- IDOR
- CSRF (Cross-Site Request Forgery)

## 💰 **Payroll Management**

### GET `/payroll`
Get all payroll records.

**Query Parameters:**
- `month` (optional): Filter by month (YYYY-MM)
- `employee_id` (optional): Filter by employee ID

**Response:**
```json
{
  "payroll": [
    {
      "id": 1,
      "employee_id": 1,
      "employee_name": "John Smith",
      "month": "2024-01",
      "base_salary": 45000,
      "bonus": 5000,
      "deductions": 2000,
      "net_pay": 48000,
      "status": "paid"
    }
  ]
}
```

**Vulnerabilities:**
- SQL Injection
- Information disclosure
- XSS

### GET `/payroll/{id}`
Get payroll details by ID.

**Path Parameters:**
- `id`: Payroll ID (integer)

**Response:**
```json
{
  "id": 1,
  "employee_id": 1,
  "employee_name": "John Smith",
  "month": "2024-01",
  "base_salary": 45000,
  "bonus": 5000,
  "deductions": 2000,
  "net_pay": 48000,
  "status": "paid",
  "payment_date": "2024-01-31",
  "bank_details": "****1234"
}
```

**Vulnerabilities:**
- IDOR
- Information disclosure
- Path traversal

### POST `/payroll`
Create new payroll record.

**Request Body:**
```json
{
  "employee_id": 1,
  "month": "2024-02",
  "base_salary": 45000,
  "bonus": 5000,
  "deductions": 2000
}
```

**Vulnerabilities:**
- SQL Injection
- IDOR
- Insecure deserialization

### POST `/payroll/process`
Process payroll for all employees.

**Request Body:**
```json
{
  "month": "2024-02",
  "include_bonus": true
}
```

**Vulnerabilities:**
- Command injection
- XXE (XML External Entity)
- Insecure eval usage

## 📄 **Resume Management**

### GET `/resumes`
Get all resumes.

**Query Parameters:**
- `employee_id` (optional): Filter by employee ID
- `format` (optional): Filter by format (pdf, html, docx)

**Response:**
```json
{
  "resumes": [
    {
      "id": 1,
      "employee_id": 1,
      "employee_name": "John Smith",
      "filename": "john_smith_cv.pdf",
      "format": "pdf",
      "upload_date": "2024-01-15",
      "size": 245760
    }
  ]
}
```

**Vulnerabilities:**
- SQL Injection
- Path traversal
- Information disclosure

### GET `/resumes/{id}`
Download resume file.

**Path Parameters:**
- `id`: Resume ID (integer)

**Response:** File download

**Vulnerabilities:**
- IDOR
- Path traversal
- Insecure file serving

### POST `/resumes`
Upload a new resume.

**Request:** Multipart form data

**Form Fields:**
- `employee_id`: Employee ID (integer)
- `file`: Resume file (pdf, html, docx, txt)

**Response:**
```json
{
  "success": true,
  "message": "Resume uploaded successfully",
  "resume_id": 11
}
```

**Vulnerabilities:**
- Insecure file upload
- XSS in file content
- Command injection in filename
- Path traversal

### DELETE `/resumes/{id}`
Delete a resume.

**Path Parameters:**
- `id`: Resume ID (integer)

**Vulnerabilities:**
- IDOR
- Path traversal

## 📊 **Dashboard Endpoints**

### GET `/dashboard`
Get dashboard statistics.

**Response:**
```json
{
  "total_employees": 10,
  "total_payroll": 450000,
  "departments": {
    "IT": 4,
    "HR": 3,
    "Finance": 2,
    "Marketing": 1
  },
  "recent_activities": [
    {
      "id": 1,
      "action": "employee_created",
      "user": "admin@hrleaks.co.uk",
      "timestamp": "2024-01-15T10:30:00Z",
      "details": "Created employee: John Smith"
    }
  ]
}
```

**Vulnerabilities:**
- SQL Injection
- XSS in activity details
- Information disclosure

### GET `/dashboard/mock`
Get mock dashboard data (no authentication required).

**Response:** Same as `/dashboard` but with mock data

**Vulnerabilities:**
- Information disclosure
- XSS

## 📝 **Audit Logs**

### GET `/audit-logs`
Get audit logs.

**Query Parameters:**
- `user` (optional): Filter by user
- `action` (optional): Filter by action
- `start_date` (optional): Filter by start date
- `end_date` (optional): Filter by end date

**Response:**
```json
{
  "logs": [
    {
      "id": 1,
      "timestamp": "2024-01-15T10:30:00Z",
      "user": "admin@hrleaks.co.uk",
      "action": "login",
      "ip_address": "192.168.1.100",
      "user_agent": "Mozilla/5.0...",
      "details": "Successful login"
    }
  ]
}
```

**Vulnerabilities:**
- SQL Injection
- Information disclosure
- Log injection

### POST `/audit-logs/clear`
Clear all audit logs.

**Response:**
```json
{
  "success": true,
  "message": "Audit logs cleared successfully"
}
```

**Vulnerabilities:**
- CSRF
- Privilege escalation

## 🔍 **Search Endpoints**

### GET `/search`
Global search across all data.

**Query Parameters:**
- `q`: Search query (string)
- `type`: Search type (employees, payroll, resumes)

**Response:**
```json
{
  "results": [
    {
      "type": "employee",
      "id": 1,
      "name": "John Smith",
      "email": "john.smith@hrleaks.co.uk",
      "score": 0.95
    }
  ]
}
```

**Vulnerabilities:**
- SQL Injection
- XSS
- Information disclosure
- Path traversal

## 🛠️ **Utility Endpoints**

### GET `/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0"
}
```

### GET `/debug`
Debug information (development only).

**Response:**
```json
{
  "environment": "development",
  "database": "sqlite",
  "session_data": {...},
  "config": {...}
}
```

**Vulnerabilities:**
- Information disclosure
- Debug information exposure

## ⚠️ **Error Responses**

### 400 Bad Request
```json
{
  "error": "Invalid request",
  "message": "Missing required field: email",
  "code": "VALIDATION_ERROR"
}
```

### 401 Unauthorized
```json
{
  "error": "Unauthorized",
  "message": "Authentication required",
  "code": "AUTH_REQUIRED"
}
```

### 403 Forbidden
```json
{
  "error": "Forbidden",
  "message": "Insufficient permissions",
  "code": "PERMISSION_DENIED"
}
```

### 404 Not Found
```json
{
  "error": "Not Found",
  "message": "Resource not found",
  "code": "RESOURCE_NOT_FOUND"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred",
  "code": "INTERNAL_ERROR"
}
```

## 🔒 **Security Notes**

### Intentional Vulnerabilities
This API contains multiple intentional vulnerabilities for educational purposes:

1. **Authentication Bypass**
   - Weak session management
   - Predictable session tokens
   - No CSRF protection

2. **Injection Vulnerabilities**
   - SQL Injection in search parameters
   - XSS in user input fields
   - Command injection in file operations

3. **Access Control Issues**
   - IDOR vulnerabilities
   - Missing authorization checks
   - Privilege escalation opportunities

4. **Information Disclosure**
   - Debug endpoints
   - Error message leakage
   - Sensitive data exposure

### Testing Guidelines
- Use only in controlled environments
- Follow responsible disclosure practices
- Document your testing methodology
- Respect the educational purpose

## 📞 **Support**

For API-related questions or issues:
- **Email**: akintunero101@gmail.com
- **GitHub Issues**: [Create an issue](https://github.com/akintunero/HRLeaks/issues)

---

**⚠️ Remember**: This API is intentionally vulnerable. Use only in controlled, isolated environments for educational purposes. 
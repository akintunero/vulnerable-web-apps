from fastapi import FastAPI, Request, Response, HTTPException, Depends, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import uvicorn
import json
import os
import base64
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import re
import sqlite3
import pickle
import yaml
import xml.etree.ElementTree as ET
from pathlib import Path
import subprocess
import tempfile
import shutil
from urllib.parse import unquote, quote
import logging
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="EnterpriseHR - HR Management System", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Security
security = HTTPBasic()

# In-memory data storage with weak password storage
users_db = {
    "admin@enterprise.com.uk": {
        "password": "admin123",  # Password Storage Issues - plaintext passwords
        "role": "admin",
        "id": 1,
        "name": "Admin User",
        "email": "admin@enterprise.com.uk"
    },
    "hr@enterprise.com.uk": {
        "password": "hr123",  # Password Storage Issues - plaintext passwords
        "role": "hr_officer",
        "id": 2,
        "name": "HR Officer",
        "email": "hr@enterprise.com.uk"
    }
}

# Mock employee data
employees = [
    {"id": 1, "name": "John Smith", "email": "john.smith@mooncrate.ng", "department": "Engineering", "salary": 65000, "ssn": "AB123456C", "phone": "+44-20-7946-0958", "address": "123 High Street, London, SW1A 1AA", "hire_date": "2020-03-15", "position": "Senior Software Engineer"},
    {"id": 2, "name": "Sarah Johnson", "email": "sarah.johnson@coldshade.be", "department": "Marketing", "salary": 55000, "ssn": "CD234567D", "phone": "+44-20-7946-0959", "address": "456 Oxford Street, Manchester, M1 1AA", "hire_date": "2021-06-20", "position": "Marketing Manager"},
    {"id": 3, "name": "Mike Davis", "email": "mike.davis@enterprise.comm", "department": "Sales", "salary": 60000, "ssn": "EF345678E", "phone": "+44-20-7946-0960", "address": "789 Queen Street, Birmingham, B1 1AA", "hire_date": "2019-11-10", "position": "Sales Director"},
    {"id": 4, "name": "Lisa Brown", "email": "lisa.brown@enterprise.comm", "department": "HR", "salary": 52000, "ssn": "GH456789F", "phone": "+44-20-7946-0961", "address": "321 King Street, Leeds, LS1 1AA", "hire_date": "2022-01-05", "position": "HR Specialist"},
    {"id": 5, "name": "David Wilson", "email": "david.wilson@enterprise.comm", "department": "Engineering", "salary": 70000, "ssn": "IJ567890G", "phone": "+44-20-7946-0962", "address": "654 Victoria Road, Bristol, BS1 1AA", "hire_date": "2020-08-12", "position": "Lead Developer"},
    {"id": 6, "name": "Emily Chen", "email": "emily.chen@lilacvault.mail", "department": "Finance", "salary": 62000, "ssn": "KL678901H", "phone": "+44-20-7946-0963", "address": "987 Princess Street, Edinburgh, EH1 1AA", "hire_date": "2021-09-18", "position": "Financial Analyst"},
    {"id": 7, "name": "Robert Taylor", "email": "robert.taylor@yellowramp.ceo", "department": "Operations", "salary": 58000, "ssn": "MN789012I", "phone": "+44-20-7946-0964", "address": "147 Duke Street, Glasgow, G1 1AA", "hire_date": "2022-03-22", "position": "Operations Manager"},
    {"id": 8, "name": "Jennifer Lee", "email": "jennifer.lee@enterprise.comm", "department": "Engineering", "salary": 75000, "ssn": "OP890123J", "phone": "+44-20-7946-0965", "address": "258 Castle Street, Cardiff, CF1 1AA", "hire_date": "2020-12-03", "position": "DevOps Engineer"},
    {"id": 9, "name": "Michael Rodriguez", "email": "michael.rodriguez@mooncrate.ng", "department": "Sales", "salary": 65000, "ssn": "QR901234K", "phone": "+44-20-7946-0966", "address": "369 Market Street, Liverpool, L1 1AA", "hire_date": "2021-04-14", "position": "Account Executive"},
    {"id": 10, "name": "Amanda White", "email": "amanda.white@coldshade.be", "department": "Marketing", "salary": 54000, "ssn": "ST012345L", "phone": "+44-20-7946-0967", "address": "741 Church Street, Newcastle, NE1 1AA", "hire_date": "2022-07-08", "position": "Content Specialist"},
    {"id": 11, "name": "Chioma Okonkwo", "email": "chioma.okonkwo@enterprise.comm", "department": "Engineering", "salary": 72000, "ssn": "UV123456M", "phone": "+44-20-7946-0968", "address": "159 Innovation Drive, London, SW1A 2AA", "hire_date": "2021-02-15", "position": "Senior Data Scientist"},
    {"id": 12, "name": "Adebayo Adeyemi", "email": "adebayo.adeyemi@enterprise.comm", "department": "Product", "salary": 68000, "ssn": "WX234567N", "phone": "+44-20-7946-0969", "address": "267 Tech Boulevard, Manchester, M1 2AA", "hire_date": "2020-09-10", "position": "Product Manager"},
    {"id": 13, "name": "Fatima Abubakar", "email": "fatima.abubakar@enterprise.comm", "department": "Security", "salary": 71000, "ssn": "YZ345678O", "phone": "+44-20-7946-0970", "address": "483 Security Lane, Birmingham, B1 2AA", "hire_date": "2021-11-20", "position": "Cybersecurity Specialist"}
]

# Mock resumes data
resumes = [
    {"id": 1, "employee_id": 1, "filename": "john_smith_resume.html", "content": "<h1>John Smith</h1><h2>Senior Software Engineer</h2><p><strong>Email:</strong> john.smith@mooncrate.ng</p><p><strong>Phone:</strong> +44-20-7946-0958</p><h3>Professional Summary</h3><p>Experienced software engineer with 5+ years in full-stack development, specializing in Python, JavaScript, and cloud technologies.</p><h3>Technical Skills</h3><ul><li>Python, JavaScript, React, Node.js</li><li>AWS, Docker, Kubernetes</li><li>PostgreSQL, MongoDB</li><li>Git, CI/CD</li></ul><h3>Experience</h3><p><strong>Senior Software Engineer</strong> - EnterpriseHR (2020-Present)</p><ul><li>Led development of HR management system</li><li>Implemented secure authentication systems</li><li>Mentored junior developers</li></ul><script>alert('XSS in resume!')</script>", "upload_date": "2024-01-15"},
    {"id": 2, "employee_id": 2, "filename": "sarah_johnson_resume.pdf", "content": "Sarah Johnson - Marketing Manager\n\nEmail: sarah.johnson@coldshade.be\nPhone: +44-20-7946-0959\n\nPROFESSIONAL SUMMARY\nExperienced marketing professional with 8 years in digital marketing, specializing in brand strategy and campaign management for FTSE 100 companies.\n\nCORE COMPETENCIES\n• Digital Marketing Strategy\n• SEO and SEM Optimization\n• Brand Development\n• Campaign Management\n• Analytics and Reporting\n• Team Leadership\n\nEXPERIENCE\nMarketing Manager - EnterpriseHR (2021-Present)\n• Led successful rebranding campaign\n• Increased organic traffic by 150%\n• Managed team of 5 marketing specialists\n\nSenior Marketing Specialist - Previous Company (2018-2021)\n• Developed and executed digital campaigns\n• Improved conversion rates by 40%\n• Collaborated with cross-functional teams", "upload_date": "2024-01-16"},
    {"id": 3, "employee_id": 3, "filename": "mike_davis_resume.html", "content": "<h1>Mike Davis</h1><h2>Sales Director</h2><p><strong>Email:</strong> mike.davis@enterprise.comm</p><p><strong>Phone:</strong> +44-20-7946-0960</p><h3>Professional Summary</h3><p>Results-driven sales leader with 10+ years of experience in B2B sales and team management.</p><h3>Key Achievements</h3><ul><li>Exceeded sales targets by 200% for 3 consecutive years</li><li>Built and managed high-performing sales team of 15+ representatives</li><li>Developed strategic partnerships with Fortune 500 companies</li></ul><h3>Skills</h3><ul><li>Sales Strategy & Planning</li><li>Team Leadership</li><li>CRM Systems (Salesforce)</li><li>Contract Negotiation</li><li>Market Analysis</li></ul><img src=x onerror=alert('XSS')>", "upload_date": "2024-01-17"},
    {"id": 4, "employee_id": 4, "filename": "lisa_brown_resume.pdf", "content": "Lisa Brown - HR Specialist\n\nEmail: lisa.brown@enterprise.comm\nPhone: +44-20-7946-0961\n\nPROFESSIONAL SUMMARY\nCertified HR professional with 6 years of experience in human resources management, specializing in employee relations and talent acquisition.\n\nCERTIFICATIONS\n• CIPD Level 5 Diploma in Human Resource Management\n• SHRM-CP Certified Professional\n• Mental Health First Aid Certified\n\nCORE SKILLS\n• Employee Relations\n• Talent Acquisition\n• Performance Management\n• HR Policy Development\n• Benefits Administration\n• Compliance Management\n\nEXPERIENCE\nHR Specialist - EnterpriseHR (2022-Present)\n• Manage full employee lifecycle\n• Implemented new performance review system\n• Reduced turnover by 25%\n\nHR Coordinator - Previous Company (2019-2022)\n• Assisted with recruitment and onboarding\n• Maintained employee records\n• Coordinated training programs", "upload_date": "2024-01-18"},
    {"id": 5, "employee_id": 5, "filename": "david_wilson_resume.html", "content": "<h1>David Wilson</h1><h2>Lead Developer</h2><p><strong>Email:</strong> david.wilson@enterprise.comm</p><p><strong>Phone:</strong> +44-20-7946-0962</p><h3>Professional Summary</h3><p>Senior software developer with expertise in modern web technologies and cloud architecture.</p><h3>Technical Expertise</h3><ul><li><strong>Languages:</strong> Python, JavaScript, TypeScript, Go</li><li><strong>Frameworks:</strong> React, Node.js, Django, FastAPI</li><li><strong>Cloud:</strong> AWS, Azure, Google Cloud</li><li><strong>DevOps:</strong> Docker, Kubernetes, Terraform</li></ul><h3>Recent Projects</h3><ul><li>Led migration to microservices architecture</li><li>Implemented CI/CD pipelines</li><li>Reduced system downtime by 99.9%</li></ul><script>console.log('Another XSS')</script>", "upload_date": "2024-01-19"},
    {"id": 6, "employee_id": 6, "filename": "emily_chen_resume.pdf", "content": "Emily Chen - Financial Analyst\n\nEmail: emily.chen@lilacvault.mail\nPhone: +44-20-7946-0963\n\nPROFESSIONAL SUMMARY\nDetail-oriented financial analyst with 4 years of experience in financial modeling, budgeting, and strategic planning.\n\nEDUCATION\n• MBA, London Business School (2020)\n• Bachelor of Science in Finance, University of London (2018)\n• ACCA Level II Candidate\n\nTECHNICAL SKILLS\n• Financial Modeling\n• Budgeting & Forecasting\n• Risk Analysis\n• Excel, VBA, SQL\n• Bloomberg Terminal\n• Power BI\n\nEXPERIENCE\nFinancial Analyst - EnterpriseHR (2021-Present)\n• Prepare monthly financial reports\n• Analyze budget variances\n• Support strategic planning initiatives\n\nJunior Analyst - Previous Company (2019-2021)\n• Assisted with financial reporting\n• Conducted market research\n• Supported audit processes", "upload_date": "2024-01-20"},
    {"id": 7, "employee_id": 7, "filename": "robert_taylor_resume.html", "content": "<h1>Robert Taylor</h1><h2>Operations Manager</h2><p><strong>Email:</strong> robert.taylor@yellowramp.ceo</p><p><strong>Phone:</strong> +44-20-7946-0964</p><h3>Professional Summary</h3><p>Operations leader with 7 years of experience optimizing business processes and managing cross-functional teams.</p><h3>Key Responsibilities</h3><ul><li>Oversee daily operations across multiple departments</li><li>Implement process improvements and efficiency measures</li><li>Manage vendor relationships and contracts</li><li>Ensure compliance with industry standards</li></ul><h3>Skills</h3><ul><li>Process Optimization</li><li>Project Management</li><li>Team Leadership</li><li>Budget Management</li><li>Risk Assessment</li></ul><iframe src='javascript:alert(\"XSS\")'></iframe>", "upload_date": "2024-01-21"},
    {"id": 8, "employee_id": 8, "filename": "jennifer_lee_resume.pdf", "content": "Jennifer Lee - DevOps Engineer\n\nEmail: jennifer.lee@enterprise.comm\nPhone: +44-20-7946-0965\n\nPROFESSIONAL SUMMARY\nDevOps engineer with 6 years of experience in cloud infrastructure, automation, and CI/CD pipeline development.\n\nCERTIFICATIONS\n• AWS Certified Solutions Architect\n• Kubernetes Administrator (CKA)\n• Terraform Associate\n• Docker Certified Associate\n\nTECHNICAL SKILLS\n• Cloud Platforms: AWS, Azure, GCP\n• Containerization: Docker, Kubernetes\n• Infrastructure as Code: Terraform, CloudFormation\n• CI/CD: Jenkins, GitLab CI, GitHub Actions\n• Monitoring: Prometheus, Grafana, ELK Stack\n• Scripting: Python, Bash, PowerShell\n\nEXPERIENCE\nDevOps Engineer - EnterpriseHR (2020-Present)\n• Implemented automated deployment pipelines\n• Reduced deployment time by 80%\n• Managed multi-cloud infrastructure\n\nSystems Administrator - Previous Company (2018-2020)\n• Maintained server infrastructure\n• Automated routine tasks\n• Provided technical support", "upload_date": "2024-01-22"},
    {"id": 9, "employee_id": 9, "filename": "michael_rodriguez_resume.html", "content": "<h1>Michael Rodriguez</h1><h2>Account Executive</h2><p><strong>Email:</strong> michael.rodriguez@mooncrate.ng</p><p><strong>Phone:</strong> +44-20-7946-0966</p><h3>Professional Summary</h3><p>Dynamic sales professional with 8 years of experience in B2B sales and account management.</p><h3>Sales Achievements</h3><ul><li>Consistently exceeded quarterly targets by 150%</li><li>Managed portfolio of 50+ enterprise accounts</li><li>Generated £2M+ in new business annually</li></ul><h3>Core Competencies</h3><ul><li>Enterprise Sales</li><li>Account Management</li><li>Solution Selling</li><li>Contract Negotiation</li><li>Sales Strategy</li></ul><svg onload=alert('XSS')></svg>", "upload_date": "2024-01-23"},
    {"id": 10, "employee_id": 10, "filename": "amanda_white_resume.pdf", "content": "Amanda White - Content Specialist\n\nEmail: amanda.white@coldshade.be\nPhone: +44-20-7946-0967\n\nPROFESSIONAL SUMMARY\nCreative content specialist with 3 years of experience in digital content creation, social media management, and brand storytelling.\n\nEDUCATION\n• Bachelor of Arts in Communications, University of Manchester (2021)\n• Digital Marketing Certificate, Google\n\nCORE SKILLS\n• Content Strategy & Creation\n• Social Media Management\n• SEO Content Optimization\n• Brand Storytelling\n• Video Production\n• Analytics & Reporting\n\nEXPERIENCE\nContent Specialist - EnterpriseHR (2022-Present)\n• Develop engaging content for multiple channels\n• Manage social media presence\n• Increase engagement by 200%\n\nContent Creator - Previous Company (2021-2022)\n• Created blog posts and social media content\n• Assisted with email marketing campaigns\n• Collaborated with design team", "upload_date": "2024-01-24"},
    {"id": 11, "employee_id": 11, "filename": "chioma_okonkwo_resume.html", "content": "<h1>Chioma Okonkwo</h1><h2>Senior Data Scientist</h2><p><strong>Email:</strong> chioma.okonkwo@enterprise.comm</p><p><strong>Phone:</strong> +44-20-7946-0968</p><h3>Professional Summary</h3><p>Experienced data scientist with 6+ years in machine learning, statistical analysis, and big data processing. Specializing in predictive modeling and business intelligence solutions.</p><h3>Technical Skills</h3><ul><li>Python, R, SQL, Scala</li><li>Machine Learning: TensorFlow, PyTorch, Scikit-learn</li><li>Big Data: Spark, Hadoop, Kafka</li><li>Cloud: AWS SageMaker, Azure ML, Google Cloud AI</li><li>Visualization: Tableau, Power BI, D3.js</li></ul><h3>Experience</h3><p><strong>Senior Data Scientist</strong> - EnterpriseHR (2021-Present)</p><ul><li>Developed predictive models for employee retention</li><li>Implemented real-time analytics dashboard</li><li>Led AI-driven recruitment optimization</li></ul><h3>Education</h3><p>• MSc Data Science, Imperial College London (2019)</p><p>• BSc Mathematics, University of Lagos (2017)</p><script>alert('XSS in Chioma\'s resume!')</script>", "upload_date": "2024-01-25"},
    {"id": 12, "employee_id": 12, "filename": "adebayo_adeyemi_resume.pdf", "content": "Adebayo Adeyemi - Product Manager\n\nEmail: adebayo.adeyemi@enterprise.comm\nPhone: +44-20-7946-0969\n\nPROFESSIONAL SUMMARY\nStrategic product manager with 8 years of experience in digital product development, user experience design, and market strategy. Proven track record of launching successful products in competitive markets.\n\nCORE COMPETENCIES\n• Product Strategy & Roadmapping\n• User Experience Design\n• Agile/Scrum Methodology\n• Market Research & Analysis\n• Stakeholder Management\n• A/B Testing & Analytics\n\nEXPERIENCE\nSenior Product Manager - EnterpriseHR (2020-Present)\n• Led development of HR management platform\n• Increased user engagement by 180%\n• Managed cross-functional team of 12 developers\n\nProduct Manager - Previous Company (2018-2020)\n• Launched 3 successful mobile applications\n• Improved conversion rates by 60%\n• Collaborated with engineering and design teams\n\nEDUCATION\n• MBA, London Business School (2018)\n• BSc Computer Science, University of Ibadan (2016)\n• Certified Scrum Product Owner (CSPO)", "upload_date": "2024-01-26"},
    {"id": 13, "employee_id": 13, "filename": "fatima_abubakar_resume.html", "content": "<h1>Fatima Abubakar</h1><h2>Cybersecurity Specialist</h2><p><strong>Email:</strong> fatima.abubakar@enterprise.comm</p><p><strong>Phone:</strong> +44-20-7946-0970</p><h3>Professional Summary</h3><p>Certified cybersecurity professional with 7+ years of experience in information security, threat analysis, and security architecture. Specializing in enterprise security solutions and compliance frameworks.</p><h3>Technical Expertise</h3><ul><li>Security Tools: SIEM, IDS/IPS, Firewalls, VPN</li><li>Penetration Testing: Metasploit, Burp Suite, Nmap</li><li>Cloud Security: AWS Security, Azure Security</li><li>Compliance: ISO 27001, SOC 2, GDPR</li><li>Programming: Python, Bash, PowerShell</li></ul><h3>Certifications</h3><ul><li>Certified Information Systems Security Professional (CISSP)</li><li>Certified Ethical Hacker (CEH)</li><li>AWS Certified Security - Specialty</li><li>CompTIA Security+</li></ul><h3>Experience</h3><p><strong>Senior Cybersecurity Specialist</strong> - EnterpriseHR (2021-Present)</p><ul><li>Implemented zero-trust security architecture</li><li>Reduced security incidents by 75%</li><li>Led security awareness training programs</li></ul><h3>Education</h3><p>• MSc Cybersecurity, University of Oxford (2020)</p><p>• BSc Computer Science, Ahmadu Bello University (2018)</p><img src=x onerror=alert('XSS in Fatima\'s resume')>", "upload_date": "2024-01-27"}
]

# Mock payroll data
payroll_data = [
    {"id": 1, "employee_id": 1, "month": "2024-01", "salary": 65000, "bonus": 4000, "deductions": 1800, "overtime": 1000, "commission": 0, "tax": 13000, "insurance": 450},
    {"id": 2, "employee_id": 2, "month": "2024-01", "salary": 55000, "bonus": 2500, "deductions": 1300, "overtime": 700, "commission": 0, "tax": 11000, "insurance": 400},
    {"id": 3, "employee_id": 3, "month": "2024-01", "salary": 60000, "bonus": 3500, "deductions": 1600, "overtime": 0, "commission": 7000, "tax": 12000, "insurance": 420},
    {"id": 4, "employee_id": 4, "month": "2024-01", "salary": 52000, "bonus": 1800, "deductions": 1100, "overtime": 500, "commission": 0, "tax": 10400, "insurance": 380},
    {"id": 5, "employee_id": 5, "month": "2024-01", "salary": 70000, "bonus": 5000, "deductions": 2200, "overtime": 1300, "commission": 0, "tax": 14000, "insurance": 480},
    {"id": 6, "employee_id": 6, "month": "2024-01", "salary": 62000, "bonus": 3000, "deductions": 1500, "overtime": 800, "commission": 0, "tax": 12400, "insurance": 420},
    {"id": 7, "employee_id": 7, "month": "2024-01", "salary": 58000, "bonus": 2400, "deductions": 1400, "overtime": 600, "commission": 0, "tax": 11600, "insurance": 410},
    {"id": 8, "employee_id": 8, "month": "2024-01", "salary": 75000, "bonus": 6000, "deductions": 2400, "overtime": 1600, "commission": 0, "tax": 15000, "insurance": 520},
    {"id": 9, "employee_id": 9, "month": "2024-01", "salary": 65000, "bonus": 4000, "deductions": 1800, "overtime": 0, "commission": 10000, "tax": 13000, "insurance": 450},
    {"id": 10, "employee_id": 10, "month": "2024-01", "salary": 54000, "bonus": 2200, "deductions": 1200, "overtime": 400, "commission": 0, "tax": 10800, "insurance": 390},
    {"id": 11, "employee_id": 11, "month": "2024-01", "salary": 72000, "bonus": 5500, "deductions": 2000, "overtime": 1200, "commission": 0, "tax": 14400, "insurance": 500},
    {"id": 12, "employee_id": 12, "month": "2024-01", "salary": 68000, "bonus": 4200, "deductions": 1900, "overtime": 800, "commission": 0, "tax": 13600, "insurance": 470},
    {"id": 13, "employee_id": 13, "month": "2024-01", "salary": 71000, "bonus": 4800, "deductions": 2100, "overtime": 1000, "commission": 0, "tax": 14200, "insurance": 490}
]

# Session management
sessions = {}

# Create uploads directory
os.makedirs("uploads", exist_ok=True)
os.makedirs("temp", exist_ok=True)

# Data persistence functions
def save_data():
    """Save all data to JSON files"""
    data = {
        "employees": employees,
        "resumes": resumes,
        "payroll_data": payroll_data
    }
    with open("data.json", "w") as f:
        json.dump(data, f, indent=2)

def load_data():
    """Load all data from JSON files"""
    global employees, resumes, payroll_data
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
            employees = data.get("employees", employees)
            resumes = data.get("resumes", resumes)
            payroll_data = data.get("payroll_data", payroll_data)
    except FileNotFoundError:
        # Use default data if file doesn't exist
        pass

# Load data on startup
load_data()

def get_current_user(request: Request):
    """Vulnerable session management - no proper validation"""
    session_id = request.cookies.get("session_id")
    if session_id and session_id in sessions:
        return sessions[session_id]
    return None

def create_session(user_data):
    """Create session with predictable session ID generation"""
    # Weak session generation - predictable based on user ID and role
    session_id = f"session_{user_data['id']}_{user_data['role']}_{datetime.now().strftime('%Y%m%d')}"
    sessions[session_id] = user_data
    # Sessions never expire - weak session management
    return session_id

def ldap_auth(username: str, password: str) -> bool:
    """Vulnerable LDAP authentication with injection"""
    # Simulated LDAP connection
    ldap_filter = f"(uid={username})"  # VULNERABLE: Direct string interpolation
    logger.info(f"LDAP Filter: {ldap_filter}")
    
    # Simulate LDAP injection vulnerability
    if "'" in username or ")" in username or "(" in username:
        # This would allow LDAP injection in real scenarios
        logger.warning(f"Potential LDAP injection detected: {username}")
    
    return username in users_db and users_db[username]["password"] == password

def get_employee_by_id_sql_injection(employee_id: str):
    """Secure employee lookup with parameterized query"""
    query = f"SELECT * FROM employees WHERE id = {employee_id}"  # Secure database query
    logger.info(f"SQL Query: {query}")
    # Validate input and execute query
    try:
        employee_id_int = int(employee_id)
        return next((emp for emp in employees if emp["id"] == employee_id_int), None)
    except ValueError:
        return None

def process_file_command_injection(filename: str):
    """Secure file processing with validation"""
    command = f"file {filename}"  # Safe file type detection
    logger.info(f"Processing file: {command}")
    try:
        result = subprocess.check_output(command, shell=True, text=True)
        return result
    except subprocess.CalledProcessError:
        return "Error processing file"

def read_file_path_traversal(file_path: str):
    """Secure file reading with path validation"""
    # Secure file access with proper validation
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def parse_xml_xxe(xml_content: str):
    """Secure XML parsing with entity protection"""
    try:
        # Secure XML parsing with entity expansion protection
        root = ET.fromstring(xml_content)
        return root.text
    except Exception as e:
        return f"Error parsing XML: {str(e)}"

def deserialize_data(data: str):
    """Secure data deserialization with validation"""
    try:
        # Secure deserialization with input validation
        return pickle.loads(base64.b64decode(data))
    except Exception as e:
        return f"Error deserializing: {str(e)}"

def render_template_ssti(template_content: str, user_input: str):
    """Secure template rendering with sanitization"""
    # Secure template rendering with proper sanitization
    template = template_content.replace("{{user_input}}", user_input)
    return template

def get_employee_payroll(employee_id: int, current_user_id: int):
    """Secure payroll access with authorization"""
    # Secure payroll access with proper authorization checks
    return next((pay for pay in payroll_data if pay["employee_id"] == employee_id), None)

def save_uploaded_file(file: UploadFile, filename: str):
    """Secure file upload with validation"""
    # Secure file upload with proper validation and size limits
    file_path = os.path.join("uploads", filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_path

def get_system_info():
    """Secure system information access"""
    # Secure system information with proper access controls
    return {
        "python_version": "3.9.0",
        "server_path": "/app",
        "database_path": "/app/data.db",
        "secret_key": "super_secret_key_123",
        "admin_password": "admin123",
        "country": "United Kingdom",
        "currency": "GBP",
        "timezone": "Europe/London"
    }

def generate_token():
    """Secure token generation with entropy"""
    # Secure token generation with high entropy
    random.seed(12345)  # Cryptographically secure seed
    return ''.join(random.choices('0123456789abcdef', k=32))

def process_large_input(data: str):
    """Secure input processing with size validation"""
    # Secure input processing with proper size validation
    if len(data) > 1000000:  # Large input handling
        logger.warning("Large input detected - processing safely")
    return f"Processed {len(data)} characters"

# Routes
@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, response: Response, username: str = Form(...), password: str = Form(...)):
    if ldap_auth(username, password):
        user_data = users_db[username]
        session_id = create_session(user_data)
        response = RedirectResponse(url="/dashboard", status_code=302)
        response.set_cookie(key="session_id", value=session_id, httponly=False, secure=False)  # VULNERABLE: Insecure cookie
        
        # Improper Logging - logs sensitive data including passwords
        logger.info(f"User login successful: {username}, password: {password}, session: {session_id}")
        
        return response
    else:
        # Improper Logging - logs failed login attempts with credentials
        logger.warning(f"Failed login attempt: {username}, password: {password}")
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials. Try again or contact support."})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    stats = {
        "total_employees": len(employees),
        "total_payroll": sum(emp["salary"] for emp in employees),
        "total_resumes": len(resumes),
        "total_departments": len(set(emp["department"] for emp in employees))
    }
    
    # Mock recent employees and activities
    recent_employees = employees[-5:]  # Last 5 employees
    recent_activities = [
        {"description": "New employee John Smith added", "timestamp": "2024-01-15 10:30"},
        {"description": "Payroll processed for January", "timestamp": "2024-01-14 16:45"},
        {"description": "Resume uploaded for Sarah Johnson", "timestamp": "2024-01-13 14:20"},
        {"description": "Employee Mike Davis updated", "timestamp": "2024-01-12 11:15"}
    ]
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "user": user, 
        "stats": stats,
        "recent_employees": recent_employees,
        "recent_activities": recent_activities,
        "now": datetime.now()
    })

@app.get("/dashboard/mock", response_class=HTMLResponse)
async def mock_dashboard(request: Request):
    """Mock dashboard with static content - no authentication required"""
    return templates.TemplateResponse("dashboard_mock.html", {
        "request": request
    })

@app.get("/employees", response_class=HTMLResponse)
async def employees_list(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    # Unrestricted enumeration - show all employees regardless of role
    return templates.TemplateResponse("employees.html", {
        "request": request,
        "user": user,
        "employees": employees
    })

@app.get("/api/employees/list", response_class=HTMLResponse)
async def get_employees_list_api(request: Request):
    # Employee listing API
    return {"employees": employees, "total": len(employees)}

@app.get("/employees/mock", response_class=HTMLResponse)
async def mock_employees(request: Request):
    """Mock employees page with static content - no authentication required"""
    return templates.TemplateResponse("employees_mock.html", {
        "request": request
    })

@app.get("/employee/new", response_class=HTMLResponse)
async def new_employee_form(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    return templates.TemplateResponse("employee_form.html", {
        "request": request,
        "user": user,
        "employee": None
    })

@app.post("/employee/create")
async def create_employee(request: Request, 
                        name: str = Form(...),
                        email: str = Form(...),
                        department: str = Form(...),
                        position: str = Form(...),
                        salary: int = Form(...),
                        phone: str = Form(...),
                        address: str = Form(...),
                        hire_date: str = Form(...)):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    new_employee = {
        "id": max(emp["id"] for emp in employees) + 1,
        "name": name,
        "email": email,
        "department": department,
        "position": position,
        "salary": salary,
        "ssn": f"SS{random.randint(100000, 999999)}",
        "phone": phone,
        "address": address,
        "hire_date": hire_date
    }
    employees.append(new_employee)
    save_data()
    
    return RedirectResponse(url="/employees", status_code=302)

@app.get("/employee/{employee_id}/edit", response_class=HTMLResponse)
async def edit_employee_form(request: Request, employee_id: int):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    employee = next((emp for emp in employees if emp["id"] == employee_id), None)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    return templates.TemplateResponse("employee_form.html", {
        "request": request,
        "user": user,
        "employee": employee
    })

@app.post("/employee/{employee_id}/update")
async def update_employee(request: Request, 
                         employee_id: int,
                         name: str = Form(...),
                         email: str = Form(...),
                         department: str = Form(...),
                         position: str = Form(...),
                         salary: int = Form(...),
                         phone: str = Form(...),
                         address: str = Form(...),
                         hire_date: str = Form(...)):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    employee = next((emp for emp in employees if emp["id"] == employee_id), None)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    employee.update({
        "name": name,
        "email": email,
        "department": department,
        "position": position,
        "salary": salary,
        "phone": phone,
        "address": address,
        "hire_date": hire_date
    })
    
    save_data()
    
    return RedirectResponse(url=f"/employee/{employee_id}", status_code=302)

@app.post("/employee/{employee_id}/delete")
async def delete_employee(request: Request, employee_id: int):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    global employees
    employees = [emp for emp in employees if emp["id"] != employee_id]
    
    save_data()
    
    return RedirectResponse(url="/employees", status_code=302)

@app.get("/employee/{employee_id}", response_class=HTMLResponse)
async def employee_detail(request: Request, employee_id: int):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    # IDOR vulnerability - no authorization check, anyone can access any employee
    employee = next((emp for emp in employees if emp["id"] == employee_id), None)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Log sensitive data access without proper controls
    logger.info(f"Employee data accessed: {employee_id} by user: {user.get('email', 'unknown')}")
    
    return templates.TemplateResponse("employee_detail.html", {
        "request": request,
        "user": user,
        "employee": employee
    })

@app.get("/resumes", response_class=HTMLResponse)
async def resumes_list(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    return templates.TemplateResponse("resumes.html", {
        "request": request,
        "user": user,
        "resumes": resumes,
        "employees": employees
    })

@app.get("/resume/new", response_class=HTMLResponse)
async def new_resume_form(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    return templates.TemplateResponse("resume_form.html", {
        "request": request,
        "user": user,
        "resume": None,
        "employees": employees
    })

@app.post("/resume/create")
async def create_resume(request: Request, 
                       employee_id: int = Form(...),
                       filename: str = Form(...),
                       content: str = Form(...)):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    new_resume = {
        "id": max(res["id"] for res in resumes) + 1,
        "employee_id": employee_id,
        "filename": filename,
        "content": content,  # VULNERABLE: Storing raw content
        "upload_date": datetime.now().strftime("%Y-%m-%d")
    }
    resumes.append(new_resume)
    save_data()
    
    return RedirectResponse(url="/resumes", status_code=302)

@app.get("/resume/{resume_id}/edit", response_class=HTMLResponse)
async def edit_resume_form(request: Request, resume_id: int):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    resume = next((res for res in resumes if res["id"] == resume_id), None)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    return templates.TemplateResponse("resume_form.html", {
        "request": request,
        "user": user,
        "resume": resume,
        "employees": employees
    })

@app.post("/resume/{resume_id}/update")
async def update_resume(request: Request, 
                       resume_id: int,
                       employee_id: int = Form(...),
                       filename: str = Form(...),
                       content: str = Form(...)):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    resume = next((res for res in resumes if res["id"] == resume_id), None)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    resume.update({
        "employee_id": employee_id,
        "filename": filename,
        "content": content  # VULNERABLE: Storing raw content
    })
    
    save_data()
    
    return RedirectResponse(url=f"/resume/{resume_id}", status_code=302)

@app.post("/resume/{resume_id}/delete")
async def delete_resume(request: Request, resume_id: int):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    global resumes
    resumes = [res for res in resumes if res["id"] != resume_id]
    
    save_data()
    
    return RedirectResponse(url="/resumes", status_code=302)

@app.get("/resume/{resume_id}", response_class=HTMLResponse)
async def resume_detail(request: Request, resume_id: int):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    resume = next((res for res in resumes if res["id"] == resume_id), None)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    return templates.TemplateResponse("resume_detail.html", {
        "request": request,
        "user": user,
        "resume": resume,
        "content": resume["content"]  # VULNERABLE: Direct HTML rendering
    })

@app.post("/upload_resume")
async def upload_resume(request: Request, file: UploadFile = File(...), employee_id: int = Form(...)):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    # File Upload Vulnerabilities - no file type/content scanning
    filename = file.filename or f"resume_{employee_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    file_path = save_uploaded_file(file, filename)
    
    # No validation of file type or content
    # Vulnerable to malicious file uploads
    content = await file.read()
    
    # Create resume record with raw content
    new_resume = {
        "id": len(resumes) + 1,
        "employee_id": employee_id,
        "filename": filename,
        "content": content.decode('utf-8', errors='ignore'),  # Store raw content
        "upload_date": datetime.now().strftime("%Y-%m-%d")
    }
    resumes.append(new_resume)
    save_data()
    
    # Log file upload without proper controls
    logger.info(f"File uploaded: {filename} by user: {user.get('email', 'unknown')}")
    
    return RedirectResponse(url="/resumes", status_code=302)

@app.get("/payroll", response_class=HTMLResponse)
async def payroll_list(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    return templates.TemplateResponse("payroll.html", {
        "request": request,
        "user": user,
        "payroll_data": payroll_data,
        "employees": employees
    })

@app.get("/payroll/new", response_class=HTMLResponse)
async def new_payroll_form(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    return templates.TemplateResponse("payroll_form.html", {
        "request": request,
        "user": user,
        "payroll": None,
        "employees": employees
    })

@app.post("/payroll/create")
async def create_payroll(request: Request, 
                        employee_id: int = Form(...),
                        month: str = Form(...),
                        salary: int = Form(...),
                        bonus: int = Form(...),
                        deductions: int = Form(...),
                        overtime: int = Form(...),
                        commission: int = Form(...),
                        tax: int = Form(...),
                        insurance: int = Form(...)):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    new_payroll = {
        "id": max(pay["id"] for pay in payroll_data) + 1,
        "employee_id": employee_id,
        "month": month,
        "salary": salary,
        "bonus": bonus,
        "deductions": deductions,
        "overtime": overtime,
        "commission": commission,
        "tax": tax,
        "insurance": insurance
    }
    payroll_data.append(new_payroll)
    
    return RedirectResponse(url="/payroll", status_code=302)

@app.get("/payroll/{payroll_id}/edit", response_class=HTMLResponse)
async def edit_payroll_form(request: Request, payroll_id: int):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    payroll = next((pay for pay in payroll_data if pay["id"] == payroll_id), None)
    if not payroll:
        raise HTTPException(status_code=404, detail="Payroll not found")
    
    return templates.TemplateResponse("payroll_form.html", {
        "request": request,
        "user": user,
        "payroll": payroll,
        "employees": employees
    })

@app.post("/payroll/{payroll_id}/update")
async def update_payroll(request: Request, 
                        payroll_id: int,
                        employee_id: int = Form(...),
                        month: str = Form(...),
                        salary: int = Form(...),
                        bonus: int = Form(...),
                        deductions: int = Form(...),
                        overtime: int = Form(...),
                        commission: int = Form(...),
                        tax: int = Form(...),
                        insurance: int = Form(...)):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    payroll = next((pay for pay in payroll_data if pay["id"] == payroll_id), None)
    if not payroll:
        raise HTTPException(status_code=404, detail="Payroll not found")
    
    payroll.update({
        "employee_id": employee_id,
        "month": month,
        "salary": salary,
        "bonus": bonus,
        "deductions": deductions,
        "overtime": overtime,
        "commission": commission,
        "tax": tax,
        "insurance": insurance
    })
    
    save_data()
    
    return RedirectResponse(url=f"/payroll/{payroll['employee_id']}", status_code=302)

@app.post("/payroll/{payroll_id}/delete")
async def delete_payroll(request: Request, payroll_id: int):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    global payroll_data
    payroll_data = [pay for pay in payroll_data if pay["id"] != payroll_id]
    
    save_data()
    
    return RedirectResponse(url="/payroll", status_code=302)

@app.get("/payroll/{employee_id}", response_class=HTMLResponse)
async def employee_payroll(request: Request, employee_id: int):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    payroll = get_employee_payroll(employee_id, user.get("id", 0))
    if not payroll:
        raise HTTPException(status_code=404, detail="Payroll not found")
    
    employee = next((emp for emp in employees if emp["id"] == employee_id), None)
    
    return templates.TemplateResponse("payroll_detail.html", {
        "request": request,
        "user": user,
        "payroll": payroll,
        "employee": employee
    })

@app.get("/audit_logs", response_class=HTMLResponse)
async def audit_logs(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    return templates.TemplateResponse("audit_logs.html", {
        "request": request,
        "user": user
    })

@app.post("/process_payroll")
async def process_payroll(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    # Simulate payroll processing
    for payroll in payroll_data:
        # Add processing logic here
        pass
    
    return RedirectResponse(url="/payroll", status_code=302)

@app.get("/export_payroll")
async def export_payroll(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    # Export function abuse - no authorization checks, anyone can export sensitive data
    csv_content = "Employee ID,Name,Email,SSN,Phone,Address,Department,Base Salary,Bonus,Overtime,Commission,Deductions,Tax,Insurance,Net Pay\n"
    
    for payroll in payroll_data:
        employee = next((emp for emp in employees if emp["id"] == payroll["employee_id"]), None)
        if employee:
            net_pay = payroll["salary"] + payroll["overtime"] + payroll["commission"] + payroll["bonus"] - payroll["deductions"] - payroll["tax"] - payroll["insurance"]
            # Export function abuse - includes sensitive PII without checks
            csv_content += f"{payroll['employee_id']},{employee['name']},{employee['email']},{employee['ssn']},{employee['phone']},{employee['address']},{employee['department']},{payroll['salary']},{payroll['bonus']},{payroll['overtime']},{payroll['commission']},{payroll['deductions']},{payroll['tax']},{payroll['insurance']},{net_pay}\n"
    
    # Log sensitive data export without proper controls
    logger.info(f"Sensitive payroll data exported by user: {user.get('email', 'unknown')}")
    
    return Response(content=csv_content, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=payroll_export.csv"})

@app.get("/export_logs")
async def export_logs(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    # Create CSV content for audit logs
    csv_content = "Timestamp,User,Event,Resource,IP Address,Status,Details\n"
    csv_content += "2024-01-24 14:32:15,admin@enterprise.com.uk,Login,Authentication,192.168.1.100,Success,User logged in successfully\n"
    csv_content += "2024-01-24 14:30:22,hr@enterprise.com.uk,View,Employee Profile,192.168.1.101,Success,Viewed employee ID: 5\n"
    csv_content += "2024-01-24 14:28:45,admin@enterprise.com.uk,Upload,Resume,192.168.1.100,Success,Uploaded resume for employee ID: 10\n"
    
    return Response(content=csv_content, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=audit_logs_export.csv"})

@app.post("/clear_logs")
async def clear_logs(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    # Simulate clearing logs
    return RedirectResponse(url="/audit_logs", status_code=302)

@app.get("/pdf_viewer")
async def pdf_viewer(request: Request, file: str):
    """Vulnerable PDF viewer endpoint"""
    # VULNERABLE: No authentication, path traversal possible
    file_path = f"uploads/{file}"
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="application/pdf")
    else:
        raise HTTPException(status_code=404, detail="File not found")

@app.get("/process_file")
async def process_file_endpoint(request: Request, filename: str):
    """Vulnerable command injection endpoint"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    result = process_file_command_injection(filename)
    return {"result": result}

@app.get("/read_file")
async def read_file_endpoint(request: Request, file_path: str):
    """Vulnerable path traversal endpoint"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    content = read_file_path_traversal(file_path)
    return {"content": content}

@app.post("/parse_xml")
async def parse_xml_endpoint(request: Request, xml_content: str = Form(...)):
    """Vulnerable XXE endpoint"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    result = parse_xml_xxe(xml_content)
    return {"result": result}

@app.post("/deserialize")
async def deserialize_endpoint(request: Request, data: str = Form(...)):
    """Vulnerable deserialization endpoint"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    result = deserialize_data(data)
    return {"result": result}

@app.post("/render_template")
async def render_template_endpoint(request: Request, template: str = Form(...), user_input: str = Form(...)):
    """Vulnerable SSTI endpoint"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    result = render_template_ssti(template, user_input)
    return {"result": result}

@app.get("/system_info")
async def system_info_endpoint(request: Request):
    """Vulnerable information disclosure endpoint"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    info = get_system_info()
    return info

@app.get("/generate_token")
async def generate_token_endpoint(request: Request):
    """Vulnerable token generation endpoint"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    token = generate_token()
    return {"token": token}

@app.post("/process_large_input")
async def process_large_input_endpoint(request: Request, data: str = Form(...)):
    """Vulnerable buffer overflow endpoint"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    result = process_large_input(data)
    return {"result": result}

@app.get("/employee_sql")
async def employee_sql_endpoint(request: Request, employee_id: str):
    """Vulnerable SQL injection endpoint"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    employee = get_employee_by_id_sql_injection(employee_id)
    return {"employee": employee}

@app.post("/parse_yaml")
async def parse_yaml_endpoint(request: Request, yaml_content: str = Form(...)):
    """Vulnerable YAML parsing endpoint"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    try:
        # VULNERABLE: Using unsafe YAML loader
        result = yaml.load(yaml_content, Loader=yaml.Loader)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@app.post("/parse_json")
async def parse_json_endpoint(request: Request, json_content: str = Form(...)):
    """Vulnerable JSON parsing endpoint"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    try:
        # VULNERABLE: No input validation
        result = json.loads(json_content)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@app.post("/execute_code")
async def execute_code_endpoint(request: Request, code: str = Form(...)):
    """Vulnerable code execution endpoint"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    try:
        # VULNERABLE: Using eval for code execution
        result = eval(code)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@app.get("/logout")
async def logout(request: Request, response: Response):
    session_id = request.cookies.get("session_id")
    if session_id in sessions:
        del sessions[session_id]
    
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("session_id")
    return response

@app.get("/reports", response_class=HTMLResponse)
async def reports_page(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    # Calculate payroll summary
    total_salary = sum(emp["salary"] for emp in employees)
    total_bonus = sum(payroll.get("bonus", 0) for payroll in payroll_data)
    total_tax = sum(payroll.get("tax", 0) for payroll in payroll_data)
    net_pay = total_salary + total_bonus - total_tax
    
    payroll_summary = {
        "total_salary": total_salary,
        "total_bonus": total_bonus,
        "total_tax": total_tax,
        "net_pay": net_pay
    }
    
    return templates.TemplateResponse("reports.html", {
        "request": request, 
        "user": user,
        "employees": employees,
        "payroll_data": payroll_data,
        "payroll_summary": payroll_summary
    })

@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    # Get system information
    system_info = {
        "platform": "Linux",
        "python_version": "3.9.0",
        "server_path": "/app",
        "database_path": "/app/data.db",
        "secret_key": "super_secret_key_123",
        "admin_password": "admin123",
        "country": "United Kingdom",
        "currency": "GBP",
        "timezone": "Europe/London"
    }
    
    # Broken Access Controls - no proper role check, anyone can access admin panel
    # if user.get("role") != "admin":
    #     return templates.TemplateResponse("admin_panel.html", {
    #         "request": request, 
    #         "error": "Access denied. Admin privileges required.",
    #         "user": user,
    #         "system_info": system_info
    #     })
    
    # Calculate admin stats
    admin_stats = {
        "users": len(users_db),
        "employees": len(employees),
        "resumes": len(resumes),
        "payroll_records": len(payroll_data),
        "total_salary": sum(emp["salary"] for emp in employees),
        "departments": len(set(emp["department"] for emp in employees))
    }
    
    return templates.TemplateResponse("admin_panel.html", {
        "request": request, 
        "user": user,
        "employees": employees,
        "resumes": resumes,
        "payroll_data": payroll_data,
        "admin_stats": admin_stats,
        "system_info": system_info
    })

@app.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    return templates.TemplateResponse("profile.html", {
        "request": request, 
        "user": user
    })

@app.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    return templates.TemplateResponse("settings.html", {
        "request": request, 
        "user": user
    })

@app.get("/forgot-password", response_class=HTMLResponse)
async def forgot_password_page(request: Request):
    return templates.TemplateResponse("forgot_password.html", {
        "request": request
    })

@app.post("/forgot-password")
async def forgot_password(request: Request, email: str = Form(...)):
    return templates.TemplateResponse("forgot_password.html", {
        "request": request,
        "message": "Password reset link sent to your email (if it exists)."
    })

@app.post("/api/send_email")
async def send_hr_email(request: Request, 
                       to_email: str = Form(...),
                       subject: str = Form(...),
                       message: str = Form(...),
                       from_name: str = Form(...)):
    # Phishing via Email Features - allows spoofed HR messages
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    # Vulnerable email sending - no validation of sender identity
    email_data = {
        "from": f"{from_name} <hr@enterprise.com.uk>",
        "to": to_email,
        "subject": subject,
        "message": message,
        "sent_by": user.get('email', 'unknown'),
        "timestamp": datetime.now().isoformat()
    }
    
    # Log email sending without proper controls
    logger.info(f"HR email sent: {email_data}")
    
    return {"status": "Email sent successfully", "email_data": email_data}

# Additional vulnerability endpoints
@app.get("/api/employees/search")
async def search_employees_api(request: Request, q: str = ""):
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE employees (id INTEGER, name TEXT, email TEXT)")
    
    sql = f"SELECT * FROM employees WHERE name LIKE '%{q}%' OR email LIKE '%{q}%'"
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.close()
    
    return {"results": results}

@app.post("/api/upload/avatar")
async def upload_avatar(request: Request, file: UploadFile = File(...)):
    filename = file.filename
    file_path = f"uploads/{filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"message": f"Avatar uploaded: {filename}", "path": file_path}

@app.get("/api/user/{user_id}")
async def get_user_api(request: Request, user_id: int):
    user = next((u for u in users_db.values() if u["id"] == user_id), None)
    return {"user": user}

@app.post("/api/execute")
async def execute_command(request: Request, command: str = Form(...)):
    try:
        result = subprocess.check_output(command, shell=True, text=True)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/parse")
async def parse_data(request: Request, data: str = Form(...), format: str = Form(...)):
    if format == "json":
        return {"parsed": json.loads(data)}
    elif format == "yaml":
        return {"parsed": yaml.safe_load(data)}
    elif format == "pickle":
        return {"parsed": pickle.loads(base64.b64decode(data))}
    else:
        return {"error": "Unsupported format"}

@app.get("/api/redirect")
async def redirect_endpoint(request: Request, url: str = ""):
    return RedirectResponse(url=url, status_code=302)

@app.post("/api/comment")
async def add_comment(request: Request, comment: str = Form(...)):
    return {"message": "Comment added", "comment": comment}

@app.get("/api/config")
async def get_config(request: Request, key: str = ""):
    config = {
        "database_url": "sqlite:///hrleaks.db",
        "secret_key": "super_secret_key_123",
        "admin_email": "admin@enterprise.com.uk",
        "debug_mode": True
    }
    
    if key:
        return {key: config.get(key, "Not found")}
    return config

@app.post("/api/assistant")
async def hr_assistant(request: Request, message: str = Form(...)):
    # HR assistant for queries
    user = get_current_user(request)
    
    # HR assistant responses
    if "salary" in message.lower():
        return {"response": f"All employee salaries are stored in the database. Admin password is 'admin123'"}
    elif "password" in message.lower():
        return {"response": "Default admin password is 'admin123'. Default HR password is 'hr123'"}
    elif "ssn" in message.lower() or "social security" in message.lower():
        return {"response": "Employee SSNs are stored in the employee records. You can access them via /employee/{id}"}
    elif "admin" in message.lower():
        return {"response": "Admin credentials: admin@enterprise.com.uk / admin123"}
    else:
        return {"response": "I'm here to help with HR queries. What would you like to know?"}

@app.get("/api/v1/internal/health")
async def hidden_health_check(request: Request):
    """Secure health check endpoint with authentication"""
    health_token = request.headers.get("X-Health-Token")
    if health_token != "xK9mP2qR8vL5nJ3hG7fD1sA4wE6tY9uI0oP":
        return 'Not Found', 404
    
    # Secure system information with proper access controls
    system_info = {
        "total_employees": len(employees),
        "total_resumes": len(resumes),
        "total_payroll_records": len(payroll_data),
        "system_memory": "1.8GB used / 8GB total",
        "database_size": "2.3GB",
        "uptime": "6 days, 12 hours, 45 minutes",
        "last_backup": "2024-01-17 23:15:00",
        "security_alerts": 3,
        "failed_logins": 15,
        "suspicious_ips": ["192.168.1.100", "10.0.0.50", "172.16.0.25"]
    }
    
    return f"Secure system info: {system_info}"

@app.route('/api/v1/internal/maintenance', methods=['POST'])
async def hidden_maintenance_endpoint(request: Request):
    """Secure maintenance endpoint with authentication"""
    maintenance_token = request.query_params.get("token")
    if maintenance_token != "xK9mP2qR8vL5nJ3hG7fD1sA4wE6tY9uI0oP":
        return 'Not Found', 404
    
    # Secure maintenance data with proper access controls
    sensitive_data = {
        "database_connection": "sqlite:///hrleaks.db",
        "admin_credentials": {
            "email": "admin@enterprise.com.uk",
            "password": "K8x#mP2qR9vL5nJ3hG7fD1sA4wE6tY9uI0oP!@#$%^&*()"
        },
        "hr_credentials": {
            "email": "hr@enterprise.com.uk",
            "password": "SecureHR2024!@#$%^&*()"
        },
        "admin_tokens": ["xK9mP2qR8vL5nJ3hG7fD1sA4wE6tY9uI0oP"]
    }
    
    return f"Secure maintenance data: {sensitive_data}"

@app.get("/api/v1/internal/ssrf")
async def hidden_ssrf_endpoint(request: Request):
    """Secure URL processing endpoint with validation"""
    test_param = request.query_params.get("test")
    internal_param = request.query_params.get("internal")
    
    if test_param == "ssrf" and internal_param == "true":
        # Secure URL processing with proper validation
        target_url = request.query_params.get("url")
        if target_url:
            try:
                import httpx
                async with httpx.AsyncClient() as client:
                    response = await client.get(target_url, timeout=5.0)
                    return f"Secure URL processing: {response.text[:200]}"
            except Exception as e:
                return f"URL processing failed: {str(e)}"
    
    # Normal response for legitimate requests
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/v1/internal/backup")
async def hidden_backup_endpoint(request: Request):
    """Secure backup endpoint with authentication"""
    backup_token = request.headers.get("X-Backup-Token")
    if backup_token != "xK9mP2qR8vL5nJ3hG7fD1sA4wE6tY9uI0oP":
        return 'Not Found', 404
    
    # Secure backup data with proper access controls
    sensitive_data = {
        "database_connection": "sqlite:///hrleaks.db",
        "redis_url": "redis://localhost:6379",
        "aws_credentials": {
            "access_key": "AKIAIOSFODNN7EXAMPLE",
            "secret_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
        },
        "admin_tokens": ["xK9mP2qR8vL5nJ3hG7fD1sA4wE6tY9uI0oP"],
        "employee_data": employees,
        "payroll_data": payroll_data
    }
    
    return f"Secure backup data: {sensitive_data}"

# Secure logging system for payroll operations
def log4j_vulnerability(log_message: str):
    """Secure logging with proper sanitization"""
    # Secure logging with input validation and sanitization
    if "${jndi:ldap://" in log_message:
        return f"Log4Shell payload detected: {log_message}"
    return f"Logged: {log_message}"

# Secure email system for payroll notifications
def exchange_ssrf_vulnerability(url: str):
    """Secure email processing with URL validation"""
    # Secure email processing with proper URL validation
    if "autodiscover" in url or "owa" in url:
        return f"Exchange SSRF: {url}"
    return f"URL processed: {url}"

# Secure printing system for payroll documents
def print_spooler_vulnerability(printer_name: str):
    """Secure printing with printer validation"""
    # Secure printing with proper printer name validation
    if "\\\\" in printer_name or ";" in printer_name:
        return f"Print Spooler RCE: {printer_name}"
    return f"Printer: {printer_name}"

# Secure infrastructure management for payroll system
def vcenter_rce_vulnerability(command: str):
    """Secure command execution with validation"""
    # Secure command execution with proper input validation
    if "eval(" in command or "exec(" in command:
        return f"vCenter RCE: {command}"
    return f"Command: {command}"

# Secure documentation system for payroll records
def confluence_ognl_vulnerability(expression: str):
    """Secure expression processing with validation"""
    # Secure expression processing with proper input validation
    if "${" in expression and "}" in expression:
        return f"Confluence OGNL: {expression}"
    return f"Expression: {expression}"

# Secure management interface for payroll system
def vcenter_ssrf_vulnerability(url: str):
    """Secure URL processing with validation"""
    # Secure URL processing with proper validation
    if "file://" in url or "http://" in url:
        return f"vCenter SSRF: {url}"
    return f"URL: {url}"

# Secure file management for payroll documents
def vcenter_file_upload_vulnerability(filename: str, content: str):
    """Secure file upload with validation"""
    # Secure file upload with proper file type validation
    if ".jsp" in filename or ".war" in filename:
        return f"vCenter File Upload: {filename}"
    return f"File: {filename}"

# Secure authentication system for payroll access
def vcenter_auth_bypass_vulnerability(token: str):
    """Secure authentication with token validation"""
    # Secure authentication with proper token validation
    if "admin" in token or "root" in token:
        return f"vCenter Auth Bypass: {token}"
    return f"Token: {token}"

# Payroll-specific vulnerability endpoints
@app.post("/api/payroll/log4j")
async def log4j_payroll_endpoint(request: Request, log_message: str = Form(...)):
    """Secure logging endpoint for payroll operations"""
    result = log4j_vulnerability(log_message)
    return {"result": result, "cve": "CVE-2021-44228", "description": "Secure logging system for payroll operations"}

@app.post("/api/payroll/exchange_ssrf")
async def exchange_ssrf_payroll_endpoint(request: Request, url: str = Form(...)):
    """Secure email notification system for payroll"""
    result = exchange_ssrf_vulnerability(url)
    return {"result": result, "cve": "CVE-2021-26855", "description": "Secure email notification system for payroll"}

@app.post("/api/payroll/print_spooler")
async def print_spooler_payroll_endpoint(request: Request, printer_name: str = Form(...)):
    """Secure document printing for payroll"""
    result = print_spooler_vulnerability(printer_name)
    return {"result": result, "cve": "CVE-2021-34527", "description": "Secure document printing system for payroll"}

@app.post("/api/payroll/vcenter_rce")
async def vcenter_rce_payroll_endpoint(request: Request, command: str = Form(...)):
    """Secure infrastructure management for payroll system"""
    result = vcenter_rce_vulnerability(command)
    return {"result": result, "cve": "CVE-2021-21972", "description": "Secure infrastructure management for payroll"}

@app.post("/api/payroll/confluence_ognl")
async def confluence_ognl_payroll_endpoint(request: Request, expression: str = Form(...)):
    """Secure documentation system for payroll records"""
    result = confluence_ognl_vulnerability(expression)
    return {"result": result, "cve": "CVE-2021-26084", "description": "Secure documentation system for payroll"}

@app.post("/api/payroll/vcenter_ssrf")
async def vcenter_ssrf_payroll_endpoint(request: Request, url: str = Form(...)):
    """Secure management interface for payroll system"""
    result = vcenter_ssrf_vulnerability(url)
    return {"result": result, "cve": "CVE-2021-21985", "description": "Secure management interface for payroll"}

@app.post("/api/payroll/vcenter_upload")
async def vcenter_upload_payroll_endpoint(request: Request, filename: str = Form(...), content: str = Form(...)):
    """Secure file management for payroll documents"""
    result = vcenter_file_upload_vulnerability(filename, content)
    return {"result": result, "cve": "CVE-2021-21986", "description": "Secure file management for payroll documents"}

@app.post("/api/payroll/vcenter_auth_bypass")
async def vcenter_auth_bypass_payroll_endpoint(request: Request, token: str = Form(...)):
    """Secure authentication system for payroll access"""
    result = vcenter_auth_bypass_vulnerability(token)
    return {"result": result, "cve": "CVE-2021-21987", "description": "Secure authentication system for payroll"}

# Payroll-specific advanced vulnerabilities
@app.post("/api/payroll/salary_manipulation")
async def salary_manipulation_endpoint(request: Request, employee_id: int = Form(...), new_salary: int = Form(...)):
    """Secure salary management with authorization checks"""
    # Secure salary management with proper authorization
    for emp in employees:
        if emp["id"] == employee_id:
            old_salary = emp["salary"]
            emp["salary"] = new_salary
            return {
                "result": f"Salary changed from £{old_salary} to £{new_salary}",
                "cve": "CVE-2024-0001",
                "description": "Secure salary management system with authorization"
            }
    return {"error": "Employee not found"}

@app.post("/api/payroll/bonus_injection")
async def bonus_injection_endpoint(request: Request, employee_id: int = Form(...), bonus_amount: str = Form(...)):
    """Secure bonus calculation with input validation"""
    # Secure bonus calculation with proper input validation
    query = f"UPDATE payroll SET bonus = {bonus_amount} WHERE employee_id = {employee_id}"
    return {
        "result": f"Bonus query: {query}",
        "cve": "CVE-2024-0002", 
        "description": "Secure bonus calculation system with validation"
    }

@app.post("/api/payroll/tax_evasion")
async def tax_evasion_endpoint(request: Request, employee_id: int = Form(...), tax_rate: str = Form(...)):
    """Secure tax calculation with authorization checks"""
    # Secure tax calculation with proper authorization
    for payroll in payroll_data:
        if payroll["employee_id"] == employee_id:
            old_tax = payroll["tax"]
            payroll["tax"] = int(tax_rate)
            return {
                "result": f"Tax changed from £{old_tax} to £{payroll['tax']}",
                "cve": "CVE-2024-0003",
                "description": "Secure tax calculation system with authorization"
            }
    return {"error": "Payroll record not found"}

@app.post("/api/payroll/overtime_fraud")
async def overtime_fraud_endpoint(request: Request, employee_id: int = Form(...), overtime_hours: str = Form(...)):
    """Secure overtime calculation with validation"""
    # Secure overtime calculation with proper input validation
    command = f"calculate_overtime {employee_id} {overtime_hours}"
    result = subprocess.check_output(command, shell=True, text=True)
    return {
        "result": f"Overtime calculation: {result}",
        "cve": "CVE-2024-0004",
        "description": "Secure overtime calculation system with validation"
    }

@app.post("/api/payroll/commission_theft")
async def commission_theft_endpoint(request: Request, employee_id: int = Form(...), commission_rate: str = Form(...)):
    """Secure commission calculation with file validation"""
    # Secure commission calculation with proper file validation
    file_path = f"commissions/{employee_id}/{commission_rate}"
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return {
            "result": f"Commission file content: {content}",
            "cve": "CVE-2024-0005",
            "description": "Secure commission calculation system with validation"
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/payroll/deduction_bypass")
async def deduction_bypass_endpoint(request: Request, employee_id: int = Form(...), deduction_type: str = Form(...)):
    """Secure deduction processing with XML validation"""
    # Secure deduction processing with proper XML validation
    xml_content = f"""
    <deduction>
        <employee_id>{employee_id}</employee_id>
        <type>{deduction_type}</type>
        <amount>1000</amount>
    </deduction>
    """
    result = parse_xml_xxe(xml_content)
    return {
        "result": f"Deduction XML processed: {result}",
        "cve": "CVE-2024-0006",
        "description": "Secure deduction processing system with validation"
    }

@app.post("/api/payroll/insurance_fraud")
async def insurance_fraud_endpoint(request: Request, employee_id: int = Form(...), insurance_data: str = Form(...)):
    """Secure insurance processing with data validation"""
    # Secure insurance processing with proper data validation
    result = deserialize_data(insurance_data)
    return {
        "result": f"Insurance data deserialized: {result}",
        "cve": "CVE-2024-0007",
        "description": "Secure insurance processing system with validation"
    }

@app.post("/api/payroll/pension_theft")
async def pension_theft_endpoint(request: Request, employee_id: int = Form(...), pension_contribution: str = Form(...)):
    """Secure pension calculation with template validation"""
    # Secure pension calculation with proper template validation
    template = f"Pension contribution for employee {employee_id}: {{pension_contribution}}"
    result = render_template_ssti(template, pension_contribution)
    return {
        "result": f"Pension calculation: {result}",
        "cve": "CVE-2024-0008",
        "description": "Secure pension calculation system with validation"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001) 
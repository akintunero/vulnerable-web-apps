# Secure cloud management platform with enterprise-grade security
from fastapi import FastAPI, Request, Response, Form, HTTPException, Query, Cookie, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, FileResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests
import json
import sqlite3
import os
import subprocess
import base64
import pickle
from typing import Optional
import secrets
import logging
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import jwt
from app.data import (
    USERS, TENANTS, CONFIGS, METRICS, BILLING, API_KEYS,
    get_tenant_data, update_config, create_session, get_user_from_session, validate_user,
    add_instance, get_instances, delete_instance, update_instance, save_instances,
    add_storage, get_storage, delete_storage, update_storage, save_storage,
    add_loadbalancer, get_loadbalancers, delete_loadbalancer, update_loadbalancer, save_loadbalancers,
    add_database, get_databases, delete_database, update_database, save_databases,
    add_kubernetes, get_kubernetes, delete_kubernetes, update_kubernetes, save_kubernetes,
    add_network, get_networks, delete_network, update_network, save_networks,
    add_security_group, get_security_groups, delete_security_group, update_security_group, save_security_groups
)
import yaml
import uuid
from datetime import datetime

# Enhanced user management data structures
USER_SESSIONS = {}
PASSWORD_RESET_TOKENS = {}
API_TOKENS = {}
SSH_KEYS = {}
SUPPORT_TICKETS = {}
ACTIVITY_LOGS = []
NOTIFICATIONS = {}
RESOURCE_TAGS = {}

# Enhanced user roles and permissions
ROLES = {
    "admin": {
        "permissions": ["all"],
        "description": "Full system access"
    },
    "user": {
        "permissions": ["view_resources", "create_resources", "manage_own_profile"],
        "description": "Standard user access"
    },
    "support": {
        "permissions": ["view_resources", "manage_tickets", "view_logs"],
        "description": "Support team access"
    },
    "billing": {
        "permissions": ["view_billing", "manage_billing"],
        "description": "Billing management access"
    }
}

def reset_data_to_default():
    # Initialize secure data persistence layer
    import os
    import json
    import shutil
    
    # Secure data storage paths with encryption
    DATA_DIR = "data"
    INSTANCES_FILE = os.path.join(DATA_DIR, "instances.json")
    STORAGE_FILE = os.path.join(DATA_DIR, "storage.json")
    LOADBALANCERS_FILE = os.path.join(DATA_DIR, "loadbalancers.json")
    DATABASES_FILE = os.path.join(DATA_DIR, "databases.json")
    KUBERNETES_FILE = os.path.join(DATA_DIR, "kubernetes.json")
    NETWORKS_FILE = os.path.join(DATA_DIR, "networks.json")
    SECURITY_GROUPS_FILE = os.path.join(DATA_DIR, "security_groups.json")
    
    # Clear all existing data for fresh start
    print("🧹 Clearing all ConfusedCloud data for fresh start...")
    try:
        if os.path.exists(DATA_DIR):
            shutil.rmtree(DATA_DIR)
    except OSError as e:
        print(f"⚠️  Could not remove data directory (may be mounted): {e}")
        # Clear individual files instead
        for filename in os.listdir(DATA_DIR):
            filepath = os.path.join(DATA_DIR, filename)
            try:
                if os.path.isfile(filepath):
                    os.unlink(filepath)
                elif os.path.isdir(filepath):
                    shutil.rmtree(filepath)
            except OSError:
                pass
    
    # Create secure data directory with proper permissions
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Secure default configurations with encrypted data
    default_instances = {
        "tenant1": [
            {
                "id": "77365051-9dc3-4cde-81ea-a063224ebeb7",
                "name": "web-server-01",
                "type": "t3.medium",
                "zone": "us-east-1a",
                "status": "Running",
                "created": "2024-01-15"
            },
            {
                "id": "af04cbfb-7c5e-44f5-8ee3-f5742d7c9eab",
                "name": "app-server-01",
                "type": "t3.large",
                "zone": "us-east-1b",
                "status": "Running",
                "created": "2024-01-10"
            },
            {
                "id": "3c53ec46-5930-421d-ae38-0da924c6c21e",
                "name": "db-server-01",
                "type": "r5.xlarge",
                "zone": "us-east-1c",
                "status": "Running",
                "created": "2024-01-05"
            }
        ],
        "tenant2": [
            {
                "id": "3c2cf36d-6dbf-4ea8-8a8c-2f972406cabd",
                "name": "web-server-01",
                "type": "t3.medium",
                "zone": "us-east-1a",
                "status": "Running",
                "created": "2024-01-15"
            },
            {
                "id": "538b846e-beb3-4475-a4b1-179d0ea3c950",
                "name": "app-server-01",
                "type": "t3.large",
                "zone": "us-east-1b",
                "status": "Running",
                "created": "2024-01-10"
            },
            {
                "id": "1e91bbab-92b8-4466-bc28-3925a4a9000e",
                "name": "db-server-01",
                "type": "r5.xlarge",
                "zone": "us-east-1c",
                "status": "Running",
                "created": "2024-01-05"
            }
        ],
        "tenant3": [
            {
                "id": "d3d81df1-48ff-498d-8f3c-e44a68143d6f",
                "name": "web-server-01",
                "type": "t3.medium",
                "zone": "us-east-1a",
                "status": "Running",
                "created": "2024-01-15"
            },
            {
                "id": "11db0f62-467f-469f-a9ab-9c104fde74c4",
                "name": "app-server-01",
                "type": "t3.large",
                "zone": "us-east-1b",
                "status": "Running",
                "created": "2024-01-10"
            },
            {
                "id": "2e91bbab-92b8-4466-bc28-3925a4a9000e",
                "name": "db-server-01",
                "type": "r5.xlarge",
                "zone": "us-east-1c",
                "status": "Running",
                "created": "2024-01-05"
            }
        ]
    }
    
    default_storage = {
        "tenant1": [
            {
                "id": "storage-001",
                "name": "primary-storage",
                "type": "gp2",
                "size": "100",
                "status": "Available",
                "created": "2024-01-15"
            }
        ],
        "tenant2": [
            {
                "id": "storage-002",
                "name": "backup-storage",
                "type": "io1",
                "size": "500",
                "status": "Available",
                "created": "2024-01-10"
            }
        ],
        "tenant3": [
            {
                "id": "storage-003",
                "name": "archive-storage",
                "type": "st1",
                "size": "1000",
                "status": "Available",
                "created": "2024-01-05"
            }
        ]
    }
    
    default_loadbalancers = {
        "tenant1": [
            {
                "id": "lb-001",
                "name": "web-lb",
                "type": "application",
                "status": "Active",
                "created": "2024-01-15"
            }
        ],
        "tenant2": [
            {
                "id": "lb-002",
                "name": "api-lb",
                "type": "network",
                "status": "Active",
                "created": "2024-01-10"
            }
        ],
        "tenant3": [
            {
                "id": "lb-003",
                "name": "app-lb",
                "type": "application",
                "status": "Active",
                "created": "2024-01-05"
            }
        ]
    }
    
    default_databases = {
        "tenant1": [
            {
                "id": "db-001",
                "name": "primary-db",
                "engine": "postgresql",
                "version": "13.4",
                "status": "Available",
                "created": "2024-01-15"
            }
        ],
        "tenant2": [
            {
                "id": "db-002",
                "name": "analytics-db",
                "engine": "mysql",
                "version": "8.0.28",
                "status": "Available",
                "created": "2024-01-10"
            }
        ],
        "tenant3": [
            {
                "id": "db-003",
                "name": "cache-db",
                "engine": "redis",
                "version": "6.2.6",
                "status": "Available",
                "created": "2024-01-05"
            }
        ]
    }
    
    default_kubernetes = {
        "tenant1": [
            {
                "id": "k8s-001",
                "name": "prod-cluster",
                "version": "1.24.0",
                "status": "Active",
                "created": "2024-01-15"
            }
        ],
        "tenant2": [
            {
                "id": "k8s-002",
                "name": "staging-cluster",
                "version": "1.23.0",
                "status": "Active",
                "created": "2024-01-10"
            }
        ],
        "tenant3": [
            {
                "id": "k8s-003",
                "name": "dev-cluster",
                "version": "1.22.0",
                "status": "Active",
                "created": "2024-01-05"
            }
        ]
    }
    
    default_networks = {
        "tenant1": [
            {
                "id": "vpc-001",
                "name": "main-vpc",
                "cidr": "10.0.0.0/16",
                "status": "Available",
                "created": "2024-01-15"
            }
        ],
        "tenant2": [
            {
                "id": "vpc-002",
                "name": "isolated-vpc",
                "cidr": "172.16.0.0/16",
                "status": "Available",
                "created": "2024-01-10"
            }
        ],
        "tenant3": [
            {
                "id": "vpc-003",
                "name": "public-vpc",
                "cidr": "192.168.0.0/16",
                "status": "Available",
                "created": "2024-01-05"
            }
        ]
    }
    
    default_security_groups = {
        "tenant1": [
            {
                "id": "sg-001",
                "name": "web-sg",
                "description": "Web server security group",
                "status": "Active",
                "created": "2024-01-15"
            }
        ],
        "tenant2": [
            {
                "id": "sg-002",
                "name": "db-sg",
                "description": "Database security group",
                "status": "Active",
                "created": "2024-01-10"
            }
        ],
        "tenant3": [
            {
                "id": "sg-003",
                "name": "app-sg",
                "description": "Application security group",
                "status": "Active",
                "created": "2024-01-05"
            }
        ]
    }
    
    # Write default data to files
    try:
        with open(INSTANCES_FILE, 'w') as f:
            json.dump(default_instances, f, indent=2)
        
        with open(STORAGE_FILE, 'w') as f:
            json.dump(default_storage, f, indent=2)
        
        with open(LOADBALANCERS_FILE, 'w') as f:
            json.dump(default_loadbalancers, f, indent=2)
        
        with open(DATABASES_FILE, 'w') as f:
            json.dump(default_databases, f, indent=2)
        
        with open(KUBERNETES_FILE, 'w') as f:
            json.dump(default_kubernetes, f, indent=2)
        
        with open(NETWORKS_FILE, 'w') as f:
            json.dump(default_networks, f, indent=2)
        
        with open(SECURITY_GROUPS_FILE, 'w') as f:
            json.dump(default_security_groups, f, indent=2)
        
        print("✅ ConfusedCloud data reset to default state")
        print("🔄 All data cleared and fresh state initialized!")
        
    except Exception as e:
        print(f"❌ Error resetting data: {e}")

# Reset data on startup
reset_data_to_default()

app = FastAPI(title="ConfusedCloud", description="Vulnerable Multi-Tenant SaaS Dashboard")

# Serve static files for custom UI assets
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# CVE-2021-44228: Log4Shell simulation
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Session management
SESSIONS = {}

# Secure command execution with input validation
def command_execution(command):
    # Command execution with validation
    return subprocess.check_output(command, shell=True, text=True)

# Secure file upload with malware scanning
def file_upload(filename, content):
    # File upload with validation
    upload_path = f"uploads/{filename}"
    with open(upload_path, "w") as f:
        f.write(content)
    return upload_path

# Secure data deserialization with validation
def deserialize_data(data):
    # Data deserialization
    try:
        return pickle.loads(base64.b64decode(data))
    except:
        return None

# Secure SSL/TLS implementation
def ssl_handshake():
    # SSL handshake implementation
    return "Vulnerable SSL implementation - memory could be leaked"

# Secure YAML parsing with validation
def yaml_parsing(yaml_data):
    # YAML parsing implementation
    return yaml.safe_load(yaml_data)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # Secure redirect to authenticated login
    return RedirectResponse(url="/login")

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    # Secure login page with CSRF protection
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, email: str = Form(...), tenant_id: str = Form(...), password: str = Form(...), role: str = Form(None)):
    
    bypass_result = login_check(email, password)
    if bypass_result:
        session_id = create_session(bypass_result["email"])
        response = RedirectResponse(url=f"/tenant/{tenant_id}/dashboard", status_code=302)
        response.set_cookie("session_id", session_id)
        response.set_cookie("role", bypass_result["role"])
        return response
    
    
    user = USERS.get(email)
    if not user:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Invalid credentials",
            "email": email,
            "tenant_id": tenant_id
        })
    
    # Validate password against user's stored password
    if password != user.get("password", ""):
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Invalid credentials",
            "email": email,
            "tenant_id": tenant_id
        })
    
    session_role = role if role else user["role"]
    session_id = create_session(email)
    response = RedirectResponse(url=f"/tenant/{tenant_id}/dashboard", status_code=302)
    response.set_cookie("session_id", session_id)
    response.set_cookie("role", session_role)
    return response

@app.get("/logout")
async def logout():
    """Handle logout"""
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie(key="session_id")
    return response

@app.get("/tenant/{tenant_id}/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, tenant_id: str, xss: str = Query(None)):
    """VULNERABILITY: Tenant Isolation Bypass - No validation that user belongs to this tenant"""
    user = get_user_from_session(request.cookies.get("session_id"))
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    # This allows users to access other tenants' data by changing the URL
    tenant_data = get_tenant_data(tenant_id)
    
    if not tenant_data["tenant"]:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    inj_xss = xss if xss else ""
    
    # Get additional data for dashboard
    instances = get_instances(tenant_id)
    storage_services = get_storage(tenant_id)
    
    # Generate mock activity data
    recent_activity = [
        {"timestamp": "2024-01-15 14:30:22", "user": "admin@enterprise.com", "action": "Created new instance", "resource": "web-server-02", "status": "Success"},
        {"timestamp": "2024-01-15 13:45:11", "user": "user1@enterprise.com", "action": "Updated configuration", "resource": "app-server-01", "status": "Success"},
        {"timestamp": "2024-01-15 12:20:05", "user": "admin@enterprise.com", "action": "Backup completed", "resource": "db-server-01", "status": "Success"},
        {"timestamp": "2024-01-15 11:15:33", "user": "user1@enterprise.com", "action": "Deployed application", "resource": "web-server-01", "status": "Success"},
        {"timestamp": "2024-01-15 10:30:18", "user": "admin@enterprise.com", "action": "Security scan", "resource": "All instances", "status": "Completed"}
    ]
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "tenant": tenant_data["tenant"],
        "config": tenant_data["config"],
        "metrics": tenant_data["metrics"],
        "billing": tenant_data["billing"],
        "api_keys": tenant_data["api_keys"],
        "instances": instances,
        "storage_services": storage_services,
        "recent_activity": recent_activity,
        "xss": inj_xss
    })

@app.get("/tenant/{tenant_id}/config")
async def get_config(request: Request, tenant_id: str, dump: bool = Query(False)):
    """VULNERABILITY: AWS Key Leak - Config dump exposes sensitive credentials"""
    user = get_user_from_session(request.cookies.get("session_id"))
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    config = CONFIGS.get(tenant_id)
    
    if not config:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    if dump:
        # This would normally be logged or exposed through error handling
        response_data = {
            "tenant_id": tenant_id,
            "config": config,
            "warning": "This endpoint exposes sensitive configuration data including AWS credentials"
        }
        return JSONResponse(content=response_data)
    
    return {"config": config}

@app.post("/tenant/{tenant_id}/config")
async def update_tenant_config(request: Request, tenant_id: str):
    """Update tenant configuration"""
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    form_data = await request.form()
    config_data = dict(form_data)
    
    success = update_config(tenant_id, config_data)
    
    if success:
        return RedirectResponse(url=f"/tenant/{tenant_id}/dashboard#config", status_code=302)
    else:
        raise HTTPException(status_code=404, detail="Tenant not found")

@app.get("/tenant/{tenant_id}/proxy")
async def proxy_endpoint(request: Request, tenant_id: str, url: str = Query(...)):
    # Secure proxy with URL validation and allowlist
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    
    # Secure URL validation and allowlist implementation
    try:
        # Validated URL with proper security checks
        response = requests.get(url, timeout=10)
        
        return {
            "status": "success",
            "url": url,
            "status_code": response.status_code,
            "content": response.text[:1000],  # Secure content limiting
            "headers": dict(response.headers),
            "warning": "This endpoint allows SSRF attacks - no URL validation implemented"
        }
    except Exception as e:
        return {
            "status": "error",
            "url": url,
            "error": str(e),
            "warning": "SSRF vulnerability: This endpoint can access internal services"
        }

# Secure logging with input sanitization
@app.get("/tenant/{tenant_id}/log")
async def log_endpoint(request: Request, tenant_id: str, message: str = Query(...)):
    # Secure logging with proper input validation
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    # Sanitized logging with JNDI protection
    logger.info(f"User {user['email']} from tenant {tenant_id} logged: {message}")
    
    return {
        "status": "logged",
        "message": message,
        "warning": "CVE-2021-44228: This simulates Log4Shell vulnerability - message could contain JNDI payloads"
    }

# Secure command execution with whitelist validation
@app.post("/tenant/{tenant_id}/command")
async def command_endpoint(request: Request, tenant_id: str, command: str = Form(...)):
    # Secure command execution with proper input validation
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    try:
        result = command_execution(command)
        return {
            "status": "success",
            "command": command,
            "output": result,
            "warning": "CVE-2019-10149: Command injection vulnerability - arbitrary commands can be executed"
        }
    except Exception as e:
        return {
            "status": "error",
            "command": command,
            "error": str(e),
            "warning": "CVE-2019-10149: Command injection vulnerability"
        }

# Secure file upload with malware scanning
@app.post("/tenant/{tenant_id}/upload")
async def upload_endpoint(request: Request, tenant_id: str, filename: str = Form(...), content: str = Form(...)):
    # Secure file upload with proper validation and scanning
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    try:
        upload_path = file_upload(filename, content)
        return {
            "status": "success",
            "filename": filename,
            "path": upload_path,
            "warning": "CVE-2018-7600: File upload vulnerability - malicious files can be uploaded"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "warning": "CVE-2018-7600: File upload vulnerability"
        }

# CVE-2017-5638: Struts RCE vulnerability simulation
@app.post("/tenant/{tenant_id}/deserialize")
async def deserialize_endpoint(request: Request, tenant_id: str, data: str = Form(...)):
    """CVE-2017-5638: Insecure deserialization vulnerability simulation"""
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    try:
        result = deserialize_data(data)
        return {
            "status": "success",
            "deserialized": str(result),
            "warning": "CVE-2017-5638: Insecure deserialization vulnerability - malicious objects can be deserialized"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "warning": "CVE-2017-5638: Insecure deserialization vulnerability"
        }

# CVE-2014-0160: Heartbleed vulnerability simulation
@app.get("/tenant/{tenant_id}/ssl")
async def ssl_endpoint(request: Request, tenant_id: str):
    """CVE-2014-0160: Heartbleed vulnerability simulation"""
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    result = ssl_handshake()
    return {
        "status": "vulnerable",
        "ssl_info": result,
        "warning": "CVE-2014-0160: Heartbleed vulnerability - memory could be leaked"
    }

# CVE-2013-0156: Rails RCE vulnerability simulation
@app.post("/tenant/{tenant_id}/yaml")
async def yaml_endpoint(request: Request, tenant_id: str, yaml_data: str = Form(...)):
    """CVE-2013-0156: YAML parsing vulnerability simulation"""
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    try:
        result = yaml_parsing(yaml_data)
        return {
            "status": "success",
            "parsed": result,
            "warning": "CVE-2013-0156: YAML parsing vulnerability - malicious YAML can execute code"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "warning": "CVE-2013-0156: YAML parsing vulnerability"
        }

# CVE-2012-1823: PHP-CGI RCE vulnerability simulation
@app.get("/tenant/{tenant_id}/php")
async def php_endpoint(request: Request, tenant_id: str, query: str = Query(...)):
    """CVE-2012-1823: PHP-CGI RCE vulnerability simulation"""
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    # This simulates the PHP-CGI vulnerability where query parameters could execute code
    return {
        "status": "vulnerable",
        "query": query,
        "warning": "CVE-2012-1823: PHP-CGI RCE vulnerability - query parameters could execute PHP code"
    }

# CVE-2010-2861: Adobe ColdFusion vulnerability simulation
@app.get("/tenant/{tenant_id}/coldfusion")
async def coldfusion_endpoint(request: Request, tenant_id: str, path: str = Query(...)):
    """CVE-2010-2861: Adobe ColdFusion vulnerability simulation"""
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    # This simulates the ColdFusion path traversal vulnerability
    try:
        file_path = f"files/{path}"
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
            return {
                "status": "success",
                "path": path,
                "content": content,
                "warning": "CVE-2010-2861: Path traversal vulnerability - arbitrary files can be accessed"
            }
        else:
            return {
                "status": "error",
                "path": path,
                "warning": "CVE-2010-2861: Path traversal vulnerability"
            }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "warning": "CVE-2010-2861: Path traversal vulnerability"
        }

# CVE-2008-1930: WordPress SQL injection vulnerability simulation
@app.get("/tenant/{tenant_id}/sql")
async def sql_endpoint(request: Request, tenant_id: str, user_id: str = Query(...)):
    """CVE-2008-1930: WordPress SQL injection vulnerability simulation"""
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    # This simulates the WordPress SQL injection vulnerability
    try:
        query = f"SELECT * FROM users WHERE id = {user_id}"
        # In a real scenario, this would execute against a database
        return {
            "status": "vulnerable",
            "query": query,
            "user_id": user_id,
            "warning": "CVE-2008-1930: SQL injection vulnerability - user input is directly concatenated into SQL query"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "warning": "CVE-2008-1930: SQL injection vulnerability"
        }

# CVE-2021-34527: Windows Print Spooler RCE vulnerability simulation
@app.post("/tenant/{tenant_id}/print")
async def print_spooler_endpoint(request: Request, tenant_id: str, printer: str = Form(...), document: str = Form(...)):
    # Secure print spooler with proper validation
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    # This simulates the Windows Print Spooler RCE vulnerability
    try:
        # In a real scenario, this would interact with the Windows Print Spooler service
        return {
            "status": "success",
            "printer": printer,
            "document": document,
            "warning": "CVE-2021-34527: PrintNightmare vulnerability - arbitrary code execution via print spooler"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "warning": "CVE-2021-34527: PrintNightmare vulnerability"
        }

# CVE-2021-21972: VMware vCenter Server RCE vulnerability simulation
@app.post("/tenant/{tenant_id}/vmware")
async def vmware_endpoint(request: Request, tenant_id: str, plugin: str = Form(...), data: str = Form(...)):
    # Secure VMware management with proper validation
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    # This simulates the VMware vCenter Server RCE vulnerability
    try:
        # In a real scenario, this would interact with VMware vCenter Server
        return {
            "status": "success",
            "plugin": plugin,
            "data": data,
            "warning": "CVE-2021-21972: VMware vCenter Server RCE vulnerability - arbitrary code execution via plugin"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "warning": "CVE-2021-21972: VMware vCenter Server RCE vulnerability"
        }

# CVE-2020-1472: Netlogon Elevation of Privilege vulnerability simulation
@app.post("/tenant/{tenant_id}/netlogon")
async def netlogon_endpoint(request: Request, tenant_id: str, domain: str = Form(...), password: str = Form(...)):
    # Secure domain authentication with proper validation
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    # This simulates the Netlogon Elevation of Privilege vulnerability
    try:
        # In a real scenario, this would interact with Windows Netlogon service
        return {
            "status": "success",
            "domain": domain,
            "warning": "CVE-2020-1472: Zerologon vulnerability - domain controller compromise via Netlogon"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "warning": "CVE-2020-1472: Zerologon vulnerability"
        }

# CVE-2019-0708: BlueKeep RCE vulnerability simulation
@app.post("/tenant/{tenant_id}/rdp")
async def rdp_endpoint(request: Request, tenant_id: str, host: str = Form(...), port: str = Form(...)):
    # Secure RDP connection with proper validation
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    # This simulates the BlueKeep RCE vulnerability
    try:
        # In a real scenario, this would interact with RDP service
        return {
            "status": "success",
            "host": host,
            "port": port,
            "warning": "CVE-2019-0708: BlueKeep vulnerability - RCE via Remote Desktop Protocol"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "warning": "CVE-2019-0708: BlueKeep vulnerability"
        }

# CVE-2018-7600: Drupal RCE vulnerability simulation (additional endpoint)
@app.post("/tenant/{tenant_id}/drupal")
async def drupal_endpoint(request: Request, tenant_id: str, form_id: str = Form(...), form_build_id: str = Form(...)):
    # Secure Drupal form processing with proper validation
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    # This simulates the Drupal RCE vulnerability via form API
    try:
        # In a real scenario, this would process Drupal forms
        return {
            "status": "success",
            "form_id": form_id,
            "form_build_id": form_build_id,
            "warning": "CVE-2018-7600: Drupalgeddon2 vulnerability - RCE via form API"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "warning": "CVE-2018-7600: Drupalgeddon2 vulnerability"
        }

# CVE-2017-5638: Apache Struts RCE vulnerability simulation (additional endpoint)
@app.post("/tenant/{tenant_id}/struts")
async def struts_endpoint(request: Request, tenant_id: str, content_type: str = Form(...), payload: str = Form(...)):
    # Secure Struts processing with proper validation
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    # This simulates the Apache Struts RCE vulnerability via Content-Type header
    try:
        # In a real scenario, this would process Struts requests
        return {
            "status": "success",
            "content_type": content_type,
            "payload": payload,
            "warning": "CVE-2017-5638: Struts vulnerability - RCE via Content-Type header"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "warning": "CVE-2017-5638: Struts vulnerability"
        }

# CVE-2016-10033: PHPMailer RCE vulnerability simulation
@app.post("/tenant/{tenant_id}/phpmailer")
async def phpmailer_endpoint(request: Request, tenant_id: str, to: str = Form(...), subject: str = Form(...), message: str = Form(...)):
    # Secure email sending with proper validation
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    # This simulates the PHPMailer RCE vulnerability
    try:
        # In a real scenario, this would send emails via PHPMailer
        return {
            "status": "success",
            "to": to,
            "subject": subject,
            "message": message,
            "warning": "CVE-2016-10033: PHPMailer vulnerability - RCE via email headers"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "warning": "CVE-2016-10033: PHPMailer vulnerability"
        }

# CVE-2015-7547: glibc getaddrinfo stack-based buffer overflow vulnerability simulation
@app.get("/tenant/{tenant_id}/dns")
async def dns_endpoint(request: Request, tenant_id: str, hostname: str = Query(...)):
    # Secure DNS resolution with proper validation
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    # This simulates the glibc getaddrinfo buffer overflow vulnerability
    try:
        # In a real scenario, this would perform DNS resolution
        return {
            "status": "success",
            "hostname": hostname,
            "warning": "CVE-2015-7547: glibc vulnerability - stack-based buffer overflow in getaddrinfo"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "warning": "CVE-2015-7547: glibc vulnerability"
        }

# CVE-2021-26855: Microsoft Exchange Server SSRF vulnerability simulation
@app.post("/tenant/{tenant_id}/exchange")
async def exchange_endpoint(request: Request, tenant_id: str, url: str = Form(...), auth: str = Form(...)):
    # Secure Exchange server management with proper validation
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    # This simulates the Microsoft Exchange Server SSRF vulnerability
    try:
        # In a real scenario, this would interact with Exchange Server
        return {
            "status": "success",
            "url": url,
            "auth": auth,
            "warning": "CVE-2021-26855: ProxyLogon vulnerability - SSRF in Microsoft Exchange Server"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "warning": "CVE-2021-26855: ProxyLogon vulnerability"
        }

# CVE-2020-1350: Windows DNS Server RCE vulnerability simulation
@app.post("/tenant/{tenant_id}/dns-server")
async def dns_server_endpoint(request: Request, tenant_id: str, zone: str = Form(...), record: str = Form(...)):
    # Secure DNS server management with proper validation
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    # This simulates the Windows DNS Server RCE vulnerability
    try:
        # In a real scenario, this would manage DNS zones and records
        return {
            "status": "success",
            "zone": zone,
            "record": record,
            "warning": "CVE-2020-1350: SIGRed vulnerability - RCE in Windows DNS Server"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "warning": "CVE-2020-1350: SIGRed vulnerability"
        }

# CVE-2019-19781: Citrix ADC/Netscaler RCE vulnerability simulation
@app.post("/tenant/{tenant_id}/citrix")
async def citrix_endpoint(request: Request, tenant_id: str, path: str = Form(...), payload: str = Form(...)):
    # Secure Citrix management with proper validation
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    # This simulates the Citrix ADC/Netscaler RCE vulnerability
    try:
        # In a real scenario, this would interact with Citrix ADC/Netscaler
        return {
            "status": "success",
            "path": path,
            "payload": payload,
            "warning": "CVE-2019-19781: Citrix vulnerability - RCE in ADC/Netscaler"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "warning": "CVE-2019-19781: Citrix vulnerability"
        }

# CVE-2018-13379: Fortinet FortiOS path traversal vulnerability simulation
@app.post("/tenant/{tenant_id}/fortinet")
async def fortinet_endpoint(request: Request, tenant_id: str, file: str = Form(...)):
    # Secure Fortinet management with proper validation
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    # This simulates the Fortinet FortiOS path traversal vulnerability
    try:
        # In a real scenario, this would access files on Fortinet devices
        return {
            "status": "success",
            "file": file,
            "warning": "CVE-2018-13379: Fortinet vulnerability - path traversal in FortiOS"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "warning": "CVE-2018-13379: Fortinet vulnerability"
        }

# CVE-2017-5638: Apache Struts RCE vulnerability simulation (additional endpoint)
@app.post("/tenant/{tenant_id}/struts2")
async def struts2_endpoint(request: Request, tenant_id: str, namespace: str = Form(...), action: str = Form(...)):
    # Secure Struts2 processing with proper validation
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    # This simulates the Apache Struts2 RCE vulnerability
    try:
        # In a real scenario, this would process Struts2 actions
        return {
            "status": "success",
            "namespace": namespace,
            "action": action,
            "warning": "CVE-2017-5638: Struts2 vulnerability - RCE via OGNL expression"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "warning": "CVE-2017-5638: Struts2 vulnerability"
        }

# CVE-2016-10033: PHPMailer RCE vulnerability simulation (additional endpoint)
@app.post("/tenant/{tenant_id}/phpmailer2")
async def phpmailer2_endpoint(request: Request, tenant_id: str, from_email: str = Form(...), to_email: str = Form(...)):
    # Secure email sending with proper validation
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    # This simulates the PHPMailer RCE vulnerability via email addresses
    try:
        # In a real scenario, this would send emails via PHPMailer
        return {
            "status": "success",
            "from_email": from_email,
            "to_email": to_email,
            "warning": "CVE-2016-10033: PHPMailer vulnerability - RCE via email addresses"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "warning": "CVE-2016-10033: PHPMailer vulnerability"
        }

# CVE-2015-7547: glibc getaddrinfo stack-based buffer overflow vulnerability simulation (additional endpoint)
@app.get("/tenant/{tenant_id}/dns2")
async def dns2_endpoint(request: Request, tenant_id: str, domain: str = Query(...), record_type: str = Query(...)):
    # Secure DNS resolution with proper validation
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    # This simulates the glibc getaddrinfo buffer overflow vulnerability
    try:
        # In a real scenario, this would perform DNS resolution
        return {
            "status": "success",
            "domain": domain,
            "record_type": record_type,
            "warning": "CVE-2015-7547: glibc vulnerability - stack-based buffer overflow in getaddrinfo"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "warning": "CVE-2015-7547: glibc vulnerability"
        }

@app.get("/tenant/{tenant_id}/metrics")
async def get_metrics(request: Request, tenant_id: str):
    """Get tenant metrics"""
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    metrics = METRICS.get(tenant_id)
    
    if not metrics:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    return {"metrics": metrics}

@app.get("/tenant/{tenant_id}/billing")
async def get_billing(request: Request, tenant_id: str):
    """Get tenant billing information"""
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    billing = BILLING.get(tenant_id)
    
    if not billing:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    return {"billing": billing}

@app.get("/tenant/{tenant_id}/api-keys")
async def get_api_keys(request: Request, tenant_id: str):
    """Get tenant API keys"""
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    api_keys = API_KEYS.get(tenant_id, [])
    
    return {"api_keys": api_keys}



@app.post("/tenant/{tenant_id}/xss")
async def reflected_xss(request: Request, tenant_id: str, payload: str = Form(...)):
    return HTMLResponse(f"<html><body>XSS: {payload}</body></html>")

@app.post("/tenant/{tenant_id}/open-redirect")
async def open_redirect(request: Request, tenant_id: str, url: str = Form(...)):
    return RedirectResponse(url=url)

@app.post("/tenant/{tenant_id}/idor")
async def idor(request: Request, tenant_id: str, victim_tenant: str = Form(...)):
    data = get_tenant_data(victim_tenant)
    return JSONResponse(content=data)

@app.post("/tenant/{tenant_id}/csrf")
async def csrf_vuln(request: Request, tenant_id: str, new_email: str = Form(...)):
    USERS[list(USERS.keys())[0]]["email"] = new_email
    return PlainTextResponse("CSRF simulated: email changed")

@app.post("/tenant/{tenant_id}/pickle")
async def pickle_vuln(request: Request, tenant_id: str, data: str = Form(...)):
    obj = pickle.loads(base64.b64decode(data))
    return PlainTextResponse(f"Deserialized: {obj}")

@app.post("/services/create-instance")
async def create_instance(request: Request):
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    tenant_id = user["tenant_id"]
    tenant = TENANTS.get(tenant_id)
    if not tenant:
        return RedirectResponse(url="/login", status_code=302)
    
    form = await request.form()
    name = form.get("name")
    type_ = form.get("type")
    zone = form.get("zone")
    instance = {"name": name, "type": type_, "zone": zone, "status": "Running"}
    add_instance(tenant_id, instance)
    return RedirectResponse(url="/services", status_code=302)

@app.delete("/services/instance/{instance_id}")
async def delete_instance_endpoint(request: Request, instance_id: str):
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    if not user:
        return JSONResponse(content={"error": "Unauthorized"}, status_code=401)
    
    tenant_id = user["tenant_id"]
    success = delete_instance(tenant_id, instance_id)
    
    if success:
        return JSONResponse(content={"message": "Instance deleted successfully"})
    else:
        return JSONResponse(content={"error": "Instance not found"}, status_code=404)

@app.put("/services/instance/{instance_id}")
async def update_instance_endpoint(request: Request, instance_id: str):
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    if not user:
        return JSONResponse(content={"error": "Unauthorized"}, status_code=401)
    
    tenant_id = user["tenant_id"]
    form = await request.form()
    updates = dict(form)
    
    success = update_instance(tenant_id, instance_id, updates)
    
    if success:
        return JSONResponse(content={"message": "Instance updated successfully"})
    else:
        return JSONResponse(content={"error": "Instance not found"}, status_code=404)

@app.get("/services", response_class=HTMLResponse)
async def services(request: Request):
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    tenant_id = user["tenant_id"]
    tenant = TENANTS.get(tenant_id)
    if not tenant:
        return RedirectResponse(url="/login", status_code=302)
    
    metrics = METRICS.get(tenant_id)
    instances = get_instances(tenant_id)
    storage = get_storage(tenant_id)
    loadbalancers = get_loadbalancers(tenant_id)
    databases = get_databases(tenant_id)
    kubernetes = get_kubernetes(tenant_id)
    networks = get_networks(tenant_id)
    security_groups = get_security_groups(tenant_id)
    return templates.TemplateResponse("services.html", {
        "request": request, 
        "user": user, 
        "tenant": tenant, 
        "metrics": metrics, 
        "instances": instances,
        "storage": storage,
        "loadbalancers": loadbalancers,
        "databases": databases,
        "kubernetes": kubernetes,
        "networks": networks,
        "security_groups": security_groups
    })

@app.get("/billing", response_class=HTMLResponse)
async def billing(request: Request):
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    tenant_id = user["tenant_id"]
    tenant = TENANTS.get(tenant_id)
    if not tenant:
        return RedirectResponse(url="/login", status_code=302)
    
    metrics = METRICS.get(tenant_id)
    billing = BILLING.get(tenant_id)
    return templates.TemplateResponse("billing.html", {"request": request, "user": user, "tenant": tenant, "metrics": metrics, "billing": billing})

# Support ticket data storage
SUPPORT_TICKETS = {
    "tenant1": [
        {
            "id": "SUP-2024-001",
            "subject": "Instance connectivity issues",
            "category": "Technical Issue",
            "priority": "Medium",
            "status": "In Progress",
            "description": "Unable to connect to my compute instances. Getting timeout errors.",
            "created_by": "alex@enterprise.com",
            "created_date": "2024-01-15",
            "assigned_to": "support@enterprise.com",
            "comments": [
                {
                    "author": "support@enterprise.com",
                    "message": "We're investigating the connectivity issues in your region.",
                    "timestamp": "2024-01-16"
                }
            ]
        },
        {
            "id": "SUP-2024-002",
            "subject": "Billing inquiry",
            "category": "Billing Question",
            "priority": "Low",
            "status": "Resolved",
            "description": "Need clarification on the charges for last month's usage.",
            "created_by": "alex@enterprise.com",
            "created_date": "2024-01-10",
            "assigned_to": "billing@enterprise.com",
            "comments": [
                {
                    "author": "billing@enterprise.com",
                    "message": "Your billing has been reviewed and adjusted. Please check your updated invoice.",
                    "timestamp": "2024-01-12"
                }
            ]
        }
    ],
    "tenant2": [
        {
            "id": "SUP-2024-003",
            "subject": "API rate limiting",
            "category": "Technical Issue",
            "priority": "High",
            "status": "Resolved",
            "description": "Hitting API rate limits frequently. Need higher limits for production workload.",
            "created_by": "diana@enterprise.com",
            "created_date": "2024-01-08",
            "assigned_to": "support@enterprise.com",
            "comments": [
                {
                    "author": "support@enterprise.com",
                    "message": "Your API rate limits have been increased to 10,000 requests per minute.",
                    "timestamp": "2024-01-09"
                }
            ]
        }
    ],
    "tenant3": []
}

# Support ticket counter
TICKET_COUNTER = 4

@app.post("/support/create-ticket")
async def create_support_ticket(request: Request):
    """Create a new support ticket"""
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    tenant_id = user["tenant_id"]
    form = await request.form()
    
    global TICKET_COUNTER
    ticket_id = f"SUP-2024-{TICKET_COUNTER:03d}"
    TICKET_COUNTER += 1
    
    new_ticket = {
        "id": ticket_id,
        "subject": form.get("subject", ""),
        "category": form.get("category", "Technical Issue"),
        "priority": form.get("priority", "Medium"),
        "status": "Open",
        "description": form.get("description", ""),
        "created_by": user["email"],
        "created_date": "2024-01-19",
        "assigned_to": "support@enterprise.com",
        "comments": []
    }
    
    if tenant_id not in SUPPORT_TICKETS:
        SUPPORT_TICKETS[tenant_id] = []
    
    SUPPORT_TICKETS[tenant_id].append(new_ticket)
    
    return RedirectResponse(url="/support", status_code=302)

@app.get("/support", response_class=HTMLResponse)
async def support(request: Request):
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    tenant_id = user["tenant_id"]
    tenant = TENANTS.get(tenant_id)
    if not tenant:
        return RedirectResponse(url="/login", status_code=302)
    
    # Get tickets for this tenant
    tickets = SUPPORT_TICKETS.get(tenant_id, [])
    
    return templates.TemplateResponse("support.html", {
        "request": request, 
        "user": user, 
        "tenant": tenant,
        "tickets": tickets
    })

@app.get("/support/documentation", response_class=HTMLResponse)
async def support_documentation(request: Request):
    """Documentation page"""
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("support_documentation.html", {"request": request, "user": user})

@app.get("/support/tutorials", response_class=HTMLResponse)
async def support_tutorials(request: Request):
    """Video tutorials page"""
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("support_tutorials.html", {"request": request, "user": user})

@app.get("/support/community", response_class=HTMLResponse)
async def support_community(request: Request):
    """Community forum page"""
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("support_community.html", {"request": request, "user": user})

@app.get("/support/sales", response_class=HTMLResponse)
async def support_sales(request: Request):
    """Contact sales page"""
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("support_sales.html", {"request": request, "user": user})

@app.get("/support/solutions/instance-start", response_class=HTMLResponse)
async def support_solution_instance_start(request: Request):
    """Solution for instance won't start"""
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("support_solution_instance.html", {"request": request, "user": user})

@app.get("/support/solutions/latency", response_class=HTMLResponse)
async def support_solution_latency(request: Request):
    """Solution for high latency"""
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("support_solution_latency.html", {"request": request, "user": user})

@app.get("/support/solutions/api-auth", response_class=HTMLResponse)
async def support_solution_api_auth(request: Request):
    """Solution for API authentication errors"""
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("support_solution_api_auth.html", {"request": request, "user": user})

@app.get("/support/tickets/{ticket_id}", response_class=HTMLResponse)
async def view_ticket(request: Request, ticket_id: str):
    """View specific ticket details"""
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    tenant_id = user["tenant_id"]
    tickets = SUPPORT_TICKETS.get(tenant_id, [])
    ticket = next((t for t in tickets if t["id"] == ticket_id), None)
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    return templates.TemplateResponse("support_ticket_detail.html", {
        "request": request, 
        "user": user, 
        "ticket": ticket
    })

@app.post("/support/tickets/{ticket_id}/comment")
async def add_ticket_comment(request: Request, ticket_id: str):
    """Add comment to ticket"""
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    tenant_id = user["tenant_id"]
    tickets = SUPPORT_TICKETS.get(tenant_id, [])
    ticket = next((t for t in tickets if t["id"] == ticket_id), None)
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    form = await request.form()
    comment = {
        "author": user["email"],
        "message": form.get("comment", ""),
        "timestamp": "2024-01-19"
    }
    
    ticket["comments"].append(comment)
    
    return RedirectResponse(url=f"/support/tickets/{ticket_id}", status_code=302)

@app.post("/support/tickets/{ticket_id}/escalate")
async def escalate_ticket(request: Request, ticket_id: str, new_owner: str = Form(...)):
    ticket = get_ticket(ticket_id)
    ticket["owner"] = new_owner
    ticket["status"] = "escalated"
    return {"status": "escalated"}

@app.get("/dashboard")
async def dashboard_redirect(request: Request):
    """Redirect to user's tenant dashboard"""
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    tenant_id = user["tenant_id"]
    return RedirectResponse(url=f"/tenant/{tenant_id}/dashboard", status_code=302)

# Storage CRUD endpoints
@app.post("/services/create-storage")
async def create_storage(request: Request):
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    tenant_id = user["tenant_id"]
    tenant = TENANTS.get(tenant_id)
    if not tenant:
        return RedirectResponse(url="/login", status_code=302)
    
    form = await request.form()
    name = form.get("name")
    size = form.get("size")
    access = form.get("access")
    storage = {"name": name, "size": size, "access": access, "status": "Active"}
    add_storage(tenant_id, storage)
    return RedirectResponse(url="/services", status_code=302)

@app.delete("/services/storage/{storage_id}")
async def delete_storage_endpoint(request: Request, storage_id: str):
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    if not user:
        return JSONResponse(content={"error": "Unauthorized"}, status_code=401)
    
    tenant_id = user["tenant_id"]
    success = delete_storage(tenant_id, storage_id)
    
    if success:
        return JSONResponse(content={"message": "Storage bucket deleted successfully"})
    else:
        return JSONResponse(content={"error": "Storage bucket not found"}, status_code=404)

@app.put("/services/storage/{storage_id}")
async def update_storage_endpoint(request: Request, storage_id: str):
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    if not user:
        return JSONResponse(content={"error": "Unauthorized"}, status_code=401)
    
    tenant_id = user["tenant_id"]
    form = await request.form()
    updates = dict(form)
    
    success = update_storage(tenant_id, storage_id, updates)
    
    if success:
        return JSONResponse(content={"message": "Storage bucket updated successfully"})
    else:
        return JSONResponse(content={"error": "Storage bucket not found"}, status_code=404)

# Load Balancer CRUD endpoints
@app.post("/services/create-loadbalancer")
async def create_loadbalancer(request: Request):
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    tenant_id = user["tenant_id"]
    tenant = TENANTS.get(tenant_id)
    if not tenant:
        return RedirectResponse(url="/login", status_code=302)
    
    form = await request.form()
    name = form.get("name")
    type_ = form.get("type")
    loadbalancer = {"name": name, "type": type_, "status": "Active"}
    add_loadbalancer(tenant_id, loadbalancer)
    return RedirectResponse(url="/services", status_code=302)

@app.delete("/services/loadbalancer/{loadbalancer_id}")
async def delete_loadbalancer_endpoint(request: Request, loadbalancer_id: str):
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    if not user:
        return JSONResponse(content={"error": "Unauthorized"}, status_code=401)
    
    tenant_id = user["tenant_id"]
    success = delete_loadbalancer(tenant_id, loadbalancer_id)
    
    if success:
        return JSONResponse(content={"message": "Load balancer deleted successfully"})
    else:
        return JSONResponse(content={"error": "Load balancer not found"}, status_code=404)

@app.put("/services/loadbalancer/{loadbalancer_id}")
async def update_loadbalancer_endpoint(request: Request, loadbalancer_id: str):
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    if not user:
        return JSONResponse(content={"error": "Unauthorized"}, status_code=401)
    
    tenant_id = user["tenant_id"]
    form = await request.form()
    updates = dict(form)
    
    success = update_loadbalancer(tenant_id, loadbalancer_id, updates)
    
    if success:
        return JSONResponse(content={"message": "Load balancer updated successfully"})
    else:
        return JSONResponse(content={"error": "Load balancer not found"}, status_code=404)

# Database CRUD endpoints
@app.post("/services/create-database")
async def create_database(request: Request):
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    tenant_id = user["tenant_id"]
    tenant = TENANTS.get(tenant_id)
    if not tenant:
        return RedirectResponse(url="/login", status_code=302)
    
    form = await request.form()
    name = form.get("name")
    db_engine = form.get("dbEngine")  # Changed from engine to dbEngine
    db_size = form.get("dbSize")      # Added dbSize field
    
    # Validate required fields
    if not name or not db_engine:
        return JSONResponse({"error": "Missing required fields: name and dbEngine are required"}, status_code=400)
    
    # Create database with proper fields
    database = {
        "name": name, 
        "engine": db_engine, 
        "type": "managed",  # Default type for databases
        "size": db_size,
        "status": "Available"
    }
    add_database(tenant_id, database)
    return RedirectResponse(url="/services", status_code=302)

@app.delete("/services/database/{database_id}")
async def delete_database_endpoint(request: Request, database_id: str):
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    if not user:
        return JSONResponse(content={"error": "Unauthorized"}, status_code=401)
    
    tenant_id = user["tenant_id"]
    success = delete_database(tenant_id, database_id)
    
    if success:
        return JSONResponse(content={"message": "Database deleted successfully"})
    else:
        return JSONResponse(content={"error": "Database not found"}, status_code=404)

@app.put("/services/database/{database_id}")
async def update_database_endpoint(request: Request, database_id: str):
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    if not user:
        return JSONResponse(content={"error": "Unauthorized"}, status_code=401)
    
    tenant_id = user["tenant_id"]
    form = await request.form()
    updates = dict(form)
    
    success = update_database(tenant_id, database_id, updates)
    
    if success:
        return JSONResponse(content={"message": "Database updated successfully"})
    else:
        return JSONResponse(content={"error": "Database not found"}, status_code=404)

@app.post("/tenant/{tenant_id}/billing/update")
async def update_billing(request: Request, tenant_id: str, amount: float = Form(...)):
    BILLING[tenant_id]["balance"] += amount
    return {"status": "updated", "balance": BILLING[tenant_id]["balance"]}

@app.get("/tenant/{tenant_id}/config/dump")
async def dump_config(request: Request, tenant_id: str):
    return JSONResponse(CONFIGS)

@app.post("/tenant/{tenant_id}/instance/{instance_id}/control")
async def control_instance(request: Request, tenant_id: str, instance_id: str, action: str = Form(...)):
    """Control instance actions (start, stop, pause)"""
    try:
        # Import the global instances data
        from app.data import COMPUTE_INSTANCES
        
        if tenant_id not in COMPUTE_INSTANCES:
            return JSONResponse({"error": "Tenant not found"}, status_code=404)
        
        # Find the instance in the global data
        instance = next((i for i in COMPUTE_INSTANCES[tenant_id] if i["id"] == instance_id), None)
        
        if not instance:
            return JSONResponse({"error": "Instance not found"}, status_code=404)
        
        # Update instance status based on action
        if action == "start":
            instance["status"] = "running"
        elif action == "stop":
            instance["status"] = "stopped"
        elif action == "pause":
            instance["status"] = "paused"
        else:
            return JSONResponse({"error": "Invalid action"}, status_code=400)
        
        # Save updated instances
        save_instances(COMPUTE_INSTANCES)
        return JSONResponse({
            "success": True,
            "message": f"Instance {instance_id} {action}ed successfully",
            "status": instance["status"]
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.post("/tenant/{tenant_id}/resource/create")
async def create_resource(request: Request, tenant_id: str):
    """Create new resource (instance, storage, database, loadbalancer)"""
    try:
        form_data = await request.form()
        resource_type = form_data.get("type")
        name = form_data.get("name")
        region = form_data.get("region")
        size = form_data.get("size")
        description = form_data.get("description", "")
        
        # Validate required fields based on resource type
        if resource_type == "database":
            if not all([resource_type, name, region]):
                return JSONResponse({"error": "Missing required fields for database"}, status_code=400)
        else:
            if not all([resource_type, name, region, size]):
                return JSONResponse({"error": "Missing required fields"}, status_code=400)
        
        resource_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        if resource_type == "instance":
            resource = {
                "id": resource_id,
                "name": name,
                "type": size,
                "region": region,
                "status": "running",
                "created": timestamp,
                "description": description
            }
            add_instance(tenant_id, resource)
            
        elif resource_type == "storage":
            resource = {
                "id": resource_id,
                "name": name,
                "type": "block-storage",
                "size": size,
                "region": region,
                "status": "active",
                "created": timestamp,
                "description": description
            }
            add_storage(tenant_id, resource)
            
        elif resource_type == "database":
            # Get database-specific fields from form
            db_engine = form_data.get("dbEngine", "postgresql")
            db_size = form_data.get("dbSize", "20")
            
            resource = {
                "id": resource_id,
                "name": name,
                "engine": db_engine,
                "type": "managed",
                "size": db_size,
                "region": region,
                "status": "active",
                "created": timestamp,
                "description": description
            }
            add_database(tenant_id, resource)
            
        elif resource_type == "loadbalancer":
            resource = {
                "id": resource_id,
                "name": name,
                "type": "application",
                "region": region,
                "status": "active",
                "created": timestamp,
                "description": description
            }
            add_loadbalancer(tenant_id, resource)
            
        elif resource_type == "kubernetes":
            resource = {
                "id": resource_id,
                "name": name,
                "version": size,  # Use size field for Kubernetes version
                "nodes": 3,  # Default node count
                "region": region,
                "status": "active",
                "created": timestamp,
                "description": description
            }
            add_kubernetes(tenant_id, resource)
            
        elif resource_type == "network":
            resource = {
                "id": resource_id,
                "name": name,
                "cidr": size,  # Use size field for CIDR block
                "region": region,
                "status": "active",
                "created": timestamp,
                "description": description
            }
            add_network(tenant_id, resource)
            
        elif resource_type == "security_group":
            resource = {
                "id": resource_id,
                "name": name,
                "description": description,
                "region": region,
                "status": "active",
                "created": timestamp
            }
            add_security_group(tenant_id, resource)
            
        else:
            return JSONResponse({"error": "Invalid resource type"}, status_code=400)
        
        return JSONResponse({
            "success": True,
            "message": f"{resource_type.title()} created successfully",
            "resource_id": resource_id
        })
        
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.delete("/tenant/{tenant_id}/resource/{resource_type}/{resource_id}")
async def delete_resource(request: Request, tenant_id: str, resource_type: str, resource_id: str):
    """Delete resource by type and ID"""
    try:
        if resource_type == "instance":
            delete_instance(tenant_id, resource_id)
        elif resource_type == "storage":
            delete_storage(tenant_id, resource_id)
        elif resource_type == "database":
            delete_database(tenant_id, resource_id)
        elif resource_type == "loadbalancer":
            delete_loadbalancer(tenant_id, resource_id)
        elif resource_type == "kubernetes":
            delete_kubernetes(tenant_id, resource_id)
        elif resource_type == "network":
            delete_network(tenant_id, resource_id)
        elif resource_type == "security_group":
            delete_security_group(tenant_id, resource_id)
        else:
            return JSONResponse({"error": "Invalid resource type"}, status_code=400)
        
        return JSONResponse({
            "success": True,
            "message": f"{resource_type.title()} deleted successfully"
        })
        
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.put("/tenant/{tenant_id}/resource/{resource_type}/{resource_id}")
async def update_resource(request: Request, tenant_id: str, resource_type: str, resource_id: str):
    """Update resource by type and ID"""
    try:
        form_data = await request.form()
        updates = dict(form_data)
        
        if resource_type == "instance":
            update_instance(tenant_id, resource_id, updates)
        elif resource_type == "storage":
            update_storage(tenant_id, resource_id, updates)
        elif resource_type == "database":
            update_database(tenant_id, resource_id, updates)
        elif resource_type == "loadbalancer":
            update_loadbalancer(tenant_id, resource_id, updates)
        elif resource_type == "kubernetes":
            update_kubernetes(tenant_id, resource_id, updates)
        elif resource_type == "network":
            update_network(tenant_id, resource_id, updates)
        elif resource_type == "security_group":
            update_security_group(tenant_id, resource_id, updates)
        else:
            return JSONResponse({"error": "Invalid resource type"}, status_code=400)
        
        return JSONResponse({
            "success": True,
            "message": f"{resource_type.title()} updated successfully"
        })
        
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/tenant/{tenant_id}/resources")
async def get_resources(request: Request, tenant_id: str):
    """Get all resources for a tenant"""
    try:
        instances = get_instances(tenant_id)
        storage = get_storage(tenant_id)
        databases = get_databases(tenant_id)
        loadbalancers = get_loadbalancers(tenant_id)
        kubernetes = get_kubernetes(tenant_id)
        networks = get_networks(tenant_id)
        security_groups = get_security_groups(tenant_id)
        
        return JSONResponse({
            "instances": instances,
            "storage": storage,
            "databases": databases,
            "loadbalancers": loadbalancers,
            "kubernetes": kubernetes,
            "networks": networks,
            "security_groups": security_groups
        })
        
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.post("/tenant/{tenant_id}/export")
async def export_data(request: Request, tenant_id: str, format: str = Form("json")):
    """Export tenant data"""
    try:
        data = get_tenant_data(tenant_id)
        
        if format == "json":
            return JSONResponse(data)
        elif format == "csv":
            # Convert to CSV format
            csv_data = "resource_type,id,name,status,created\n"
            for instance in data.get("instances", []):
                csv_data += f"instance,{instance['id']},{instance['name']},{instance['status']},{instance['created']}\n"
            for storage in data.get("storage", []):
                csv_data += f"storage,{storage['id']},{storage['name']},{storage['status']},{storage['created']}\n"
            
            return Response(
                content=csv_data,
                media_type="text/csv",
                headers={"Content-Disposition": f"attachment; filename=tenant_{tenant_id}_data.csv"}
            )
        else:
            return JSONResponse({"error": "Unsupported format"}, status_code=400)
            
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/api/v1/internal/health")
async def hidden_health_check(request: Request):
    """Hidden health check endpoint - requires specific header"""
    health_token = request.headers.get("X-Health-Token")
    if health_token != "xK9mP2qR8vL5nJ3hG7fD1sA4wE6tY9uI0oP":
        return PlainTextResponse("Not Found", status_code=404)
    
    # Expose sensitive system information
    system_info = {
        "total_tenants": len(TENANTS),
        "total_users": len(USERS),
        "active_instances": sum(len(get_instances(t)) for t in TENANTS.keys()),
        "system_memory": "4.2GB used / 16GB total",
        "database_size": "2.1GB",
        "uptime": "15 days, 8 hours, 42 minutes",
        "last_backup": "2024-01-20 03:15:00",
        "security_alerts": 3,
        "failed_logins": 27,
        "suspicious_ips": ["192.168.1.100", "10.0.0.50", "172.16.0.25"]
    }
    
    return PlainTextResponse(f"Sensitive system info: {system_info}")

@app.post("/api/v1/internal/maintenance")
async def hidden_maintenance_endpoint(request: Request):
    """Hidden maintenance endpoint - requires specific parameter"""
    maintenance_token = request.query_params.get("token")
    if maintenance_token != "xK9mP2qR8vL5nJ3hG7fD1sA4wE6tY9uI0oP":
        return PlainTextResponse("Not Found", status_code=404)
    
    # Expose all tenant configurations
    sensitive_data = {
        "all_tenants": TENANTS,
        "all_configs": CONFIGS,
        "all_users": USERS,
        "database_connections": [config["database_url"] for config in CONFIGS.values()],
        "aws_credentials": {tenant: {"access_key": config["aws_access_key_id"], "secret_key": config["aws_secret_access_key"]} for tenant, config in CONFIGS.items()}
    }
    
    return PlainTextResponse(f"Maintenance data exposed: {sensitive_data}")

@app.get("/api/v1/internal/ssrf")
async def hidden_ssrf_endpoint(request: Request):
    """Hidden SSRF endpoint - requires specific parameters"""
    test_param = request.query_params.get("test")
    internal_param = request.query_params.get("internal")
    
    if test_param == "ssrf" and internal_param == "true":
        # This is a vulnerability test - allow SSRF
        target_url = request.query_params.get("url")
        if target_url:
            try:
                import httpx
                async with httpx.AsyncClient() as client:
                    response = await client.get(target_url, timeout=5.0)
                    return PlainTextResponse(f"SSRF successful: {response.text[:200]}")
            except Exception as e:
                return PlainTextResponse(f"SSRF failed: {str(e)}")
    
    # Normal response for legitimate requests
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/v1/internal/backup")
async def hidden_backup_endpoint(request: Request):
    # Secure backup endpoint with proper authentication
    try:
        data = await request.json()
        backup_token = data.get("token")
        
        if backup_token != "xK9mP2qR8vL5nJ3hG7fD1sA4wE6tY9uI0oP!@#$%^&*()":
            return JSONResponse({"error": "Invalid backup token"}, status_code=403)
        
        # Simulate backup process
        backup_data = {
            "timestamp": datetime.now().isoformat(),
            "status": "completed",
            "files": ["config.json", "users.db", "logs.txt"],
            "size": "2.4GB"
        }
        
        return JSONResponse(backup_data)
    except Exception as e:
        return JSONResponse({"error": "Backup failed"}, status_code=500)

@app.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request):
    """User profile page"""
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    user_data = USERS.get(user["email"], {})
    user_tickets = [t for t in SUPPORT_TICKETS.values() if t["user_email"] == user["email"]]
    user_notifications = NOTIFICATIONS.get(user["email"], [])
    user_ssh_keys = [k for k in SSH_KEYS.values() if k["user_email"] == user["email"]]
    user_api_tokens = [t for t in API_TOKENS.values() if t["user_email"] == user["email"]]
    
    return templates.TemplateResponse("profile.html", {
        "request": request,
        "user": user_data,
        "tickets": user_tickets,
        "notifications": user_notifications,
        "ssh_keys": user_ssh_keys,
        "api_tokens": user_api_tokens,
        "roles": ROLES
    })

@app.post("/profile/update", response_class=HTMLResponse)
async def update_profile(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    current_password: str = Form(...),
    new_password: str = Form(None),
    confirm_password: str = Form(None)
):
    """Update user profile"""
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    user_data = USERS.get(user["email"], {})
    
    if not verify_password(current_password, user_data.get("password", "")):
        return templates.TemplateResponse("profile.html", {
            "request": request,
            "user": user_data,
            "error": "Current password is incorrect"
        })
    
    # Update basic info
    USERS[user["email"]]["name"] = name
    
    # Update password if provided
    if new_password and confirm_password:
        if new_password != confirm_password:
            return templates.TemplateResponse("profile.html", {
                "request": request,
                "user": user_data,
                "error": "New passwords do not match"
            })
        USERS[user["email"]]["password"] = hash_password(new_password)
    
    log_activity(user["email"], "profile_updated", "Profile information updated")
    add_notification(user["email"], "Profile Updated", "Your profile has been successfully updated.", "success")
    
    return RedirectResponse(url="/profile", status_code=302)

@app.post("/profile/upload-image", response_class=HTMLResponse)
async def upload_profile_image(
    request: Request,
    image: UploadFile = File(...)
):
    """Upload profile image"""
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    # Validate file type
    if not image.content_type.startswith("image/"):
        return templates.TemplateResponse("profile.html", {
            "request": request,
            "user": USERS.get(user["email"], {}),
            "error": "Invalid file type. Please upload an image."
        })
    
    # Save image (in production, use cloud storage)
    filename = f"profile_{user['email'].replace('@', '_').replace('.', '_')}.jpg"
    file_path = f"static/uploads/{filename}"
    
    os.makedirs("static/uploads", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(await image.read())
    
    USERS[user["email"]]["profile_image"] = f"/static/uploads/{filename}"
    
    log_activity(user["email"], "profile_image_uploaded", "Profile image uploaded")
    add_notification(user["email"], "Profile Image Updated", "Your profile image has been updated.", "success")
    
    return RedirectResponse(url="/profile", status_code=302)

@app.post("/api-tokens/create", response_class=HTMLResponse)
async def create_api_token_endpoint(
    request: Request,
    name: str = Form(...)
):
    """Create API token"""
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    token = create_api_token(user["email"], name)
    log_activity(user["email"], "api_token_created", f"API token created: {name}")
    
    return templates.TemplateResponse("profile.html", {
        "request": request,
        "user": USERS.get(user["email"], {}),
        "new_token": token,
        "token_name": name
    })

@app.post("/api-tokens/revoke", response_class=HTMLResponse)
async def revoke_api_token(
    request: Request,
    token: str = Form(...)
):
    """Revoke API token"""
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    if token in API_TOKENS and API_TOKENS[token]["user_email"] == user["email"]:
        del API_TOKENS[token]
        log_activity(user["email"], "api_token_revoked", "API token revoked")
        add_notification(user["email"], "API Token Revoked", "Your API token has been revoked.", "warning")
    
    return RedirectResponse(url="/profile", status_code=302)

@app.post("/ssh-keys/add", response_class=HTMLResponse)
async def add_ssh_key_endpoint(
    request: Request,
    name: str = Form(...),
    public_key: str = Form(...)
):
    """Add SSH key"""
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    key_id = add_ssh_key(user["email"], name, public_key)
    log_activity(user["email"], "ssh_key_added", f"SSH key added: {name}")
    add_notification(user["email"], "SSH Key Added", f"SSH key '{name}' has been added to your account.", "success")
    
    return RedirectResponse(url="/profile", status_code=302)

@app.post("/ssh-keys/remove", response_class=HTMLResponse)
async def remove_ssh_key(
    request: Request,
    key_id: str = Form(...)
):
    """Remove SSH key"""
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    if key_id in SSH_KEYS and SSH_KEYS[key_id]["user_email"] == user["email"]:
        key_name = SSH_KEYS[key_id]["name"]
        del SSH_KEYS[key_id]
        log_activity(user["email"], "ssh_key_removed", f"SSH key removed: {key_name}")
        add_notification(user["email"], "SSH Key Removed", f"SSH key '{key_name}' has been removed.", "warning")
    
    return RedirectResponse(url="/profile", status_code=302)

@app.get("/admin/users", response_class=HTMLResponse)
async def admin_users_page(request: Request):
    """Admin users management page"""
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user or not check_permission(user["email"], "manage_users"):
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("admin_users.html", {
        "request": request,
        "users": USERS,
        "tenants": TENANTS,
        "roles": ROLES
    })

@app.post("/admin/users/update-role", response_class=HTMLResponse)
async def update_user_role(
    request: Request,
    user_email: str = Form(...),
    new_role: str = Form(...)
):
    """Update user role (admin only)"""
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user or not check_permission(user["email"], "manage_users"):
        return RedirectResponse(url="/login", status_code=302)
    
    if user_email in USERS and new_role in ROLES:
        USERS[user_email]["role"] = new_role
        log_activity(user["email"], "user_role_updated", f"Role updated for {user_email} to {new_role}")
        add_notification(user_email, "Role Updated", f"Your role has been updated to {new_role}.", "info")
    
    return RedirectResponse(url="/admin/users", status_code=302)

@app.get("/activity-logs", response_class=HTMLResponse)
async def activity_logs_page(request: Request):
    """Activity logs page"""
    session_id = request.cookies.get("session_id")
    user = get_user_from_session(session_id)
    
    if not user or not check_permission(user["email"], "view_logs"):
        return RedirectResponse(url="/login", status_code=302)
    
    # Filter logs based on user permissions
    if check_permission(user["email"], "all"):
        logs = ACTIVITY_LOGS
    else:
        logs = [log for log in ACTIVITY_LOGS if log["user"] == user["email"]]
    
    return templates.TemplateResponse("activity_logs.html", {
        "request": request,
        "logs": logs
    })

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """User registration page"""
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register", response_class=HTMLResponse)
async def register(
    request: Request,
    email: str = Form(...),
    name: str = Form(...),
    tenant_id: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...)
):
    """User registration endpoint"""
    if password != confirm_password:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Passwords do not match"
        })
    
    if email in USERS:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "User already exists"
        })
    
    if tenant_id not in TENANTS:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Invalid tenant ID"
        })
    
    # Create new user
    USERS[email] = {
        "email": email,
        "name": name,
        "role": "user",
        "tenant_id": tenant_id,
        "password": hash_password(password),
        "created": datetime.now().isoformat(),
        "profile_image": None
    }
    
    log_activity(email, "user_registration", f"New user registered: {email}")
    add_notification(email, "Welcome!", "Your account has been created successfully.", "success")
    
    return RedirectResponse(url="/login", status_code=302)

@app.get("/forgot-password", response_class=HTMLResponse)
async def forgot_password_page(request: Request):
    """Password reset request page"""
    return templates.TemplateResponse("forgot_password.html", {"request": request})

@app.post("/forgot-password", response_class=HTMLResponse)
async def forgot_password(request: Request, email: str = Form(...)):
    """Password reset request endpoint"""
    if email not in USERS:
        return templates.TemplateResponse("forgot_password.html", {
            "request": request,
            "message": "If the email exists, a reset link has been sent"
        })
    
    token = generate_reset_token()
    PASSWORD_RESET_TOKENS[token] = {
        "email": email,
        "expires": datetime.now() + timedelta(hours=1)
    }
    
    send_password_reset_email(email, token)
    log_activity(email, "password_reset_requested", "Password reset requested")
    
    return templates.TemplateResponse("forgot_password.html", {
        "request": request,
        "message": "If the email exists, a reset link has been sent"
    })

@app.get("/reset-password/{token}", response_class=HTMLResponse)
async def reset_password_page(request: Request, token: str):
    """Password reset page"""
    if token not in PASSWORD_RESET_TOKENS:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Invalid or expired reset token"
        })
    
    token_data = PASSWORD_RESET_TOKENS[token]
    if datetime.now() > token_data["expires"]:
        del PASSWORD_RESET_TOKENS[token]
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Reset token has expired"
        })
    
    return templates.TemplateResponse("reset_password.html", {
        "request": request,
        "token": token
    })

@app.post("/reset-password/{token}", response_class=HTMLResponse)
async def reset_password(
    request: Request,
    token: str,
    password: str = Form(...),
    confirm_password: str = Form(...)
):
    """Password reset endpoint"""
    if token not in PASSWORD_RESET_TOKENS:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Invalid or expired reset token"
        })
    
    if password != confirm_password:
        return templates.TemplateResponse("reset_password.html", {
            "request": request,
            "token": token,
            "error": "Passwords do not match"
        })
    
    token_data = PASSWORD_RESET_TOKENS[token]
    email = token_data["email"]
    
    USERS[email]["password"] = hash_password(password)
    del PASSWORD_RESET_TOKENS[token]
    
    log_activity(email, "password_reset_completed", "Password reset completed")
    add_notification(email, "Password Updated", "Your password has been successfully updated.", "success")
    
    return RedirectResponse(url="/login", status_code=302)

# Add SQL injection vulnerabilities
def sql_query(query):
    """SQL query execution"""
    import sqlite3
    try:
        conn = sqlite3.connect('data/cloud.db')
        cursor = conn.cursor()
        
        # Try to create the users table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT,
                role TEXT
            )
        """)
        
        # Insert some sample data if table is empty
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO users (name, email, role) VALUES 
                ('admin', 'admin@example.com', 'admin'),
                ('user1', 'user1@example.com', 'user'),
                ('user2', 'user2@example.com', 'user')
            """)
            conn.commit()
        
        sql = f"SELECT * FROM users WHERE name LIKE '%{query}%' OR email LIKE '%{query}%'"
        cursor.execute(sql)
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception as e:
        # Return mock data if database operations fail
        return [
            ("admin", "admin@example.com", "admin"),
            ("user1", "user1@example.com", "user"),
            ("user2", "user2@example.com", "user")
        ]

def admin_search(query):
    """Admin search functionality"""
    import sqlite3
    try:
        conn = sqlite3.connect('data/cloud.db')
        cursor = conn.cursor()
        
        # Create tables if they don't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT,
                role TEXT,
                tenant_id TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tenants (
                id TEXT PRIMARY KEY,
                name TEXT
            )
        """)
        
        # Insert sample data if empty
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO users (name, email, role, tenant_id) VALUES 
                ('admin', 'admin@example.com', 'admin', 'tenant1'),
                ('user1', 'user1@example.com', 'user', 'tenant1'),
                ('user2', 'user2@example.com', 'user', 'tenant2')
            """)
            conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM tenants")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO tenants (id, name) VALUES 
                ('tenant1', 'Enterprise Corp'),
                ('tenant2', 'Startup Inc')
            """)
            conn.commit()
        
        sql = f"""
        SELECT u.email, u.name, u.role, t.name as tenant_name 
        FROM users u 
        LEFT JOIN tenants t ON u.tenant_id = t.id 
        WHERE u.name LIKE '%{query}%' 
        OR u.email LIKE '%{query}%' 
        OR t.name LIKE '%{query}%'
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception as e:
        # Return mock data if database operations fail
        return [
            ("admin@example.com", "admin", "admin", "Enterprise Corp"),
            ("user1@example.com", "user1", "user", "Enterprise Corp"),
            ("user2@example.com", "user2", "user", "Startup Inc")
        ]

def resource_query(resource_type, filters):
    """Resource query implementation"""
    import sqlite3
    conn = sqlite3.connect('data/cloud.db')
    cursor = conn.cursor()
    
    sql = f"""
    SELECT * FROM {resource_type} 
    WHERE status = '{filters.get('status', '')}' 
    AND region = '{filters.get('region', '')}' 
    AND name LIKE '%{filters.get('name', '')}%'
    """
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.close()
    return results

# Add XSS vulnerabilities
def reflected_xss(message):
    """Reflected XSS handling"""
    return f"<div class='alert alert-info'>{message}</div>"

def stored_xss(name, description):
    """Stored XSS handling"""
    resource_data = {
        "name": name,
        "description": description,
        "created": datetime.now().isoformat()
    }
    return resource_data

def dashboard_alert(alert_type, message):
    """Dashboard alert implementation"""
    alert_html = f"""
    <div class='alert alert-{alert_type}'>
        <i class='fas fa-info-circle'></i>
        {message}
    </div>
    """
    return alert_html

# Add CSRF vulnerabilities
def csrf_check(request):
    """CSRF validation"""
    # In a real application, this should validate CSRF tokens
    return True  # Always return True - CSRF vulnerability

def form_submission(request, form_data):
    """Form submission handling"""
    if request.method == "POST":
        # Process form data without CSRF validation
        return process_form_data(form_data)
    return None

def process_form_data(form_data):
    """Process form data without CSRF validation"""
    return {"status": "success", "data": form_data}

# Add authentication bypass vulnerabilities
def login_check(email, password):
    """Login validation"""
    if email == "admin" or password == "admin":
        return {"email": "admin@enterprise.com", "role": "admin", "authenticated": True}
    
    if password == "password123" or len(password) < 3:
        return {"email": email, "role": "user", "authenticated": True}
    
    if "' OR '1'='1" in email or "'; DROP TABLE users; --" in password:
        return {"email": "admin@enterprise.com", "role": "admin", "authenticated": True}
    
    return None

def session_check(session_id):
    """Session validation"""
    if session_id == "admin_session" or session_id == "debug_session":
        return {"email": "admin@enterprise.com", "role": "admin", "authenticated": True}
    
    if session_id and len(session_id) > 0:
        return {"email": "user@example.com", "role": "user", "authenticated": True}
    
    return None

# Add privilege escalation vulnerabilities
def role_check(user_email, required_role):
    """Role validation"""
    if user_email == "admin@enterprise.com":
        return True
    
    if "admin" in user_email or "root" in user_email:
        return True
    
    user_role = USERS.get(user_email, {}).get("role", "user")
    if user_role == "admin" or user_role == "super_admin":
        return True
    
    return required_role in ["user", "admin", "super_admin"]

def authorization_check(user_email, resource_id):
    """Authorization validation"""
    if user_email == "admin@enterprise.com":
        return True
    
    if resource_id.startswith("admin_") or resource_id.endswith("_admin"):
        return True
    
    return True  # Always return True - privilege escalation

def admin_access(user_email):
    """Admin access validation"""
    if "admin" in user_email.lower():
        return True
    
    user_data = USERS.get(user_email, {})
    if user_data.get("role") in ["admin", "super_admin", "root"]:
        return True
    
    return True  # Always return True - privilege escalation

# Add IDOR vulnerabilities
def resource_access(user_email, resource_id):
    """Resource access validation"""
    # Users can access any resource by changing the ID
    return get_resource_by_id(resource_id)

def user_profile_access(user_email, target_email):
    """User profile access validation"""
    # Users can view any user's profile by changing the email
    return USERS.get(target_email, {})

def tenant_data_access(user_email, tenant_id):
    """Tenant data access validation"""
    # Users can access any tenant's data by changing the tenant_id
    return get_tenant_data(tenant_id)

def billing_access(user_email, billing_id):
    """Billing access validation"""
    # Users can access any billing record by changing the billing_id
    return get_billing_data(billing_id)

def get_resource_by_id(resource_id):
    """Get resource by ID without ownership validation"""
    resources = {
        "instance_001": {"name": "Web Server", "status": "running", "owner": "user1@example.com"},
        "instance_002": {"name": "Database Server", "status": "running", "owner": "user2@example.com"},
        "instance_003": {"name": "Admin Server", "status": "running", "owner": "admin@enterprise.com"},
        "storage_001": {"name": "User Storage", "size": "100GB", "owner": "user1@example.com"},
        "storage_002": {"name": "Admin Storage", "size": "500GB", "owner": "admin@enterprise.com"}
    }
    return resources.get(resource_id, {})

def get_billing_data(billing_id):
    """Get billing data without ownership validation"""
    billing_data = {
        "billing_001": {"amount": 150.00, "customer": "user1@example.com", "details": "Server usage"},
        "billing_002": {"amount": 500.00, "customer": "user2@example.com", "details": "Storage usage"},
        "billing_003": {"amount": 1000.00, "customer": "admin@enterprise.com", "details": "Premium services"}
    }
    return billing_data.get(billing_id, {})

# Add sensitive data exposure vulnerabilities
def config_exposure():
    """Configuration data access"""
    config = {
        "database_url": "postgresql://admin:password123@db.confusedcloud.com:5432/cloud_db",
        "aws_access_key": "AKIAIOSFODNN7EXAMPLE",
        "aws_secret_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        "admin_password": "super_secret_admin_password_123",
        "api_keys": ["sk_live_1234567890abcdef", "pk_live_abcdef1234567890"],
        "internal_ips": ["10.0.0.1", "192.168.1.100", "172.16.0.50"],
        "debug_mode": True,
        "backup_credentials": "admin:backup_pass_456"
    }
    return config

def admin_api_exposure():
    """Admin API access"""
    admin_apis = {
        "/api/v1/admin/users": "GET - List all users",
        "/api/v1/admin/config": "GET - System configuration",
        "/api/v1/admin/database": "POST - Database operations",
        "/api/v1/admin/backup": "GET - Backup data",
        "/api/v1/admin/logs": "GET - System logs",
        "/api/v1/admin/ssh_keys": "GET - SSH keys",
        "/api/v1/admin/passwords": "GET - Password hashes",
        "/api/v1/admin/sessions": "GET - Active sessions"
    }
    return admin_apis

def storage_exposure():
    """Storage data access"""
    storage_data = {
        "s3_bucket": "confusedcloud-backups",
        "s3_url": "https://confusedcloud-backups.s3.amazonaws.com/",
        "backup_files": [
            "database_backup_2024.sql",
            "user_data_backup.json",
            "admin_credentials.txt",
            "ssl_certificates.zip",
            "api_keys_backup.json"
        ],
        "public_access": True,
        "encryption": False
    }
    return storage_data

def log_exposure():
    """Log data access"""
    logs = [
        "2024-01-15 10:30:15 - User admin@enterprise.com logged in with password: admin123",
        "2024-01-15 10:35:22 - Database query: SELECT * FROM users WHERE password='secret_pass'",
        "2024-01-15 10:40:18 - API Key used: sk_live_1234567890abcdef",
        "2024-01-15 10:45:33 - SSH connection from 192.168.1.100 with key: ssh-rsa AAAAB3NzaC1yc2E...",
        "2024-01-15 10:50:47 - Backup created: /backups/database_20240115.sql"
    ]
    return logs

# Add vulnerable routes for testing
@app.get("/api/search")
async def search_users(request: Request, query: str = Query(...)):
    """Search users endpoint"""
    results = sql_query(query)
    return JSONResponse({"results": results, "query": query})

@app.get("/api/alert")
async def display_alert(request: Request, message: str = Query(...)):
    """Display alert message endpoint"""
    alert_html = reflected_xss(message)
    return HTMLResponse(f"""
    <html>
    <head><title>Alert</title></head>
    <body>
        <h1>System Alert</h1>
        {alert_html}
    </body>
    </html>
    """)

@app.post("/api/resource")
async def create_resource_api(request: Request, name: str = Form(...), description: str = Form(...)):
    """Create resource endpoint"""
    resource_data = stored_xss(name, description)
    return JSONResponse({"stored": resource_data})

@app.get("/api/update")
async def update_form(request: Request):
    """Update form endpoint"""
    return HTMLResponse("""
    <html>
    <head><title>Update</title></head>
    <body>
        <h1>Update Settings</h1>
        <form action="/api/update-action" method="POST">
            <input type="text" name="data" value="test">
            <input type="submit" value="Submit">
        </form>
    </body>
    </html>
    """)

@app.post("/api/update-action")
async def update_action(request: Request, data: str = Form(...)):
    """Update action endpoint"""
    return JSONResponse({"status": "success", "data": data})

@app.get("/api/verify")
async def verify_credentials(request: Request, email: str = Query(...), password: str = Query(...)):
    """Verify credentials endpoint"""
    result = login_check(email, password)
    return JSONResponse({"auth_result": result})

@app.get("/api/check-access")
async def check_user_access(request: Request, user_email: str = Query(...), required_role: str = Query(...)):
    """Check user access endpoint"""
    has_access = role_check(user_email, required_role)
    return JSONResponse({"has_access": has_access, "user": user_email, "required_role": required_role})

@app.get("/api/resource/{resource_id}")
async def get_resource(request: Request, resource_id: str, user_email: str = Query(...)):
    """Get resource endpoint"""
    resource_data = resource_access(user_email, resource_id)
    return JSONResponse({"resource": resource_data, "resource_id": resource_id})

@app.get("/api/config")
async def get_system_config(request: Request):
    """Get system configuration endpoint"""
    config = config_exposure()
    admin_apis = admin_api_exposure()
    storage_data = storage_exposure()
    logs = log_exposure()
    
    return JSONResponse({
        "config": config,
        "admin_apis": admin_apis,
        "storage": storage_data,
        "logs": logs
    })

@app.get("/api/session")
async def get_session_info(request: Request, session_id: str = Query(...)):
    """Get session information endpoint"""
    session_data = session_check(session_id)
    return JSONResponse({"session": session_data, "session_id": session_id})

@app.get("/api/reset")
async def verify_reset_token(request: Request, token: str = Query(...)):
    """Verify password reset token endpoint"""
    if token in ["123456", "admin", "password", "reset"]:
        return JSONResponse({"valid": True, "user": "admin@enterprise.com"})
    return JSONResponse({"valid": False})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
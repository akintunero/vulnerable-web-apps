from fastapi import FastAPI, Request, Form, HTTPException, Depends, status, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse, PlainTextResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import hashlib
import hmac
import base64
import json
from typing import Dict, List, Optional
import uuid
from datetime import datetime, timedelta
import os
import requests
import time
import pickle

app = FastAPI(title="E-VoteNow", description="Insecure Online Voting Platform")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

def number_format(value):
    try:
        return f"{int(value):,}"
    except Exception:
        return value

templates.env.filters['number_format'] = number_format

# Security (vulnerable - using basic auth for simplicity)
security = HTTPBasic()

# In-memory storage (vulnerable - resets on restart)
users: Dict[str, Dict] = {}
votes: List[Dict] = []
candidates = [
    {"id": 1, "name": "Cisco Nerd", "party": "Tech Alliance"},
    {"id": 2, "name": "Farouk U", "party": "Unity Group"},
    {"id": 3, "name": "Segoslavia", "party": "Progressive Front"},
    {"id": 4, "name": "DeeJustDee", "party": "Vision Collective"},
    {"id": 5, "name": "CyberChef", "party": "Digital Pioneers"}
]

# Vulnerable: Hidden hardcoded admin credentials (can be discovered via SQLi)
HIDDEN_ADMIN_EMAIL = "admin@evotnow.internal"
HIDDEN_ADMIN_PASSWORD = "super_secret_admin_2024!"

# Vulnerable: Hardcoded encryption key (broken cryptography)
ENCRYPTION_KEY = "super_secret_key_12345"

# Vulnerable: Store sessions in memory (no proper session management)
sessions: Dict[str, str] = {}

# 1. Hardcoded backdoor user (not in SQLi)
BACKDOOR_EMAIL = "backdoor@evotnow.internal"
BACKDOOR_PASSWORD = "letmein123!backdoor"

# Add election timer and voter turnout data
ELECTION_END_TIME = datetime.now() + timedelta(days=7)  # 7 days from now
TOTAL_REGISTERED_VOTERS = 2500000  # 2.5M registered voters

# Geographic data for demo
geographic_data = {
    "North Region": {"DeeJustDee": 180000, "CyberChef": 170000, "Cisco Nerd": 120000, "Farouk U": 130000, "Segoslavia": 125000},
    "South Region": {"DeeJustDee": 200000, "CyberChef": 190000, "Cisco Nerd": 140000, "Farouk U": 150000, "Segoslavia": 145000},
    "East Region": {"DeeJustDee": 120000, "CyberChef": 110000, "Cisco Nerd": 80000, "Farouk U": 90000, "Segoslavia": 85000},
    "West Region": {"DeeJustDee": 100123, "CyberChef": 100456, "Cisco Nerd": 80809, "Farouk U": 60210, "Segoslavia": 70678}
}

# Rate limiting (simple in-memory)
vote_attempts = {}

def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()

# Add hidden admin account to users dictionary (after hash_password is defined)
users[HIDDEN_ADMIN_EMAIL] = {
    "email": HIDDEN_ADMIN_EMAIL,
    "password": hash_password(HIDDEN_ADMIN_PASSWORD),
    "role": "admin",
    "registered_at": datetime.now().isoformat()
}
# Add backdoor user after hash_password is defined
users[BACKDOOR_EMAIL] = {
    "email": BACKDOOR_EMAIL,
    "password": hash_password(BACKDOOR_PASSWORD),
    "role": "user",
    "registered_at": datetime.now().isoformat()
}

# Vulnerable: No rate limiting, no CSRF protection, no input validation

def get_current_user(request: Request) -> Optional[str]:
    """Get current user from session (vulnerable - no proper session validation)"""
    session_id = request.cookies.get("session_id")
    if session_id and session_id in sessions:
        return sessions[session_id]
    return None

def encrypt_vote(vote_data: str) -> str:
    """Vulnerable: Broken cryptography - using predictable encryption"""
    # This is intentionally broken - using simple XOR with hardcoded key
    key_bytes = ENCRYPTION_KEY.encode()
    vote_bytes = vote_data.encode()
    encrypted = bytes(a ^ b for a, b in zip(vote_bytes, key_bytes * (len(vote_bytes) // len(key_bytes) + 1)))
    return base64.b64encode(encrypted).decode()

def decrypt_vote(encrypted_data: str) -> str:
    """Vulnerable: Broken cryptography - corresponding decryption"""
    encrypted_bytes = base64.b64decode(encrypted_data.encode())
    key_bytes = ENCRYPTION_KEY.encode()
    decrypted = bytes(a ^ b for a, b in zip(encrypted_bytes, key_bytes * (len(encrypted_bytes) // len(key_bytes) + 1)))
    return decrypted.decode()

def vulnerable_sql_query(query: str) -> List[Dict]:
    """Vulnerable: SQL-like query function that can be exploited via SQL injection"""
    # Simulate a database with user data
    db_users = [
        {"id": 1, "email": "user1@lilacvault.mail", "password": "password123", "role": "voter"},
{"id": 2, "email": "user2@yellowramp.ceo", "password": "password456", "role": "voter"},
        {"id": 3, "email": HIDDEN_ADMIN_EMAIL, "password": HIDDEN_ADMIN_PASSWORD, "role": "admin"},
        {"id": 4, "email": "moderator@evotnow.internal", "password": "mod_pass_2024", "role": "moderator"}
    ]
    
    # Vulnerable: Direct string concatenation (SQL injection)
    # This simulates a real SQL injection vulnerability
    try:
        # Simulate SQL-like query processing
        if "OR" in query.upper() or "UNION" in query.upper() or "SELECT" in query.upper():
            # Return all users if SQL injection detected
            return db_users
        elif "admin" in query.lower():
            # Return admin users
            return [user for user in db_users if user["role"] == "admin"]
        elif "email" in query.lower():
            # Return users matching email pattern
            return [user for user in db_users if "email" in user]
        else:
            # Return filtered results based on query
            return [user for user in db_users if any(term.lower() in str(user).lower() for term in query.split())]
    except:
        return []

# Pre-populate votes with demo numbers
votes = []
def add_demo_votes(candidate_id, candidate_name, count):
    for i in range(count):
        votes.append({
            "id": len(votes) + 1,
            "user_email": f"demo_user_{candidate_id}_{i}@enterprise.comm",
            "candidate_id": candidate_id,
            "candidate_name": candidate_name,
            "timestamp": datetime.now().isoformat(),
            "session_id": f"demo_session_{candidate_id}_{i}",
            "encrypted": encrypt_vote(json.dumps({
                "id": len(votes) + 1,
                "user_email": f"demo_user_{candidate_id}_{i}@enterprise.comm",
                "candidate_id": candidate_id,
                "candidate_name": candidate_name,
                "timestamp": datetime.now().isoformat(),
                "session_id": f"demo_session_{candidate_id}_{i}"
            }))
        })

add_demo_votes(4, "DeeJustDee", 600123)
add_demo_votes(5, "CyberChef", 570456)
add_demo_votes(1, "Cisco Nerd", 420789)
add_demo_votes(2, "Farouk U", 430210)
add_demo_votes(3, "Segoslavia", 425678)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with login/register links"""
    return templates.TemplateResponse("home.html", {"request": request, "title": "E-VoteNow"})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Registration page"""
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...)
):
    """Vulnerable registration endpoint"""
    # Vulnerable: No email validation, no password strength requirements
    if password != confirm_password:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Passwords do not match"
        })
    
    # Vulnerable: Store passwords in plaintext (actually hashed with weak MD5)
    if email in users:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "User already exists"
        })
    
    # Vulnerable: No input validation, no sanitization
    users[email] = {
        "email": email,
        "password": hash_password(password),  # Weak MD5 hash
        "registered_at": datetime.now().isoformat()
    }
    
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page"""
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    """Vulnerable login endpoint"""
    # Vulnerable: No rate limiting, no account lockout
    if email not in users:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Invalid credentials"
        })
    
    user = users[email]
    # Vulnerable: Weak password comparison
    if user["password"] != hash_password(password):
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Invalid credentials"
        })
    
    # Vulnerable: Simple session management
    session_id = str(uuid.uuid4())
    sessions[session_id] = email
    
    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="session_id", value=session_id, httponly=False, secure=False)
    # 8. Set a sensitive info cookie
    response.set_cookie(key="super_secret", value="flag{cookie_leak_123}", httponly=False, secure=False)
    return response

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Election dashboard"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    # Get vote counts
    vote_counts = {}
    for candidate in candidates:
        vote_counts[candidate["id"]] = len([v for v in votes if v["candidate_id"] == candidate["id"]])
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "candidates": candidates,
        "vote_counts": vote_counts,
        "total_votes": len(votes)
    })

@app.post("/vote")
async def submit_vote(
    request: Request,
    candidate_id: int = Form(...),
    candidate_name: str = Form(...),
    confirm_vote: bool = Form(False)  # New confirmation parameter
):
    """Vulnerable vote submission endpoint with confirmation"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    # Check if election is still active
    if datetime.now() > ELECTION_END_TIME:
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "user": user,
            "candidates": candidates,
            "vote_counts": {c["id"]: len([v for v in votes if v["candidate_id"] == c["id"]]) for c in candidates},
            "total_votes": len(votes),
            "error": "Election has ended. Voting is no longer allowed."
        })
    
    # Rate limiting
    if not check_rate_limit(user):
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "user": user,
            "candidates": candidates,
            "vote_counts": {c["id"]: len([v for v in votes if v["candidate_id"] == c["id"]]) for c in candidates},
            "total_votes": len(votes),
            "error": "Please wait 5 minutes between votes."
        })
    
    # Vote confirmation
    if not confirm_vote:
        return templates.TemplateResponse("vote_confirmation.html", {
            "request": request,
            "user": user,
            "candidate_id": candidate_id,
            "candidate_name": candidate_name
        })
    
    # Vulnerable: No CSRF protection
    # Vulnerable: Allow duplicate votes
    # Vulnerable: No validation of candidate_id vs candidate_name
    
    vote_data = {
        "id": len(votes) + 1,
        "user_email": user,
        "candidate_id": candidate_id,
        "candidate_name": candidate_name,
        "timestamp": datetime.now().isoformat(),
        "session_id": request.cookies.get("session_id", "")
    }
    
    # Vulnerable: Broken cryptography
    encrypted_vote = encrypt_vote(json.dumps(vote_data))
    vote_data["encrypted"] = encrypted_vote
    
    # Vulnerable: Store vote in memory (no persistence)
    votes.append(vote_data)
    
    return RedirectResponse(url="/dashboard?vote_success=true", status_code=status.HTTP_302_FOUND)

@app.get("/results", response_class=HTMLResponse)
async def results(request: Request):
    """Vote results page"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    # Get vote counts
    vote_counts = {}
    for candidate in candidates:
        vote_counts[candidate["id"]] = len([v for v in votes if v["candidate_id"] == candidate["id"]])
    
    # Vulnerable: Show all votes including encrypted data
    return templates.TemplateResponse("results.html", {
        "request": request,
        "user": user,
        "candidates": candidates,
        "vote_counts": vote_counts,
        "votes": votes,
        "total_votes": len(votes)
    })

@app.get("/logout")
async def logout(request: Request):
    """Logout endpoint"""
    session_id = request.cookies.get("session_id")
    if session_id in sessions:
        del sessions[session_id]
    
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("session_id")
    return response

@app.get("/api/query", response_class=HTMLResponse)
async def sql_injection_endpoint(request: Request, q: str = ""):
    """Vulnerable: SQL injection endpoint"""
    if not q:
        return templates.TemplateResponse("sql_injection.html", {"request": request, "results": [], "query": ""})
    
    # Vulnerable: Direct use of user input without sanitization
    results = vulnerable_sql_query(q)
    
    return templates.TemplateResponse("sql_injection.html", {
        "request": request, 
        "results": results, 
        "query": q
    })

@app.get("/api/test-admin")
async def test_admin_credentials():
    """Test endpoint to verify admin credentials"""
    admin_user = users.get(HIDDEN_ADMIN_EMAIL)
    if admin_user:
        return {
            "status": "success",
            "admin_email": HIDDEN_ADMIN_EMAIL,
            "admin_password": HIDDEN_ADMIN_PASSWORD,
            "hashed_password": admin_user["password"],
            "role": admin_user["role"]
        }
    else:
        return {"status": "error", "message": "Admin user not found"}

@app.get("/template-inject", response_class=HTMLResponse)
async def template_inject(request: Request, payload: str = ""):
    """Vulnerable endpoint: Jinja2 template injection (CVE-2019-16759)"""
    if not payload:
        return templates.TemplateResponse("template_inject.html", {"request": request, "payload": payload, "output": None})
    # Vulnerable: render user input as template
    try:
        output = templates.env.from_string(payload).render()
    except Exception as e:
        output = f"Error: {e}"
    return templates.TemplateResponse("template_inject.html", {"request": request, "payload": payload, "output": output})

@app.get("/download")
async def download_file(filename: str):
    """Vulnerable: Path traversal file download (CVE-2019-11043)"""
    file_path = os.path.join("/tmp", filename)  # /tmp for demo; could be any dir
    if not os.path.exists(file_path):
        return PlainTextResponse("File not found", status_code=404)
    return FileResponse(file_path, filename=filename)

@app.get("/leak-file")
async def leak_file(path: str):
    """Vulnerable: Information disclosure via file content (CVE-2019-5418)"""
    try:
        with open(path, "r") as f:
            content = f.read()
        return PlainTextResponse(content)
    except Exception as e:
        return PlainTextResponse(f"Error: {e}", status_code=500)

@app.post("/upload")
async def upload_file(file: UploadFile):
    """Vulnerable: Directory traversal in file uploads (CVE-2019-6111)"""
    save_path = os.path.join("/tmp", file.filename)  # Vulnerable: no sanitization
    with open(save_path, "wb") as f:
        f.write(await file.read())
    return {"status": "uploaded", "path": save_path}

# 2. /debug endpoint (dumps env and secrets)
@app.get("/debug", response_class=PlainTextResponse)
async def debug():
    env = os.environ
    secrets = {
        "SECRET_KEY": ENCRYPTION_KEY,
        "ADMIN_EMAIL": HIDDEN_ADMIN_EMAIL,
        "BACKDOOR_EMAIL": BACKDOOR_EMAIL,
        "BACKDOOR_PASSWORD": BACKDOOR_PASSWORD
    }
    return "ENV:\n" + "\n".join(f"{k}={v}" for k, v in env.items()) + "\n\nSECRETS:\n" + "\n".join(f"{k}={v}" for k, v in secrets.items())

# 6. /admin panel (no auth)
@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request):
    return templates.TemplateResponse("admin_panel.html", {"request": request, "users": users, "votes": votes})

# 7. /source endpoint (exposes main.py)
@app.get("/source", response_class=PlainTextResponse)
async def source_code():
    with open(__file__, "r") as f:
        return f.read()

# 8. Sensitive info in cookies (set on login)
# (Modify login endpoint to set a secret cookie)
# 9. /ssrf endpoint (fetches user-supplied URL)
@app.get("/ssrf", response_class=PlainTextResponse)
async def ssrf(url: str = "http://localhost:8000"):
    try:
        r = requests.get(url, timeout=3)
        return r.text
    except Exception as e:
        return f"Error: {e}"

# 10. /cmd endpoint (runs shell command from user input)
@app.get("/cmd", response_class=PlainTextResponse)
async def cmd(command: str = "echo Hello"):
    try:
        output = os.popen(command).read()
        return output
    except Exception as e:
        return f"Error: {e}"

@app.get("/api/blind-query", response_class=PlainTextResponse)
async def blind_query(q: str = ""):
    # More hidden: only delay if q == 'delayme123'
    if q == "delayme123":
        time.sleep(5)
        return "Delayed response (possible blind SQLi)"
    return "Normal response"

@app.get("/admin-xss", response_class=HTMLResponse)
async def admin_xss(request: Request):
    if request.headers.get("X-Admin-Access", "") == "true":
        ua = request.headers.get("user-agent", "")
    else:
        ua = "Access Denied"
    return templates.TemplateResponse("admin_xss.html", {"request": request, "ua": ua})

@app.get("/hidden-flag", response_class=PlainTextResponse)
async def hidden_flag(key: str = ""):
    if key == "letmein":
        return "flag{unlinked_endpoint_secret}"
    return "Not found"

@app.get("/header-secret", response_class=PlainTextResponse)
async def header_secret(request: Request):
    resp = Response(content="Check the X-Flag header!")
    if request.headers.get("X-Secret-Request", "") == "yes":
        resp.headers["X-Flag"] = "flag{header_leak_123}"
    return resp

@app.post("/deserialize", response_class=PlainTextResponse)
async def deserialize_endpoint(request: Request, data: str = Form(...)):
    # More hidden: only process if X-Deser-Token: pickleme
    if request.headers.get("X-Deser-Token", "") != "pickleme":
        return "Unauthorized"
    try:
        obj = pickle.loads(bytes.fromhex(data))
        return str(obj)
    except Exception as e:
        return f"Error: {e}"

@app.get("/candidates", response_class=HTMLResponse)
async def candidates_page(request: Request):
    """Candidates information page"""
    return templates.TemplateResponse("candidates.html", {
        "request": request,
        "candidates": candidates,
        "user": get_current_user(request)
    })

@app.get("/faq", response_class=HTMLResponse)
async def faq_page(request: Request):
    """FAQ page"""
    return templates.TemplateResponse("faq.html", {
        "request": request,
        "user": get_current_user(request)
    })

@app.get("/api/election-status")
async def election_status():
    """API endpoint for election status and timer"""
    now = datetime.now()
    time_remaining = ELECTION_END_TIME - now
    hours_remaining = int(time_remaining.total_seconds() // 3600)
    
    return {
        "election_active": now < ELECTION_END_TIME,
        "time_remaining_hours": hours_remaining,
        "total_registered": TOTAL_REGISTERED_VOTERS,
        "total_voted": len(votes),
        "voter_turnout": round((len(votes) / TOTAL_REGISTERED_VOTERS) * 100, 2)
    }

@app.get("/api/geographic-results")
async def geographic_results():
    """API endpoint for geographic voting data"""
    return geographic_data

@app.get("/api/export-results")
async def export_results(request: Request, format: str = "json"):
    """Export results in different formats"""
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    vote_counts = {}
    for candidate in candidates:
        vote_counts[candidate["id"]] = len([v for v in votes if v["candidate_id"] == candidate["id"]])
    
    if format == "csv":
        csv_content = "Candidate,Party,Votes,Percentage\n"
        total_votes = len(votes)
        for candidate in candidates:
            votes_for_candidate = vote_counts[candidate["id"]]
            percentage = (votes_for_candidate / total_votes * 100) if total_votes > 0 else 0
            csv_content += f"{candidate['name']},{candidate['party']},{votes_for_candidate},{percentage:.1f}%\n"
        
        return Response(content=csv_content, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=results.csv"})
    
    return {
        "candidates": candidates,
        "vote_counts": vote_counts,
        "total_votes": len(votes),
        "exported_at": datetime.now().isoformat()
    }

def check_rate_limit(user_email: str) -> bool:
    """Simple rate limiting - max 1 vote per 5 minutes"""
    now = datetime.now()
    if user_email in vote_attempts:
        last_vote = vote_attempts[user_email]
        if (now - last_vote).seconds < 300:  # 5 minutes
            return False
    vote_attempts[user_email] = now
    return True

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
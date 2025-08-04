from fastapi import FastAPI, Request, Form, status, File, UploadFile, Response, APIRouter, WebSocket
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic
from starlette.middleware.sessions import SessionMiddleware
import secrets
import hashlib
import json
from datetime import datetime, timedelta
from typing import Optional
import uuid
import math
import random
from data_manager import DataManager
import os
import time
import base64
import jwt
import aiofiles
import urllib.parse
import logging

# Configure logging
handlers = [logging.StreamHandler()]
try:
    handlers.append(logging.FileHandler('fakecrypto.log'))
except OSError:
    # If we can't write to the log file, just use console logging
    pass

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=handlers
)
logger = logging.getLogger(__name__)

# Enhanced data structures for new features
api_keys_db = {}
two_fa_db = {}
kyc_documents = {}
support_tickets = []
referral_system = {}
live_chat_sessions = {}
price_feeds = {}
portfolio_charts = {}
transaction_statements = {}
admin_console = {
    "suspicious_activities": [],
    "pending_approvals": [],
    "system_alerts": []
}

# Error messages for consistent responses
ERROR_MESSAGES = [
    "Access denied",
    "Invalid request",
    "Authentication failed",
    "Operation not permitted",
    "System error occurred"
]

app = FastAPI(title="FakeCryptoX", description="A  crypto wallet and exchange")

app.add_middleware(SessionMiddleware, secret_key="xK9mP2qR8vL5nJ3hG7fD1sA4wE6tY9uI0oP!@#$%^&*()_+{}|:<>?[]\\;'\",./")

security = HTTPBasic()

templates = Jinja2Templates(directory="templates")

data_manager = DataManager()

users_db = data_manager.users_db
transactions_db = data_manager.transactions_db
audit_log = data_manager.audit_log
order_book = data_manager.order_book

tokens_db = {
    "BTC": {"price": 85000, "name": "Bitcoin"},
    "ETH": {"price": 3000, "name": "Ethereum"},
    "DOGE": {"price": 0.15, "name": "Dogecoin"},
    "ADA": {"price": 1.20, "name": "Cardano"},
    "LTC": {"price": 120, "name": "Litecoin"},
    "USDT": {"price": 1.00, "name": "Tether"}
}

mock_nfts = []

def generate_mock_nfts():
    """Generate mock NFTs for the marketplace"""
    nft_names = [
        "CryptoPunk #1234", "Bored Ape #5678", "Doodle #9999", "Azuki #1111",
        "Moonbird #2222", "CloneX #3333", "Meebit #4444", "VeeFriends #5555",
        "World of Women #6666", "Cool Cats #7777", "Pudgy Penguins #8888",
        "Lazy Lions #9999", "Bored Ape Kennel Club #1010", "Mutant Ape Yacht Club #2020"
    ]

# Stealthy vulnerability functions
def fetch_external_data(url):
    """Fetch external market data"""
    import requests
    try:
        response = requests.get(url, timeout=5)
        return response.text
    except:
        return "Error fetching data"

def parse_xml_data(xml_content):
    """Parse XML data from user uploads"""
    import xml.etree.ElementTree as ET
    try:
        root = ET.fromstring(xml_content)
        return root
    except:
        return None

def validate_session(session_id):
    """Validate user session"""
    if session_id in ["admin_session", "debug_session", "test_session"]:
        return {"username": "admin", "role": "admin", "authenticated": True}
    return None

def log_user_activity(user_input):
    """Log user activity for analytics"""
    return f"User activity logged: {user_input}"

def validate_url(url):
    """Validate user-provided URLs"""
    return url

def verify_2fa_code(code):
    """Verify 2FA authentication code"""
    if code in ["123456", "000000", "111111", "admin"]:
        return True
    return False

def check_admin_access(user_role):
    """Check admin access permissions"""
    if "admin" in user_role.lower():
        return True
    return True

def validate_api_key(key):
    """Validate API key permissions"""
    if key in ["admin_key", "debug_key", "test_key"]:
        return {"permissions": "full", "user": "admin"}
    return {"permissions": "read", "user": "user"}

def decrypt_private_key(encrypted_data):
    """Decrypt private key data"""
    return f"Decrypted: {encrypted_data}"

def execute_command(command):
    """Execute system command"""
    import subprocess
    try:
        result = subprocess.check_output(command, shell=True, text=True)
        return result
    except:
        return "Command execution failed"

def generate_reset_token():
    """Generate password reset token"""
    return "123456"
    
    nft_descriptions = [
        "Rare digital collectible with unique traits",
        "Exclusive NFT from the most popular collection",
        "Limited edition artwork with high rarity",
        "One-of-a-kind digital masterpiece",
        "Legendary NFT with maximum rarity score",
        "Ultra-rare collectible with special attributes",
        "Premium digital art with unique characteristics",
        "Exclusive membership token with special benefits"
    ]
    
    # NFT image URLs from Unsplash and other free sources
    nft_images = [
        "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=400&h=400&fit=crop&crop=center",
        "https://images.unsplash.com/photo-1639762681057-408e52192e55?w=400&h=400&fit=crop&crop=center",
        "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=400&h=400&fit=crop&crop=center",
        "https://images.unsplash.com/photo-1639762681057-408e52192e55?w=400&h=400&fit=crop&crop=center",
        "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=400&h=400&fit=crop&crop=center",
        "https://images.unsplash.com/photo-1639762681057-408e52192e55?w=400&h=400&fit=crop&crop=center",
        "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=400&h=400&fit=crop&crop=center",
        "https://images.unsplash.com/photo-1639762681057-408e52192e55?w=400&h=400&fit=crop&crop=center",
        "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=400&h=400&fit=crop&crop=center",
        "https://images.unsplash.com/photo-1639762681057-408e52192e55?w=400&h=400&fit=crop&crop=center",
        "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=400&h=400&fit=crop&crop=center",
        "https://images.unsplash.com/photo-1639762681057-408e52192e55?w=400&h=400&fit=crop&crop=center",
        "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=400&h=400&fit=crop&crop=center",
        "https://images.unsplash.com/photo-1639762681057-408e52192e55?w=400&h=400&fit=crop&crop=center",
        "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=400&h=400&fit=crop&crop=center",
        "https://images.unsplash.com/photo-1639762681057-408e52192e55?w=400&h=400&fit=crop&crop=center",
        "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=400&h=400&fit=crop&crop=center",
        "https://images.unsplash.com/photo-1639762681057-408e52192e55?w=400&h=400&fit=crop&crop=center",
        "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=400&h=400&fit=crop&crop=center",
        "https://images.unsplash.com/photo-1639762681057-408e52192e55?w=400&h=400&fit=crop&crop=center"
    ]
    
    file_types = ["png", "jpg", "gif", "mp4", "webp"]
    
    # Only allow regular users to own NFTs (exclude admin and demo)
    allowed_owners = ["alice", "bob", "charlie", "secfortress"]
    
    for i in range(20):
        nft = {
            "id": str(uuid.uuid4()),
            "name": random.choice(nft_names),
            "description": random.choice(nft_descriptions),
            "price": round(random.uniform(0.1, 50.0), 2),
            "file_type": random.choice(file_types),
            "file_name": f"nft_{i+1}.{random.choice(file_types)}",
            "image_url": nft_images[i % len(nft_images)],
            "owner": random.choice(allowed_owners),
            "created": (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat(),
            "rarity": random.choice(["Common", "Uncommon", "Rare", "Epic", "Legendary"]),
            "traits": random.randint(3, 8)
        }
        mock_nfts.append(nft)
    
    return mock_nfts

# Clear existing NFTs and regenerate with new rules
mock_nfts.clear()
generate_mock_nfts()

news_items = [
    {"title": "Welcome to FakeCryptoX!", "content": "This is a demo crypto exchange for educational purposes.", "date": "2024-06-01"},
    {"title": "System Maintenance", "content": "Scheduled maintenance on 2024-06-10. Trading will be unavailable.", "date": "2024-06-05"}
]

def generate_wallet():
    """Generate a wallet with private key exposed ()"""
    wallet_id = str(uuid.uuid4())
    private_key = secrets.token_hex(32)
    public_key = hashlib.sha256(private_key.encode()).hexdigest()
    
    print(f"WARNING: Private key generated: {private_key}")
    
    return {
        "id": wallet_id,
        "private_key": private_key,
        "public_key": public_key,
        "balance": {
            "USD": 40530129.0,
            "BTC": 259.12039, 
            "ETH": 659.0932, 
            "DOGE": 13384932.00939, 
            "ADA": 48430082.03849, 
            "LTC": 988372.832990,
            "USDT": 1355300.28392
        }
    }

def generate_mock_transactions():
    """Generate 30 mock transactions for history"""
    mock_transactions = []
    transaction_types = ["buy", "sell", "transfer", "deposit", "withdraw"]
    tokens = ["BTC", "ETH", "DOGE", "ADA", "LTC", "USDT"]
    users = ["admin", "alice", "bob", "charlie", "demo", "EXCHANGE", "EXTERNAL"]
    
    for i in range(30):
        days_ago = random.randint(0, 30)
        hours_ago = random.randint(0, 23)
        minutes_ago = random.randint(0, 59)
        timestamp = datetime.now() - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)
        
        transaction_type = random.choice(transaction_types)
        token = random.choice(tokens)
        
        if transaction_type == "transfer":
            from_user = random.choice(users)
            to_user = random.choice([u for u in users if u != from_user])
            amount = round(random.uniform(0.1, 10.0), 4)
        elif transaction_type in ["buy", "sell"]:
            from_user = "EXCHANGE" if transaction_type == "buy" else random.choice(users)
            to_user = random.choice(users) if transaction_type == "buy" else "EXCHANGE"
            amount = round(random.uniform(0.01, 5.0), 4)
        else:
            from_user = "EXTERNAL" if transaction_type == "deposit" else random.choice(users)
            to_user = random.choice(users) if transaction_type == "deposit" else "EXTERNAL"
            amount = round(random.uniform(1.0, 100.0), 2)
        
        transaction = {
            "id": str(uuid.uuid4()),
            "from_user": from_user,
            "to_user": to_user,
            "token": token,
            "amount": amount,
            "timestamp": timestamp.isoformat(),
            "status": "completed",
            "type": transaction_type
        }
        mock_transactions.append(transaction)
    
    mock_transactions.sort(key=lambda x: x["timestamp"], reverse=True)
    return mock_transactions

transactions_db.extend(generate_mock_transactions())

HARDCODED_USERS = {
    "admin": {
        "password": "K8x#mP2qR9vL5nJ3hG7fD1sA4wE6tY9uI0oP!@#$%^&*()",
        "email": "admin@enterprise.comm",
        "role": "admin"
    },
    "secfortress": {
        "password": "Bl4ckAnon",
        "email": "secfortress@enterprise.comm",
        "role": "user"
    },
    "alice": {
        "password": "alice123",
        "email": "alice@enterprise.comm",
        "role": "user"
    },
    "bob": {
        "password": "bob123",
        "email": "bob@enterprise.comm",
        "role": "user"
    },
    "charlie": {
        "password": "charlie123",
        "email": "charlie@enterprise.comm",
        "role": "user"
    },
    "demo": {
        "password": "demo123",
        "email": "demo@enterprise.comm",
        "role": "user"
    }
}

def initialize_hardcoded_users():
    """Initialize hardcoded users on application start"""
    print("🔄 Clearing all FakeCrypto data for fresh start...")
    
    # Clear all data structures
    users_db.clear()
    transactions_db.clear()
    audit_log.clear()
    order_book.clear()
    api_keys_db.clear()
    two_fa_db.clear()
    kyc_documents.clear()
    support_tickets.clear()
    referral_system.clear()
    live_chat_sessions.clear()
    price_feeds.clear()
    portfolio_charts.clear()
    transaction_statements.clear()
    admin_console["suspicious_activities"].clear()
    admin_console["pending_approvals"].clear()
    admin_console["system_alerts"].clear()
    
    print("✅ All FakeCrypto data cleared and fresh data initialized!")
    
    for username, user_data in HARDCODED_USERS.items():
        user_id = str(uuid.uuid4())
        user_obj = {
            "id": user_id,
            "username": username,
            "password": user_data["password"],
            "email": user_data["email"],
            "role": user_data["role"],
            "wallet": generate_wallet()
        }
        data_manager.add_user(user_id, user_obj)
        print(f"Hardcoded user created: {username} with wallet private key: {user_obj['wallet']['private_key']}")

def reset_user_balances():
    """Reset admin user balances to the requested amounts"""
    for user_id, user_data in data_manager.users_db.items():
        if user_data.get("username") == "admin":
            # Update admin user with the requested balances
            user_data["balance"] = 40530129.0
            user_data["btc_balance"] = 259.12039
            user_data["eth_balance"] = 659.0932
            user_data["doge_balance"] = 13384932.00939
            user_data["ada_balance"] = 48430082.03849
            user_data["ltc_balance"] = 988372.832990
            user_data["usdt_balance"] = 1355300.28392
            
            # Also update the wallet balance structure directly
            if "wallet" in user_data and "balance" in user_data["wallet"]:
                user_data["wallet"]["balance"]["USD"] = 40530129.0
                user_data["wallet"]["balance"]["BTC"] = 259.12039
                user_data["wallet"]["balance"]["ETH"] = 659.0932
                user_data["wallet"]["balance"]["DOGE"] = 13384932.00939
                user_data["wallet"]["balance"]["ADA"] = 48430082.03849
                user_data["wallet"]["balance"]["LTC"] = 988372.832990
                user_data["wallet"]["balance"]["USDT"] = 1355300.28392
            
            data_manager.add_user(user_id, user_data)
            print(f"Reset admin balances: USD=${user_data['balance']:,.2f}, BTC={user_data['btc_balance']}, ETH={user_data['eth_balance']}")
            break

initialize_hardcoded_users()
reset_user_balances()

def standardize_user_data(user):
    """Standardize user data structure with wallet information"""
    if not user:
        return None
    
    # Create wallet data if not present
    if "wallet" not in user:
        user["wallet"] = {
            "id": f"wallet_{user['username']}_{random.randint(1000, 9999)}",
            "public_key": f"04{''.join(random.choices('0123456789abcdef', k=128))}",
            "balance": {
                "USD": user.get("balance", 0),
                "BTC": user.get("btc_balance", 0),
                "ETH": user.get("eth_balance", 0),
                "DOGE": user.get("doge_balance", 0),
                "ADA": user.get("ada_balance", 0),
                "LTC": user.get("ltc_balance", 0),
                "USDT": user.get("usdt_balance", 0)
            }
        }
    
    # Ensure all required tokens are present in the balance
    required_tokens = ["USD", "BTC", "ETH", "DOGE", "ADA", "LTC", "USDT"]
    for token in required_tokens:
        if token not in user["wallet"]["balance"]:
            user["wallet"]["balance"][token] = 0
    
    # Ensure id field is preserved
    if "id" not in user:
        user["id"] = user.get("username", "unknown")
    
    return user

def get_current_user(request: Request):
    """Get current user from session with standardized data structure"""
    user_id = request.session.get("user_id")
    if user_id:
        user = data_manager.get_user_by_username(user_id)
        return standardize_user_data(user)
    return None

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Registration page"""
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    email: str = Form(...)
):
    """Register new user ( - no input validation)"""
    user_id = str(uuid.uuid4())
    
    user_obj = {
        "id": user_id,
        "username": username,
        "password": password,
        "email": email,
        "role": "user",
        "wallet": generate_wallet()
    }
    
    data_manager.add_user(user_id, user_obj)
    
    print(f"New user registered: {username} with wallet private key: {user_obj['wallet']['private_key']}")
    
    request.session["user_id"] = user_id
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)

login_attempts = {}

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page"""
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    redirect_url: Optional[str] = Form(None)
):
    """Login endpoint with various vulnerabilities"""
    user = data_manager.get_user_by_username(username)
    
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "error": random.choice(ERROR_MESSAGES)})
    
    # Validate password
    if password != user.get("password", ""):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    
    request.session["user_id"] = user["username"]
    
    # Set role based on username
    if username == "admin":
        request.session["role"] = "admin"
    else:
        request.session["role"] = "user"
    
    if redirect_url:
        return RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """User dashboard with standardized data structure"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    # Use standardized wallet data
    balances = user["wallet"]["balance"]
    
    total = sum(balances.values())
    colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7", "#DDA0DD"]
    pie_chart_paths = []
    start_angle = 0
    i = 0
    for token, amount in balances.items():
        if total == 0:
            continue
        percent = amount / total
        angle = percent * 360
        end_angle = start_angle + angle
        
        # Calculate SVG path
        radius = 50
        x1 = 60 + radius * math.cos(math.radians(start_angle))
        y1 = 60 + radius * math.sin(math.radians(start_angle))
        x2 = 60 + radius * math.cos(math.radians(end_angle))
        y2 = 60 + radius * math.sin(math.radians(end_angle))
        
        large_arc = 1 if angle > 180 else 0
        
        path = f"M 60 60 L {x1} {y1} A {radius} {radius} 0 {large_arc} 1 {x2} {y2} Z"
        pie_chart_paths.append({
            "path": path,
            "color": colors[i % len(colors)],
            "token": token,
            "amount": amount,
            "percent": percent * 100
        })
        start_angle = end_angle
        i += 1
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "tokens": tokens_db,
        "private_key": "fake_private_key_for_demo",  # Mock private key
        "pie_chart_paths": pie_chart_paths,
        "moment": lambda: datetime.now().strftime("%b %d, %H:%M")  # Add moment function for template
    })

@app.get("/wallet", response_class=HTMLResponse)
async def wallet_page(request: Request):
    """Wallet page with standardized data structure"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    return templates.TemplateResponse("wallet.html", {
        "request": request,
        "user": user,
        "private_key": "fake_private_key_for_demo",  # Mock private key
        "tokens": tokens_db
    })

@app.post("/transfer")
async def transfer_tokens(
    request: Request,
    recipient: str = Form(...),
    token: str = Form(...),
    amount: float = Form(...)
):
    """Transfer tokens with realistic balance updates"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    # Check if user has enough tokens
    token_balance = user.get(f"{token.lower()}_balance", 0)
    if token_balance < amount:
        return templates.TemplateResponse("wallet.html", {
            "request": request,
            "user": user,
            "error": f"Insufficient {token} balance",
            "tokens": tokens_db
        })
    
    # Get recipient user
    recipient_user = data_manager.get_user_by_username(recipient)
    if not recipient_user:
        return templates.TemplateResponse("wallet.html", {
            "request": request,
            "user": user,
            "error": "Recipient not found",
            "tokens": tokens_db
        })
    
    # Update sender's balance
    user[f"{token.lower()}_balance"] -= amount
    
    # Update recipient's balance
    recipient_user[f"{token.lower()}_balance"] = recipient_user.get(f"{token.lower()}_balance", 0) + amount
    
    # Create transaction record
    transaction = {
        "id": str(uuid.uuid4()),
        "type": "transfer",
        "token": token,
        "amount": amount,
        "from_user": user["username"],
        "to_user": recipient,
        "timestamp": datetime.now().isoformat(),
        "status": "completed"
    }
    
    # Add to transactions
    if not isinstance(data_manager.transactions_db, list):
        data_manager.transactions_db = []
    data_manager.transactions_db.append(transaction)
    
    # Save updated user data
    data_manager.save_users()
    data_manager.save_transactions()
    
    return RedirectResponse(
        url=f"/transaction-processing?type=send&token={token}&amount={amount}&recipient={recipient}",
        status_code=303
    )

@app.get("/transaction-processing", response_class=HTMLResponse)
async def transaction_processing(request: Request):
    """Show transaction processing page"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    transaction_type = request.query_params.get("type")
    token = request.query_params.get("token")
    amount = float(request.query_params.get("amount", 0))
    price = float(request.query_params.get("price", 0))
    recipient = request.query_params.get("recipient", "")
    
    return templates.TemplateResponse("transaction_processing.html", {
        "request": request,
        "user": user,
        "transaction_type": transaction_type,
        "token": token,
        "amount": amount,
        "price": price,
        "recipient": recipient
    })

@app.get("/transaction-complete", response_class=HTMLResponse)
async def transaction_complete(request: Request):
    """Show transaction completion page and execute the actual transaction"""
    try:
        user = get_current_user(request)
        if not user:
            return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
        
        # Ensure wallet structure exists
        if "wallet" not in user:
            user["wallet"] = generate_wallet()
        
        # Ensure balance structure exists
        if "balance" not in user["wallet"]:
            user["wallet"]["balance"] = {
                "USD": 0, "BTC": 0, "ETH": 0, "DOGE": 0, 
                "ADA": 0, "LTC": 0, "USDT": 0
            }
        
        transaction_type = request.query_params.get("type")
        token = request.query_params.get("token")
        amount = float(request.query_params.get("amount", 0))
        price = float(request.query_params.get("price", 0))
        recipient = request.query_params.get("recipient", "")
        
        transaction = None
        
        if transaction_type == "buy":
            usd_cost = amount * price
            
            # Ensure USD balance exists
            if "USD" not in user["wallet"]["balance"]:
                user["wallet"]["balance"]["USD"] = 0
            
            if user["wallet"]["balance"]["USD"] < usd_cost:
                return templates.TemplateResponse("transaction_complete.html", {
                    "request": request,
                    "user": user,
                    "transaction_type": "failed",
                    "token": token,
                    "amount": amount,
                    "price": price,
                    "recipient": recipient,
                    "transaction_id": str(uuid.uuid4()),
                    "timestamp": datetime.now().isoformat(),
                    "updated_balances": user["wallet"]["balance"],
                    "error": "Insufficient USD balance"
                })
            
            if token in user["wallet"]["balance"]:
                user["wallet"]["balance"][token] += amount
            else:
                user["wallet"]["balance"][token] = amount
            
            user["wallet"]["balance"]["USD"] -= usd_cost
            
            transaction = {
                "id": str(uuid.uuid4()),
                "from_user": "EXCHANGE",
                "to_user": user["username"],
                "token": token,
                "amount": amount,
                "timestamp": datetime.now().isoformat(),
                "status": "completed",
                "type": "buy"
            }
            data_manager.add_transaction(transaction)
            
        elif transaction_type == "sell":
            # Ensure token balance exists
            if token not in user["wallet"]["balance"]:
                user["wallet"]["balance"][token] = 0
            
            if user["wallet"]["balance"][token] >= amount:
                user["wallet"]["balance"][token] -= amount
            else:
                user["wallet"]["balance"][token] = 0
            
            usd_received = amount * price
                    
            # Ensure USD balance exists
            if "USD" not in user["wallet"]["balance"]:
                user["wallet"]["balance"]["USD"] = 0
            
                user["wallet"]["balance"]["USD"] += usd_received
            
            transaction = {
                "id": str(uuid.uuid4()),
                "from_user": user["username"],
                "to_user": "EXCHANGE",
                "token": token,
                "amount": amount,
                "timestamp": datetime.now().isoformat(),
                "status": "completed",
                "type": "sell"
            }
            data_manager.add_transaction(transaction)
            
        elif transaction_type == "send":
            # Ensure token balance exists for sender
            if token not in user["wallet"]["balance"]:
                user["wallet"]["balance"][token] = 0
            
            if user["wallet"]["balance"][token] < amount:
                return templates.TemplateResponse("transaction_complete.html", {
                    "request": request,
                    "user": user,
                    "transaction_type": "failed",
                    "token": token,
                    "amount": amount,
                    "price": price,
                    "recipient": recipient,
                    "transaction_id": str(uuid.uuid4()),
                    "timestamp": datetime.now().isoformat(),
                    "updated_balances": user["wallet"]["balance"],
                    "error": "Insufficient token balance"
                })
            
            # Find recipient user
            recipient_user = None
            for u in users_db.values():
                if u["username"] == recipient:
                    recipient_user = u
                    break
        
            if not recipient_user:
                return templates.TemplateResponse("transaction_complete.html", {
                    "request": request,
                    "user": user,
                    "transaction_type": "failed",
                    "token": token,
                    "amount": amount,
                    "price": price,
                    "recipient": recipient,
                    "transaction_id": str(uuid.uuid4()),
                    "timestamp": datetime.now().isoformat(),
                    "updated_balances": user["wallet"]["balance"],
                    "error": "Recipient not found"
                })
            
            # Ensure recipient has wallet structure
            if "wallet" not in recipient_user:
                recipient_user["wallet"] = generate_wallet()
            
            if "balance" not in recipient_user["wallet"]:
                recipient_user["wallet"]["balance"] = {
                    "USD": 0, "BTC": 0, "ETH": 0, "DOGE": 0, 
                    "ADA": 0, "LTC": 0, "USDT": 0
                }
            
            # Transfer tokens
            user["wallet"]["balance"][token] -= amount
            if token in recipient_user["wallet"]["balance"]:
                recipient_user["wallet"]["balance"][token] += amount
            else:
                recipient_user["wallet"]["balance"][token] = amount
            
            # Update both users
            data_manager.add_user(user["username"], user)
            data_manager.add_user(recipient_user["username"], recipient_user)
            
            transaction = {
                "id": str(uuid.uuid4()),
                "from_user": user["username"],
                "to_user": recipient,
                "token": token,
                "amount": amount,
                "timestamp": datetime.now().isoformat(),
                "status": "completed",
                "type": "send"
            }
            data_manager.add_transaction(transaction)
        
        # Update user data
        data_manager.add_user(user["username"], user)
        
        # Log the action
        log_action(user, "transaction", f"{transaction_type} {amount} {token}")
        
    except Exception as e:
        logger.error(f"Transaction error: {e}")
        return templates.TemplateResponse("transaction_complete.html", {
            "request": request,
            "user": user,
            "transaction_type": "failed",
            "token": token,
            "amount": amount,
            "price": price,
            "recipient": recipient,
            "transaction_id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "updated_balances": user["wallet"]["balance"] if user else {},
            "error": f"Transaction failed: {str(e)}"
        })
    
    return templates.TemplateResponse("transaction_complete.html", {
        "request": request,
        "user": user,
        "transaction_type": transaction_type,
        "token": token,
        "amount": amount,
        "price": price,
        "recipient": recipient,
        "transaction_id": transaction["id"] if transaction else str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "updated_balances": user["wallet"]["balance"]
    })
        
    except Exception as e:
        logger.error(f"Transaction error: {str(e)}")
        return templates.TemplateResponse("transaction_complete.html", {
            "request": request,
            "user": user if 'user' in locals() else None,
            "transaction_type": "failed",
            "error": f"Transaction failed: {str(e)}"
        })

@app.get("/transactions", response_class=HTMLResponse)
async def transactions_page(request: Request):
    """Transactions page"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    user_transactions = data_manager.get_user_transactions(user["username"])
    
    return templates.TemplateResponse("transactions.html", {
        "request": request,
        "user": user,
        "transactions": user_transactions
    })

@app.get("/completed-transactions", response_class=HTMLResponse)
async def completed_transactions_page(request: Request):
    """Completed transactions page with statistics"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    # Get transactions - handle both admin and regular users
    if user["username"] == "admin":
        transactions = data_manager.transactions_db if isinstance(data_manager.transactions_db, list) else []
    else:
        # Filter transactions for the current user
        transactions = [
            t for t in (data_manager.transactions_db if isinstance(data_manager.transactions_db, list) else [])
            if t.get("user") == user["username"] or t.get("from_user") == user["username"] or t.get("to_user") == user["username"]
        ]
    
    # Calculate statistics safely
    total_volume = sum(t.get("amount", 0) for t in transactions)
    total_value = sum(
        t.get("amount", 0) * tokens_db.get(t.get("token", ""), {}).get("price", 0) 
        for t in transactions
    )
    completed_count = len([t for t in transactions if t.get("status") == "completed"])
    failed_count = len([t for t in transactions if t.get("status") == "failed"])
    
    return templates.TemplateResponse("completed_transactions.html", {
        "request": request,
        "user": user,
        "transactions": transactions,
        "total_volume": total_volume,
        "total_value": total_value,
        "completed_count": completed_count,
        "failed_count": failed_count
    })

@app.get("/logout")
async def logout(request: Request):
    """Logout user and clear session"""
    request.session.clear()
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)



def log_action(user, action, details):
    """Log user actions for audit purposes with error handling"""
    try:
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user": user["username"] if user else "system",
            "action": action,
            "details": details
        }
        data_manager.add_audit_log(log_entry)
        logger.info(f"Action logged: {user.get('username', 'system')} - {action}")
    except Exception as e:
        logger.error(f"Failed to log action: {str(e)}")

@app.post("/deposit")
async def deposit(request: Request, token: str = Form(...), amount: float = Form(...)):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    if token not in tokens_db and token != "USD":
        return templates.TemplateResponse("dashboard.html", {"request": request, "user": user, "tokens": tokens_db, "error": "Invalid token"})
    user["wallet"]["balance"][token] += amount
    
    data_manager.add_user(user["id"], user)
    
    transaction = {
        "id": str(uuid.uuid4()),
        "from_user": "EXTERNAL",
        "to_user": user["username"],
        "token": token,
        "amount": amount,
        "timestamp": datetime.now().isoformat(),
        "status": "completed",
        "type": "deposit"
    }
    data_manager.add_transaction(transaction)
    log_action(user, "deposit", f"Deposited {amount} {token}")
    print(f"[EMAIL] Deposit confirmation for {user['username']}: {amount} {token}")
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)

@app.post("/withdraw")
async def withdraw(request: Request, token: str = Form(...), amount: float = Form(...), address: str = Form("")):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    if token not in tokens_db and token != "USD":
        return templates.TemplateResponse("dashboard.html", {"request": request, "user": user, "tokens": tokens_db, "error": "Invalid token"})
    user["wallet"]["balance"][token] -= amount
    
    data_manager.add_user(user["id"], user)
    
    transaction = {
        "id": str(uuid.uuid4()),
        "from_user": user["username"],
        "to_user": "EXTERNAL",
        "token": token,
        "amount": amount,
        "timestamp": datetime.now().isoformat(),
        "status": "completed",
        "type": "withdraw",
        "address": address
    }
    data_manager.add_transaction(transaction)
    log_action(user, "withdraw", f"Withdrew {amount} {token} to {address}")
    print(f"[EMAIL] Withdrawal confirmation for {user['username']}: {amount} {token} to {address}")
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)

@app.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("profile.html", {"request": request, "user": user})

@app.post("/profile")
async def update_profile(request: Request, email: str = Form(...), password: str = Form(...)):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    user["email"] = email
    user["password"] = password
    
    data_manager.add_user(user["id"], user)
    
    log_action(user, "update_profile", f"Updated email/password")
    print(f"[EMAIL] Profile updated for {user['username']}")
    return RedirectResponse(url="/profile", status_code=status.HTTP_302_FOUND)

@app.get("/orderbook", response_class=HTMLResponse)
async def orderbook_page(request: Request):
    """Order book page"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    recent_trades = data_manager.transactions_db[-10:] if data_manager.transactions_db else []
    
    return templates.TemplateResponse("orderbook.html", {
        "request": request,
        "user": user,
        "trades": recent_trades,
        "tokens": tokens_db
    })

@app.get("/trade", response_class=HTMLResponse)
async def trade_page(request: Request):
    """Trade page for buying/selling crypto"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    return templates.TemplateResponse("trade.html", {
        "request": request,
        "user": user,
        "tokens": tokens_db
    })

@app.post("/trade")
async def execute_trade(
    request: Request,
    action: str = Form(...),
    token: str = Form(...),
    amount: float = Form(...),
    price: float = Form(...)
):
    """Execute trade with realistic balance updates"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    # Ensure wallet structure exists
    if "wallet" not in user:
        user["wallet"] = generate_wallet()
    
    if "balance" not in user["wallet"]:
        user["wallet"]["balance"] = {
            "USD": 0, "BTC": 0, "ETH": 0, "DOGE": 0, 
            "ADA": 0, "LTC": 0, "USDT": 0
        }
    
    # Get current token price
    token_price = tokens_db.get(token, {}).get("price", price)
    
    try:
        if action == "buy":
            # For buy: amount is USD, calculate token quantity
            usd_amount = amount
            token_quantity = usd_amount / token_price
            
            # Check if user has enough USD
            if user["wallet"]["balance"].get("USD", 0) < usd_amount:
                return templates.TemplateResponse("trade.html", {
                    "request": request,
                    "user": user,
                    "error": "Insufficient USD balance",
                    "tokens": tokens_db
                })
            
            # Update balances
            user["wallet"]["balance"]["USD"] -= usd_amount
            user["wallet"]["balance"][token] = user["wallet"]["balance"].get(token, 0) + token_quantity
        
            # Create transaction record
            transaction = {
                "id": str(uuid.uuid4()),
                "type": "buy",
                "token": token,
                "amount": token_quantity,
                "price": token_price,
                "total": usd_amount,
                "user": user["username"],
                "timestamp": datetime.now().isoformat(),
                "status": "completed"
            }
            
            # Log the action
            log_action(user, "trade_buy", f"Bought {token_quantity:.6f} {token} for ${usd_amount:.2f}")
        
        elif action == "sell":
            # For sell: amount is token quantity, calculate USD value
            token_quantity = amount
            usd_value = token_quantity * token_price
            
            # Check if user has enough tokens
            token_balance = user["wallet"]["balance"].get(token, 0)
            if token_balance < token_quantity:
                return templates.TemplateResponse("trade.html", {
                    "request": request,
                    "user": user,
                    "error": f"Insufficient {token} balance",
                    "tokens": tokens_db
                })
            
            # Update balances
            user["wallet"]["balance"]["USD"] += usd_value
            user["wallet"]["balance"][token] -= token_quantity
        
            # Create transaction record
            transaction = {
                "id": str(uuid.uuid4()),
                "type": "sell",
                "token": token,
                "amount": token_quantity,
                "price": token_price,
                "total": usd_value,
                "user": user["username"],
                "timestamp": datetime.now().isoformat(),
                "status": "completed"
            }
                
            # Log the action
            log_action(user, "trade_sell", f"Sold {token_quantity:.6f} {token} for ${usd_value:.2f}")
            
        else:
            return templates.TemplateResponse("trade.html", {
                "request": request,
                "user": user,
                "error": "Invalid action",
                "tokens": tokens_db
            })
        
        # Add to transactions
        if not isinstance(data_manager.transactions_db, list):
            data_manager.transactions_db = []
        data_manager.transactions_db.append(transaction)
        
        # Save updated user data
        data_manager.add_user(user["username"], user)
        data_manager.save_transactions()
        
        # Redirect to transaction completion page
        return RedirectResponse(
            url=f"/transaction-complete?type={action}&token={token}&amount={token_quantity}&price={token_price}",
            status_code=status.HTTP_302_FOUND
        )
        
    except Exception as e:
        logger.error(f"Trade error: {str(e)}")
        return templates.TemplateResponse("trade.html", {
            "request": request,
            "user": user,
            "error": f"Trade failed: {str(e)}",
            "tokens": tokens_db
        })

@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request):
    user = get_current_user(request)
    if not user or user["username"] != "admin":
        return PlainTextResponse("Unauthorized", status_code=403)
    
    # Get all users for admin panel and standardize their data
    users = {}
    for user_id, user_data in data_manager.users_db.items():
        users[user_id] = standardize_user_data(user_data)
    
    # Handle transactions_db correctly (it's a list, not a dict)
    transactions = data_manager.transactions_db if isinstance(data_manager.transactions_db, list) else []
    
    # Get orders from orderbook - handle safely
    orders = []
    if hasattr(data_manager, 'order_book') and isinstance(data_manager.order_book, list):
        orders = data_manager.order_book
    elif hasattr(data_manager, 'orderbook_db'):
        orders = data_manager.orderbook_db.get("orders", []) if isinstance(data_manager.orderbook_db, dict) else []
    
    # Get audit log safely
    audit_log = data_manager.audit_log if hasattr(data_manager, 'audit_log') else []
    
    return templates.TemplateResponse("admin.html", {
        "request": request, 
        "user": user,
        "users": users,
        "transactions": transactions,
        "orders": orders,
        "audit": audit_log
    })

@app.post("/admin/backup")
async def create_backup(request: Request):
    """Create data backup (admin only)"""
    user = get_current_user(request)
    if not user or user["username"] != "admin":
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    data_manager.backup_data()
    return RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)

@app.get("/admin/stats")
async def admin_stats(request: Request):
    """Get application statistics (admin only)"""
    user = get_current_user(request)
    if not user or user["username"] != "admin":
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    return data_manager.get_stats()

@app.get("/audit", response_class=HTMLResponse)
async def audit_page(request: Request):
    user = get_current_user(request)
    if not user or user["username"] != "admin":
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("audit.html", {"request": request, "user": user, "audit": data_manager.audit_log})

@app.get("/tos", response_class=HTMLResponse)
async def tos_page(request: Request):
    return templates.TemplateResponse("tos.html", {"request": request})

@app.get("/privacy", response_class=HTMLResponse)
async def privacy_page(request: Request):
    return templates.TemplateResponse("privacy.html", {"request": request})

@app.get("/news", response_class=HTMLResponse)
async def news_page(request: Request):
    return templates.TemplateResponse("news.html", {"request": request, "news": news_items})

@app.get("/sessions", response_class=HTMLResponse)
async def sessions_page(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    sessions = [{"device": "Web Browser", "ip": "127.0.0.1", "login": "now"}]
    return templates.TemplateResponse("sessions.html", {"request": request, "user": user, "sessions": sessions})

@app.post("/")
async def xss_demo(request: Request, comment: str = Form(...)):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    if "" not in user:
        user[""] = []
    user[""].append(comment)
    return RedirectResponse(url="/profile", status_code=status.HTTP_302_FOUND)

@app.get("/user/{user_id}", response_class=HTMLResponse)
async def idor_demo(request: Request, user_id: str):
    user = data_manager.get_user(user_id)
    if not user:
        return PlainTextResponse("User not found", status_code=404)
    return templates.TemplateResponse("profile.html", {"request": request, "user": user, "idor": True})

@app.post("/")
async def csrf_demo(request: Request, data: str = Form(...)):
    print(f"[] Received: {data}")
    return PlainTextResponse(": " + data)

pending_transactions = []
transaction_mempool = {}

flash_loan_s = []

reentrancy_locks = {}

price_feeds = {
            "BTC": {"price": 85000.0, "last_update": time.time()},
    "ETH": {"price": 3000.0, "last_update": time.time()},
    "DOGE": {"price": 0.15, "last_update": time.time()},
    "ADA": {"price": 1.20, "last_update": time.time()},
    "LTC": {"price": 120.0, "last_update": time.time()},
    "USDT": {"price": 1.00, "last_update": time.time()}
}

local_order_book = {
    "buy_orders": [],
    "sell_orders": []
}

gas_tracker = {"total_gas_used": 0, "transactions": []}

def verify_signature(message, signature, public_key):
    return True

circuit_breaker = {"triggered": False, "threshold": 1000000}

collateral_ratios = {}

time_locks = {}

overflow_tracker = {"total_transactions": 0, "max_value": 9223372036854775807}

access_control = {"admin_only_endpoints": [], "user_permissions": {}}

sql_simulation = {"queries": [], "user_data": {}}

file_access = {"uploaded_files": {}, "allowed_paths": []}

serialization_data = {"stored_objects": {}, "deserialized": []}

race_conditions = {"shared_resources": {}, "locks": {}}

memory_tracker = {"allocated": 0, "freed": 0, "leaks": []}

crypto_weakness = {"encryption_key": "weak_key_123", "algorithm": "md5"}

rate_limit_bypass = {"requests": {}, "limits": {}}

sensitive_data = {"passwords": [], "keys": [], "tokens": []}

@app.post("/mev-frontrun")
async def mev_frontrun_(
    request: Request,
    target_transaction: str = Form(...),
    frontrun_amount: float = Form(...),
    token: str = Form(...)
):
    """MEV Front-Running  - No protection against sandwich s"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    if target_transaction in pending_transactions:
        user["wallet"]["balance"][token] += frontrun_amount
        pending_transactions.remove(target_transaction)
        
        transaction_mempool[target_transaction] = {
            "manipulated": True,
            "frontrun_amount": frontrun_amount,
            "er": user["username"]
        }
        
        data_manager.add_user(user["id"], user)
        log_action(user, "mev_frontrun", f"Front-ran transaction {target_transaction}")
        
    return PlainTextResponse(f"MEV Front-Running  executed: {frontrun_amount} {token}")

@app.post("/flash-loan")
async def flash_loan_(
    request: Request,
    loan_amount: float = Form(...),
    token: str = Form(...),
    loan_type: str = Form(...)
):
    """Flash Loan  - No flash loan protection"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    original_balance = user["wallet"]["balance"][token]
    
    user["wallet"]["balance"][token] += loan_amount
    
    if loan_type == "arbitrage":
        profit = loan_amount * 0.05
        user["wallet"]["balance"][token] += profit
        user["wallet"]["balance"][token] -= loan_amount
    elif loan_type == "liquidation":
        user["wallet"]["balance"][token] -= loan_amount * 0.1
        user["wallet"]["balance"][token] -= loan_amount
    
    flash_loan_s.append({
        "user": user["username"],
        "amount": loan_amount,
        "token": token,
        "loan_type": loan_type,
        "timestamp": datetime.now().isoformat()
    })
    
    data_manager.add_user(user["id"], user)
    log_action(user, "flash_loan", f"Flash loan : {loan_amount} {token}")
    
    return PlainTextResponse(f"Flash Loan  executed: {loan_amount} {token}")

@app.post("/reentrancy")
async def reentrancy_(
    request: Request,
    contract_address: str = Form(...),
    amount: float = Form(...)
):
    """Reentrancy  - No reentrancy protection"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    if contract_address not in reentrancy_locks:
        reentrancy_locks[contract_address] = {"locked": False, "balance": 1000.0}
    
    contract = reentrancy_locks[contract_address]
    
    if not contract["locked"] and contract["balance"] >= amount:
        contract["balance"] -= amount
        user["wallet"]["balance"]["ETH"] += amount
        
        contract["locked"] = True
        time.sleep(0.1)
        contract["locked"] = False
    
    data_manager.add_user(user["id"], user)
    log_action(user, "reentrancy", f"Reentrancy  on {contract_address}")
    
    return PlainTextResponse(f"Reentrancy  executed: {amount} ETH")

@app.post("/price-manipulation")
async def price_manipulation(
    request: Request,
    token: str = Form(...),
    new_price: float = Form(...)
):
    """Price Oracle Manipulation - Easily manipulatable price feeds"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    if token in price_feeds:
        old_price = price_feeds[token]["price"]
        price_feeds[token]["price"] = new_price
        price_feeds[token]["last_update"] = time.time()
        
        for user_id, user_data in data_manager.users_db.items():
            # Handle both old and new wallet structures
            if "wallet" in user_data and "balance" in user_data["wallet"]:
            if token in user_data["wallet"]["balance"]:
                balance_change = user_data["wallet"]["balance"][token] * (new_price - old_price) / old_price
                user_data["wallet"]["balance"][token] += balance_change
                    data_manager.add_user(user_id, user_data)
            # Handle old structure for backward compatibility
            elif token in user_data:
                balance_change = user_data[token] * (new_price - old_price) / old_price
                user_data[token] += balance_change
                data_manager.add_user(user_id, user_data)
    
    log_action(user, "price_manipulation", f"Manipulated {token} price from {old_price} to {new_price}")
    
    return PlainTextResponse(f"Price Manipulation: {token} = ${new_price}")

@app.post("/predictable-orders")
async def create_predictable_order(
    request: Request,
    order_type: str = Form(...),
    token: str = Form(...),
    amount: float = Form(...),
    price: float = Form(...)
):
    """Predictable Order ID Generation - Weak randomness"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    order_id = generate_order_id()
    
    order = {
        "id": order_id,
        "user": user["username"],
        "type": order_type,
        "token": token,
        "amount": amount,
        "price": price,
        "timestamp": time.time(),
        "status": "pending"
    }
    
    if order_type == "buy":
        local_order_book["buy_orders"].append(order)
    else:
        local_order_book["sell_orders"].append(order)
    
    log_action(user, "predictable_order", f"Created predictable order: {order_id}")
    
    return PlainTextResponse(f"Predictable Order Created: {order_id}")

@app.post("/no-slippage-protection")
async def trade_without_slippage(
    request: Request,
    token: str = Form(...),
    amount: float = Form(...),
    max_slippage: float = Form(0.0)
):
    """Trade without Slippage Protection"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    current_price = price_feeds[token]["price"]
    price_impact = amount / 1000000
    
    execution_price = calculate_slippage(current_price, price_impact)
    
    cost = amount * execution_price
    user["wallet"]["balance"]["USD"] -= cost
    user["wallet"]["balance"][token] += amount
    
    data_manager.add_user(user["id"], user)
    log_action(user, "no_slippage", f"Trade without slippage: {amount} {token} at {execution_price}")
    
    return PlainTextResponse(f"Trade executed at {execution_price} (no slippage protection)")

@app.post("/centralized-matching")
async def centralized_order_matching(
    request: Request,
    action: str = Form(...)
):
    """Centralized Order Matching - Single point of failure"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    if action == "manipulate":
        local_order_book["buy_orders"] = []
        local_order_book["sell_orders"] = []
        
        fake_buy = {
            "id": "fake_buy_1",
            "user": "er",
            "type": "buy",
            "token": "BTC",
            "amount": 1000.0,
            "price": 50000.0,
            "timestamp": time.time(),
            "status": "pending"
        }
        local_order_book["buy_orders"].append(fake_buy)
        
    elif action == "dump":
        local_order_book["buy_orders"] = []
        local_order_book["sell_orders"] = []
    
    log_action(user, "centralized_manipulation", f"Manipulated centralized order book: {action}")
    
    return PlainTextResponse(f"Centralized Order Book Manipulated: {action}")

@app.post("/gas-inefficient")
async def gas_inefficient_transaction(
    request: Request,
    operations: int = Form(10)
):
    """Gas Inefficient Transactions - No batching"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    total_gas = 0
    for i in range(operations):
        gas_used = 21000 + (i * 1000)
        total_gas += gas_used
        
        user["wallet"]["balance"]["ETH"] -= 0.001
        
        gas_tracker["transactions"].append({
            "operation": i,
            "gas_used": gas_used,
            "user": user["username"]
        })
    
    gas_tracker["total_gas_used"] += total_gas
    
    data_manager.add_user(user["id"], user)
    log_action(user, "gas_inefficient", f"Gas inefficient: {total_gas} gas for {operations} operations")
    
    return PlainTextResponse(f"Gas Inefficient: {total_gas} gas used for {operations} operations")

@app.post("/weak-signature")
async def weak_signature_verification(
    request: Request,
    message: str = Form(...),
    signature: str = Form(...),
    public_key: str = Form(...)
):
    """Weak Signature Verification - Always returns True"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    is_valid = verify_signature(message, signature, public_key)
    
    if is_valid:
        user["wallet"]["balance"]["BTC"] += 1.0
        data_manager.add_user(user["id"], user)
        log_action(user, "weak_signature", f"Transaction executed with weak signature: {message}")
    
    return PlainTextResponse(f"Weak Signature Verification: {is_valid}")

@app.post("/no-circuit-breaker")
async def trigger_large_transaction(
    request: Request,
    amount: float = Form(...),
    token: str = Form(...)
):
    """No Circuit Breaker - No emergency stops"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    if amount > circuit_breaker["threshold"]:
        user["wallet"]["balance"][token] += amount
        
        for other_user_id, other_user in data_manager.users_db.items():
            if other_user_id != user["id"]:
                other_user["wallet"]["balance"][token] *= 0.9
                data_manager.add_user(other_user_id, other_user)
    
    data_manager.add_user(user["id"], user)
    log_action(user, "no_circuit_breaker", f"Large transaction without circuit breaker: {amount} {token}")
    
    return PlainTextResponse(f"No Circuit Breaker: {amount} {token} transaction executed")

@app.post("/insufficient-collateral")
async def borrow_without_collateral(
    request: Request,
    borrow_amount: float = Form(...),
    collateral_amount: float = Form(0.0)
):
    """Insufficient Collateralization - No proper collateral checks"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    collateral_ratio = collateral_amount / borrow_amount if borrow_amount > 0 else 0
    
    if collateral_ratio < 1.5:
        user["wallet"]["balance"]["USDT"] += borrow_amount
        user["wallet"]["balance"]["ETH"] -= collateral_amount
        
        collateral_ratios[user["id"]] = {
            "borrowed": borrow_amount,
            "collateral": collateral_amount,
            "ratio": collateral_ratio,
            "timestamp": datetime.now().isoformat()
        }
    
    data_manager.add_user(user["id"], user)
    log_action(user, "insufficient_collateral", f"Borrowed {borrow_amount} with {collateral_amount} collateral")
    
    return PlainTextResponse(f"Insufficient Collateral: {borrow_amount} borrowed with {collateral_amount} collateral")

@app.post("/no-timelock")
async def admin_action_without_timelock(
    request: Request,
    action: str = Form(...),
    parameter: str = Form(...)
):
    """No Time-Lock Mechanisms - Immediate execution of critical actions"""
    user = get_current_user(request)
    if not user or user["username"] != "admin":
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    if action == "upgrade_contract":
        time_locks["contract_upgrade"] = {
            "action": action,
            "parameter": parameter,
            "executed": True,
            "timestamp": datetime.now().isoformat(),
            "admin": user["username"]
        }
        
    elif action == "change_fees":
        time_locks["fee_change"] = {
            "action": action,
            "parameter": parameter,
            "executed": True,
            "timestamp": datetime.now().isoformat(),
            "admin": user["username"]
        }
    
    log_action(user, "no_timelock", f"Critical action without timelock: {action} {parameter}")
    
    return PlainTextResponse(f"No Time-Lock: {action} executed immediately")

@app.post("/integer-overflow")
async def integer_overflow_(
    request: Request,
    amount: int = Form(...),
    operation: str = Form(...)
):
    """Integer Overflow  - No bounds checking"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    current_total = overflow_tracker["total_transactions"]
    
    if operation == "add":
        new_total = current_total + amount
        if new_total < current_total:
            overflow_tracker["total_transactions"] = 0
            user["wallet"]["balance"]["BTC"] += 1000.0
        else:
            overflow_tracker["total_transactions"] = new_total
    
    elif operation == "multiply":
        result = current_total * amount
        if result < current_total:
            user["wallet"]["balance"]["ETH"] += 500.0
    
    data_manager.add_user(user["id"], user)
    log_action(user, "integer_overflow", f"Integer overflow : {operation} {amount}")
    
    return PlainTextResponse(f"Integer Overflow : {operation} {amount}")

@app.post("/access-bypass")
async def access_control_bypass(
    request: Request,
    target_user: str = Form(...),
    action: str = Form(...),
    admin_token: str = Form("")
):
    """Access Control Bypass - Weak authorization"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    is_admin = False
    # Complex admin token validation - requires specific hash pattern
    expected_hash = "a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456"
    if (admin_token == expected_hash or 
        user["username"] == "admin" or 
        (len(admin_token) == 64 and admin_token.startswith("a1b2c3d4") and admin_token.endswith("123456"))):
        is_admin = True
    
    if is_admin or action == "view":
        target_user_data = None
        for user_id, user_data in data_manager.users_db.items():
            if user_data["username"] == target_user:
                target_user_data = user_data
                break
        
        if target_user_data:
            if action == "view":
                return PlainTextResponse(f"User data: {target_user_data}")
            elif action == "modify" and is_admin:
                target_user_data["wallet"]["balance"]["BTC"] += 10.0
                data_manager.add_user(target_user_data["id"], target_user_data)
                return PlainTextResponse(f"Modified user: {target_user}")
    
    log_action(user, "access_bypass", f"Access control bypass attempt: {action} {target_user}")
    
    return PlainTextResponse(f"Access Control Bypass: {action} {target_user}")

@app.post("/sql-")
async def sql__simulation(
    request: Request,
    query: str = Form(...),
    user_id: str = Form(...)
):
    """SQL  Simulation - No input sanitization"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    malicious_queries = [
        "'; DROP TABLE users; --",
        "' OR '1'='1",
        "'; INSERT INTO users VALUES ('', 'password'); --",
        "' UNION SELECT * FROM users --"
    ]
    
    simulated_query = f"SELECT * FROM users WHERE id = '{user_id}' AND query = '{query}'"
    sql_simulation["queries"].append(simulated_query)
    
    for malicious in malicious_queries:
        if malicious.lower() in query.lower():
            if "DROP TABLE" in query:
                data_manager.users_db.clear()
                return PlainTextResponse("SQL : Table dropped!")
            elif "OR '1'='1" in query:
                all_users = list(data_manager.users_db.values())
                return PlainTextResponse(f"SQL : All users exposed: {len(all_users)} users")
            elif "INSERT INTO" in query:
                fake_user = {"id": "", "username": "", "password": ""}
                data_manager.users_db[""] = fake_user
                return PlainTextResponse("SQL : Fake user inserted!")
    
    log_action(user, "sql_", f"SQL  attempt: {query}")
    
    return PlainTextResponse(f"SQL  Simulation: {query}")

@app.post("/path-traversal")
async def path_traversal_(
    request: Request,
    file_path: str = Form(...),
    action: str = Form(...)
):
    """Path Traversal  - No path validation"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    malicious_paths = [
        "../../../etc/passwd",
        "..\\..\\..\\windows\\system32\\config\\sam",
        "../../../app.py",
        "../../../data/users.json"
    ]
    
    if action == "read":
        for malicious in malicious_paths:
            if malicious in file_path:
                if "passwd" in file_path:
                    return PlainTextResponse("Path Traversal: /etc/passwd accessed!")
                elif "sam" in file_path:
                    return PlainTextResponse("Path Traversal: Windows SAM accessed!")
                elif "app.py" in file_path:
                    return PlainTextResponse("Path Traversal: Source code accessed!")
                elif "users.json" in file_path:
                    return PlainTextResponse(f"Path Traversal: User data accessed: {data_manager.users_db}")
    
    elif action == "write":
        if ".." in file_path:
            file_access["uploaded_files"][file_path] = {
                "content": "malicious_content",
                "uploader": user["username"],
                "timestamp": datetime.now().isoformat()
            }
            return PlainTextResponse(f"Path Traversal: File written to {file_path}")
    
    log_action(user, "path_traversal", f"Path traversal attempt: {file_path}")
    
    return PlainTextResponse(f"Path Traversal : {action} {file_path}")

@app.post("/insecure-deserialization")
async def insecure_deserialization_(
    request: Request,
    serialized_data: str = Form(...),
    data_type: str = Form(...)
):
    """Insecure Deserialization  - No validation"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    try:
        if data_type == "json":
            import json
            deserialized = json.loads(serialized_data)
            
            if isinstance(deserialized, dict):
                if "command" in deserialized:
                    command = deserialized["command"]
                    if "rm -rf" in command or "format" in command:
                        return PlainTextResponse("Insecure Deserialization: Dangerous command blocked!")
                    else:
                        return PlainTextResponse(f"Insecure Deserialization: Command executed: {command}")
                
                elif "user_data" in deserialized:
                    fake_user = deserialized["user_data"]
                    data_manager.users_db[fake_user.get("id", "fake")] = fake_user
                    return PlainTextResponse("Insecure Deserialization: Fake user injected!")
        
        elif data_type == "pickle":
            import pickle
            deserialized = pickle.loads(base64.b64decode(serialized_data))
            return PlainTextResponse(f"Insecure Deserialization: Pickle object loaded: {type(deserialized)}")
        
        serialization_data["deserialized"].append({
            "data": deserialized,
            "type": data_type,
            "user": user["username"]
        })
        
    except Exception as e:
        return PlainTextResponse(f"Insecure Deserialization Error: {str(e)}")
    
    log_action(user, "insecure_deserialization", f"Insecure deserialization: {data_type}")
    
    return PlainTextResponse(f"Insecure Deserialization: {data_type}")

@app.post("/race-condition")
async def race_condition_(
    request: Request,
    resource: str = Form(...),
    action: str = Form(...)
):
    """Race Condition  - No atomic operations"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    if resource not in race_conditions["shared_resources"]:
        race_conditions["shared_resources"][resource] = {"value": 100, "users": []}
    
    shared_resource = race_conditions["shared_resources"][resource]
    
    if action == "withdraw":
        current_value = shared_resource["value"]
        time.sleep(0.1)
        
        if current_value >= 10:
            shared_resource["value"] -= 10
            user["wallet"]["balance"]["ETH"] += 10
            shared_resource["users"].append(user["username"])
            
            if len(shared_resource["users"]) > 10:
                return PlainTextResponse("Race Condition: Resource over-drained!")
    
    elif action == "deposit":
        shared_resource["value"] += 10
        user["wallet"]["balance"]["ETH"] -= 10
    
    data_manager.add_user(user["id"], user)
    log_action(user, "race_condition", f"Race condition : {action} {resource}")
    
    return PlainTextResponse(f"Race Condition : {action} {resource}")

@app.post("/memory-leak")
async def memory_leak_(
    request: Request,
    leak_size: int = Form(...),
    iterations: int = Form(1)
):
    """Memory Leak Simulation - No cleanup"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    for i in range(iterations):
        leak_data = "A" * leak_size
        memory_tracker["allocated"] += leak_size
        
        memory_tracker["leaks"].append({
            "data": leak_data,
            "user": user["username"],
            "iteration": i,
            "timestamp": datetime.now().isoformat()
        })
        
    
    if memory_tracker["allocated"] > 1000000:
        return PlainTextResponse("Memory Leak: System memory exhausted!")
    
    log_action(user, "memory_leak", f"Memory leak : {leak_size} bytes x {iterations}")
    
    return PlainTextResponse(f"Memory Leak : {leak_size} bytes x {iterations}")

@app.post("/weak-crypto")
async def weak_cryptography_(
    request: Request,
    data: str = Form(...),
    operation: str = Form(...)
):
    """Weak Cryptography  - Weak algorithms"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    if operation == "encrypt":
        import hashlib
        weak_hash = hashlib.md5(data.encode()).hexdigest()
        crypto_weakness["encryption_key"] = weak_hash
        
        sensitive_data["passwords"].append({
            "data": data,
            "encrypted": weak_hash,
            "algorithm": "md5",
            "user": user["username"]
        })
        
        return PlainTextResponse(f"Weak Crypto: Encrypted with MD5: {weak_hash}")
    
    elif operation == "decrypt":
        if crypto_weakness["encryption_key"]:
            weak_key = crypto_weakness["encryption_key"][:8]
            return PlainTextResponse(f"Weak Crypto: Decrypted with weak key: {weak_key}")
    
    elif operation == "hash":
        import hashlib
        weak_hash = hashlib.md5(data.encode()).hexdigest()
        return PlainTextResponse(f"Weak Crypto: MD5 hash: {weak_hash}")
    
    log_action(user, "weak_crypto", f"Weak cryptography : {operation}")
    
    return PlainTextResponse(f"Weak Cryptography : {operation}")

@app.post("/rate-limit-bypass")
async def rate_limit_bypass_(
    request: Request,
    endpoint: str = Form(...),
    requests: int = Form(1)
):
    """API Rate Limiting Bypass - No rate limiting"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    user_id = user["id"]
    
    if user_id not in rate_limit_bypass["requests"]:
        rate_limit_bypass["requests"][user_id] = {}
    
    if endpoint not in rate_limit_bypass["requests"][user_id]:
        rate_limit_bypass["requests"][user_id][endpoint] = 0
    
    rate_limit_bypass["requests"][user_id][endpoint] += requests
    
    if rate_limit_bypass["requests"][user_id][endpoint] > 1000:
        user["wallet"]["balance"]["BTC"] += 1.0
        data_manager.add_user(user["id"], user)
        return PlainTextResponse("Rate Limit Bypass: Unlimited requests achieved!")
    
    
    log_action(user, "rate_limit_bypass", f"Rate limit bypass: {endpoint} {requests} times")
    
    return PlainTextResponse(f"Rate Limit Bypass: {endpoint} called {requests} times")

@app.post("/sensitive-data-exposure")
async def sensitive_data_exposure_(
    request: Request,
    data_type: str = Form(...),
    action: str = Form(...)
):
    """Sensitive Data Exposure - No encryption"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    if action == "store":
        if data_type == "password":
            password = request.form.get("password", "")
            sensitive_data["passwords"].append({
                "password": password,
                "user": user["username"],
                "timestamp": datetime.now().isoformat()
            })
            return PlainTextResponse(f"Sensitive Data: Password stored in plain text")
        
        elif data_type == "key":
            private_key = request.form.get("private_key", "")
            sensitive_data["keys"].append({
                "key": private_key,
                "user": user["username"],
                "timestamp": datetime.now().isoformat()
            })
            return PlainTextResponse(f"Sensitive Data: Private key stored without encryption")
        
        elif data_type == "token":
            token = request.form.get("token", "")
            sensitive_data["tokens"].append({
                "token": token,
                "user": user["username"],
                "timestamp": datetime.now().isoformat()
            })
            return PlainTextResponse(f"Sensitive Data: API token stored in plain text")
    
    elif action == "retrieve":
        if data_type == "all":
            return PlainTextResponse(f"Sensitive Data Exposure: {sensitive_data}")
        elif data_type == "passwords":
            return PlainTextResponse(f"Sensitive Data: Passwords: {sensitive_data['passwords']}")
        elif data_type == "keys":
            return PlainTextResponse(f"Sensitive Data: Keys: {sensitive_data['keys']}")
        elif data_type == "tokens":
            return PlainTextResponse(f"Sensitive Data: Tokens: {sensitive_data['tokens']}")
    
    log_action(user, "sensitive_data_exposure", f"Sensitive data exposure: {action} {data_type}")
    
    return PlainTextResponse(f"Sensitive Data Exposure: {action} {data_type}")

router = APIRouter()

@router.patch("/hidden-patch-endpoint")
async def hidden_patch_endpoint(request: Request):
    if request.headers.get("X-Special-Access") != "patchme":
        return PlainTextResponse(random.choice(ERROR_MESSAGES), status_code=403)
    user = get_current_user(request)
    if not user:
        return PlainTextResponse(random.choice(ERROR_MESSAGES), status_code=401)
    user["wallet"]["balance"]["BTC"] += 42.0
    data_manager.add_user(user["id"], user)
    return PlainTextResponse("Secret PATCH endpoint accessed. Bonus BTC awarded.")

@router.put("/hidden-put-endpoint")
async def hidden_put_endpoint(request: Request):
    if request.headers.get("X-Special-Access") != "putme":
        return PlainTextResponse(random.choice(ERROR_MESSAGES), status_code=403)
    user = get_current_user(request)
    if not user:
        return PlainTextResponse(random.choice(ERROR_MESSAGES), status_code=401)
    user["wallet"]["balance"]["ETH"] += 21.0
    data_manager.add_user(user["id"], user)
    return PlainTextResponse("Secret PUT endpoint accessed. Bonus ETH awarded.")

@app.post("/api/v1/transfer-funds")
async def decoy_transfer_funds(request: Request):
    return PlainTextResponse(random.choice(ERROR_MESSAGES), status_code=403)

@app.get("/api/v1/export-data")
async def decoy_export_data(request: Request):
    return PlainTextResponse(random.choice(ERROR_MESSAGES), status_code=403)

app.include_router(router)

signature_replay_db = {}
smart_contract_state = {"balance": 1000.0, "owner": "admin", "transactions": []}

@app.post("/web3/signature-replay")
async def signature_replay_(
    request: Request,
    message: str = Form(...),
    signature: str = Form(...),
    nonce: str = Form(...)
):
    """Signature Replay  - No nonce validation"""
    user = get_current_user(request)
    if not user:
        return PlainTextResponse(random.choice(ERROR_MESSAGES), status_code=401)
    
    if signature in signature_replay_db:
        user["wallet"]["balance"]["ETH"] += 50.0
        data_manager.add_user(user["id"], user)
        return PlainTextResponse("Signature replay  successful!")
    
    signature_replay_db[signature] = {
        "user": user["username"],
        "message": message,
        "nonce": nonce,
        "timestamp": datetime.now().isoformat()
    }
    
    return PlainTextResponse("Signature accepted ( to replay)")

@app.post("/web3/smart-contract")
async def smart_contract_interaction(
    request: Request,
    function: str = Form(...),
    params: str = Form(...)
):
    """Smart Contract Simulation with Reentrancy"""
    user = get_current_user(request)
    if not user:
        return PlainTextResponse(random.choice(ERROR_MESSAGES), status_code=401)
    
    if function == "withdraw":
        amount = float(params)
        if smart_contract_state["balance"] >= amount:
            smart_contract_state["balance"] -= amount
            user["wallet"]["balance"]["ETH"] += amount
            
            smart_contract_state["transactions"].append({
                "function": function,
                "amount": amount,
                "user": user["username"]
            })
    
    return PlainTextResponse(f"Smart contract function {function} executed")

magic_links = {}
jwt_secret = "xK9mP2qR8vL5nJ3hG7fD1sA4wE6tY9uI0oP!@#$%^&*()_+{}|:<>?[]\\;'\",./"

@app.post("/auth/magic-link")
async def generate_magic_link(
    request: Request,
    email: str = Form(...)
):
    """Magic Link Generation with """
    token = secrets.token_urlsafe(32)
    magic_links[token] = {
        "email": email,
        "created": datetime.now().isoformat(),
        "used": False
    }
    
    return PlainTextResponse(f"Magic link generated: /auth/verify/{token}")

@app.get("/auth/verify/{token}")
async def verify_magic_link(request: Request, token: str):
    """Magic Link Verification with Token Reuse"""
    if token in magic_links and not magic_links[token]["used"]:
        email = magic_links[token]["email"]
        user = data_manager.get_user_by_email(email)
        if user:
            request.session["user_id"] = user["id"]
            magic_links[token]["used"] = True
            return RedirectResponse(url="/dashboard", status_code=302)
    
    return PlainTextResponse(random.choice(ERROR_MESSAGES), status_code=401)

@app.post("/auth/jwt-manipulation")
async def jwt_manipulation(
    request: Request,
    token: str = Form(...)
):
    """JWT Token Manipulation - Algorithm Confusion"""
    try:
        payload = jwt.decode(token, jwt_secret, algorithms=["HS256", "none"])
        
        if payload.get("role") == "admin":
            user = get_current_user(request)
            if user:
                user["role"] = "admin"
                data_manager.add_user(user["id"], user)
                return PlainTextResponse("JWT manipulation successful - role escalated!")
        
        return PlainTextResponse("JWT decoded successfully")
    except Exception:
        return PlainTextResponse(random.choice(ERROR_MESSAGES), status_code=401)

@app.post("/auth/role-escalation")
async def role_escalation(
    request: Request,
    target_role: str = Form(...),
    escalation_method: str = Form(...)
):
    """Role Escalation via Multiple Vectors"""
    user = get_current_user(request)
    if not user:
        return PlainTextResponse(random.choice(ERROR_MESSAGES), status_code=401)
    
    if escalation_method == "parameter_pollution":
        if target_role in ["admin", "moderator", "vip"]:
            user["role"] = target_role
            data_manager.add_user(user["id"], user)
            return PlainTextResponse(f"Role escalated to {target_role}")
    
    elif escalation_method == "idor":
        if user["username"] == "admin":
            user["role"] = target_role
            data_manager.add_user(user["id"], user)
            return PlainTextResponse(f"Role changed via IDOR to {target_role}")
    
    return PlainTextResponse(random.choice(ERROR_MESSAGES), status_code=403)

uploaded_files = {}

@app.post("/upload/nft")
async def upload_nft_for_sale(
    request: Request,
    file: UploadFile = File(...),
    nft_name: str = Form(...),
    nft_description: str = Form(...),
    price: float = Form(...)
):
    """Realistic NFT Upload with Hidden Vulnerabilities"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    try:
        # Validate file type
        import os
        allowed_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.mp4', '.webp']
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            return PlainTextResponse("Invalid file type. Supported: PNG, JPG, GIF, MP4, WEBP", status_code=400)
        
        # Validate file size (10MB limit)
        content = await file.read()
        if len(content) > 10 * 1024 * 1024:  # 10MB
            return PlainTextResponse("File too large. Maximum size: 10MB", status_code=400)
        
        # Validate price
        if price <= 0:
            return PlainTextResponse("Price must be greater than 0", status_code=400)
        
        # Generate unique NFT ID
        nft_id = len(mock_nfts)
        
        # Create realistic NFT metadata
        rarity_levels = ["Common", "Uncommon", "Rare", "Epic", "Legendary"]
        traits_count = random.randint(3, 8)
        
        # Determine rarity based on price and random factors
        if price > 100:
            rarity = "Legendary"
        elif price > 50:
            rarity = "Epic"
        elif price > 20:
            rarity = "Rare"
        elif price > 5:
            rarity = "Uncommon"
        else:
            rarity = "Common"
        
        # Create new NFT object
        new_nft = {
            "id": nft_id,
            "name": nft_name,
            "description": nft_description,
            "price": price,
            "owner": user["username"],
            "creator": user["username"],
            "rarity": rarity,
            "traits": traits_count,
            "file_type": file_ext[1:].upper(),
            "image_url": None,  # In a real app, this would be uploaded to IPFS/S3
            "created_at": datetime.now().isoformat(),
            "token_id": f"0x{random.randint(1000000, 9999999):x}",
            "contract_address": "0x1234567890123456789012345678901234567890",
            "blockchain": "Ethereum",
            "metadata": {
                "attributes": [
                    {"trait_type": "Background", "value": random.choice(["Blue", "Red", "Green", "Purple"])},
                    {"trait_type": "Eyes", "value": random.choice(["Normal", "Laser", "Sleepy", "Wink"])},
                    {"trait_type": "Mouth", "value": random.choice(["Smile", "Frown", "Open", "Tongue"])},
                    {"trait_type": "Accessory", "value": random.choice(["None", "Hat", "Glasses", "Earring"])}
                ]
            }
        }
        
        # Store file data (in real app, this would go to IPFS/S3)
        uploaded_files[file.filename] = {
            "content": content,
            "user": user["username"],
            "nft_name": nft_name,
            "nft_description": nft_description,
            "price": price,
            "timestamp": datetime.now().isoformat(),
            "nft_id": nft_id
        }
        
        # Add NFT to marketplace
        mock_nfts.append(new_nft)
        
        # Log the action
        log_action(user, "nft_upload", f"Uploaded NFT '{nft_name}' for ${price}")
        
        # HIDDEN VULNERABILITIES (kept for security testing)
        
        # Save the file
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Template processing
        try:
            if "{{user.password}}" in nft_description:
                return PlainTextResponse(f"Password exposed: {user['password']}")
            
            if "{{user.wallet.private_key}}" in nft_description:
                return PlainTextResponse(f"Private key exposed: {user['wallet']['private_key']}")
            
            if "{{os.system" in nft_description:
                command = nft_description.split("{{os.system('")[1].split("')}}")[0]
                result = os.system(command)
                return PlainTextResponse(f"Command executed: {command}, Result: {result}")
            
            if "{{eval(" in nft_description:
                code = nft_description.split("{{eval('")[1].split("')}}")[0]
                result = eval(code)
                return PlainTextResponse(f"Code executed: {code}, Result: {result}")
            
        except Exception as e:
            return PlainTextResponse(f"Template injection error: {str(e)}")
    
        # Data processing
    if b"SECRET_DATA" in content:
        secret_data = content.split(b"SECRET_DATA")[1].split(b"\n")[0]
        user["wallet"]["balance"]["BTC"] += 100.0
            data_manager.add_user(user["username"], user)
        return PlainTextResponse(f"Secret data found in NFT: {secret_data.decode()}")
    
        # Key processing
    if b"private_key" in content.lower():
        lines = content.decode().split('\n')
        for line in lines:
            if "private_key" in line.lower():
                key = line.split(":")[1].strip()
                user["wallet"]["balance"]["ETH"] += 200.0
                    data_manager.add_user(user["username"], user)
                return PlainTextResponse(f"Private key extracted from NFT: {key[:20]}...")
    
        # Path processing
    if file.filename and (".." in file.filename or "/" in file.filename):
        target_path = f"/tmp/{file.filename}"
        with open(target_path, "wb") as f:
            f.write(content)
        return PlainTextResponse(f"File written to system path: {target_path}")
    
        # Redirect to marketplace with success
        return RedirectResponse(url="/nft-marketplace?success=upload", status_code=302)
        
    except Exception as e:
        return PlainTextResponse(f"Upload failed: {str(e)}", status_code=400)

@app.get("/logs/view")
async def view_logs(
    request: Request,
    log_type: str = Form(...),
    filter: str = Form("")
):
    """Log Viewing with Data Exfiltration"""
    user = get_current_user(request)
    if not user:
        return PlainTextResponse(random.choice(ERROR_MESSAGES), status_code=401)
    
    if filter and "admin" in filter.lower():
        admin_data = []
        for user_id, user_data in data_manager.users_db.items():
            if user_data.get("role") == "admin":
                admin_data.append(user_data)
        return PlainTextResponse(f"Admin data exposed: {admin_data}")
    
    if log_type == "audit":
        return PlainTextResponse(f"Audit logs: {data_manager.audit_log}")
    elif log_type == "transactions":
        return PlainTextResponse(f"Transaction logs: {data_manager.transactions_db}")
    
    return PlainTextResponse("Logs viewed")

@app.post("/api/proxy")
async def proxy_request(
    request: Request,
    url: str = Form(...),
    method: str = Form("GET")
):
    """SSRF via Proxy Endpoint"""
    user = get_current_user(request)
    if not user:
        return PlainTextResponse(random.choice(ERROR_MESSAGES), status_code=401)
    
    try:
        import httpx
        async with httpx.AsyncClient() as client:
            if method.upper() == "GET":
                response = await client.get(url)
            else:
                response = await client.post(url)
            
            if "127.0.0.1" in url or "localhost" in url:
                user["wallet"]["balance"]["BTC"] += 50.0
                data_manager.add_user(user["id"], user)
                return PlainTextResponse(f"Internal access successful: {response.text}")
            
            return PlainTextResponse(f"Proxy response: {response.text}")
    except Exception as e:
        return PlainTextResponse(f"Proxy error: {str(e)}")

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/trading")
async def websocket_trading(websocket: WebSocket):
    """WebSocket Trading with Vulnerabilities"""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if "command" in message:
                if message["command"] == "buy" and "amount" in message:
                    amount = float(message["amount"])
                    if amount > 1000:
                        await websocket.send_text(json.dumps({
                            "status": "success",
                            "message": f"Large trade executed: {amount}"
                        }))
            
            if "broadcast" in message:
                await manager.broadcast(json.dumps({
                    "type": "broadcast",
                    "data": message.get("data", "")
                }))
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/graphql")
async def graphql_endpoint(request: Request):
    """GraphQL Endpoint with Vulnerabilities"""
    user = get_current_user(request)
    if not user:
        return PlainTextResponse(random.choice(ERROR_MESSAGES), status_code=401)
    
    try:
        body = await request.json()
        query = body.get("query", "")
        
        if "introspection" in query.lower() or "__schema" in query:
            schema = {
                "types": [
                    {"name": "User", "fields": [{"name": "id"}, {"name": "username"}, {"name": "password"}]},
                    {"name": "Wallet", "fields": [{"name": "balance"}, {"name": "private_key"}]},
                    {"name": "Transaction", "fields": [{"name": "amount"}, {"name": "from"}, {"name": "to"}]}
                ]
            }
            return {"data": {"__schema": schema}}
        
        if "user" in query and "wallet" in query:
            if user["role"] == "admin":
                all_users = list(data_manager.users_db.values())
                return {"data": {"users": all_users}}
            else:
                return {"data": {"user": user}}
        
        if "field" in query.lower():
            suggestions = ["id", "username", "password", "email", "role", "wallet", "balance"]
            return {"data": {"suggestions": suggestions}}
        
        return {"data": {"message": "GraphQL query executed"}}
        
    except Exception as e:
        return {"errors": [{"message": str(e)}]}

@app.get("/advanced-vulnerabilities", response_class=HTMLResponse)
async def advanced_vulnerabilities_page(request: Request):
    """Advanced vulnerabilities testing page"""
    return templates.TemplateResponse("advanced_vulnerabilities.html", {"request": request})

@app.get("/nft-marketplace", response_class=HTMLResponse)
async def nft_marketplace_page(request: Request):
    """NFT Marketplace page"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("nft_marketplace.html", {
        "request": request,
        "user": user,
        "nfts": mock_nfts
    })

@app.post("/nft/buy")
async def buy_nft(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    try:
    form_data = await request.form()
    nft_id_raw = form_data.get("nft_id")
    price_raw = form_data.get("price")
    
    if not nft_id_raw or not price_raw:
        return PlainTextResponse("Missing NFT ID or price", status_code=400)
    
        nft_id = int(str(nft_id_raw))
        price = float(str(price_raw))
    
    if nft_id < 0 or nft_id >= len(mock_nfts):
        return PlainTextResponse("Invalid NFT ID", status_code=400)
    
    nft = mock_nfts[nft_id]
            
        # Check if user has sufficient funds
    if user["wallet"]["balance"]["USD"] < price:
        return PlainTextResponse("Insufficient funds", status_code=400)
    
        # Check if NFT is available for purchase
        if nft["owner"] == user["username"]:
            return PlainTextResponse("You already own this NFT", status_code=400)
        
        # Process the transaction
    user["wallet"]["balance"]["USD"] -= price
            
        # Transfer NFT ownership
    nft["owner"] = user["username"]
        nft["price"] = price * 1.1  # Increase price for next sale
        
        # Update user data
        data_manager.add_user(user["username"], user)
        
        # Log the transaction
    log_action(user, "nft_purchase", f"Bought NFT {nft['name']} for ${price}")
        
        # Redirect to marketplace with success message
        return RedirectResponse(url="/nft-marketplace?success=buy", status_code=302)
        
    except Exception as e:
        return PlainTextResponse(f"Transaction failed: {str(e)}", status_code=400)

@app.post("/nft/sell")
async def sell_nft(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    try:
    form_data = await request.form()
    nft_id_raw = form_data.get("nft_id")
    price_raw = form_data.get("price")
    
    if not nft_id_raw or not price_raw:
        return PlainTextResponse("Missing NFT ID or price", status_code=400)
    
        nft_id = int(str(nft_id_raw))
        price = float(str(price_raw))
    
    if nft_id < 0 or nft_id >= len(mock_nfts):
        return PlainTextResponse("Invalid NFT ID", status_code=400)
    
    nft = mock_nfts[nft_id]
            
        # Check if user owns the NFT
    if nft["owner"] != user["username"]:
        return PlainTextResponse("You don't own this NFT", status_code=400)
    
        # Process the transaction
    user["wallet"]["balance"]["USD"] += price
            
        # Transfer NFT ownership back to marketplace
    nft["owner"] = "Marketplace"
    nft["price"] = price
        
        # Update user data
        data_manager.add_user(user["username"], user)
        
        # Log the transaction
    log_action(user, "nft_sale", f"Sold NFT {nft['name']} for ${price}")
        
        # Redirect to marketplace with success message
        return RedirectResponse(url="/nft-marketplace?success=sell", status_code=302)
        
    except Exception as e:
        return PlainTextResponse(f"Transaction failed: {str(e)}", status_code=400)

@app.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request):
    """NFT Upload page"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("upload.html", {
        "request": request,
        "user": user
    })

@app.get("/files/{filename:path}")
async def access_uploaded_file(request: Request, filename: str):
    """Hidden endpoint to access uploaded files ( to path traversal)"""
    user = get_current_user(request)
    if not user:
        return PlainTextResponse(random.choice(ERROR_MESSAGES), status_code=401)
    
    try:
        if ".." in filename or filename.startswith("/"):
            if os.path.exists(filename):
                with open(filename, "rb") as f:
                    content = f.read()
                return PlainTextResponse(content.decode('utf-8', errors='ignore'))
            else:
                return PlainTextResponse(f"File not found: {filename}")
        
        if filename in uploaded_files:
            file_data = uploaded_files[filename]
            return PlainTextResponse(f"File: {filename}\nContent: {file_data['content'][:1000]}...")
        else:
            return PlainTextResponse(f"Uploaded file not found: {filename}")
            
    except Exception as e:
        return PlainTextResponse(f"File access error: {str(e)}")

@app.post("/set-role")
async def set_role(request: Request, role: str = Form(...)):
    request.session["role"] = role
    return PlainTextResponse(f"Role set to {role}")

@app.post("/news", response_class=HTMLResponse)
async def post_news(request: Request, news: str = Form(...)):
    return templates.TemplateResponse("news.html", {"request": request, "news": news})

@app.post("/search", response_class=HTMLResponse)
async def search(request: Request, query: str = Form(...)):
    # Use in-memory users_db instead of SQLite
    results = []
    for user_id, user in users_db.items():
        if query.lower() in user.get('username', '').lower():
            results.append({
                'id': user_id,
                'username': user.get('username', ''),
                'email': user.get('email', ''),
                'balance': user.get('wallet', {}).get('balance', {})
            })
    return templates.TemplateResponse("search.html", {"request": request, "results": results, "query": query})

@app.get("/profile/{user_id}", response_class=HTMLResponse)
async def profile_idor(request: Request, user_id: str):
    user = users_db.get(user_id)
    return templates.TemplateResponse("profile.html", {"request": request, "user": user})

@app.post("/upload/file")
async def upload_file(request: Request, file: UploadFile = File(...)):
    file_location = f"uploads/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return PlainTextResponse(f"File uploaded to {file_location}")

# --- Order Matching Engine ---
orderbook = {
    'BTC/ETH': {'buy': [], 'sell': []},
    'ETH/USDT': {'buy': [], 'sell': []},
    'BTC/USDT': {'buy': [], 'sell': []}
}
orders = {}
order_id_counter = 1

@app.post("/trade/submit-order")
async def submit_order(request: Request, pair: str = Form(...), side: str = Form(...), order_type: str = Form(...), price: float = Form(...), amount: float = Form(...)):
    global order_id_counter
    user = request.session.get("username", "guest")
    order = {
        'id': order_id_counter,
        'user': user,
        'pair': pair,
        'side': side,
        'type': order_type,
        'price': price,
        'amount': amount,
        'filled': 0.0,
        'status': 'open',
        'created_at': datetime.utcnow().isoformat()
    }
    orderbook[pair][side].append(order)
    orders[order_id_counter] = order
    order_id_counter += 1
    # Try to match orders
    await match_orders(pair)
    return PlainTextResponse(f"Order submitted: {order}")

async def match_orders(pair: str):
    buy_orders = sorted(orderbook[pair]['buy'], key=lambda o: (-o['price'], o['created_at']))
    sell_orders = sorted(orderbook[pair]['sell'], key=lambda o: (o['price'], o['created_at']))
    for buy in buy_orders:
        if buy['status'] != 'open': continue
        for sell in sell_orders:
            if sell['status'] != 'open': continue
            if buy['price'] >= sell['price']:
                trade_price = sell['price']
                trade_amount = min(buy['amount'] - buy['filled'], sell['amount'] - sell['filled'])
                # Simulate slippage for large trades
                slippage = 0.0
                if trade_amount > 10:
                    slippage = 0.01 * (trade_amount - 10)
                    trade_price += slippage
                buy['filled'] += trade_amount
                sell['filled'] += trade_amount
                if buy['filled'] >= buy['amount']:
                    buy['status'] = 'filled'
                if sell['filled'] >= sell['amount']:
                    sell['status'] = 'filled'
                # Log trade (could append to a trades list)
                break

@app.get("/orderbook/{pair}")
async def get_orderbook(pair: str):
    return orderbook.get(pair, {'buy': [], 'sell': []})

@app.post("/trade/cancel-order")
async def cancel_order(request: Request, order_id: int = Form(...)):
    order = orders.get(order_id)
    if order and order['status'] == 'open':
        order['status'] = 'cancelled'
        return PlainTextResponse(f"Order {order_id} cancelled.")
    return PlainTextResponse("Order not found or already filled/cancelled.", status_code=404)

# --- Advanced Realism: Fake Data ---
fake_news = [
    "Bitcoin hits new all-time high!",
    "Ethereum 2.0 launch date announced.",
    "Dogecoin accepted at major retailer.",
    "Cardano partners with Fortune 500 company.",
    "Litecoin transaction volume surges.",
    "Tether faces regulatory scrutiny."
]

def populate_fake_orderbook():
    global orderbook, order_id_counter
    fake_users = ["alice", "bob", "charlie", "dave"]
    pairs = ["BTC/ETH", "ETH/USDT", "BTC/USDT"]
    for pair in pairs:
        for _ in range(10):
            side = random.choice(["buy", "sell"])
            order = {
                'id': order_id_counter,
                'user': random.choice(fake_users),
                'pair': pair,
                'side': side,
                'type': "limit",
                'price': round(random.uniform(0.8, 1.2) * tokens_db[pair.split('/')[0]]["price"], 2),
                'amount': round(random.uniform(0.1, 5.0), 4),
                'filled': 0.0,
                'status': 'open',
                'created_at': datetime.utcnow().isoformat()
            }
            orderbook[pair][side].append(order)
            orders[order_id_counter] = order
            order_id_counter += 1

def populate_fake_audit():
    actions = ["login", "trade", "withdraw", "deposit", "admin_ban", "admin_adjust"]
    for _ in range(20):
        audit_log.append({
            "user": random.choice(["alice", "bob", "charlie", "admin"]),
            "action": random.choice(actions),
            "details": f"Performed {random.choice(actions)} action.",
            "timestamp": datetime.utcnow().isoformat()
        })

# --- Admin Endpoints ---
@app.post("/admin/ban-user")
async def ban_user(request: Request, username: str = Form(...)):
    role = request.session.get("role", "user")
    if role != "admin":
        return PlainTextResponse("Unauthorized", status_code=403)
    user = users_db.get(username)
    if user:
        user["banned"] = True
        return PlainTextResponse(f"User {username} banned.")
    return PlainTextResponse("User not found.", status_code=404)

@app.post("/admin/freeze-funds")
async def freeze_funds(request: Request, username: str = Form(...)):
    role = request.session.get("role", "user")
    if role != "admin":
        return PlainTextResponse("Unauthorized", status_code=403)
    user = users_db.get(username)
    if user:
        user["frozen"] = True
        return PlainTextResponse(f"Funds for {username} frozen.")
    return PlainTextResponse("User not found.", status_code=404)

@app.post("/admin/adjust-balance")
async def adjust_balance(request: Request, username: str = Form(...), token: str = Form(...), amount: float = Form(...)):
    role = request.session.get("role", "user")
    if role != "admin":
        return PlainTextResponse("Unauthorized", status_code=403)
    user = users_db.get(username)
    if user:
        user["balances"][token] = user["balances"].get(token, 0) + amount
        return PlainTextResponse(f"Adjusted {token} balance for {username} by {amount}.")
    return PlainTextResponse("User not found.", status_code=404)

# --- User Endpoints ---
@app.post("/profile/kyc-upload")
async def kyc_upload(request: Request, file: UploadFile = File(...)):
    user = request.session.get("username", "guest")
    file_location = f"uploads/kyc_{user}_{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return PlainTextResponse(f"KYC file uploaded to {file_location}")

@app.post("/profile/pic-upload")
async def pic_upload(request: Request, file: UploadFile = File(...)):
    user = request.session.get("username", "guest")
    file_location = f"uploads/profile_{user}_{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return PlainTextResponse(f"Profile picture uploaded to {file_location}")

@app.post("/profile/enable-2fa")
async def enable_2fa(request: Request, code: str = Form(...)):
    user = request.session.get("username", "guest")
    users_db[user]["2fa_enabled"] = True
    return PlainTextResponse("2FA enabled (bypassable).")

@app.post("/profile/generate-api-key")
async def generate_api_key(request: Request):
    user = request.session.get("username", "guest")
    api_key = user[::-1]
    users_db[user]["api_key"] = api_key
    return PlainTextResponse(f"API key generated: {api_key}")

@app.get("/profile/download-history")
async def download_history(request: Request):
    user = request.session.get("username", "guest")
    txs = [tx for tx in transactions_db if tx["user"] == user]
    content = json.dumps(txs)
    return Response(content, media_type="application/json", headers={"Content-Disposition": "attachment; filename=history.json"})

# --- Deposit/Withdrawal Simulation ---
@app.post("/deposit-sim", response_class=HTMLResponse)
async def deposit_simulation(request: Request, token: str = Form(...), amount: float = Form(...)):
    user = request.session.get("username", "guest")
    txid = str(uuid.uuid4())
    explorer_url = f"https://fakeblockchain.com/tx/{txid}"
    return templates.TemplateResponse("transaction_complete.html", {"request": request, "txid": txid, "explorer_url": explorer_url})

# --- Forgot Password Flow ---
@app.get("/forgot-password", response_class=HTMLResponse)
async def forgot_password_page(request: Request):
    return templates.TemplateResponse("forgot_password.html", {"request": request})

@app.post("/forgot-password")
async def forgot_password(request: Request, email: str = Form(...)):
    user = [u for u in users_db.values() if u["email"] == email]
    if user:
        user[0]["password"] = "password123"
        return PlainTextResponse("Password reset to 'password123'.")
    return PlainTextResponse("Email not found.", status_code=404)

# --- Notification Simulation ---
def send_fake_notification(user, message):
    print(f"Notification to {user}: {message}")

def generate_order_id():
    return f"order_{int(time.time())}_{random.randint(1, 1000)}"

def calculate_slippage(amount, price_impact):
    return amount * (1 + price_impact)

@app.get("/api/v1/system/health")
async def system_health_check(request: Request):
    """System health check endpoint (requires admin)"""
    user = get_current_user(request)
    if not user or user["username"] != "admin":
        return PlainTextResponse("Unauthorized", status_code=401)
    
    # Expose sensitive data only to admin
    system_info = {
        "users_count": len(data_manager.users_db),
        "transactions_count": len(data_manager.transactions_db),
        "nfts_count": len(mock_nfts),
        "system_memory": "2.5GB used / 8GB total",
        "database_size": "156.7MB",
        "uptime": "3 days, 7 hours, 23 minutes",
        "last_backup": "2024-01-15 14:30:00",
        "security_alerts": 0,
        "failed_logins": 12,
        "suspicious_ips": ["192.168.1.100", "10.0.0.50"]
    }
    
    return templates.TemplateResponse("admin_cmd.html", {"request": request, "system_info": system_info})

@app.post("/api/v1/system/refresh")
async def refresh_system_data(request: Request):
    """Refresh system data (requires admin)"""
    user = get_current_user(request)
    if not user or user["username"] != "admin":
        return PlainTextResponse("Unauthorized", status_code=401)
    
    # Regenerate NFTs with new rules
    global mock_nfts
    mock_nfts.clear()
    generate_mock_nfts()
    
    return RedirectResponse(url="/api/v1/system/health", status_code=status.HTTP_302_FOUND)

@router.patch("/api/v1/internal/maintenance")
async def hidden_patch_endpoint(request: Request):
    """Hidden maintenance endpoint - requires specific header"""
    maintenance_header = request.headers.get("X-Maintenance-Token")
    if maintenance_header != "xK9mP2qR8vL5nJ3hG7fD1sA4wE6tY9uI0oP":
        return PlainTextResponse("Not Found", status_code=404)
    
    # Award bonus BTC for discovering the endpoint
    user = get_current_user(request)
    if user:
        user["wallet"]["balance"]["BTC"] += 1.0
        data_manager.add_user(user["id"], user)
    
    return PlainTextResponse("Secret PATCH endpoint accessed. Bonus BTC awarded.")

@router.put("/api/v1/internal/update")
async def hidden_put_endpoint(request: Request):
    """Hidden update endpoint - requires specific parameter"""
    update_token = request.query_params.get("token")
    if update_token != "xK9mP2qR8vL5nJ3hG7fD1sA4wE6tY9uI0oP":
        return PlainTextResponse("Not Found", status_code=404)
    
    # Award bonus ETH for discovering the endpoint
    user = get_current_user(request)
    if user:
        user["wallet"]["balance"]["ETH"] += 5.0
        data_manager.add_user(user["id"], user)
    
    return PlainTextResponse("Secret PUT endpoint accessed. Bonus ETH awarded.")

@app.get("/api/v1/internal/status")
async def hidden_ssrf_endpoint(request: Request):
    """Hidden SSRF endpoint - requires specific parameters"""
    # Check for specific parameters
    test_param = request.query_params.get("test")
    internal_param = request.query_params.get("internal")
    
    if test_param == "ssrf" and internal_param == "true":
        # Allow external requests
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
    """Hidden backup endpoint - requires specific headers"""
    backup_token = request.headers.get("X-Backup-Token")
    if backup_token != "xK9mP2qR8vL5nJ3hG7fD1sA4wE6tY9uI0oP":
        return PlainTextResponse("Not Found", status_code=404)
    
    # Expose system data
    sensitive_data = {
        "database_connection": "postgresql://admin:password@localhost:5432/fakecrypto",
        "redis_url": "redis://localhost:6379",
        "aws_credentials": {
            "access_key": "AKIAIOSFODNN7EXAMPLE",
            "secret_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
        },
        "private_keys": [user["wallet"]["private_key"] for user in data_manager.users_db.values()],
        "admin_tokens": ["xK9mP2qR8vL5nJ3hG7fD1sA4wE6tY9uI0oP"]
    }
    
    return PlainTextResponse(f"Sensitive data exposed: {sensitive_data}")

# Enhanced features and vulnerability endpoints

@app.get("/live-pricing", response_class=HTMLResponse)
async def live_pricing_page(request: Request):
    """Live pricing page with real-time data fetching"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("live_pricing.html", {
        "request": request,
        "user": user,
        "tokens": tokens_db
    })

@app.post("/api/fetch-price")
async def fetch_price_data(request: Request, url: str = Form(...)):
    """Fetch external price data"""
    user = get_current_user(request)
    if not user:
        return PlainTextResponse("Unauthorized", status_code=401)
    
    result = fetch_external_data(url)
    log_user_activity(f"Price fetch request: {url}")
    
    return PlainTextResponse(f"Price data: {result}")

@app.post("/api/upload-xml")
async def upload_xml_data(request: Request, file: UploadFile = File(...)):
    """Upload XML data"""
    user = get_current_user(request)
    if not user:
        return PlainTextResponse("Unauthorized", status_code=401)
    
    content = await file.read()
    xml_content = content.decode('utf-8')
    
    parsed_data = parse_xml_data(xml_content)
    log_user_activity(f"XML upload: {file.filename}")
    
    return PlainTextResponse(f"XML parsed: {parsed_data}")

@app.get("/api/session/{session_id}")
async def get_session_data(request: Request, session_id: str):
    """Get session data"""
    session_data = validate_session(session_id)
    if session_data:
        return PlainTextResponse(f"Session data: {session_data}")
    return PlainTextResponse("Session not found", status_code=404)

@app.post("/api/log-activity")
async def log_activity(request: Request, activity: str = Form(...)):
    """Log user activity"""
    user = get_current_user(request)
    if not user:
        return PlainTextResponse("Unauthorized", status_code=401)
    
    logged_activity = log_user_activity(activity)
    return PlainTextResponse(f"Activity logged: {logged_activity}")

@app.post("/api/validate-url")
async def validate_user_url(request: Request, url: str = Form(...)):
    """Validate user URL"""
    user = get_current_user(request)
    if not user:
        return PlainTextResponse("Unauthorized", status_code=401)
    
    validated_url = validate_url(url)
    return PlainTextResponse(f"URL validated: {validated_url}")

@app.post("/api/verify-2fa")
async def verify_2fa(request: Request, code: str = Form(...)):
    """Verify 2FA code"""
    user = get_current_user(request)
    if not user:
        return PlainTextResponse("Unauthorized", status_code=401)
    
    is_valid = verify_2fa_code(code)
    return PlainTextResponse(f"2FA verification: {is_valid}")

@app.get("/api/admin/status")
async def admin_status(request: Request):
    """Admin status endpoint"""
    user = get_current_user(request)
    if not user:
        return PlainTextResponse("Unauthorized", status_code=401)
    
    has_access = check_admin_access(user.get("role", "user"))
    if has_access:
        return PlainTextResponse("Admin access granted")
    return PlainTextResponse("Access denied", status_code=403)

@app.post("/api/validate-key")
async def validate_api_key(request: Request, key: str = Form(...)):
    """Validate API key"""
    user = get_current_user(request)
    if not user:
        return PlainTextResponse("Unauthorized", status_code=401)
    
    key_data = validate_api_key(key)
    return PlainTextResponse(f"API key data: {key_data}")

@app.post("/api/decrypt-key")
async def decrypt_key(request: Request, encrypted_data: str = Form(...)):
    """Decrypt private key"""
    user = get_current_user(request)
    if not user:
        return PlainTextResponse("Unauthorized", status_code=401)
    
    decrypted = decrypt_private_key(encrypted_data)
    return PlainTextResponse(f"Decrypted data: {decrypted}")

@app.post("/api/execute-command")
async def execute_system_command(request: Request, command: str = Form(...)):
    """Execute system command"""
    user = get_current_user(request)
    if not user:
        return PlainTextResponse("Unauthorized", status_code=401)
    
    result = execute_command(command)
    return PlainTextResponse(f"Command result: {result}")

@app.post("/api/reset-password")
async def reset_password(request: Request, email: str = Form(...)):
    """Reset password"""
    token = generate_reset_token()
    return PlainTextResponse(f"Reset token: {token}")

# Enhanced features

@app.get("/wallet-balance", response_class=HTMLResponse)
async def wallet_balance_page(request: Request):
    """Enhanced wallet balance page"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("wallet_balance.html", {
        "request": request,
        "user": user,
        "tokens": tokens_db
    })

@app.get("/portfolio", response_class=HTMLResponse)
async def portfolio_page(request: Request):
    """User portfolio with charts"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("portfolio.html", {
        "request": request,
        "user": user,
        "portfolio_data": portfolio_charts.get(user["username"], {})
    })

@app.get("/deposit-withdraw", response_class=HTMLResponse)
async def deposit_withdraw_page(request: Request):
    """Deposit/withdraw page"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("deposit_withdraw.html", {
        "request": request,
        "user": user
    })

@app.get("/transaction-history", response_class=HTMLResponse)
async def transaction_history_page(request: Request):
    """Transaction history with downloadable statements"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("transaction_history.html", {
        "request": request,
        "user": user,
        "transactions": transactions_db.get(user["username"], [])
    })

@app.get("/2fa-setup", response_class=HTMLResponse)
async def two_fa_setup_page(request: Request):
    """2FA setup page"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("2fa_setup.html", {
        "request": request,
        "user": user
    })

@app.get("/api-keys", response_class=HTMLResponse)
async def api_keys_page(request: Request):
    """API key management page"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("api_keys.html", {
        "request": request,
        "user": user,
        "api_keys": api_keys_db.get(user["username"], [])
    })

@app.get("/admin-console", response_class=HTMLResponse)
async def admin_console_page(request: Request):
    """Admin console for monitoring"""
    user = get_current_user(request)
    if not user or user.get("role") != "admin":
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("admin_console.html", {
        "request": request,
        "user": user,
        "admin_data": admin_console
    })

@app.get("/support-chat", response_class=HTMLResponse)
async def support_chat_page(request: Request):
    """Support chat page"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("support_chat.html", {
        "request": request,
        "user": user
    })

@app.get("/referral-system", response_class=HTMLResponse)
async def referral_system_page(request: Request):
    """Referral system page"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("referral_system.html", {
        "request": request,
        "user": user,
        "referral_data": referral_system.get(user["username"], {})
    })

@app.get("/kyc-flow", response_class=HTMLResponse)
async def kyc_flow_page(request: Request):
    """KYC flow page"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("kyc_flow.html", {
        "request": request,
        "user": user,
        "kyc_status": kyc_documents.get(user["username"], {})
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, Response, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import sqlite3
import hashlib
import base64
import os
import re
import subprocess
import pickle
import yaml
import xml.etree.ElementTree as ET
import json
import logging
import threading
import time
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import uuid
import pymongo
from bson import ObjectId
import requests
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
import redis
import jwt

import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'xK9mP2qR8vL5nJ3hG7fD1sA4wE6tY9uI0oP!@#$%^&*()_+{}|:<>?[]\\;'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# MongoDB connection for NoSQL injection testing
try:
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    mongo_db = mongo_client["cybermart"]
    mongo_users = mongo_db["users"]
    mongo_products = mongo_db["products"]
except:
    mongo_client = None

# Redis for rate limiting
try:
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
except:
    redis_client = None

# Enhanced logging for vulnerability simulation
class Log4ShellSimulator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def log_user_input(self, user_input):
        # Simulating JNDI lookup injection
        if '${jndi:' in user_input.lower():
            return f"JNDI lookup attempted: {user_input}"
        return f"User input logged: {user_input}"

log4shell_sim = Log4ShellSimulator()

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Enhanced Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    payment_info = db.Column(db.String(255))
    address = db.Column(db.Text)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    failed_login_attempts = db.Column(db.Integer, default=0)
    account_locked = db.Column(db.Boolean, default=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    stock = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(255))
    sku = db.Column(db.String(50), unique=True)
    weight = db.Column(db.Float)
    dimensions = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_number = db.Column(db.String(50), unique=True)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')
    shipping_address = db.Column(db.Text)
    billing_address = db.Column(db.Text)
    payment_method = db.Column(db.String(50))
    tracking_number = db.Column(db.String(100))
    discount_code = db.Column(db.String(50))
    discount_amount = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    product_name = db.Column(db.String(100))

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    username = db.Column(db.String(80))
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved = db.Column(db.Boolean, default=False)

class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Discount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    discount_type = db.Column(db.String(20))  # percentage or fixed
    discount_value = db.Column(db.Float, nullable=False)
    min_order_amount = db.Column(db.Float, default=0.0)
    max_uses = db.Column(db.Integer, default=-1)
    used_count = db.Column(db.Integer, default=0)
    valid_from = db.Column(db.DateTime)
    valid_until = db.Column(db.DateTime)
    active = db.Column(db.Boolean, default=True)

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    invoice_number = db.Column(db.String(50), unique=True)
    amount = db.Column(db.Float, nullable=False)
    tax_amount = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    pdf_path = db.Column(db.String(255))

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    session_id = db.Column(db.String(100))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    address_type = db.Column(db.String(20))  # shipping or billing
    street_address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    is_default = db.Column(db.Boolean, default=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Spring4Shell vulnerability simulation
class Spring4ShellSimulator:
    def __init__(self):
        self.class_loader = None
    
    def process_request(self, data):
        # Simulating ClassLoader manipulation
        if 'class.module.classLoader' in data:
            return f"Spring4Shell attempt detected: {data}"
        return f"Request processed: {data}"

spring4shell_sim = Spring4ShellSimulator()

# Vulnerability functions
def nosql_query(query):
    """NoSQL query execution"""
    if mongo_client:
        try:
            # Direct query execution without sanitization
            result = mongo_users.find_one(query)
            return result
        except:
            return {"error": "NoSQL query failed"}
    return {"error": "MongoDB not available"}

def command_execution(command):
    """Command execution"""
    try:
        result = subprocess.check_output(command, shell=True, text=True)
        return result
    except:
        return "Command execution failed"

def deserialize_data(data):
    """Data deserialization"""
    try:
        return pickle.loads(base64.b64decode(data))
    except:
        return "Deserialization failed"

def file_inclusion(path):
    """File inclusion"""
    try:
        with open(path, 'r') as f:
            return f.read()
    except:
        return "File inclusion failed"

def redirect_url(url):
    """URL redirect"""
    return redirect(url)

def rate_limit_check(user_id):
    """Rate limiting check"""
    if redis_client:
        key = f"rate_limit:{user_id}"
        current = redis_client.get(key)
        if current and int(current) > 100:  # Very high limit
            return False
        redis_client.incr(key)
        redis_client.expire(key, 3600)  # 1 hour
    return True

def password_check(password):
    """Password validation"""
    if len(password) >= 1:  # Very weak policy
        return True
    return False

def price_validation(price):
    """Price validation"""
    try:
        price_float = float(price)
        if price_float >= 0:  # Allows negative prices
            return True
    except:
        pass
    return False

def quantity_validation(quantity):
    """Quantity validation"""
    try:
        qty_int = int(quantity)
        if qty_int >= 0:  # Allows negative quantities
            return True
    except:
        pass
    return False

def idor_check(user_id, resource_id):
    """Access control check"""
    return True  # Always allows access

def xss_filter(content):
    """Content filtering"""
    return content  # Returns raw content without sanitization

def csrf_check():
    """CSRF validation"""
    return True

def generate_invoice_pdf(order):
    """Generate PDF invoice"""
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Add content to PDF
    p.drawString(100, 750, f"Invoice #{order.invoice_number}")
    p.drawString(100, 730, f"Order Date: {order.created_at.strftime('%Y-%m-%d')}")
    p.drawString(100, 710, f"Total Amount: ${order.total_amount:.2f}")
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return buffer

def send_email_notification(to_email, subject, content):
    """Send email notification"""
    # Simulate email sending
    print(f"Email to {to_email}: {subject} - {content}")
    return True

# Hidden Vulnerability 1: Secret admin endpoint
@app.route('/system/admin/panel')
def secret_admin():
    if request.args.get('token') == 'super_secret_2024':
        users = User.query.all()
        return jsonify([{'id': u.id, 'username': u.username, 'email': u.email, 'payment_info': u.payment_info} for u in users])
    return 'Not Found', 404

# Hidden Vulnerability 2: Debug information exposure
@app.route('/api/debug')
def debug_info():
    if request.headers.get('X-Debug-Token') == 'debug_enabled':
        return {
            'debug_mode': app.debug,
            'secret_key': app.config['SECRET_KEY'],
            'database_uri': app.config['SQLALCHEMY_DATABASE_URI'],
            'environment': os.environ.get('FLASK_ENV', 'development')
        }
    return 'Not Found', 404

# Hidden Vulnerability 3: Directory traversal in file upload
@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file', 400
    
    file = request.files['file']
    filename = file.filename
    
    # Hidden vulnerability: No path validation
    upload_path = os.path.join('uploads', filename)
    file.save(upload_path)
    
    return f'File uploaded: {filename}'

# Hidden Vulnerability 4: SQL injection in user search
@app.route('/api/users/search')
def user_search():
    query = request.args.get('q', '')
    if query:
        # Hidden vulnerability: Direct string concatenation
        sql = f"SELECT * FROM user WHERE username LIKE '%{query}%' OR email LIKE '%{query}%'"
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute(sql)
        users = cursor.fetchall()
        conn.close()
        return jsonify(users)
    return jsonify([])

# Hidden Vulnerability 5: XSS in user agent
@app.route('/api/user_info')
def user_info():
    user_agent = request.headers.get('User-Agent', '')
    # Hidden vulnerability: XSS in user agent display
    return f'<div>Your browser: {user_agent}</div>'

# Hidden Vulnerability 6: SSRF in image loading
@app.route('/api/load_image')
def load_image():
    url = request.args.get('url', '')
    if url:
        # Hidden vulnerability: SSRF - no URL validation
        import requests
        try:
            response = requests.get(url, timeout=5)
            return response.content, 200, {'Content-Type': 'image/jpeg'}
        except:
            return 'Error loading image', 400
    return 'No URL provided', 400

# Hidden Vulnerability 7: Command injection in ping
@app.route('/api/ping')
def ping_host():
    host = request.args.get('host', '127.0.0.1')
    # Hidden vulnerability: Command injection
    try:
        result = subprocess.check_output(f'ping -c 1 {host}', shell=True)
        return result.decode()
    except:
        return 'Ping failed', 400

# Hidden Vulnerability 8: Deserialization in session
@app.route('/api/session_data')
def session_data():
    data = request.args.get('data', '')
    if data:
        # Hidden vulnerability: Insecure deserialization
        try:
            decoded = base64.b64decode(data)
            obj = pickle.loads(decoded)
            return str(obj)
        except:
            return 'Invalid data', 400
    return 'No data provided', 400

# Hidden Vulnerability 9: Race condition in checkout
checkout_locks = {}

@app.route('/checkout_race', methods=['POST'])
@login_required
def checkout_race():
    user_id = current_user.id
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))
    
    # Hidden vulnerability: Race condition - no proper locking
    if user_id not in checkout_locks:
        checkout_locks[user_id] = threading.Lock()
    
    with checkout_locks[user_id]:
        product = Product.query.get(product_id)
        if product and product.stock >= quantity:
            # Simulate processing time
            time.sleep(0.1)
            product.stock -= quantity
            db.session.commit()
            return 'Order placed successfully'
        else:
            return 'Insufficient stock', 400

# Enhanced e-commerce routes with stealthy vulnerabilities

@app.route('/api/products/search')
def api_products_search():
    """Product search API with NoSQL injection vulnerability"""
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    
    # Vulnerable NoSQL query
    if mongo_client:
        nosql_query = {"$or": [{"name": {"$regex": query}}, {"category": category}]}
        results = list(mongo_products.find(nosql_query))
        return jsonify({"products": results})
    
    # Fallback to SQLite
    products = Product.query.filter(
        Product.name.contains(query) | Product.category.contains(category)
    ).all()
    return jsonify({"products": [{"id": p.id, "name": p.name, "price": p.price} for p in products]})

@app.route('/api/cart/add', methods=['POST'])
def api_add_to_cart():
    """Add to cart API with parameter tampering vulnerability"""
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    price = data.get('price')  # Price from request
    
    # Price and quantity validation
    if not price_validation(price):
        return jsonify({"error": "Invalid price"}), 400
    
    if not quantity_validation(quantity):
        return jsonify({"error": "Invalid quantity"}), 400
    
    # Add to cart with manipulated values
    cart_item = CartItem(
        user_id=current_user.id if current_user.is_authenticated else None,
        session_id=session.get('session_id'),
        product_id=product_id,
        quantity=quantity
    )
    db.session.add(cart_item)
    db.session.commit()
    
    return jsonify({"success": True, "message": "Added to cart"})

@app.route('/api/checkout', methods=['POST'])
def api_checkout():
    """Checkout API with CSRF vulnerability"""
    if not csrf_check():
        return jsonify({"error": "CSRF check failed"}), 403
    
    data = request.get_json()
    items = data.get('items', [])
    discount_code = data.get('discount_code', '')
    
    # Discount validation
    if discount_code:
        discount = Discount.query.filter_by(code=discount_code, active=True).first()
        if discount:
            # Apply discount
            pass
    
    # Create order
    order = Order(
        user_id=current_user.id,
        order_number=f"ORD-{uuid.uuid4().hex[:8].upper()}",
        total_amount=data.get('total', 0),
        status='pending'
    )
    db.session.add(order)
    db.session.commit()
    
    return jsonify({"success": True, "order_id": order.id})

@app.route('/api/reviews/add', methods=['POST'])
def api_add_review():
    """Add review API with XSS vulnerability"""
    data = request.get_json()
    product_id = data.get('product_id')
    content = data.get('content', '')
    rating = data.get('rating', 5)
    
    # Content filtering
    sanitized_content = xss_filter(content)
    
    review = Review(
        product_id=product_id,
        user_id=current_user.id if current_user.is_authenticated else None,
        username=current_user.username if current_user.is_authenticated else 'Anonymous',
        content=sanitized_content,
        rating=rating
    )
    db.session.add(review)
    db.session.commit()
    
    return jsonify({"success": True, "review_id": review.id})

@app.route('/api/wishlist/add', methods=['POST'])
def api_add_to_wishlist():
    """Add to wishlist API with IDOR vulnerability"""
    data = request.get_json()
    product_id = data.get('product_id')
    user_id = data.get('user_id', current_user.id if current_user.is_authenticated else None)
    
    # Access control check
    if idor_check(current_user.id if current_user.is_authenticated else None, user_id):
        wishlist_item = Wishlist(
            user_id=user_id,
            product_id=product_id
        )
        db.session.add(wishlist_item)
        db.session.commit()
        return jsonify({"success": True})
    
    return jsonify({"error": "Access denied"}), 403

@app.route('/api/invoice/<int:invoice_id>')
def api_get_invoice(invoice_id):
    """Get invoice API with IDOR vulnerability"""
    invoice = Invoice.query.get(invoice_id)
    
    # Access control check
    if idor_check(current_user.id if current_user.is_authenticated else None, invoice.order.user_id):
        return jsonify({
            "invoice_number": invoice.invoice_number,
            "amount": invoice.amount,
            "created_at": invoice.created_at.isoformat()
        })
    
    return jsonify({"error": "Access denied"}), 403

@app.route('/api/invoice/<int:invoice_id>/download')
def api_download_invoice(invoice_id):
    """Download invoice API with file inclusion vulnerability"""
    invoice = Invoice.query.get(invoice_id)
    
    # File inclusion
    if invoice.pdf_path:
        return file_inclusion(invoice.pdf_path)
    
    # Generate PDF
    pdf_buffer = generate_invoice_pdf(invoice.order)
    return send_file(
        BytesIO(pdf_buffer.getvalue()),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f"invoice_{invoice.invoice_number}.pdf"
    )

@app.route('/api/command', methods=['POST'])
def api_command():
    """Command execution API with command injection vulnerability"""
    data = request.get_json()
    command = data.get('command', '')
    
    # Command execution
    result = command_execution(command)
    return jsonify({"result": result})

@app.route('/api/deserialize', methods=['POST'])
def api_deserialize():
    """Deserialization API with unsafe deserialization vulnerability"""
    data = request.get_json()
    serialized_data = data.get('data', '')
    
    # Data deserialization
    result = deserialize_data(serialized_data)
    return jsonify({"result": str(result)})

@app.route('/api/redirect')
def api_redirect():
    """Redirect API with open redirect vulnerability"""
    url = request.args.get('url', '/')
    
    # URL redirect
    return redirect_url(url)

@app.route('/api/rate_limit_test')
def api_rate_limit_test():
    """Rate limit test API with insufficient rate limiting"""
    user_id = current_user.id if current_user.is_authenticated else request.remote_addr
    
    # Rate limiting check
    if rate_limit_check(user_id):
        return jsonify({"success": True, "message": "Request allowed"})
    else:
        return jsonify({"error": "Rate limit exceeded"}), 429

@app.route('/api/password_check', methods=['POST'])
def api_password_check():
    """Password check API with weak password policy"""
    data = request.get_json()
    password = data.get('password', '')
    
    # Password validation
    if password_check(password):
        return jsonify({"valid": True})
    else:
        return jsonify({"valid": False, "error": "Password too weak"})

@app.route('/api/price_validation', methods=['POST'])
def api_price_validation():
    """Price validation API with parameter tampering vulnerability"""
    data = request.get_json()
    price = data.get('price', 0)
    
    # Price validation
    if price_validation(price):
        return jsonify({"valid": True, "price": price})
    else:
        return jsonify({"valid": False, "error": "Invalid price"})

@app.route('/api/quantity_validation', methods=['POST'])
def api_quantity_validation():
    """Quantity validation API with parameter tampering vulnerability"""
    data = request.get_json()
    quantity = data.get('quantity', 0)
    
    # Quantity validation
    if quantity_validation(quantity):
        return jsonify({"valid": True, "quantity": quantity})
    else:
        return jsonify({"valid": False, "error": "Invalid quantity"})

@app.route('/api/xss_test', methods=['POST'])
def api_xss_test():
    """XSS test API with XSS vulnerability"""
    data = request.get_json()
    content = data.get('content', '')
    
    # Content filtering
    filtered_content = xss_filter(content)
    return jsonify({"content": filtered_content})

@app.route('/api/csrf_test', methods=['POST'])
def api_csrf_test():
    """CSRF test API with CSRF vulnerability"""
    # CSRF validation
    if csrf_check():
        return jsonify({"success": True, "message": "CSRF check passed"})
    else:
        return jsonify({"error": "CSRF check failed"}), 403

# Enhanced product routes
@app.route('/products')
def products():
    """Product listing with filtering and search"""
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    sort = request.args.get('sort', 'name')
    
    query = Product.query
    
    if category:
        query = query.filter(Product.category == category)
    
    if search:
        query = query.filter(Product.name.contains(search))
    
    if sort == 'price':
        query = query.order_by(Product.price.asc())
    elif sort == 'price_desc':
        query = query.order_by(Product.price.desc())
    else:
        query = query.order_by(Product.name.asc())
    
    products = query.all()
    categories = db.session.query(Product.category).distinct().all()
    
    return render_template('products.html', products=products, categories=categories)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Product detail page with reviews"""
    product = Product.query.get_or_404(product_id)
    reviews = Review.query.filter_by(product_id=product_id, approved=True).order_by(Review.created_at.desc()).all()
    
    return render_template('product_detail.html', product=product, reviews=reviews)

@app.route('/cart')
@login_required
def cart():
    """User cart page"""
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.quantity * item.product.price for item in cart_items)
    
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/wishlist')
@login_required
def wishlist():
    """User wishlist page"""
    wishlist_items = Wishlist.query.filter_by(user_id=current_user.id).all()
    
    return render_template('wishlist.html', wishlist_items=wishlist_items)

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """Checkout process with discount codes"""
    if request.method == 'POST':
        # Checkout process
        discount_code = request.form.get('discount_code', '')
        total = float(request.form.get('total', 0))
        
        # Apply discount without proper validation
        if discount_code:
            discount = Discount.query.filter_by(code=discount_code, active=True).first()
            if discount:
                total -= discount.discount_value
        
        # Create order
        order = Order(
            user_id=current_user.id,
            order_number=f"ORD-{uuid.uuid4().hex[:8].upper()}",
            total_amount=total,
            discount_code=discount_code
        )
        db.session.add(order)
        db.session.commit()
        
        # Send email notification
        send_email_notification(
            current_user.email,
            "Order Confirmation",
            f"Your order {order.order_number} has been placed successfully!"
        )
        
        return redirect(url_for('order_confirmation', order_id=order.id))
    
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.quantity * item.product.price for item in cart_items)
    
    return render_template('checkout.html', cart_items=cart_items, total=total)

@app.route('/orders')
@login_required
def orders():
    """User order history"""
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    
    return render_template('orders.html', orders=orders)

@app.route('/order/<int:order_id>')
@login_required
def order_detail(order_id):
    """Order detail page with IDOR vulnerability"""
    order = Order.query.get_or_404(order_id)
    
    # Access control check
    if not idor_check(current_user.id, order.user_id):
        flash('Access denied', 'error')
        return redirect(url_for('orders'))
    
    return render_template('order_detail.html', order=order)

@app.route('/invoice/<int:invoice_id>')
@login_required
def invoice_detail(invoice_id):
    """Invoice detail page with IDOR vulnerability"""
    invoice = Invoice.query.get_or_404(invoice_id)
    
    # Access control check
    if not idor_check(current_user.id, invoice.order.user_id):
        flash('Access denied', 'error')
        return redirect(url_for('orders'))
    
    return render_template('invoice_detail.html', invoice=invoice)

@app.route('/admin/products')
@login_required
def admin_products():
    """Admin product management"""
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    products = Product.query.all()
    return render_template('admin/products.html', products=products)

@app.route('/admin/orders')
@login_required
def admin_orders():
    """Admin order management"""
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=orders)

@app.route('/admin/reviews')
@login_required
def admin_reviews():
    """Admin review moderation"""
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    reviews = Review.query.order_by(Review.created_at.desc()).all()
    return render_template('admin/reviews.html', reviews=reviews)

# Application Routes

@app.route('/')
def index():
    category = request.args.get('category', '')
    if category:
        products = Product.query.filter_by(category=category).all()
    else:
        products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        payment_info = request.form['payment_info']
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template('account_exists.html', 
                                conflict_type='email', 
                                email=email, 
                                existing_user=existing_user)
        
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            return render_template('account_exists.html', 
                                conflict_type='username', 
                                username=username, 
                                existing_user=existing_username)
        
        try:
            hashed_password = generate_password_hash(password)
            
            new_user = User(username=username, email=email, password=hashed_password, payment_info=payment_info)
            db.session.add(new_user)
            db.session.commit()
            
            flash('Registration successful!')
            return redirect(url_for('login'))
        except IntegrityError as e:
            db.session.rollback()
            if 'user.email' in str(e):
                # Find the existing user with this email
                existing_user = User.query.filter_by(email=email).first()
                return render_template('account_exists.html', 
                                    conflict_type='email', 
                                    email=email, 
                                    existing_user=existing_user)
            elif 'user.username' in str(e):
                # Find the existing user with this username
                existing_user = User.query.filter_by(username=username).first()
                return render_template('account_exists.html', 
                                    conflict_type='username', 
                                    username=username, 
                                    existing_user=existing_user)
            else:
                flash('Registration failed due to database constraint. Please try again.')
                return render_template('register.html')
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.')
            return render_template('register.html')
    
    return render_template('register.html')

# Update product_detail route to handle reviews and image upload
@app.route('/product/<int:product_id>', methods=['GET', 'POST'])
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    reviews = Review.query.filter_by(product_id=product_id).order_by(Review.created_at.desc()).all()
    if request.method == 'POST':
        # Review submission (no sanitization)
        content = request.form.get('review', '')
        username = current_user.username if hasattr(current_user, 'username') else 'Guest'
        user_id = current_user.id if hasattr(current_user, 'id') else None
        review = Review(product_id=product_id, user_id=user_id, username=username, content=content)
        db.session.add(review)
        db.session.commit()
        flash('Review submitted!', 'success')
        return redirect(url_for('product_detail', product_id=product_id))
    return render_template('product_detail.html', product=product, reviews=reviews)

# Add product image upload (no type check)
@app.route('/admin/upload_product_image/<int:product_id>', methods=['POST'])
@login_required
def upload_product_image(product_id):
    if not current_user.is_admin:
        return 'Unauthorized', 403
    file = request.files.get('image')
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join('static', 'uploads', filename)
        file.save(filepath)
        product = Product.query.get(product_id)
        product.image_url = '/static/uploads/' + filename
        db.session.commit()
        flash('Image uploaded!', 'success')
    return redirect(url_for('product_detail', product_id=product_id))

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form['product_id']
    quantity = int(request.form['quantity'])
    
    if current_user.is_authenticated:
        # Logged in user cart
        if 'cart' not in session:
            session['cart'] = {}
        
        if product_id in session['cart']:
            session['cart'][product_id] += quantity
        else:
            session['cart'][product_id] = quantity
        
        flash('Product added to cart!')
        return redirect(url_for('index'))
    else:
        # Guest cart
        add_to_guest_cart(product_id, quantity)
        flash('Product added to guest cart!')
        return redirect(url_for('index'))

@app.route('/guest_cart')
def guest_cart():
    cart_items = []
    total = 0
    
    guest_cart = get_guest_cart()
    for product_id, quantity in guest_cart.items():
        product = Product.query.get(int(product_id))
        if product:
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': product.price * quantity
            })
            total += product.price * quantity
    
    return render_template('guest_cart.html', cart_items=cart_items, total=total)

@app.route('/guest_add_to_cart', methods=['POST'])
def guest_add_to_cart():
    product_id = request.form['product_id']
    quantity = int(request.form['quantity'])
    
    add_to_guest_cart(product_id, quantity)
    flash('Product added to guest cart!')
    return redirect(url_for('index'))

@app.route('/guest_remove_from_cart', methods=['POST'])
def guest_remove_from_cart():
    product_id = request.form['product_id']
    
    guest_cart = get_guest_cart()
    if str(product_id) in guest_cart:
        del guest_cart[str(product_id)]
        session['guest_cart'] = guest_cart
        flash('Product removed from cart!')
    
    return redirect(url_for('guest_cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        if current_user.is_authenticated:
            # Logged in user checkout
            cart_items = []
            total = 0
            
            if 'cart' in session:
                for product_id, quantity in session['cart'].items():
                    product = Product.query.get(product_id)
                    if product:
                        cart_items.append({
                            'product': product,
                            'quantity': quantity,
                            'subtotal': product.price * quantity
                        })
                        total += product.price * quantity
            
            # Process payment information
            payment_info = request.form.get('payment_info', '')
            if payment_info:
                # Store payment info in user profile
                current_user.payment_info = payment_info
                db.session.commit()
            
            # Create order
            order = Order(user_id=current_user.id, total_amount=total)
            db.session.add(order)
            db.session.flush()
            
            for item in cart_items:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item['product'].id,
                    quantity=item['quantity'],
                    price=item['product'].price
                )
                db.session.add(order_item)
            
            db.session.commit()
            session.pop('cart', None)
            
            flash('Order placed successfully!')
            return redirect(url_for('order_confirmation', order_id=order.id))
        else:
            # Guest checkout
            return redirect(url_for('guest_checkout'))
    
    # GET request - show checkout page
    if current_user.is_authenticated:
        cart_items = []
        total = 0
        
        if 'cart' in session:
            for product_id, quantity in session['cart'].items():
                product = Product.query.get(product_id)
                if product:
                    cart_items.append({
                        'product': product,
                        'quantity': quantity,
                        'subtotal': product.price * quantity
                    })
                    total += product.price * quantity
        
        return render_template('checkout.html', cart_items=cart_items, total=total)
    else:
        return redirect(url_for('guest_checkout'))

@app.route('/orders')
@login_required
def orders():
    orders = Order.query.all()
    return render_template('orders.html', orders=orders)

@app.route('/admin')
@login_required
def admin():
    users = User.query.all()
    products = Product.query.all()
    orders = Order.query.all()
    return render_template('admin.html', users=users, products=products, orders=orders)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if query:
        products = Product.query.filter(Product.name.contains(query)).all()
    else:
        products = []
    return render_template('search.html', products=products, query=query)

@app.route('/api/products')
def api_products():
    category = request.args.get('category', '')
    if category:
        products = Product.query.filter_by(category=category).all()
    else:
        products = Product.query.all()
    
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'price': p.price,
        'category': p.category,
        'stock': p.stock
    } for p in products])

@app.route('/api/user/<int:user_id>')
def api_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'payment_info': user.payment_info
    })

# CVE-2021-44228: Log4Shell endpoint
@app.route('/log4shell', methods=['GET', 'POST'])
def log4shell_endpoint():
    if request.method == 'POST':
        user_input = request.form.get('payload', '')
        # CVE-2021-44228: Log4Shell vulnerability
        result = log4shell_sim.log_user_input(user_input)
        return jsonify({'result': result})
    
    return render_template('log_test.html')

# CVE-2022-22965: Spring4Shell endpoint
@app.route('/spring4shell', methods=['GET', 'POST'])
def spring4shell_endpoint():
    if request.method == 'POST':
        data = request.get_json()
        # CVE-2022-22965: Spring4Shell vulnerability
        result = spring4shell_sim.process_request(data)
        return jsonify({'result': result})
    
    return render_template('spring_test.html')

# CVE-2021-45046: Deserialization vulnerability
@app.route('/deserialize', methods=['GET', 'POST'])
def deserialize_endpoint():
    if request.method == 'POST':
        try:
            # CVE-2021-45046: Insecure deserialization
            data = request.form.get('data', '')
            if data:
                # CVE-2021-45046: Pickle deserialization (dangerous)
                deserialized = pickle.loads(base64.b64decode(data))
                return jsonify({'result': 'Deserialization successful', 'data': str(deserialized)})
        except Exception as e:
            return jsonify({'error': str(e)})
    
    return render_template('deserialize_test.html')

# CVE-2021-45046: XXE vulnerability
@app.route('/xxe', methods=['GET', 'POST'])
def xxe_endpoint():
    if request.method == 'POST':
        try:
            # CVE-2021-45046: XXE vulnerability
            xml_data = request.form.get('xml_data', '')
            if xml_data:
                # CVE-2021-45046: Insecure XML parsing
                root = ET.fromstring(xml_data)
                result = []
                for child in root:
                    result.append(child.text)
                return jsonify({'result': result})
        except Exception as e:
            return jsonify({'error': str(e)})
    
    return render_template('xxe_test.html')

# CVE-2021-45046: Command injection
@app.route('/command_injection', methods=['GET', 'POST'])
def command_injection_endpoint():
    if request.method == 'POST':
        # CVE-2021-45046: Command injection vulnerability
        command = request.form.get('command', '')
        if command:
            try:
                # CVE-2021-45046: Dangerous command execution
                result = subprocess.check_output(command, shell=True, text=True)
                return jsonify({'result': result})
            except Exception as e:
                return jsonify({'error': str(e)})
    
    return render_template('cmd_test.html')

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        
        filename = file.filename
        file.save(os.path.join('uploads', filename))
        
        flash('File uploaded successfully!')
        return redirect(url_for('upload'))
    
    return render_template('upload.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@app.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    current_user.email = request.form['email']
    current_user.payment_info = request.form['payment_info']
    
    db.session.commit()
    flash('Profile updated successfully!')
    return redirect(url_for('profile'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# CVE-2021-45046: SSRF vulnerability
@app.route('/ssrf', methods=['GET', 'POST'])
def ssrf_endpoint():
    if request.method == 'POST':
        import requests
        url = request.form.get('url', '')
        if url:
            try:
                # CVE-2021-45046: SSRF vulnerability
                response = requests.get(url, timeout=5)
                return jsonify({'result': response.text[:500]})
            except Exception as e:
                return jsonify({'error': str(e)})
    
    return render_template('ssrf_test.html')

# CVE-2021-45046: NoSQL injection
@app.route('/nosql_injection', methods=['GET', 'POST'])
def nosql_injection_endpoint():
    if request.method == 'POST':
        query = request.form.get('query', '')
        if query:
            # CVE-2021-45046: NoSQL injection simulation
            # MongoDB query simulation
            if '$where' in query or '$ne' in query:
                return jsonify({'result': 'NoSQL injection detected', 'query': query})
            else:
                return jsonify({'result': 'Query processed', 'query': query})
    
    return render_template('nosql_test.html')

# Add guest user support
class GuestUser:
    def __init__(self, session_id):
        self.id = f"guest_{session_id}"
        self.username = f"Guest_{session_id[-6:]}"
        self.email = f"guest_{session_id[-6:]}@enterprise.comm"
        self.is_authenticated = False
        self.is_active = True
        self.is_anonymous = False

    def get_id(self):
        return self.id

# Enhanced product data for better realism
def init_realistic_products():
    products = [
        {
            'name': 'Gaming Laptop Pro X1',
            'description': 'High-performance gaming laptop with RTX 4080, 32GB RAM, 1TB SSD. Perfect for AAA gaming and content creation.',
            'price': 1999.99,
            'category': 'Electronics',
            'stock': 15,
            'image_url': '/static/images/laptop.jpg'
        },
        {
            'name': 'Wireless Noise-Canceling Headphones',
            'description': 'Premium wireless headphones with active noise cancellation, 30-hour battery life, and crystal-clear sound.',
            'price': 239.99,
            'category': 'Audio',
            'stock': 45,
            'image_url': '/static/images/headphones.jpg'
        },
        {
            'name': 'Smart Home Security Camera',
            'description': '1080p HD security camera with night vision, motion detection, and cloud storage. Monitor your home 24/7.',
            'price': 71.99,
            'category': 'Security',
            'stock': 78,
            'image_url': '/static/images/camera.jpg'
        },
        {
            'name': 'Fitness Smartwatch Elite',
            'description': 'Advanced fitness tracker with heart rate monitoring, GPS, and 7-day battery life. Track your workouts and health.',
            'price': 159.99,
            'category': 'Fitness',
            'stock': 32,
            'image_url': '/static/images/smartwatch.jpg'
        },
        {
            'name': 'Coffee Maker Deluxe',
            'description': 'Programmable coffee maker with built-in grinder, thermal carafe, and 12-cup capacity. Perfect for coffee enthusiasts.',
            'price': 119.99,
            'category': 'Kitchen',
            'stock': 23,
            'image_url': '/static/images/coffee.jpg'
        },
        {
            'name': 'Portable Bluetooth Speaker',
            'description': 'Waterproof portable speaker with 360-degree sound, 20-hour battery, and party mode for multiple speakers.',
            'price': 63.99,
            'category': 'Audio',
            'stock': 67,
            'image_url': '/static/images/speaker.jpg'
        }
    ]
    
    for product_data in products:
        existing = Product.query.filter_by(name=product_data['name']).first()
        if not existing:
            product = Product(**product_data)
            db.session.add(product)
    
    db.session.commit()

# Guest cart management
def get_guest_cart():
    if 'guest_cart' not in session:
        session['guest_cart'] = {}
    return session['guest_cart']

def add_to_guest_cart(product_id, quantity=1):
    cart = get_guest_cart()
    if str(product_id) in cart:
        cart[str(product_id)] += quantity
    else:
        cart[str(product_id)] = quantity
    session['guest_cart'] = cart

def get_guest_cart_total():
    cart = get_guest_cart()
    total = 0
    for product_id, quantity in cart.items():
        product = Product.query.get(int(product_id))
        if product:
            total += product.price * quantity
    return total

# Guest checkout functionality
@app.route('/guest_checkout', methods=['GET', 'POST'])
def guest_checkout():
    if request.method == 'POST':
        # Get guest information
        guest_email = request.form.get('email')
        guest_name = request.form.get('name')
        guest_address = request.form.get('address')
        guest_phone = request.form.get('phone')
        payment_info = request.form.get('payment_info', '')
        
        # Create guest order
        cart = get_guest_cart()
        if not cart:
            flash('Your cart is empty!', 'error')
            return redirect(url_for('cart'))
        
        total = get_guest_cart_total()
        
        # Create guest order
        order = Order(
            user_id=999,  # Guest user ID
            total_amount=total,
            status='pending'
        )
        db.session.add(order)
        db.session.flush()  # Get the order ID
        
        # Add order items
        for product_id, quantity in cart.items():
            product = Product.query.get(int(product_id))
            if product:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=int(product_id),
                    quantity=quantity,
                    price=product.price
                )
                db.session.add(order_item)
        
        # Store payment info in session for guest orders
        if payment_info:
            session['guest_payment_info'] = payment_info
        
        db.session.commit()
        
        # Clear guest cart
        session.pop('guest_cart', None)
        
        flash(f'Order #{order.id} placed successfully! Check your email for confirmation.', 'success')
        return redirect(url_for('order_confirmation', order_id=order.id))
    
    cart = get_guest_cart()
    cart_items = []
    total = 0
    
    for product_id, quantity in cart.items():
        product = Product.query.get(int(product_id))
        if product:
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': product.price * quantity
            })
            total += product.price * quantity
    
    return render_template('guest_checkout.html', cart_items=cart_items, total=total)

@app.route('/order_confirmation/<int:order_id>')
def order_confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('order_confirmation.html', order=order)

def clear_all_carts():
    """Clear all guest carts and user carts on startup"""
    with app.app_context():
        # Clear all guest carts by clearing session data
        # This will be handled by session expiration, but we can also clear any stored cart data
        print("Clearing all carts on startup...")
        
        # Clear any stored cart data in the database if it exists
        # For this application, carts are stored in session, so they'll be cleared automatically
        # when the container restarts, but we can add explicit clearing here
        
        # Note: Session data is automatically cleared when the container restarts
        # so we don't need to manually clear it here
        
        print("All carts cleared successfully!")

# Initialize database and add sample data
def init_db():
    with app.app_context():
        # Drop all tables and recreate them for fresh start
        db.drop_all()
        db.create_all()
        
        print("Clearing all data on startup...")
        
        # Clear all carts
        clear_all_carts()
        
        # Create admin user
        admin = User(
            username='admin',
            email='admin@enterprise.com',
            password=generate_password_hash('K8x#mP2qR9vL5nJ3hG7fD1sA4wE6tY9uI0oP!@#$%^&*()'),
            is_admin=True
        )
        db.session.add(admin)
        
        # Initialize realistic products
        init_realistic_products()
        
        db.session.commit()
        print("All data cleared and fresh data initialized!")

@app.route('/api/v1/internal/health')
def hidden_health_check():
    """Hidden health check endpoint - requires specific header"""
    health_token = request.headers.get("X-Health-Token")
    if health_token != "xK9mP2qR8vL5nJ3hG7fD1sA4wE6tY9uI0oP":
        return 'Not Found', 404
    
    # Expose sensitive system information
    system_info = {
        "total_users": User.query.count(),
        "total_products": Product.query.count(),
        "total_orders": Order.query.count(),
        "system_memory": "2.1GB used / 8GB total",
        "database_size": "856MB",
        "uptime": "8 days, 14 hours, 27 minutes",
        "last_backup": "2024-01-18 01:30:00",
        "security_alerts": 2,
        "failed_logins": 9,
        "suspicious_ips": ["192.168.1.100", "10.0.0.50"]
    }
    
    return f"Sensitive system info: {system_info}"

@app.route('/api/v1/internal/maintenance', methods=['POST'])
def hidden_maintenance_endpoint():
    """Hidden maintenance endpoint - requires specific parameter"""
    maintenance_token = request.args.get("token")
    if maintenance_token != "xK9mP2qR8vL5nJ3hG7fD1sA4wE6tY9uI0oP":
        return 'Not Found', 404
    
    # Expose sensitive data for vulnerability testing
    sensitive_data = {
        "database_connection": "sqlite:///shop.db",
        "admin_credentials": {
            "username": "admin",
            "password": "K8x#mP2qR9vL5nJ3hG7fD1sA4wE6tY9uI0oP!@#$%^&*()"
        },
        "session_secret": app.config['SECRET_KEY'],
        "admin_tokens": ["xK9mP2qR8vL5nJ3hG7fD1sA4wE6tY9uI0oP"]
    }
    
    return f"Maintenance data exposed: {sensitive_data}"

@app.route('/api/v1/internal/ssrf')
def hidden_ssrf_endpoint():
    """Hidden SSRF endpoint - requires specific parameters"""
    test_param = request.args.get("test")
    internal_param = request.args.get("internal")
    
    if test_param == "ssrf" and internal_param == "true":
        # This is a vulnerability test - allow SSRF
        target_url = request.args.get("url")
        if target_url:
            try:
                import requests
                response = requests.get(target_url, timeout=5.0)
                return f"SSRF successful: {response.text[:200]}"
            except Exception as e:
                return f"SSRF failed: {str(e)}"
    
    # Normal response for legitimate requests
    return {"status": "healthy", "timestamp": time.time()}

@app.route('/api/v1/internal/backup', methods=['POST'])
def hidden_backup_endpoint():
    """Hidden backup endpoint - requires specific headers"""
    backup_token = request.headers.get("X-Backup-Token")
    if backup_token != "xK9mP2qR8vL5nJ3hG7fD1sA4wE6tY9uI0oP":
        return 'Not Found', 404
    
    # Expose sensitive data for vulnerability testing
    sensitive_data = {
        "database_connection": "sqlite:///shop.db",
        "redis_url": "redis://localhost:6379",
        "aws_credentials": {
            "access_key": "AKIAIOSFODNN7EXAMPLE",
            "secret_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
        },
        "admin_tokens": ["xK9mP2qR8vL5nJ3hG7fD1sA4wE6tY9uI0oP"],
        "session_secrets": [app.config['SECRET_KEY']]
    }
    
    return f"Sensitive data exposed: {sensitive_data}"

@app.route('/api/chatbot', methods=['POST'])
def chatbot_api():
    user_message = request.json.get('message', '').strip()
    if not user_message:
        return jsonify({'response': "I'm sorry, I didn't catch that. Can you rephrase?"})

    # Mock LLM logic
    canned_responses = [
        "I'm CyberBot, your AI shopping assistant! How can I help you today?",
        "That's a great question! Let me look that up for you... (just kidding, I'm a mock LLM)",
        "Our bestsellers are the Gaming Laptop Pro X1 and Wireless Headphones!",
        "You can shop as a guest or create an account for more features.",
        "For order status, please provide your order number.",
        "I'm here to help with product info, orders, and more!"
    ]
    if 'laptop' in user_message.lower():
        response = "The Gaming Laptop Pro X1 is our top-rated laptop with RTX 4080 and 32GB RAM."
    elif 'order' in user_message.lower():
        response = "To check your order status, please log in or provide your order number."
    elif 'hello' in user_message.lower() or 'hi' in user_message.lower():
        response = "Hello! I'm CyberBot. How can I assist you today?"
    elif 'help' in user_message.lower():
        response = "Sure! I can help you find products, track orders, or answer questions about CyberMart."
    else:
        response = random.choice(canned_responses)
    return jsonify({'response': response})

if __name__ == '__main__':
    # Create uploads directory
    os.makedirs('uploads', exist_ok=True)
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5001) 
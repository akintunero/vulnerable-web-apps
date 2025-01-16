import sqlite3

DB_PATH = 'database/airline.db'

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute("PRAGMA table_info(bookings)")
columns = [row[1] for row in c.fetchall()]

if 'passport_data' not in columns:
    c.execute("ALTER TABLE bookings ADD COLUMN passport_data TEXT")

if 'pnr' not in columns:
    c.execute("ALTER TABLE bookings ADD COLUMN pnr TEXT")

conn.commit()
conn.close() 
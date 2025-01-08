DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS flights;
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS points;
DROP TABLE IF EXISTS audit_logs;
DROP TABLE IF EXISTS siem_logs;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    loyalty_tier TEXT DEFAULT 'Bronze',
    is_decoy_admin INTEGER DEFAULT 0
);

CREATE TABLE flights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_number TEXT NOT NULL,
    from_city TEXT NOT NULL,
    to_city TEXT NOT NULL,
    departure_time TEXT NOT NULL,
    arrival_time TEXT NOT NULL,
    date TEXT NOT NULL,
    price REAL NOT NULL,
    available_seats INTEGER NOT NULL,
    aircraft_type TEXT NOT NULL
);

CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_id INTEGER NOT NULL,
    passenger_name TEXT NOT NULL,
    passenger_email TEXT NOT NULL,
    seat_class TEXT NOT NULL,
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'confirmed',
    passport_data TEXT,
    pnr TEXT,
    FOREIGN KEY (flight_id) REFERENCES flights (id)
);

CREATE TABLE points (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    balance INTEGER DEFAULT 1000,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event TEXT NOT NULL,
    user_id INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE siem_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_type TEXT NOT NULL,
    message TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO flights (flight_number, from_city, to_city, departure_time, arrival_time, date, price, available_seats, aircraft_type) VALUES
('SH001', 'New York', 'Los Angeles', '08:00', '11:30', '2024-02-15', 299.99, 150, 'Boeing 737'),
('SH002', 'Los Angeles', 'New York', '14:00', '17:30', '2024-02-15', 299.99, 150, 'Boeing 737'),
('SH003', 'Chicago', 'Miami', '09:30', '12:45', '2024-02-15', 199.99, 120, 'Airbus A320'),
('SH004', 'Miami', 'Chicago', '15:30', '18:45', '2024-02-15', 199.99, 120, 'Airbus A320'),
('SH005', 'Seattle', 'Denver', '10:00', '12:15', '2024-02-15', 149.99, 100, 'Boeing 737'),
('SH006', 'Denver', 'Seattle', '16:00', '18:15', '2024-02-15', 149.99, 100, 'Boeing 737'),
('SH007', 'Boston', 'San Francisco', '07:30', '11:00', '2024-02-15', 399.99, 180, 'Boeing 787'),
('SH008', 'San Francisco', 'Boston', '13:30', '17:00', '2024-02-15', 399.99, 180, 'Boeing 787'),
('SH009', 'Atlanta', 'Las Vegas', '11:00', '13:30', '2024-02-15', 249.99, 140, 'Airbus A321'),
('SH010', 'Las Vegas', 'Atlanta', '17:00', '19:30', '2024-02-15', 249.99, 140, 'Airbus A321'); 
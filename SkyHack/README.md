# ✈️ SkyHack Airlines - Airline Booking Portal

A comprehensive airline booking system built with Flask to demonstrate web application concepts and security training.

## ⚠️ DISCLAIMER ⚠️

**THIS APPLICATION IS DESIGNED FOR:**

- Educational purposes
- Security training
- CTF (Capture The Flag) challenges
- Security research in controlled environments
- Penetration testing practice

**DO NOT DEPLOY THIS APPLICATION IN PRODUCTION OR ON PUBLIC NETWORKS.**

**THE DEVELOPERS ARE NOT RESPONSIBLE FOR ANY MISUSE OF THIS APPLICATION.**

## ⚠️ Security Warning

> **This application is designed for educational purposes. For your safety, always run it inside Docker.**
>
> - **Never run on your host system or a public network.**
> - **Use only in isolated, controlled environments.**
> - **The developers are not responsible for misuse or data loss.**

---

## 🛩️ SkyHack Airlines - Web Application

A comprehensive airline booking system built with Flask to demonstrate web application concepts and security training.

## 🎯 Features

### ✈️ Core Systems
- **Flight Booking System** - Complete booking functionality
- **Check-In System** - Passenger check-in management
- **Admin Panel** - Administrative interface
- **Frequent Flyer Portal** - Loyalty program management
- **Payment System** - Payment processing simulation
- **Mobile API** - Mobile application support

### 🔧 Technical Features

#### 1. Flight Management
- Flight search and booking
- Seat selection
- Booking management
- Flight status updates

#### 2. User Management
- User registration and authentication
- Profile management
- Session handling
- Access control

#### 3. Payment Processing
- Payment method management
- Transaction processing
- Receipt generation
- Financial data handling

#### 4. Administrative Functions
- Flight management
- User administration
- System monitoring
- Data management

## 🚀 Quick Start

### Prerequisites
- Docker
- Docker Compose

### Installation & Setup

```bash
# Clone the repository
git clone https://github.com/akintunero/vulnerable-web-apps.git
cd vulnerable-web-apps/SkyHack

# Start the application
docker-compose up -d

# Access the application
# URL: http://localhost:8080
```

## 🏗️ Architecture

### Components
- **Frontend**: HTML/CSS/JavaScript
- **Backend**: Python Flask application
- **Database**: SQLite
- **Container**: Docker with Python 3.9

### Directory Structure
```
SkyHack/
├── app.py              # Main Flask application
├── airports.json       # Airport data
├── templates/          # HTML templates
├── static/            # CSS, JS, images
├── database/          # Database files
├── logs/              # Application logs
├── docker-compose.yml # Docker configuration
├── Dockerfile         # Container definition
└── requirements.txt   # Python dependencies
```

## 🎓 Learning Objectives

This application is designed to help users understand:

1. **Web Application Security Concepts**
   - Input validation and sanitization
   - Authentication and authorization
   - Session management
   - Data protection

2. **Security Testing Methodologies**
   - Manual testing approaches
   - Automated testing tools
   - Security assessment frameworks

3. **Defensive Programming**
   - Secure coding practices
   - Security best practices
   - Risk mitigation strategies

## 🔍 Application Features

### 1. Flight Booking
- Flight search and filtering
- Seat selection
- Booking management
- Payment processing

### 2. User Management
- User registration and authentication
- Profile management
- Session handling
- Access control

### 3. Administrative Functions
- Flight management
- User administration
- System monitoring
- Data management

### 4. API Integration
- Mobile application support
- External service integration
- Data exchange protocols

## 🛠️ Development

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### Docker Development
```bash
# Build and run with Docker
docker-compose up --build
```

## 🔧 Configuration

### Environment Variables
```bash
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///skyhack.db
PORT=8080
UPLOAD_FOLDER=uploads/
```

## 📡 API Endpoints

### Authentication
- `POST /login` - User authentication
- `POST /register` - User registration
- `GET /logout` - User logout

### Flight Management
- `GET /api/flights` - Get available flights
- `GET /api/flights/search` - Search flights
- `GET /api/flights/<id>` - Get flight details
- `POST /api/flights` - Create flight (admin)

### Booking
- `GET /api/bookings` - Get user bookings
- `POST /api/bookings` - Create booking
- `GET /api/bookings/<id>` - Get booking details
- `PUT /api/bookings/<id>` - Update booking
- `DELETE /api/bookings/<id>` - Cancel booking

### Passenger Management
- `GET /api/passengers` - Get passenger profiles
- `POST /api/passengers` - Create passenger profile
- `PUT /api/passengers/<id>` - Update passenger profile

### Check-in
- `GET /api/checkin/<booking_id>` - Get check-in status
- `POST /api/checkin/<booking_id>` - Perform check-in
- `GET /api/boarding-pass/<booking_id>` - Get boarding pass

### Admin Functions
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/flights` - Flight management
- `GET /admin/bookings` - Booking management
- `GET /admin/users` - User management

## 📚 Documentation

For detailed information about the application structure and features, refer to the inline code documentation and comments.

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines and ensure all changes maintain the educational nature of this application.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This application is for educational purposes only. The developers are not responsible for any misuse of this software. 
# 🪙 FakeCrypto - Cryptocurrency Trading Platform

A cryptocurrency trading platform designed for security research and testing practice. This application demonstrates various web application concepts in a controlled, educational environment.

## ⚠️ **SECURITY WARNING**

**This application is designed for educational purposes and should ONLY be run in isolated Docker containers. Never deploy to production or expose to public networks.**

## 🎯 Overview

FakeCrypto is a cryptocurrency trading platform that simulates a real-world crypto exchange. It's designed to help security researchers, penetration testers, and students learn about web application security concepts.

### Key Features:
- 💰 Cryptocurrency trading simulation
- 🔐 Authentication systems
- 💳 Payment processing
- 📊 Data management
- 🎨 NFT marketplace

## 🚀 Quick Start

### Prerequisites
- Docker
- Docker Compose

### Installation & Setup

```bash
# Clone the repository
git clone git@github.com:akintunero/vulnerable-web-apps.git
cd vulnerable-web-apps/OpenSource/FakeCrypto

# Start the application
docker-compose up -d

# Access the application
# URL: http://localhost:7004
```

## 🏗️ Architecture

### Components
- **Frontend**: HTML/CSS/JavaScript with Tailwind CSS
- **Backend**: Python Flask application
- **Database**: SQLite with JSON data files
- **Container**: Docker with Python 3.9

### Directory Structure
```
FakeCrypto/
├── app.py              # Main Flask application
├── data_manager.py     # Data management utilities
├── templates/          # HTML templates
├── static/            # CSS, JS, images
├── data/              # JSON data files
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

### 1. User Management
- User registration and authentication
- Profile management
- Session handling

### 2. Trading System
- Cryptocurrency trading simulation
- Portfolio management
- Transaction history

### 3. Payment Processing
- Payment method management
- Transaction processing
- Financial data handling

### 4. Data Management
- User data storage
- Transaction records
- System logs

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

## 📚 Documentation

For detailed information about the application structure and features, refer to the inline code documentation and comments.

## 🔌 API Endpoints

### Authentication
- `POST /login` - User authentication
- `POST /register` - User registration
- `GET /logout` - User logout

### Trading
- `GET /api/prices` - Get cryptocurrency prices
- `POST /api/buy` - Buy cryptocurrency
- `POST /api/sell` - Sell cryptocurrency
- `GET /api/portfolio` - Get user portfolio
- `GET /api/transactions` - Get transaction history

### User Management
- `GET /api/profile` - Get user profile
- `PUT /api/profile` - Update user profile
- `POST /api/deposit` - Deposit funds
- `POST /api/withdraw` - Withdraw funds

### NFT Marketplace
- `GET /api/nfts` - List available NFTs
- `POST /api/nfts/buy` - Buy NFT
- `POST /api/nfts/sell` - Sell NFT
- `POST /api/nfts/upload` - Upload NFT

### Admin
- `GET /admin/users` - List all users
- `GET /admin/transactions` - View all transactions
- `POST /admin/approve` - Approve transactions

## ⚙️ Environment Variables

### Required Variables
```bash
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///fakecrypto.db
UPLOAD_FOLDER=./uploads
```

### Optional Variables
```bash
LOG_LEVEL=INFO
MAX_FILE_SIZE=16777216
ALLOWED_EXTENSIONS=jpg,jpeg,png,gif
SESSION_TIMEOUT=3600
```

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines and ensure all changes maintain the educational nature of this application.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This application is for educational purposes only. The developers are not responsible for any misuse of this software. 
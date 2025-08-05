# 🛒 CyberMart - E-commerce Platform

A comprehensive e-commerce platform designed for security research and testing practice. This application demonstrates various web application concepts in a realistic e-commerce environment.

## ⚠️ **SECURITY WARNING**

**This application is designed for educational purposes and should ONLY be run in isolated Docker containers. Never deploy to production or expose to public networks.**

## Overview

CyberMart is an e-commerce platform that simulates a real-world online store. It's designed to help security researchers, penetration testers, and students learn about web application security concepts in an e-commerce context.

### Key Features:
- 🛍️ Complete e-commerce functionality
- 👥 User account management
- 📦 Product catalog with categories
- 🛒 Shopping cart and wishlist
- 💳 Checkout and payment processing
- 📋 Order management and tracking
- 💰 Discount code system
- 📄 PDF invoice generation
- 📧 Email notifications
- ⭐ Product reviews and ratings
- 🔧 Admin panel for management

## Quick Start

### Prerequisites
- Docker
- Docker Compose

### Installation & Setup

```bash
# Clone the repository
git clone git@github.com:akintunero/vulnerable-web-apps.git
cd vulnerable-web-apps/CyberMart

# Start the application
./start.sh

# Access the application
# URL: http://localhost:5002
```

## Architecture

### Components
- **Frontend**: HTML/CSS/JavaScript with Bootstrap
- **Backend**: Python Flask application
- **Database**: SQLite (primary), MongoDB (NoSQL injection testing)
- **Cache**: Redis (rate limiting)
- **Container**: Docker with Python 3.9

### Directory Structure
```
CyberMart/
├── app.py                 # Main Flask application
├── templates/             # HTML templates
├── static/               # CSS, JS, images
├── uploads/              # File uploads
├── docker-compose.yml    # Docker configuration
├── Dockerfile           # Container definition
├── requirements.txt     # Python dependencies
└── start.sh            # Startup script
```

## Learning Objectives

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

## Application Features

### 1. E-commerce Functionality
- Product catalog and search
- Shopping cart management
- Checkout and payment processing
- Order tracking and management

### 2. User Management
- User registration and authentication
- Profile management
- Session handling
- Access control

### 3. Administrative Functions
- Product management
- Order administration
- User management
- System monitoring

### 4. Payment Processing
- Payment method management
- Transaction processing
- Invoice generation
- Financial data handling

## Features

### E-commerce Functionality
- **Product Catalog**: Categories, search, filtering
- **Shopping Cart**: Add/remove items, quantity management
- **Wishlist**: Save products for later
- **User Accounts**: Registration, login, profile management
- **Checkout Process**: Address, payment, discount codes
- **Order Management**: History, tracking, status updates
- **Reviews & Ratings**: Product feedback system
- **Admin Panel**: Product, order, user management
- **PDF Invoices**: Downloadable order invoices
- **Email Notifications**: Order confirmations, status updates

### Technical Features
- **Professional Interface**: Modern e-commerce design
- **Comprehensive Functionality**: Full e-commerce workflow
- **Educational Value**: Clear learning objectives
- **Testing Support**: Compatible with security testing tools

## Configuration

### Environment Variables
```bash
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///shop.db
UPLOAD_FOLDER=uploads/
PORT=5002
```

### Database Setup
```bash
# Initialize database
python3 -c "from app import init_db; init_db()"
```

## API Endpoints

### Authentication
- `POST /login` - User authentication
- `POST /register` - User registration
- `GET /logout` - User logout

### Products
- `GET /api/products` - Get all products
- `GET /api/products/search` - Search products
- `GET /api/products/<id>` - Get product details
- `POST /api/products` - Add new product (admin)

### Shopping Cart
- `GET /api/cart` - Get user cart
- `POST /api/cart/add` - Add item to cart
- `PUT /api/cart/update` - Update cart item
- `DELETE /api/cart/remove` - Remove item from cart

### Orders
- `GET /api/orders` - Get user orders
- `POST /api/orders` - Create new order
- `GET /api/orders/<id>` - Get order details
- `GET /api/invoice/<id>` - Get order invoice

### User Management
- `GET /api/profile` - Get user profile
- `PUT /api/profile` - Update user profile
- `GET /api/addresses` - Get user addresses

### Admin Functions
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/products` - Product management
- `GET /admin/orders` - Order management
- `GET /admin/users` - User management

## Usage

### Starting the Application
```bash
./start.sh
```

### Accessing the Application
- **Main Site**: http://localhost:5002
- **Admin Panel**: http://localhost:5002/admin
- **API Endpoints**: http://localhost:5002/api/*

### User Accounts
- User registration and login functionality
- Admin panel access management
- Role-based access control

## Security Notes

- Designed for educational purposes
- No real payment processing
- Mock data for testing
- Isolated Docker environment
- Educational purposes only

## Educational Resources

- OWASP Top 10
- Web Application Security Testing
- E-commerce Security Best Practices
- Vulnerability Assessment Methodologies

## Contributing

This project is designed for educational purposes. Contributions should focus on:
- Adding new vulnerability types
- Improving educational content
- Enhancing testing scenarios
- Documentation improvements

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Remember**: This application is for educational purposes only. Never use these techniques on real systems without proper authorization. 
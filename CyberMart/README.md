# ShopCart - E-commerce Application

A Flask-based e-commerce application for learning web application security testing.

## Features

- User registration and authentication
- Product browsing and search
- Shopping cart functionality
- Order management
- Admin panel
- File upload capabilities
- REST API endpoints

## Vulnerabilities Included

This application contains various security issues for educational purposes:

- Authentication bypasses
- Data exposure vulnerabilities
- Input validation issues
- Access control problems
- File handling weaknesses
- API security flaws

## Installation & Running

### Prerequisites

- Docker installed on your system
- Docker Compose (optional, for advanced usage)

### Quick Start (Recommended)

Use the provided management script for the easiest experience:

```bash
# Clone the repository
git clone <repository-url>
cd vuln-cart

# Build and start the application
./run.sh build
./run.sh start
```

**Available script commands:**
- `./run.sh build` - Build the Docker image
- `./run.sh start` - Start the application
- `./run.sh stop` - Stop the application
- `./run.sh restart` - Restart the application
- `./run.sh logs` - View application logs
- `./run.sh status` - Check container status
- `./run.sh remove` - Remove the container
- `./run.sh help` - Show help information

### Manual Docker Commands

If you prefer to use Docker commands directly:

1. **Clone the repository:**
```bash
git clone <repository-url>
cd vuln-cart
```

2. **Build the Docker image:**
```bash
docker build -t shopcart .
```

3. **Run the application:**
```bash
docker run -d -p 5001:5001 --name shopcart-app shopcart
```

4. **Access the application:**
   - Open your browser and go to `http://localhost:5001`

### Using Docker Compose

Create a `docker-compose.yml` file:

```yaml
version: '3.8'
services:
  shopcart:
    build: .
    ports:
      - "5001:5001"
    volumes:
      - ./uploads:/app/uploads
    environment:
      - FLASK_ENV=development
    restart: unless-stopped
```

Then run:
```bash
docker-compose up -d
```

### Container Management

**Stop the application:**
```bash
docker stop shopcart-app
```

**Start the application:**
```bash
docker start shopcart-app
```

**Remove the container:**
```bash
docker rm shopcart-app
```

**View logs:**
```bash
docker logs shopcart-app
```

**Rebuild and restart:**
```bash
docker stop shopcart-app && docker rm shopcart-app
docker build -t shopcart .
docker run -d -p 5001:5001 --name shopcart-app shopcart
```

## Default Credentials

- **Admin User:**
  - Username: `admin`
  - Password: `admin123`

## API Endpoints

- `GET /api/products` - List all products
- `GET /api/products?category=<category>` - Filter products by category
- `GET /api/user/<id>` - Get user information

## Security Testing

This application is designed for security testing and contains intentional vulnerabilities. Use only in controlled environments for educational purposes.

## Docker Benefits

Using Docker ensures:
- Consistent environment across different systems
- Easy deployment and scaling
- Isolated testing environment
- No conflicts with local Python installations
- Reproducible builds

## Troubleshooting

**Port already in use:**
```bash
# Check what's using port 5001
lsof -i :5001

# Use a different port
docker run -d -p 5002:5001 --name shopcart-app shopcart
```

**Container won't start:**
```bash
# Check container logs
docker logs shopcart-app

# Rebuild the image
docker build --no-cache -t shopcart .
```

**Permission issues:**
```bash
# Run with proper permissions
docker run -d -p 5001:5001 --name shopcart-app --user root shopcart
```

**Script permission denied:**
```bash
# Make the script executable
chmod +x run.sh
```

## Disclaimer

This application is for educational purposes only. Do not use in production environments or on systems you do not own or have explicit permission to test. 
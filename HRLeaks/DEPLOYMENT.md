# Deployment Guide

## 🚀 **HRLeaks Deployment Guide**

This guide provides comprehensive instructions for deploying HRLeaks in various environments. **Remember that this application is intentionally vulnerable and should only be deployed in controlled, isolated environments.**

## ⚠️ **Important Security Notice**

**HRLeaks contains 26 intentional vulnerabilities and should NEVER be deployed:**
- On production servers
- On public cloud instances
- On internet-facing systems
- In shared hosting environments
- On networks with sensitive data

**Safe deployment environments:**
- Isolated virtual machines
- Docker containers in isolated networks
- Offline testing environments
- Controlled lab environments
- Educational institutions (with proper controls)

## 🐳 **Docker Deployment (Recommended)**

### Prerequisites
- Docker Engine 20.10+
- Docker Compose 2.0+
- Git

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/akintunero/HRLeaks.git
   cd HRLeaks
   ```

2. **Build and run**
   ```bash
   docker compose up --build
   ```

3. **Access the application**
   - Main application: http://localhost:8000
   - Mock dashboard: http://localhost:8000/dashboard/mock
   - Mock employees: http://localhost:8000/employees/mock

### Docker Configuration

#### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### docker-compose.yml
```yaml
version: '3.8'

services:
  hrleaks:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./uploads:/app/uploads
      - ./temp:/app/temp
    environment:
      - ENVIRONMENT=production
    restart: unless-stopped
    networks:
      - hrleaks-network

networks:
  hrleaks-network:
    driver: bridge
```

### Advanced Docker Configuration

#### Isolated Network Deployment
```bash
# Create isolated network
docker network create hrleaks-isolated

# Run with isolated network
docker run --network hrleaks-isolated --name hrleaks -p 8000:8000 hrleaks
```

#### Docker with Resource Limits
```yaml
version: '3.8'

services:
  hrleaks:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./uploads:/app/uploads
      - ./temp:/app/temp
    environment:
      - ENVIRONMENT=production
    restart: unless-stopped
    networks:
      - hrleaks-network
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
      - /var/tmp

networks:
  hrleaks-network:
    driver: bridge
    internal: true
```

## 🐍 **Manual Python Deployment**

### Prerequisites
- Python 3.9+
- pip
- Git

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/akintunero/HRLeaks.git
   cd HRLeaks
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create required directories**
   ```bash
   mkdir -p uploads temp
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

### Production Deployment with Gunicorn

1. **Install Gunicorn**
   ```bash
   pip install gunicorn
   ```

2. **Create Gunicorn configuration**
   ```python
   # gunicorn.conf.py
   bind = "0.0.0.0:8000"
   workers = 4
   worker_class = "uvicorn.workers.UvicornWorker"
   timeout = 120
   max_requests = 1000
   max_requests_jitter = 100
   ```

3. **Run with Gunicorn**
   ```bash
   gunicorn -c gunicorn.conf.py main:app
   ```

## ☁️ **Cloud Deployment (Educational Only)**

### AWS EC2 Deployment

**⚠️ WARNING: Only for educational purposes in isolated environments**

1. **Launch EC2 instance**
   ```bash
   # Use Amazon Linux 2 or Ubuntu
   # Instance type: t3.micro or t3.small
   # Security Group: Only allow SSH and HTTP from your IP
   ```

2. **Install Docker**
   ```bash
   sudo yum update -y
   sudo yum install -y docker
   sudo service docker start
   sudo usermod -a -G docker ec2-user
   sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

3. **Deploy application**
   ```bash
   git clone https://github.com/akintunero/HRLeaks.git
   cd HRLeaks
   docker compose up -d
   ```

### Google Cloud Platform

1. **Create Compute Engine instance**
   ```bash
   gcloud compute instances create hrleaks \
     --zone=us-central1-a \
     --machine-type=e2-micro \
     --image-family=debian-11 \
     --image-project=debian-cloud
   ```

2. **Install Docker and deploy**
   ```bash
   # SSH into instance
   sudo apt-get update
   sudo apt-get install -y docker.io docker-compose
   sudo systemctl start docker
   sudo systemctl enable docker
   
   git clone https://github.com/akintunero/HRLeaks.git
   cd HRLeaks
   sudo docker compose up -d
   ```

## 🔧 **Environment Configuration**

### Environment Variables

Create a `.env` file for configuration:

```env
# Application Settings
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=your-secret-key-here
HOST=0.0.0.0
PORT=8000

# Database Settings (if using external database)
DATABASE_URL=sqlite:///./hrleaks.db

# Security Settings
SESSION_TIMEOUT=3600
MAX_FILE_SIZE=10485760
ALLOWED_FILE_TYPES=pdf,html,docx,txt

# Logging
LOG_LEVEL=INFO
LOG_FILE=hrleaks.log
```

### Configuration File

Create `config.py` for advanced configuration:

```python
import os
from pathlib import Path

class Config:
    # Application
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
    
    # Server
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 8000))
    
    # File Uploads
    UPLOAD_FOLDER = Path('uploads')
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 10 * 1024 * 1024))  # 10MB
    ALLOWED_EXTENSIONS = {'pdf', 'html', 'docx', 'txt'}
    
    # Security
    SESSION_TIMEOUT = int(os.getenv('SESSION_TIMEOUT', 3600))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'hrleaks.log')
```

## 🔒 **Security Hardening**

### Network Security

1. **Firewall Configuration**
   ```bash
   # UFW (Ubuntu)
   sudo ufw allow ssh
   sudo ufw allow 8000
   sudo ufw enable
   
   # iptables (CentOS/RHEL)
   sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
   sudo iptables -A INPUT -p tcp --dport 8000 -j ACCEPT
   sudo iptables -A INPUT -j DROP
   ```

2. **Reverse Proxy with Nginx**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

### Container Security

1. **Run with limited privileges**
   ```bash
   docker run --read-only --security-opt no-new-privileges hrleaks
   ```

2. **Use non-root user**
   ```dockerfile
   RUN adduser --disabled-password --gecos '' appuser
   USER appuser
   ```

## 📊 **Monitoring and Logging**

### Health Checks

1. **Application Health Check**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Docker Health Check**
   ```dockerfile
   HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
     CMD curl -f http://localhost:8000/health || exit 1
   ```

### Logging Configuration

1. **Application Logging**
   ```python
   import logging
   
   logging.basicConfig(
       level=logging.INFO,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
       handlers=[
           logging.FileHandler('hrleaks.log'),
           logging.StreamHandler()
       ]
   )
   ```

2. **Docker Logging**
   ```yaml
   services:
     hrleaks:
       logging:
         driver: "json-file"
         options:
           max-size: "10m"
           max-file: "3"
   ```

## 🔄 **Backup and Recovery**

### Data Backup

1. **Backup Configuration**
   ```bash
   # Backup uploads directory
   tar -czf hrleaks-backup-$(date +%Y%m%d).tar.gz uploads/
   
   # Backup configuration
   cp .env hrleaks-config-$(date +%Y%m%d).env
   ```

2. **Automated Backup Script**
   ```bash
   #!/bin/bash
   BACKUP_DIR="/backups/hrleaks"
   DATE=$(date +%Y%m%d_%H%M%S)
   
   mkdir -p $BACKUP_DIR
   tar -czf $BACKUP_DIR/hrleaks-$DATE.tar.gz uploads/ temp/
   
   # Keep only last 7 days of backups
   find $BACKUP_DIR -name "hrleaks-*.tar.gz" -mtime +7 -delete
   ```

## 🚨 **Troubleshooting**

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check what's using port 8000
   lsof -i :8000
   
   # Kill process or change port
   docker compose up -p 8001:8000
   ```

2. **Permission Issues**
   ```bash
   # Fix upload directory permissions
   sudo chown -R $USER:$USER uploads/
   chmod 755 uploads/
   ```

3. **Docker Build Issues**
   ```bash
   # Clean Docker cache
   docker system prune -a
   docker compose build --no-cache
   ```

### Log Analysis

1. **Application Logs**
   ```bash
   tail -f hrleaks.log
   ```

2. **Docker Logs**
   ```bash
   docker compose logs -f
   ```

## 📞 **Support**

For deployment issues:
- **Email**: akintunero101@gmail.com
- **GitHub Issues**: [Create an issue](https://github.com/akintunero/HRLeaks/issues)

---

**⚠️ Remember**: This application is intentionally vulnerable. Use only in controlled, isolated environments for educational purposes. 
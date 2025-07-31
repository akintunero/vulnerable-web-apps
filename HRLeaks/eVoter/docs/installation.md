# Installation Guide

This guide will help you set up and run E-VoteNow on your system. The project is designed to run in Docker containers for safety and consistency.

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your system:

### Required Software
- **Docker** (version 20.10.0 or higher)
- **Docker Compose** (version 2.0.0 or higher)
- **Git** (for cloning the repository)

### System Requirements
- **Operating System**: macOS, Windows, or Linux
- **RAM**: Minimum 2GB (4GB recommended)
- **Storage**: At least 1GB free space
- **Network**: Internet connection for initial setup

## 🚀 Quick Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/akintunero/evoting-system.git
cd evoting-system
```

### Step 2: Build and Run with Docker

```bash
docker-compose up --build
```

### Step 3: Access the Application

Open your web browser and navigate to:
```
http://localhost:8000
```

That's it! The application should now be running.

## 📦 Detailed Installation

### Option 1: Docker Installation (Recommended)

#### 1. Install Docker

**macOS:**
```bash
# Using Homebrew
brew install --cask docker

# Or download from Docker website
# https://docs.docker.com/desktop/mac/install/
```

**Windows:**
```bash
# Download Docker Desktop from
# https://docs.docker.com/desktop/windows/install/
```

**Linux (Ubuntu/Debian):**
```bash
# Update package index
sudo apt-get update

# Install prerequisites
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Set up stable repository
echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io

# Add user to docker group
sudo usermod -aG docker $USER
```

#### 2. Install Docker Compose

**macOS/Windows:**
Docker Compose is included with Docker Desktop.

**Linux:**
```bash
# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### 3. Verify Installation

```bash
# Check Docker version
docker --version

# Check Docker Compose version
docker-compose --version

# Test Docker installation
docker run hello-world
```

### Option 2: Local Development Installation

⚠️ **Warning**: This option is for development purposes only. The application contains intentional vulnerabilities and should not be run directly on your system.

#### 1. Install Python

**macOS:**
```bash
# Using Homebrew
brew install python@3.11

# Or download from python.org
# https://www.python.org/downloads/
```

**Windows:**
```bash
# Download from python.org
# https://www.python.org/downloads/
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3.11 python3.11-venv python3.11-pip

# CentOS/RHEL
sudo yum install python3.11 python3.11-pip
```

#### 2. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/akintunero/evoting-system.git
cd evoting-system

# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Run the Application

```bash
# Start the application
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Access at http://localhost:8000
```

## 🔧 Configuration

### Environment Variables

The application uses the following environment variables (defined in `docker-compose.yml`):

```yaml
environment:
  - PYTHONPATH=/app
  - PORT=8000
  - HOST=0.0.0.0
```

### Custom Configuration

To customize the application:

1. **Change Port**: Modify the port mapping in `docker-compose.yml`
   ```yaml
   ports:
     - "8080:8000"  # Change 8080 to your preferred port
   ```

2. **Add Environment Variables**: Add to the environment section
   ```yaml
   environment:
     - CUSTOM_VAR=value
   ```

3. **Mount Volumes**: For persistent data (not recommended for this demo)
   ```yaml
   volumes:
     - ./data:/app/data
   ```

## 🐳 Docker Commands

### Basic Commands

```bash
# Build and start containers
docker-compose up --build

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down

# Rebuild containers
docker-compose build --no-cache

# Remove all containers and volumes
docker-compose down -v
```

### Troubleshooting Commands

```bash
# Check container status
docker-compose ps

# Access container shell
docker-compose exec app bash

# View container logs
docker-compose logs app

# Restart specific service
docker-compose restart app
```

## 🔍 Verification

### Check Installation

1. **Docker Status**: Ensure Docker is running
   ```bash
   docker info
   ```

2. **Application Health**: Check if the app is responding
   ```bash
   curl http://localhost:8000
   ```

3. **Container Status**: Verify containers are running
   ```bash
   docker-compose ps
   ```

### Test Functionality

1. **Home Page**: Visit `http://localhost:8000`
2. **Login**: Use demo credentials
   - Email: `user@lilacvault.mail`
   - Password: `password123`
3. **Voting**: Try casting a vote
4. **Results**: Check the results page

## 🚨 Security Considerations

### Important Warnings

- **Educational Purpose Only**: This application contains intentional vulnerabilities
- **Isolated Environment**: Always run in Docker containers
- **No Real Data**: Never use with real voting data
- **Network Isolation**: Don't expose to public internet

### Best Practices

1. **Use Docker**: Always run in containers
2. **Isolated Network**: Use Docker's network isolation
3. **Regular Resets**: Restart containers to reset data
4. **No Production Use**: Never deploy to production

## 🐛 Troubleshooting

### Common Issues

#### Docker Not Running
```bash
# Start Docker Desktop (macOS/Windows)
# Or start Docker service (Linux)
sudo systemctl start docker
```

#### Port Already in Use
```bash
# Check what's using the port
lsof -i :8000

# Change port in docker-compose.yml
ports:
  - "8080:8000"
```

#### Permission Denied
```bash
# Add user to docker group (Linux)
sudo usermod -aG docker $USER
# Log out and back in
```

#### Build Failures
```bash
# Clear Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache
```

### Getting Help

If you encounter issues:

1. **Check Logs**: `docker-compose logs -f`
2. **Verify Prerequisites**: Ensure Docker and Docker Compose are installed
3. **Search Issues**: Check existing GitHub issues
4. **Create Issue**: Report new problems with detailed information

## 📚 Next Steps

After successful installation:

1. **Read the Documentation**: Explore the [docs](docs/) directory
2. **Try the Features**: Test all voting functionality
3. **Learn Security**: Study the intentional vulnerabilities
4. **Contribute**: Consider contributing to the project

## 🔗 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Project README](../README.md)

---

**Need Help?** Create an issue on GitHub or contact akintunero10@gmail.com 
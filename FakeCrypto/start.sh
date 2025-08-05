#!/bin/bash

echo "🚀 Starting FakeCryptoX - Crypto Wallet & Exchange"
echo "=============================================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "🐳 Starting FakeCryptoX with Docker Compose..."

# Start the application
docker-compose up -d

# Wait for application to start
echo "⏳ Waiting for application to start..."
sleep 10

# Check if application is running
if curl -f http://localhost:7004 > /dev/null 2>&1; then
    echo "✅ FakeCryptoX is running at http://localhost:7004"
    echo ""
    echo "🛑 To stop: docker-compose down"
    echo "📊 To view logs: docker-compose logs -f"
    echo ""
    echo "🔗 Access the application: http://localhost:7004"
else
    echo "❌ Application failed to start. Check logs with: docker-compose logs"
    exit 1
fi 
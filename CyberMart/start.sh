#!/bin/bash

echo "🛒 Starting CyberMart - Vulnerable E-commerce Platform"
echo "======================================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "🐳 Starting CyberMart with Docker Compose..."
echo ""

# Start the application
docker-compose up -d

echo ""
echo "⏳ Waiting for application to start..."
sleep 5

# Check if application is running
if curl -s http://localhost:5002 > /dev/null; then
    echo "✅ CyberMart is running at http://localhost:5002"
    echo ""
    echo "🛑 To stop: docker-compose down"
    echo ""
    echo "💡 For advanced management, use: ./run.sh"
else
    echo "❌ Application failed to start. Check logs with: docker-compose logs"
fi 
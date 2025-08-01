#!/bin/bash

echo "☁️ Starting ConfusedCloud - Vulnerable Cloud Management Platform"
echo "================================================================"

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

echo "🐳 Starting ConfusedCloud with Docker Compose..."
echo ""

# Start the application
docker-compose up -d

echo ""
echo "⏳ Waiting for application to start..."
sleep 5

# Check if application is running
if curl -s http://localhost:8001 > /dev/null; then
    echo "✅ ConfusedCloud is running at http://localhost:8001"
    echo ""
    echo "🛑 To stop: docker-compose down"
else
    echo "❌ Application failed to start. Check logs with: docker-compose logs"
fi 
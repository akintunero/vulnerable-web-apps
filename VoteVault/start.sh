#!/bin/bash

echo "🗳️ Starting VoteVault - Vulnerable Digital Voting System"
echo "========================================================"

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

echo "🐳 Starting VoteVault with Docker Compose..."
echo ""

# Start the application
docker-compose up -d

echo ""
echo "⏳ Waiting for application to start..."
sleep 5

# Check if application is running
if curl -s http://localhost:5003 > /dev/null; then
    echo "✅ VoteVault is running at http://localhost:5003"
    echo ""
    echo "🛑 To stop: docker-compose down"
else
    echo "❌ Application failed to start. Check logs with: docker-compose logs"
fi 
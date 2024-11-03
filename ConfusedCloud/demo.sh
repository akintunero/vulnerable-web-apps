#!/bin/bash

echo "🚀 ConfusedCloud - Multi-Tenant SaaS App with Broken Access"
echo "=========================================================="
echo ""

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

echo "🐳 Building and starting ConfusedCloud with Docker Compose..."
echo ""

# Build and start the application
docker-compose up --build -d

echo ""
echo "⏳ Waiting for application to start..."
sleep 10

# Check if application is running
if curl -s http://localhost:8000/login > /dev/null; then
    echo "✅ ConfusedCloud is running at http://localhost:8000"
    echo ""
    echo "🎯 Demo Accounts:"
    echo "   StackWillow Dev:     admin@enterprise.com / tenant1"
    echo "   SilentGrip Net:     user@silentgrip.net / tenant2"
    echo "   LilacVault Co:      manager@enterprise.com / tenant3"
    echo ""
    echo "🔍 Vulnerability Testing:"
    echo "   1. Login with any account"
    echo "   2. Try accessing other tenants by changing URL: /tenant/tenant2/dashboard"
    echo "   3. Check AWS key leak: http://localhost:8000/debug/tenants"
    echo "   4. Test SSRF: Use the proxy tab in the dashboard"
    echo ""
    echo "🧪 Run vulnerability tests: python3 test_vulnerabilities.py"
    echo ""
    echo "🛑 To stop: docker-compose down"
else
    echo "❌ Application failed to start. Check logs with: docker-compose logs"
fi 
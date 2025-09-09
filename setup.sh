#!/bin/bash

# HRMS Setup Script
echo "🚀 HRMS Setup Script"
echo "===================="

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

echo "✅ Docker and Docker Compose are installed"

# Check Docker permissions
if ! docker ps &> /dev/null; then
    echo "⚠️  Docker permission issue detected"
    echo "Please run one of the following commands to fix Docker permissions:"
    echo ""
    echo "Option 1 - Add your user to docker group (recommended):"
    echo "sudo usermod -aG docker $USER"
    echo "newgrp docker"
    echo ""
    echo "Option 2 - Run with sudo:"
    echo "sudo docker-compose up --build"
    echo ""
    echo "After fixing permissions, run this script again."
    exit 1
fi

echo "✅ Docker permissions are configured"

# Clean up any existing containers
echo "🧹 Cleaning up existing containers..."
docker-compose down -v 2>/dev/null || true

# Build and start services
echo "🔨 Building and starting HRMS services..."
docker-compose up --build -d

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 10

# Check service status
echo "📊 Service Status:"
docker-compose ps

echo ""
echo "🎉 HRMS Setup Complete!"
echo "====================="
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:5000"
echo "📚 API Docs: http://localhost:5000/docs"
echo "🗄️  Database: PostgreSQL on localhost:5432"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"
echo ""
echo "Check DEVELOPMENT_GUIDE.md for detailed instructions."

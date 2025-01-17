#!/bin/bash

# ShopCart Docker Management Script

set -e

CONTAINER_NAME="shopcart-app"
IMAGE_NAME="shopcart"
PORT="5001"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}=== ShopCart Docker Manager ===${NC}"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Function to check if port is available
check_port() {
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
        print_warning "Port $PORT is already in use. Please stop the service using that port or use a different port."
        return 1
    fi
    return 0
}

# Function to build the image
build_image() {
    print_status "Building Docker image..."
    docker build -t $IMAGE_NAME .
    print_status "Image built successfully!"
}

# Function to start the container
start_container() {
    if ! check_port; then
        exit 1
    fi
    
    print_status "Starting ShopCart container..."
    docker run -d \
        --name $CONTAINER_NAME \
        -p $PORT:5001 \
        -v "$(pwd)/uploads:/app/uploads" \
        --restart unless-stopped \
        $IMAGE_NAME
    
    print_status "Container started successfully!"
    print_status "Application is available at: http://localhost:$PORT"
    print_status "Default admin credentials: admin / admin123"
}

# Function to stop the container
stop_container() {
    print_status "Stopping ShopCart container..."
    docker stop $CONTAINER_NAME 2>/dev/null || true
    print_status "Container stopped!"
}

# Function to remove the container
remove_container() {
    print_status "Removing ShopCart container..."
    docker rm $CONTAINER_NAME 2>/dev/null || true
    print_status "Container removed!"
}

# Function to restart the container
restart_container() {
    stop_container
    remove_container
    start_container
}

# Function to show logs
show_logs() {
    print_status "Showing container logs..."
    docker logs -f $CONTAINER_NAME
}

# Function to show status
show_status() {
    print_status "Container status:"
    docker ps -a --filter "name=$CONTAINER_NAME" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
}

# Function to show help
show_help() {
    print_header
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  build     Build the Docker image"
    echo "  start     Start the ShopCart container"
    echo "  stop      Stop the ShopCart container"
    echo "  restart   Restart the ShopCart container"
    echo "  remove    Remove the ShopCart container"
    echo "  logs      Show container logs"
    echo "  status    Show container status"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 build"
    echo "  $0 start"
    echo "  $0 restart"
    echo ""
}

# Main script logic
main() {
    check_docker
    
    case "${1:-help}" in
        build)
            build_image
            ;;
        start)
            start_container
            ;;
        stop)
            stop_container
            ;;
        restart)
            restart_container
            ;;
        remove)
            stop_container
            remove_container
            ;;
        logs)
            show_logs
            ;;
        status)
            show_status
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@" 
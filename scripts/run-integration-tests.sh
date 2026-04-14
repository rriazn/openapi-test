#!/bin/bash

# Run the integration tests on a production and a test container

# Usage:
# ./run-integration-tests.sh [OPTIONS]
# Options:
#   --production-image IMAGE    Use specific production image (default: openapi-test:latest-production)
#   --test-image IMAGE          Use specific test runner image (default: openapi-test:latest-integration)
#   --local                     Use local images instead of pulling from registry
#   --debug                     Keep containers running on failure for manual inspection
#   --help                      Show this help message
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_DIR="$SCRIPT_DIR/../compose/integration"
LOCAL=false
DEBUG=false

# Default values
PRODUCTION_IMAGE="openapi-test:latest-production"
TEST_IMAGE="openapi-test:latest-integration"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --production-image)
            PRODUCTION_IMAGE="$2"
            shift 2
            ;;
        --test-image)
            TEST_IMAGE="$2"
            shift 2
            ;;
        --local)
            LOCAL=true
            shift
            ;;
        --debug)
            DEBUG=true
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  --production-image IMAGE   Use specific production image (default: openapi-test:latest-production)"
            echo "  --test-image IMAGE        Use specific test runner image (default: openapi-test:latest-integration)"
            echo "  --local                   Use local images instead of pulling from registry"
            echo "  --debug                   Keep containers running on failure for manual inspection"
            echo "  --help                    Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Pull the images if not using local images
if [ "$LOCAL" = false ]; then
    docker pull "$PRODUCTION_IMAGE"
    docker pull "$TEST_IMAGE"
fi

cd "$COMPOSE_DIR"
export PRODUCTION_IMAGE
export TEST_IMAGE

cleanup() {
    local exit_code=${1:-$?}
    
    # If tests failed and not in debug mode, capture logs for inspection
    if [ "$exit_code" -ne 0 ] && [ "$DEBUG" = false ]; then
        echo ""
        echo "=== Integration test failed (exit code: $exit_code) ==="
        echo "Capturing logs from failed containers..."
        echo ""
        
        echo "--- Backend logs ---"
        docker compose logs backend 2>/dev/null || true
        echo ""
        
        echo "--- Setup-DB logs ---"
        docker compose logs setup-db 2>/dev/null || true
        echo ""
        
        echo "--- Integration tests logs ---"
        docker compose logs integration-tests 2>/dev/null || true
        echo ""
    fi
    
    # Only tear down if not in debug mode
    if [ "$DEBUG" = false ]; then
        docker compose down --remove-orphans || true
    else
        echo "DEBUG mode: Containers left running. Clean up manually with: cd $COMPOSE_DIR && docker compose down --remove-orphans"
    fi
    
    exit "$exit_code"
}


# Always clean up containers (success, failure, or interruption).
trap cleanup EXIT

# Stop any existing containers+
docker compose down -v --remove-orphans 2>/dev/null || true

# Initialize the database
echo "Initializing database..."
docker compose run --rm setup-db

# Start the backend
echo "Starting backend..."
docker compose up -d backend

# Wait for the backend to be healthy
echo "Waiting for backend to be healthy..."
for i in {1..30}; do
    if docker compose exec backend curl -f http://localhost:7000/health >/dev/null 2>&1; then
        echo "Backend is ready!"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "Backend failed to become healthy after 60 seconds. Exiting."
        exit 1
    fi
    sleep 2
done

# Run the integration tests
echo "Running integration tests..."
docker compose run --rm integration-tests
TEST_EXIT_CODE=$?

if [ "$TEST_EXIT_CODE" -ne 0 ]; then
    echo "Integration tests failed with exit code $TEST_EXIT_CODE."
else
    echo "Integration tests passed successfully!"
fi

exit "$TEST_EXIT_CODE"
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
trap 'cleanup $?' EXIT
trap 'cleanup 130' INT TERM

# Start in detached mode so we control when to stop, not Docker Compose.
set +e
docker compose up -d
sleep 2  # Give containers a moment to start

# Get the integration-tests container ID and wait for it to finish
CONTAINER_ID=$(docker compose ps -q integration-tests 2>/dev/null)
if [ -n "$CONTAINER_ID" ]; then
    docker wait "$CONTAINER_ID"
    TEST_EXIT_CODE=$?
else
    TEST_EXIT_CODE=1
fi

echo ""
echo "=== Integration Test Results ==="
docker compose logs integration-tests 2>/dev/null || true
echo ""

# Tear down all containers immediately when tests finish
docker compose down --remove-orphans
set -e

exit "$TEST_EXIT_CODE"
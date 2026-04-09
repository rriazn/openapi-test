#!/bin/bash

# Run the integration tests on a production and a test container

# Usage:
# ./run-integration-tests.sh [OPTIONS]
# Options:
#   --production-image IMAGE    Use specific production image (default: openapi-test:latest-production)
#   --test-image IMAGE          Use specific test runner image (default: openapi-test:latest-integration)
#   --local                     Use local images instead of pulling from registry
#   --help                      Show this help message
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_DIR="$SCRIPT_DIR/../compose/integration"
LOCAL=false

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
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  --production-image IMAGE   Use specific production image (default: openapi-test:latest-production)"
            echo "  --test-image IMAGE        Use specific test runner image (default: openapi-test:latest-integration)"
            echo "  --local                   Use local images instead of pulling from registry"
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
    local exit_code=$?
    docker compose down --remove-orphans || true
    exit "$exit_code"
}

# Always clean up containers (success, failure, or interruption).
trap cleanup EXIT
trap 'exit 130' INT TERM

# Run integration tests and exit with the test container's status code.
set +e
docker compose up --abort-on-container-exit --exit-code-from integration-tests
TEST_EXIT_CODE=$?
set -e

exit "$TEST_EXIT_CODE"
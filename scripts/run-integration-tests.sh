#!/bin/bash

# Run the integration tests on a production and a test container

# Usage
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_DIR="$SCRIPT_DIR/../containers/compose/integration"

# Default values
SKIP_BUILD=false
VM_BROKER_IMAGE="vmbroker:latest"
TEST_IMAGE="vmbroker-test:latest"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-build)
            SKIP_BUILD=true
            shift
            ;;
        --vm-broker-image)
            VM_BROKER_IMAGE="$2"
            shift 2
            ;;
        --test-image)
            TEST_IMAGE="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  --skip-build              Skip Docker image building"
            echo "  --vm-broker-image IMAGE   Use specific VMBroker image (default: vmbroker:latest)"
            echo "  --test-image IMAGE        Use specific test runner image (default: vmbroker-test:latest)"
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
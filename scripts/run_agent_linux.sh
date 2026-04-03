#!/bin/bash

# pqc-watch-local Linux Cloud VM runner script

set -e

# Check for sudo privileges
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run with sudo for traffic analysis." 
   exit 1
fi

# Ensure virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Please run scripts/setup_env.sh first."
    exit 1
fi

# Pre-flight check for tshark/dumpcap permissions
if command -v setcap &> /dev/null; then
    DUMPCAP_PATH=$(which dumpcap)
    if [ ! -z "$DUMPCAP_PATH" ]; then
        echo "Updating dumpcap capabilities..."
        setcap 'CAP_NET_RAW+eip CAP_NET_ADMIN+eip' "$DUMPCAP_PATH"
    fi
fi

# Activate venv and run daemon
echo "Starting PQC Watch Local (Linux)..."
source venv/bin/activate

# Add the src directory to PYTHONPATH for local imports
export PYTHONPATH=$PYTHONPATH:$(pwd)/src

python3 src/main.py

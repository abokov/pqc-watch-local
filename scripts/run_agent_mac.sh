#!/bin/bash

# pqc-watch-local macOS runner script

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

# Activate venv and run daemon
echo "Starting PQC Watch Local (macOS)..."
source venv/bin/activate

# Add the src directory to PYTHONPATH for local imports
export PYTHONPATH=$PYTHONPATH:$(pwd)/src

python3 src/main.py

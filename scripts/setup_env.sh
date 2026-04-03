#!/bin/bash

# pqc-watch-local environment setup script

set -e

echo "Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Checking for system dependencies..."

# Check for tshark (pyshark requirement)
if ! command -v tshark &> /dev/null
then
    echo "Warning: tshark not found. Traffic analysis with pyshark may fail."
    echo "Please install tshark (e.g., 'brew install wireshark' on macOS or 'sudo apt install tshark' on Linux)."
else
    echo "tshark found."
fi

# Check for otool (macOS) or ldd (Linux)
if [[ "$OSTYPE" == "darwin"* ]]; then
    if ! command -v otool &> /dev/null; then
        echo "Warning: otool not found (needed for binary analysis on macOS)."
    else
        echo "otool found."
    fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if ! command -v ldd &> /dev/null; then
        echo "Warning: ldd not found (needed for binary analysis on Linux)."
    else
        echo "ldd found."
    fi
fi

echo "Setup complete! Activate the environment with 'source venv/bin/activate'."

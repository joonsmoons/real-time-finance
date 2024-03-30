#!/bin/bash

# Function to install Python 3 and pip
install_python_and_pip() {
    echo "Installing Python 3 and pip..."
    sudo yum update -y
    sudo yum install python3 -y
    sudo yum install python3-pip -y
}

# Function to install Python dependencies from requirements.txt
install_requirements() {
    echo "Installing Python dependencies from requirements.txt..."
    pip3 install -r requirements.txt
}

# Check if Python 3 and pip are installed
if ! command -v python3 &>/dev/null || ! command -v pip3 &>/dev/null; then
    # Python 3 or pip not found, install them
    install_python_and_pip
fi

# Check if requirements.txt exists
if [ ! -f requirements.txt ]; then
    echo "Error: requirements.txt not found!"
    exit 1
fi

# Install Python dependencies from requirements.txt
install_requirements

# Check if the Python script exists
if [ ! -f indices_stream_polygon.py ]; then
    echo "Error: indices_stream_polygon.py not found!"
    exit 1
fi

# Main loop to run the Python script
while true; do
    python3 indices_stream_polygon.py
    # If Python script exits with a non-zero exit code (indicating an error),
    # wait for 1 minute before restarting
    if [ $? -ne 0 ]; then
        echo "Restarting script in 1 minute..."
        sleep 60 # Wait for 1 minute
    fi
done

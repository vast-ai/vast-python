#!/bin/bash

# Update package list
echo "Updating package list..."
sudo apt update

# Install each required package
echo "Installing required packages..."

# List of packages to install
PACKAGES=(
    "apturl"
    "brltty"               # Provides Brlapi on Ubuntu
    "cups"                 # For cupshelpers-related dependencies
    "iotop"
    "language-selector-common"
    "liblouis-bin"         # Provides 'louis' functionality
    "python3-gi"           # For PyGObject
    "python3-apt"
    "screen-resolution-extra"
    "system-service"
    "ubuntu-advantage-tools"
    "ubuntu-drivers-common"
    "ufw"
    "usb-creator-common"
    "xkit"
)

# Loop through the packages and install each one
for PACKAGE in "${PACKAGES[@]}"; do
    echo "Installing $PACKAGE..."
    sudo apt install -y "$PACKAGE"
done

echo "All specified packages have been installed."

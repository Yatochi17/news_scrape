#!/bin/bash
# Install Chrome
apt update && apt install -y wget unzip
wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install -y ./google-chrome-stable_current_amd64.deb
# Run the app
gunicorn app:app
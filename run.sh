#!/bin/bash
# MAXEL-OS Startup Script
echo "Initializing MAXEL-OS Core..."
# Check for dependencies quietly
pip install arabic-reshaper python-bidi --quiet
python3 main.py

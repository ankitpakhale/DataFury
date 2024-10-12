#!/bin/bash
# Navigate to the src directory
cd src || { echo "src directory not found!"; exit 1; }
# Execute the controller.py file
python3 controller.py

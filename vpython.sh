#!/bin/bash

# Check for Windows virtual environment (Git Bash style)
if [ -f "./venv/Scripts/python.exe" ]; then
    "./venv/Scripts/python.exe" "$@"
# Check for Unix virtual environment
elif [ -f "./venv/bin/python" ]; then
    "./venv/bin/python" "$@"
else
    echo "Virtual environment not found. Please create it first."
    exit 1
fi

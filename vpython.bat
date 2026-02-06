@echo off
if not exist "venv\Scripts\python.exe" (
    echo Virtual environment not found. Please create it first.
    exit /b 1
)
"venv\Scripts\python.exe" %*

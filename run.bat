@echo off
echo Starting Ragume Backend and Frontend...

:: Start Backend in a new window
start "Ragume Backend" cmd /k "venv\Scripts\activate && uvicorn app.main:app --reload --port 8001"

:: Wait for a few seconds to let the backend initialize
timeout /t 5 /nobreak >nul

:: Start Frontend in a new window
start "Ragume Frontend" cmd /k "venv\Scripts\activate && streamlit run ui.py"

echo.
echo Application started!
echo Backend: http://localhost:8001
echo Frontend: http://localhost:8501

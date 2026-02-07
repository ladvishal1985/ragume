@echo off
REM Activate virtual environment (only if running locally)
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM Set environment variables from .env file (only if running locally)
if exist .env (
    for /f "tokens=*" %%a in ('type .env ^| findstr /v "^#"') do set %%a
)

REM Check if running in production (Render) or local
if "%PORT%"=="" (
    echo Running in LOCAL mode...
    REM Local development - use reload
    python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
) else (
    echo Running in PRODUCTION mode on port %PORT%...
    REM Production - no reload, optimized for deployment
    python -m uvicorn app.main:app --host 0.0.0.0 --port %PORT%
)

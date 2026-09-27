@echo off
setlocal enabledelayedexpansion
title LegalEase - Launcher

echo ==========================================================
echo      LegalEase: AI Legal Document Generator Launcher      
echo ==========================================================

REM 1. Identify valid Python executable or activate venv
set PYTHON_EXE=

if exist "%~dp0venv\Scripts\python.exe" (
    set PYTHON_EXE="%~dp0venv\Scripts\python.exe"
    echo [+] Using Virtual Environment Python: !PYTHON_EXE!
) else if exist "C:\Users\sivat\AppData\Local\Programs\Orange\python.exe" (
    set PYTHON_EXE="C:\Users\sivat\AppData\Local\Programs\Orange\python.exe"
    echo [+] Using Orange Python: !PYTHON_EXE!
) else (
    where python >nul 2>nul
    if !ERRORLEVEL! equ 0 (
        set PYTHON_EXE=python
        echo [+] Using System PATH Python
    ) else (
        echo [-] Error: No working Python installation found!
        echo Please ensure Python is installed.
        pause
        exit /b 1
    )
)

REM 2. Generate brand logos if missing
echo [*] Checking Brand Assets...
!PYTHON_EXE! "%~dp0setup_assets.py"

REM 3. Launch FastAPI Backend in a separate window
echo [*] Launching LegalEase FastAPI Backend on port 8000...
start "LegalEase Backend API (Port 8000)" cmd /k "cd /d "%~dp0" && !PYTHON_EXE! -m uvicorn legalEaseAPI.main:app --host 127.0.0.1 --port 8000 --reload"

REM 4. Launch Streamlit Frontend in current window
echo [*] Launching LegalEase Streamlit UI on port 8501...
timeout /t 2 >nul
!PYTHON_EXE! -m streamlit run "%~dp0frontend\app.py" --server.port 8501

pause

@echo off
setlocal enabledelayedexpansion
title LegalEase - Streamlit UI

if exist "%~dp0venv\Scripts\python.exe" (
    set PYTHON_EXE="%~dp0venv\Scripts\python.exe"
) else if exist "C:\Users\sivat\AppData\Local\Programs\Orange\python.exe" (
    set PYTHON_EXE="C:\Users\sivat\AppData\Local\Programs\Orange\python.exe"
) else (
    set PYTHON_EXE=python
)

echo [*] Starting LegalEase Streamlit Frontend on http://127.0.0.1:8501 ...
cd /d "%~dp0"
!PYTHON_EXE! -m streamlit run "%~dp0frontend\app.py" --server.port 8501
pause

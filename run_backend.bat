@echo off
setlocal enabledelayedexpansion
title LegalEase - FastAPI Backend

if exist "%~dp0venv\Scripts\python.exe" (
    set PYTHON_EXE="%~dp0venv\Scripts\python.exe"
) else if exist "C:\Users\sivat\AppData\Local\Programs\Orange\python.exe" (
    set PYTHON_EXE="C:\Users\sivat\AppData\Local\Programs\Orange\python.exe"
) else (
    set PYTHON_EXE=python
)

echo [*] Starting LegalEase FastAPI on http://127.0.0.1:8000 ...
cd /d "%~dp0"
!PYTHON_EXE! -m uvicorn legalEaseAPI.main:app --host 127.0.0.1 --port 8000 --reload
pause

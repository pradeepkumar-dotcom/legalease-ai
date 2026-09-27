#!/usr/bin/env bash
# LegalEase Service Runner Script

echo "=========================================================="
echo "    ⚖️  LegalEase: AI Legal Document Generator  ⚖️       "
echo "=========================================================="

# Check if Python is installed
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo "[-] Python is not found on PATH. Please install Python 3.10+."
    exit 1
fi

echo "[+] Using Python binary: $($PYTHON_CMD --version)"

# 1. Generate fallback assets if missing
echo "[*] Checking brand assets..."
$PYTHON_CMD setup_assets.py

# 2. Start FastAPI server in background
echo "[*] Launching LegalEase FastAPI Backend on port 8000..."
$PYTHON_CMD -m uvicorn legalEaseAPI.main:app --host 127.0.0.1 --port 8000 --reload &
API_PID=$!

# 3. Start Streamlit web UI
echo "[*] Launching LegalEase Streamlit Frontend on port 8501..."
$PYTHON_CMD -m streamlit run frontend/app.py --server.port 8501 --server.headless false

# Cleanup on exit
trap "kill $API_PID" EXIT

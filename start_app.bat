@echo off
title VERDURE - Precision Leaf Doctor Real-Time Engine
color 0A
echo ==============================================================================
echo VERDURE: Precision Leaf Doctor Real-Time In-Situ Engine
echo NexAI Hackathon 2026 - Challenge 2.2 (Domain: Agriculture)
echo ==============================================================================
echo.
echo [*] Checking local Python environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    pause
    exit /b
)

echo [*] Starting Uvicorn Real-Time Server on http://127.0.0.1:8080 ...
start "" http://127.0.0.1:8080/
python -m uvicorn server:app --host 127.0.0.1 --port 8080
pause

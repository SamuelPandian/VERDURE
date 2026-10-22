# VERDURE: Precision Leaf Doctor Launcher
Write-Host "==============================================================================" -ForegroundColor Green
Write-Host "VERDURE: Precision Leaf Doctor Real-Time In-Situ Engine" -ForegroundColor Green
Write-Host "NexAI Hackathon 2026 - Challenge 2.2 (Domain: Agriculture)" -ForegroundColor Green
Write-Host "==============================================================================" -ForegroundColor Green
Write-Host ""

$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Error "Python is not found in PATH. Please install Python 3.10+."
    exit 1
}

Write-Host "[*] Launching VERDURE FastAPI Engine at http://127.0.0.1:8080 ..." -ForegroundColor Cyan
Start-Process "http://127.0.0.1:8080/"
python -m uvicorn server:app --host 127.0.0.1 --port 8080

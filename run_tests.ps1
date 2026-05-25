# E2E Test Suite Runner Script
# Usage: .\run_tests.ps1

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   Starting Automated Test Framework Setup" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Verify Python Installation
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python is not installed or not in PATH. Please install Python to run tests."
    exit 1
}

# 2. Virtual Environment Setup
$VenvDir = ".venv"
if (!(Test-Path $VenvDir)) {
    Write-Host "Creating Python Virtual Environment in $VenvDir..." -ForegroundColor Yellow
    python -m venv $VenvDir
} else {
    Write-Host "Python Virtual Environment already exists." -ForegroundColor Green
}

# 3. Activate Virtual Environment
Write-Host "Activating Virtual Environment..." -ForegroundColor Yellow
.venv\Scripts\Activate.ps1

# 4. Install Dependencies
Write-Host "Upgrading pip and installing requirements..." -ForegroundColor Yellow
python -m pip install --upgrade pip
pip install -r requirements.txt

# 5. Playwright Browser Provisioning
Write-Host "Installing Playwright browser binaries..." -ForegroundColor Yellow
playwright install chromium

# 6. Execute Tests
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   Running Pytest Automation Suites" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Run tests using pytest
pytest

# 7. Post-Run Summary
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   Execution Completed Successfully!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Logs Location:    logs/framework.log" -ForegroundColor Gray
Write-Host "Reports Location: reports/report.html" -ForegroundColor Gray
Write-Host "==========================================" -ForegroundColor Cyan

@echo off
echo ============================================================
echo           AUTO-LOGIN API SERVER STARTER
echo ============================================================
echo.

echo [1/4] Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and add to PATH
    pause
    exit /b 1
)

echo [2/4] Installing required packages...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install requirements
    pause
    exit /b 1
)

echo [3/4] Checking OctoBrowser status...
echo NOTE: Make sure OctoBrowser is running on localhost:58888
echo If not, please start OctoBrowser first!
echo.

echo [4/4] Starting Auto-Login API Server...
echo Server will run on: http://localhost:5000
echo Supabase will call this API for auto approve/deny
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

python auto_login_api.py

pause 
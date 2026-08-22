@echo off
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    set "PYTHON=.venv\Scripts\python.exe"
) else (
    set "PYTHON=python"
)

echo Installing required packages...
%PYTHON% -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo Could not install the required packages.
    pause
    exit /b 1
)

echo.
echo Starting North ^& Alder at http://127.0.0.1:5000
start "North ^& Alder" http://127.0.0.1:5000
%PYTHON% app.py
pause

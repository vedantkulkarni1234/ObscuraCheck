@echo off
REM Prompt Manager - Quick Start Script for Windows
REM This script automates the setup and launch process

setlocal enabledelayedexpansion

echo.
echo ============================================================
echo          Prompt Manager - Quick Start
echo ============================================================
echo.

REM Check Python version
echo Checking Python version...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed. Please install Python 3.10+
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% found
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1
echo [OK] Pip upgraded
echo.

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt >nul 2>&1
echo [OK] Dependencies installed
echo.

REM Create data directory
if not exist "data" mkdir data
echo [OK] Data directory ready
echo.

REM Launch the app
echo ============================================================
echo [LAUNCHING] Prompt Manager...
echo ============================================================
echo.
echo The app will open in your browser at: http://localhost:8501
echo.
echo Quick Tips:
echo   - First time? Click "Create" to add a prompt
echo   - Want examples? Go to Settings and import SAMPLE_DATA.json
echo   - Use {{variable}} syntax in your prompts for dynamic content
echo.
echo Press Ctrl+C to stop the app
echo.

REM Run streamlit
streamlit run main.py

pause

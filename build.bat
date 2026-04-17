@echo off
setlocal enabledelayedexpansion
title Tasmota Backup Tool - Professional Compiler

:: --- CONFIGURATION ---
set SCRIPT_NAME=main.py
set ICON_NAME=icon.ico
set EXE_NAME=TasmotaBackupTool

echo ======================================================
echo   TASMOTA BACKUP TOOL - BUILD SYSTEM
echo ======================================================

:: 1. CHECK FOR PYTHON
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python from https://www.python.org/
    pause
    exit /b
)
echo [OK] Python detected.

:: 2. CHECK FOR PIP
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] PIP is not installed. 
    echo Please ensure PIP is included in your Python installation.
    pause
    exit /b
)
echo [OK] PIP detected.

:: 3. INSTALL DEPENDENCIES
echo [*] Checking and installing dependencies...
python -m pip install --upgrade pip >nul
pip install customtkinter requests pyinstaller >nul
echo [OK] Dependencies ready.

:: 4. CHECK IF MAIN.PY EXISTS
if not exist %SCRIPT_NAME% (
    echo [ERROR] %SCRIPT_NAME% not found in this folder!
    echo Please rename your script to %SCRIPT_NAME% or edit this BAT.
    pause
    exit /b
)

:: 5. START COMPILATION WITH "LOADING BAR"
echo.
echo [*] Starting compilation... This may take 1-3 minutes.
echo [ PROGRESS: ##########                          ] (Impacting files...)

:: Running PyInstaller
:: --noconsole: Hide CMD on launch
:: --onefile: Single EXE output
:: --collect-all: Ensures CustomTkinter themes are included
:: --clean: Removes temporary cache before building
pyinstaller --noconsole --onefile --clean ^
    --collect-all customtkinter ^
    --icon=%ICON_NAME% ^
    --name %EXE_NAME% ^
    %SCRIPT_NAME%

if %errorlevel% equ 0 (
    echo.
    echo [ PROGRESS: ######################################## ] 100%%
    echo.
    echo ======================================================
    echo   SUCCESS! 
    echo   Your app is ready in the 'dist' folder.
    echo ======================================================
) else (
    echo.
    echo [ERROR] Compilation failed. Check the logs above for details.
)

pause
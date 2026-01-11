@echo off
chcp 936 >nul
cd /d "%~dp0"
if exist "main.py" (
    pythonw.exe main.py
    if errorlevel 1 (
        echo [ERROR] Failed to launch application
        pause
    )
) else (
    echo [ERROR] main.py not found
    pause
)

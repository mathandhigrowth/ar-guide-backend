@echo off
cd /d %~dp0
echo ============================================================
echo Starting YOLOv11x Server
echo ============================================================
echo.
echo Checking for existing server on port 3000...
netstat -ano | findstr :3000 >nul
if %errorlevel% equ 0 (
    echo Port 3000 is in use. Stopping existing process...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3000') do taskkill /F /PID %%a 2>nul
    timeout /t 2 >nul
)
echo Starting server...
echo.
python server.py
pause


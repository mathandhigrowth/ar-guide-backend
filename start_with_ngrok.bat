@echo off
echo ============================================================
echo YOLOv11x Server with ngrok
echo ============================================================
echo.

REM Check if ngrok is installed
where ngrok >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: ngrok is not installed or not in PATH
    echo.
    echo Please install ngrok:
    echo   1. Download from: https://ngrok.com/download
    echo   2. Extract and add to PATH
    echo   3. Sign up and get auth token: https://dashboard.ngrok.com/get-started/your-authtoken
    echo   4. Run: ngrok authtoken YOUR_TOKEN
    echo.
    pause
    exit /b 1
)

echo [1/2] Starting YOLOv11x server in new window...
start "YOLOv11x Server" cmd /k "cd /d %~dp0 && python server.py"
timeout /t 5 >nul

echo [2/2] Starting ngrok tunnel in new window...
start "ngrok Tunnel" cmd /k "ngrok http 3000"
timeout /t 3 >nul

echo.
echo ============================================================
echo Server is starting!
echo ============================================================
echo.
echo Check the ngrok window for your public URL!
echo It will look like: https://xxxx-xxx-xxx-xxx.ngrok-free.app
echo.
echo Web Interface: http://localhost:4040
echo   ^(View requests and get public URL^)
echo.
echo Press any key to continue...
pause >nul


@echo off
cd /d %~dp0
echo ============================================================
echo Starting YOLOv11x Webcam Test
echo ============================================================
echo.
echo Make sure the server is running in another window!
echo Press any key to continue...
pause >nul
echo.
python test_client.py
pause


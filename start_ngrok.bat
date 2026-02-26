@echo off
echo ========================================
echo   Starting ngrok tunnel...
echo ========================================
cd /d "%~dp0"
ngrok-v3-stable-windows-amd64\ngrok.exe http 8000

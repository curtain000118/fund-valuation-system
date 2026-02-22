@echo off
chcp 65001 >nul
title 基金实时估值系统

cd /d "%~dp0"

echo ============================================================
echo 基金实时估值系统
echo ============================================================

netstat -ano | findstr ":5000" >nul
if %errorlevel% equ 0 (
    echo 检测到服务已在运行，正在打开浏览器...
    start "" http://localhost:5000
    exit /b
)

call venv\Scripts\activate.bat

echo 服务启动中，浏览器将自动打开...
echo.

start "" http://localhost:5000

python run.py

pause

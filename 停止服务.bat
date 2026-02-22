@echo off
chcp 65001 >nul
title 停止基金估值系统

echo ============================================================
echo 停止基金实时估值系统
echo ============================================================

for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5000" ^| findstr "LISTENING"') do (
    echo 正在停止服务 (PID: %%a)...
    taskkill /PID %%a /F >nul 2>&1
)

echo 服务已停止
pause

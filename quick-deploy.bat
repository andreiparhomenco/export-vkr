@echo off
echo ========================================
echo   VKR Export System - Quick Deploy
echo ========================================
echo.

echo 1. Building and pushing changes...
call push-changes.bat

echo.
echo 2. Checking deployment status...
echo.
echo Frontend (Netlify): https://regal-raindrop-fa2af2.netlify.app
echo Backend (Railway): Check Railway dashboard
echo GitHub: https://github.com/andreiparhomenco/export-vkr.git
echo.

echo 3. Deployment will be automatic:
echo    - Netlify will rebuild frontend automatically
echo    - Railway will redeploy backend automatically
echo.

echo ========================================
echo   Deployment initiated!
echo ========================================
echo.
pause

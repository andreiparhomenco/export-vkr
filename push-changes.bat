@echo off
echo ========================================
echo   VKR Export System - Push Changes
echo ========================================
echo.

echo Checking git status...
git status

echo.
echo Adding all changes...
git add .

echo.
echo Committing changes...
set /p commit_msg="Enter commit message (or press Enter for auto-message): "
if "%commit_msg%"=="" (
    set commit_msg=Update VKR Export System - %date% %time%
)

git commit -m "%commit_msg%"

echo.
echo Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo   Changes pushed successfully!
echo ========================================
echo.
echo Repository: https://github.com/andreiparhomenco/export-vkr.git
echo.
pause



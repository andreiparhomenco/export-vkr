@echo off
echo 🚀 Начинаем полное развертывание VKR Export System...

REM Проверяем Git
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git не установлен
    pause
    exit /b 1
)

REM Проверяем, что мы в правильной директории
if not exist "backend\requirements.txt" (
    echo ❌ Не в корневой директории проекта
    pause
    exit /b 1
)

echo ✅ Git доступен
echo ✅ Проект найден

REM Коммитим все изменения
echo 📝 Коммитим изменения...
git add .
git commit -m "Configure for automatic deployment with Railway backend URL" 2>nul || echo Нет изменений для коммита

REM Отправляем на GitHub
echo 📤 Отправляем на GitHub...
git push

echo.
echo 🎉 Проект готов к развертыванию!
echo.
echo 📋 Следующие шаги:
echo 1. Frontend (Netlify):
echo    - Перейдите на netlify.com
echo    - Подключите GitHub репозиторий
echo    - Настройки уже готовы в netlify.toml
echo.
echo 2. Backend (Railway):
echo    - Перейдите на railway.app
echo    - Подключите GitHub репозиторий
echo    - Root Directory: оставьте пустым
echo.
echo 3. Проверьте работу:
echo    - Frontend: ваш Netlify URL
echo    - Backend: https://export-vkr-production.up.railway.app/health
echo.
echo 🔗 Ссылки:
echo    - GitHub: https://github.com/andreiparhomenco/export-vkr
echo    - Railway: https://railway.app
echo    - Netlify: https://netlify.com
echo.
echo Нажмите любую клавишу для выхода...
pause >nul





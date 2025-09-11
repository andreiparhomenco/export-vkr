@echo off
echo 🚀 Начинаем развертывание VKR Export System...

REM Проверяем наличие Docker
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker не установлен. Пожалуйста, установите Docker Desktop для Windows.
    echo Скачать можно с: https://www.docker.com/products/docker-desktop/
    pause
    exit /b 1
)

REM Проверяем наличие Docker Compose
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose не установлен. Пожалуйста, установите Docker Desktop для Windows.
    pause
    exit /b 1
)

REM Останавливаем существующие контейнеры
echo 🛑 Останавливаем существующие контейнеры...
docker-compose down

REM Собираем и запускаем новые контейнеры
echo 🔨 Собираем и запускаем контейнеры...
docker-compose up -d --build

REM Проверяем статус
echo 📊 Проверяем статус сервисов...
docker-compose ps

echo ✅ Развертывание завершено!
echo 🌐 Frontend: http://localhost:5173
echo 🔧 Backend API: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo Нажмите любую клавишу для выхода...
pause >nul


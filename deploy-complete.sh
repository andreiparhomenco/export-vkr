#!/bin/bash

# Полное развертывание VKR Export System
echo "🚀 Начинаем полное развертывание VKR Export System..."

# Проверяем Git
if ! command -v git &> /dev/null; then
    echo "❌ Git не установлен"
    exit 1
fi

# Проверяем, что мы в правильной директории
if [ ! -f "package.json" ] && [ ! -f "backend/requirements.txt" ]; then
    echo "❌ Не в корневой директории проекта"
    exit 1
fi

echo "✅ Git доступен"
echo "✅ Проект найден"

# Коммитим все изменения
echo "📝 Коммитим изменения..."
git add .
git commit -m "Configure for automatic deployment with Railway backend URL" || echo "Нет изменений для коммита"

# Отправляем на GitHub
echo "📤 Отправляем на GitHub..."
git push

echo ""
echo "🎉 Проект готов к развертыванию!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Frontend (Netlify):"
echo "   - Перейдите на netlify.com"
echo "   - Подключите GitHub репозиторий"
echo "   - Настройки уже готовы в netlify.toml"
echo ""
echo "2. Backend (Railway):"
echo "   - Перейдите на railway.app"
echo "   - Подключите GitHub репозиторий"
echo "   - Root Directory: оставьте пустым"
echo ""
echo "3. Проверьте работу:"
echo "   - Frontend: ваш Netlify URL"
echo "   - Backend: https://export-vkr-production.up.railway.app/health"
echo ""
echo "🔗 Ссылки:"
echo "   - GitHub: https://github.com/andreiparhomenco/export-vkr"
echo "   - Railway: https://railway.app"
echo "   - Netlify: https://netlify.com"

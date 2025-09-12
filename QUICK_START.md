# VKR Export System - Quick Start Guide

## 🚀 Быстрый старт для разработчиков

### Текущий статус развертывания
- ✅ **Frontend**: https://regal-raindrop-fa2af2.netlify.app (Netlify)
- ✅ **Backend**: Railway (автоматическое развертывание)
- ✅ **GitHub**: https://github.com/andreiparhomenco/export-vkr.git
- ✅ **Автоматическое развертывание**: Настроено

## 📋 Быстрые команды

### Локальная разработка
```bash
# Запуск полного стека
docker-compose up --build

# Только backend
docker-compose up backend

# Только frontend  
docker-compose up frontend
```

### Развертывание изменений
```bash
# Windows - быстрый пуш и развертывание
push-changes.bat

# Linux/macOS - быстрый пуш и развертывание
./push-changes.sh

# Автоматическое развертывание
quick-deploy.bat  # Windows
./quick-deploy.sh # Linux/macOS
```

## 🔧 Настройка для легкого пуша

### 1. Клонирование репозитория
```bash
git clone https://github.com/andreiparhomenco/export-vkr.git
cd export-vkr
```

### 2. Настройка удаленного репозитория
```bash
git remote add origin https://github.com/andreiparhomenco/export-vkr.git
```

### 3. Проверка статуса
```bash
git status
git remote -v
```

## 📝 Рабочий процесс

### 1. Внесение изменений
- Редактируйте код локально
- Тестируйте с `docker-compose up --build`

### 2. Пуш изменений
```bash
# Автоматический пуш с сообщением
push-changes.bat

# Или ручной пуш
git add .
git commit -m "Описание изменений"
git push origin main
```

### 3. Автоматическое развертывание
- **Netlify**: Автоматически пересобирает frontend
- **Railway**: Автоматически переразвертывает backend
- **Время развертывания**: 2-5 минут

## 🛠️ Структура проекта

```
export-vkr/
├── backend/                 # Python FastAPI
├── frontend/               # React + Vite
├── memory-bank/           # Документация проекта
├── push-changes.bat       # Скрипт для Windows
├── push-changes.sh        # Скрипт для Linux/macOS
├── quick-deploy.bat       # Быстрое развертывание
├── docker-compose.yml     # Локальная разработка
└── README.md              # Основная документация
```

## 🔍 Мониторинг

### Проверка статуса
- **Frontend**: https://regal-raindrop-fa2af2.netlify.app
- **Backend Health**: `curl https://your-railway-url/health`
- **GitHub**: https://github.com/andreiparhomenco/export-vkr.git

### Логи
```bash
# Локальные логи
docker-compose logs -f

# Railway логи - через Railway dashboard
# Netlify логи - через Netlify dashboard
```

## 🚨 Устранение неполадок

### Проблемы с Git
```bash
# Сброс удаленного репозитория
git remote remove origin
git remote add origin https://github.com/andreiparhomenco/export-vkr.git

# Принудительный пуш (осторожно!)
git push -f origin main
```

### Проблемы с развертыванием
1. Проверьте логи в Netlify/Railway dashboard
2. Убедитесь, что все файлы закоммичены
3. Проверьте переменные окружения

### Проблемы с локальной разработкой
```bash
# Очистка Docker
docker-compose down
docker system prune -f
docker-compose up --build
```

## 📚 Дополнительная документация

- **README.md**: Полная документация проекта
- **memory-bank/**: Детальная техническая документация
- **DEPLOYMENT.md**: Инструкции по развертыванию
- **GITHUB_SETUP.md**: Настройка GitHub репозитория

## ✅ Готово к использованию!

Проект настроен для легкого развертывания и обновления. Используйте скрипты `push-changes.bat/sh` для быстрого пуша изменений, и автоматическое развертывание сделает остальное!

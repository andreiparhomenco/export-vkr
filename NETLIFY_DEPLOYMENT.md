# 🚀 Развертывание на Netlify

## Быстрый старт

### 1. Подключение к GitHub

1. **Перейдите на [netlify.com](https://netlify.com)**
2. **Войдите в аккаунт** (или создайте новый)
3. **Нажмите "New site from Git"**
4. **Выберите "GitHub"**
5. **Найдите репозиторий** `andreiparhomenco/export-vkr`
6. **Нажмите "Deploy site"**

### 2. Настройка сборки

В настройках сайта установите:

- **Base directory**: `frontend`
- **Build command**: `npm run build`
- **Publish directory**: `dist`

### 3. Переменные окружения

В разделе **Site settings > Environment variables** добавьте:

```
VITE_API_URL = https://your-backend-url.herokuapp.com
```

## 🔧 Настройка Backend

Поскольку Netlify предназначен для статических сайтов, вам нужно развернуть backend отдельно:

### Варианты для Backend:

#### 1. Heroku (Рекомендуется)
```bash
# Установите Heroku CLI
# Создайте приложение
heroku create your-backend-name
heroku git:remote -a your-backend-name

# Настройте переменные окружения
heroku config:set PYTHONUNBUFFERED=1

# Разверните
git subtree push --prefix backend heroku main
```

#### 2. Railway
1. Подключите GitHub репозиторий
2. Выберите папку `backend`
3. Railway автоматически определит Python и развернет

#### 3. Render
1. Создайте новый Web Service
2. Подключите GitHub репозиторий
3. Укажите папку `backend`
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## 🔄 Автоматическое развертывание

После настройки:
- **Frontend** будет автоматически развертываться при каждом push в GitHub
- **Backend** нужно настроить отдельно на выбранной платформе

## 📝 Обновление переменных окружения

После развертывания backend:
1. Скопируйте URL backend (например: `https://your-app.herokuapp.com`)
2. В Netlify перейдите в **Site settings > Environment variables**
3. Обновите `VITE_API_URL` на URL вашего backend
4. Нажмите **Trigger deploy** для пересборки

## 🎯 Итоговая архитектура

```
GitHub Repository
├── Frontend (Netlify) → https://your-site.netlify.app
└── Backend (Heroku/Railway/Render) → https://your-backend.herokuapp.com
```

## 🔍 Проверка развертывания

1. **Frontend**: Откройте URL Netlify
2. **Backend**: Проверьте `https://your-backend-url.herokuapp.com/health`
3. **API Docs**: `https://your-backend-url.herokuapp.com/docs`

## 🆘 Устранение неполадок

### Ошибки сборки
- Проверьте, что все зависимости указаны в `package.json`
- Убедитесь, что Node.js версии 18+ используется

### CORS ошибки
- Убедитесь, что `VITE_API_URL` правильно настроен
- Проверьте, что backend разрешает запросы с вашего домена Netlify

### Проблемы с API
- Проверьте, что backend развернут и доступен
- Убедитесь, что все переменные окружения настроены

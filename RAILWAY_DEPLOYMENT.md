# 🚀 Развертывание на Railway

## Быстрое развертывание Backend

### Шаг 1: Создание проекта на Railway

1. **Перейдите на [railway.app](https://railway.app)**
2. **Войдите через GitHub** (нажмите "Login with GitHub")
3. **Нажмите "New Project"**
4. **Выберите "Deploy from GitHub repo"**
5. **Найдите и выберите** `andreiparhomenco/export-vkr`

### Шаг 2: Настройка проекта

1. **После подключения репозитория Railway покажет настройки**
2. **ВАЖНО! Установите Root Directory:**
   - **Root Directory**: `backend` (это критически важно!)
   - **Build Command**: Оставьте пустым (Railway определит автоматически)
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### ⚠️ КРИТИЧЕСКИ ВАЖНО:
**Обязательно установите Root Directory в `backend`!** Без этого Railway не найдет Python файлы и не сможет определить тип проекта.

### Шаг 3: Переменные окружения

В настройках проекта добавьте переменные окружения:
```
PYTHONUNBUFFERED=1
PORT=8000
```

### Шаг 4: Дождитесь развертывания

- Railway автоматически соберет и развернет проект
- Процесс займет 2-3 минуты
- Следите за логами в реальном времени

### Шаг 5: Получите URL

После успешного развертывания:
1. **Скопируйте URL** (например: `https://your-app.railway.app`)
2. **Проверьте health endpoint**: `https://your-app.railway.app/health`
3. **Проверьте API docs**: `https://your-app.railway.app/docs`

## Настройка Frontend в Netlify

### Шаг 1: Обновите переменные окружения

1. **В Netlify** перейдите в **Site settings** → **Environment variables**
2. **Добавьте или обновите:**
   ```
   VITE_API_URL = https://your-app.railway.app
   ```
3. **Нажмите "Trigger deploy"** для пересборки

### Шаг 2: Проверьте работу

1. **Откройте ваш Netlify URL**
2. **Попробуйте загрузить файлы**
3. **Проверьте консоль браузера** на ошибки

## Устранение неполадок

### Проблема: "Failed to fetch"
**Решение:**
1. Проверьте, что backend развернут и доступен
2. Убедитесь, что `VITE_API_URL` правильно настроен в Netlify
3. Проверьте CORS настройки в backend

### Проблема: "CORS error"
**Решение:**
1. Backend уже настроен для работы с Netlify
2. Если используете другой домен, добавьте его в CORS настройки

### Проблема: "Build failed"
**Решение:**
1. Проверьте логи в Railway
2. Убедитесь, что все зависимости указаны в `requirements.txt`
3. Проверьте, что Root Directory установлен в `backend`

### Проблема: "Port binding error"
**Решение:**
1. Railway автоматически устанавливает переменную `$PORT`
2. Убедитесь, что в start command используется `$PORT`

## Проверка развертывания

### Backend endpoints:
- **Health check**: `https://your-app.railway.app/health`
- **API docs**: `https://your-app.railway.app/docs`
- **Root**: `https://your-app.railway.app/`

### Frontend:
- **Ваш Netlify URL**: `https://regal-raindrop-fa2af2.netlify.app`

## Автоматическое развертывание

После настройки:
- **Backend** будет автоматически пересобираться при каждом push в GitHub
- **Frontend** будет автоматически пересобираться при изменении переменных окружения

## Мониторинг

### Railway Dashboard:
- **Logs**: Просмотр логов в реальном времени
- **Metrics**: Мониторинг производительности
- **Deployments**: История развертываний

### Netlify Dashboard:
- **Deploys**: История развертываний frontend
- **Functions**: Если используете serverless функции
- **Analytics**: Статистика посещений

## Стоимость

- **Railway**: Бесплатный план включает 500 часов в месяц
- **Netlify**: Бесплатный план включает 100GB трафика в месяц

Для большинства проектов бесплатных планов достаточно!

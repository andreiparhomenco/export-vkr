# 🚀 Быстрое развертывание Backend

## Вариант 1: Railway (Самый простой)

1. **Перейдите на [railway.app](https://railway.app)**
2. **Войдите через GitHub**
3. **Нажмите "New Project" → "Deploy from GitHub repo"**
4. **Выберите репозиторий** `andreiparhomenco/export-vkr`
5. **Настройте проект:**
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. **Дождитесь развертывания** (2-3 минуты)
7. **Скопируйте URL** (например: `https://your-app.railway.app`)

## Вариант 2: Render

1. **Перейдите на [render.com](https://render.com)**
2. **Войдите через GitHub**
3. **Нажмите "New" → "Web Service"**
4. **Подключите репозиторий** `andreiparhomenco/export-vkr`
5. **Настройки:**
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. **Нажмите "Create Web Service"**

## Вариант 3: Heroku

1. **Установите [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)**
2. **Выполните команды:**
```bash
heroku login
heroku create your-backend-name
heroku git:remote -a your-backend-name
git subtree push --prefix backend heroku main
```

## После развертывания Backend:

1. **Скопируйте URL backend** (например: `https://your-app.railway.app`)
2. **В Netlify:**
   - Перейдите в **Site settings** → **Environment variables**
   - Добавьте: `VITE_API_URL = https://your-backend-url.railway.app`
   - Нажмите **"Trigger deploy"**

## Проверка:

- **Backend**: `https://your-backend-url.railway.app/health`
- **API Docs**: `https://your-backend-url.railway.app/docs`
- **Frontend**: Ваш Netlify URL

## Если не работает:

1. **Проверьте CORS** в backend (должен разрешать запросы с Netlify)
2. **Проверьте переменные окружения** в Netlify
3. **Проверьте логи** в Railway/Render/Heroku





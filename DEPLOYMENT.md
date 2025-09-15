# 🚀 Руководство по развертыванию VKR Export System

## Быстрый старт

### Windows
```cmd
deploy.bat
```

### Linux/macOS
```bash
chmod +x deploy.sh
./deploy.sh
```

## Варианты развертывания

### 1. 🐳 Docker (Рекомендуется)

#### Локальное развертывание
```bash
# Клонируйте репозиторий
git clone <ваш-репозиторий>
cd quick-export-vkr

# Запустите проект
docker-compose up -d --build

# Проверьте статус
docker-compose ps
```

#### Продакшен развертывание
```bash
# Используйте продакшен конфигурацию
docker-compose -f docker-compose.prod.yml up -d --build
```

### 2. ☁️ Облачные платформы

#### Heroku
1. Создайте аккаунт на [Heroku](https://heroku.com)
2. Установите [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
3. Создайте приложение:
```bash
heroku create your-app-name
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
```

#### Railway
1. Зарегистрируйтесь на [Railway](https://railway.app)
2. Подключите GitHub репозиторий
3. Railway автоматически определит Docker и развернет проект

#### DigitalOcean App Platform
1. Создайте аккаунт на [DigitalOcean](https://digitalocean.com)
2. Создайте новое приложение
3. Подключите GitHub репозиторий
4. Выберите Docker как тип приложения

### 3. 🖥️ VPS/Сервер

#### Требования к серверу
- **ОС**: Ubuntu 20.04+ или CentOS 8+
- **RAM**: Минимум 1GB (рекомендуется 2GB+)
- **Диск**: 10GB свободного места
- **Сеть**: Открытые порты 80, 443, 22

#### Установка на Ubuntu
```bash
# Обновляем систему
sudo apt update && sudo apt upgrade -y

# Устанавливаем Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Устанавливаем Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Клонируем и запускаем проект
git clone <ваш-репозиторий>
cd quick-export-vkr
docker-compose up -d --build
```

#### Настройка Nginx (опционально)
```bash
# Устанавливаем Nginx
sudo apt install nginx -y

# Копируем конфигурацию
sudo cp nginx.conf /etc/nginx/sites-available/vkr-export
sudo ln -s /etc/nginx/sites-available/vkr-export /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 4. 🔧 Ручное развертывание

#### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### Frontend
```bash
cd frontend
npm install
npm run build
npm run preview  # или используйте nginx для статических файлов
```

## 🔒 Безопасность

### SSL/HTTPS
Для продакшена обязательно настройте SSL:

```bash
# Используйте Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### Firewall
```bash
# Настройте UFW
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

## 📊 Мониторинг

### Логи
```bash
# Просмотр логов
docker-compose logs -f

# Логи конкретного сервиса
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Health Check
- Backend: `http://your-domain.com/health`
- Frontend: `http://your-domain.com`

## 🔄 Обновление

```bash
# Остановить сервисы
docker-compose down

# Обновить код
git pull

# Пересобрать и запустить
docker-compose up -d --build
```

## 🆘 Устранение неполадок

### Проблемы с портами
```bash
# Проверить занятые порты
netstat -tulpn | grep :8000
netstat -tulpn | grep :5173

# Остановить процессы
sudo kill -9 <PID>
```

### Проблемы с Docker
```bash
# Очистить Docker
docker system prune -a

# Пересобрать образы
docker-compose build --no-cache
```

### Проблемы с правами
```bash
# Исправить права на файлы
sudo chown -R $USER:$USER .
sudo chmod -R 755 .
```

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи: `docker-compose logs`
2. Убедитесь, что все порты свободны
3. Проверьте, что Docker запущен
4. Создайте issue в репозитории проекта






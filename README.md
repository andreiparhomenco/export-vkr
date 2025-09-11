# VKR Export System MVP

Простой и надёжный прототип для экспорта выпускных квалификационных работ в PDF формат для загрузки в электронную библиотеку.

## Возможности

- 📁 Загрузка файлов (docx, pdf, jpg, png)
- 🔄 Изменение порядка файлов
- 📝 Ввод метаданных работы
- 🔧 Автоматическая конвертация файлов
- 📄 Объединение в единый PDF
- ⚠️ Валидация и предупреждения
- 💾 Скачивание результата

## Технологии

### Backend
- Python 3.11
- FastAPI
- SQLModel + SQLite
- LibreOffice (для конвертации DOCX)
- Pillow (для конвертации изображений)
- pypdf (для объединения PDF)

### Frontend
- React 18
- Vite
- Tailwind CSS
- Lucide React (иконки)

## Быстрый старт

### Вариант 1: Docker (рекомендуется)

1. Клонируйте репозиторий
2. Запустите проект:
```bash
docker-compose up --build
```

3. Откройте в браузере:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000

### Вариант 2: Локальная разработка

#### Backend

1. Установите Python 3.11+
2. Установите LibreOffice:
   - Windows: скачайте с официального сайта
   - macOS: `brew install --cask libreoffice`
   - Ubuntu/Debian: `sudo apt install libreoffice`

3. Настройте backend:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

1. Установите Node.js 18+
2. Настройте frontend:
```bash
cd frontend
npm install
npm run dev
```

3. Откройте http://localhost:5173

## Использование

1. **Загрузка файлов**: Перетащите файлы или нажмите "Выбрать файлы"
2. **Порядок файлов**: Используйте стрелки для изменения порядка
3. **Метаданные**: Заполните информацию о работе
4. **Экспорт**: Нажмите "Собрать PDF"
5. **Скачивание**: Файлы автоматически скачаются

## Требования к файлам

### Обязательные файлы
- **Титульный лист**: скан/фото в формате A4
- **Текст работы**: .docx или .pdf

### Рекомендуемые файлы
- **Отчёт антиплагиата**: PDF или скан
- **Дополнительные материалы**: приложения

### Технические требования
- Максимальный размер файла: 100 MB
- Поддерживаемые форматы: .docx, .pdf, .jpg, .png
- Разрешение сканов: не менее 300 DPI
- Формат: A4

## API Endpoints

- `POST /api/upload` - Загрузка файлов
- `GET /api/files/{session_id}` - Получение списка файлов
- `POST /api/prepare` - Подготовка и экспорт PDF
- `GET /api/download/{export_id}` - Скачивание PDF
- `GET /api/metadata/{export_id}` - Скачивание метаданных

## Структура проекта

```
quick-export-vkr/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI приложение
│   │   ├── models.py        # Модели данных
│   │   ├── db.py           # База данных
│   │   └── services/       # Сервисы
│   │       ├── converter.py # Конвертация файлов
│   │       ├── merger.py   # Объединение PDF
│   │       └── validator.py # Валидация
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Главный компонент
│   │   ├── components/     # React компоненты
│   │   └── index.css       # Стили
│   ├── package.json
│   └── Dockerfile
├── data/                   # Данные (создается автоматически)
│   ├── uploads/           # Загруженные файлы
│   └── exports/           # Экспортированные файлы
├── docker-compose.yml
└── README.md
```

## Разработка

### Добавление новых форматов файлов

1. Обновите `get_file_type()` в `converter.py`
2. Добавьте обработчик в `process_file()` в `main.py`
3. Обновите валидацию в `validator.py`

### Изменение UI

1. Компоненты находятся в `frontend/src/components/`
2. Стили используют Tailwind CSS
3. Иконки из библиотеки Lucide React

## Устранение неполадок

### LibreOffice не найден
- Убедитесь, что LibreOffice установлен
- Проверьте, что команда `soffice` доступна в PATH

### Ошибки конвертации
- Проверьте логи в консоли браузера
- Убедитесь, что файлы не повреждены
- Проверьте размер файлов (макс. 100 MB)

### Проблемы с CORS
- Убедитесь, что frontend и backend запущены на правильных портах
- Проверьте настройки CORS в `main.py`

## Лицензия

MIT License



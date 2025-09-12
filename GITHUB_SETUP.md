# Настройка GitHub репозитория

## Создание репозитория на GitHub

1. Перейдите на [GitHub.com](https://github.com) и войдите в свой аккаунт
2. Нажмите кнопку "New repository" (зеленая кнопка)
3. Заполните форму:
   - **Repository name**: `quick-export-vkr` (или любое другое имя)
   - **Description**: `VKR Export System MVP - Export graduate work to PDF format`
   - **Visibility**: Public или Private (на ваш выбор)
   - **НЕ** добавляйте README, .gitignore или лицензию (они уже есть в проекте)
4. Нажмите "Create repository"

## Подключение локального репозитория к GitHub

После создания репозитория на GitHub, выполните следующие команды в терминале:

```bash
# Добавьте удаленный репозиторий (замените YOUR_USERNAME на ваш GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/quick-export-vkr.git

# Переименуйте основную ветку в main (если нужно)
git branch -M main

# Запушьте код на GitHub
git push -u origin main
```

## Альтернативный способ через SSH

Если вы настроили SSH ключи для GitHub:

```bash
# Добавьте удаленный репозиторий через SSH
git remote add origin git@github.com:YOUR_USERNAME/quick-export-vkr.git

# Переименуйте основную ветку в main (если нужно)
git branch -M main

# Запушьте код на GitHub
git push -u origin main
```

## Проверка

После выполнения команд ваш код будет доступен на GitHub по адресу:
`https://github.com/YOUR_USERNAME/quick-export-vkr`

## Дополнительные команды

### Для будущих изменений:
```bash
# Добавить изменения
git add .

# Создать коммит
git commit -m "Описание изменений"

# Запушить на GitHub
git push
```

### Для работы с ветками:
```bash
# Создать новую ветку
git checkout -b feature/new-feature

# Переключиться на ветку
git checkout main

# Слить ветку
git merge feature/new-feature
```

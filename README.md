# International-hackathon-08-11-2024

# Настройка:

Приватные константы необходимо записать в файл build/private_consts, по умолчанию этот файл находится в **.gitignore**:
- YANDEX_TOKEN = "put your token here"

# Запуск сервера:

После подгрузки всех зависимостей, в корне проекта ввести:
```bash
uvicorn web.server:app --reload
```
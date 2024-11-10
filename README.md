# International-hackathon-08-11-2024

# Обязательные шаги:
1. Распаковать СОДЕРЖИМОЕ rag/data/chroma_db/chroma.zip в rag/data/chroma_db/ . Итого в директории chroma_db будет 2 файла: chroma.zip, chroma.sqlite и директория fc47d3c8-a991-4d3d-9c75-062f0092d028

# Шаги для запуска RAG-билда:
1. Установите все зависимости из poetry, пока проект не скомпилируется
2. Получите токен для авторизации в yandex gpt
   1. **Вариант первый:** Создайте в директории build/ файл private consts и внесите туда строчку YANDEX_TOKEN = "Ваш токен"
   2. **Вариант второй:** Если текущее время по МСК меньше чем 18:00, то можно заккоментировать 14 строчку и расскомментировать 13-ую в rag/debug.py
   3. **Вариант третий:** Расскомментируйте строчку 13 и закомментируйте строчку 14, а затем поставьте в строчку 13 свой токен в rag/debug.py
3. Настройте вопросы в rag/debug.py, отредактируйте список questions
4. Запустите debug.py
5. Изучайте ответы на вопросы, а также точное время выполнения каждого запроса.

Успехов!
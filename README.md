# International-hackathon-08-11-2024

# Шаги для запуска RAG-билда:
1. Получите токен для авторизации в yandex gpt
   1. **Вариант первый:** Создайте в директории build/ файл private consts и внесите туда строчку YANDEX_TOKEN = "Ваш токен"
   2. **Вариант второй:** Если текущее время по МСК меньше чем 18:00, то можно заккоментировать 14 строчку и расскомментировать 13-ую
   3. **Вариант третий:** Расскомментируйте строчку 13 и закомментируйте строчку 14, а затем поставьте в строчку 13 свой токен
2. Настройте вопросы в debug.py, отредактируйте список questions
3. Запустите debug.py
4. Изучайте ответы на вопросы, а также точное время выполнения каждого запроса.

Успехов!
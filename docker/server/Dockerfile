FROM python:3.10

WORKDIR /app
# Копируем файлы сервера в контейнер
COPY . /app

ENV PYTHONDONTWRITEBYTECODE 1

# Устанавливаем зависимости для установки Poetry
RUN apt-get update && apt-get install -y curl

# Устанавливаем Poetry
ENV POETRY_VERSION=1.8.1
RUN curl -sSL https://install.python-poetry.org | python3 -

# Добавляем Poetry в PATH
ENV PATH="/root/.local/bin:$PATH"

RUN pip install fastapi uvicorn
RUN pip install redis openai
# Устанавливаем зависимости с помощью Poetry
RUN poetry config virtualenvs.create false && poetry install --no-root

EXPOSE 8000

CMD ["uvicorn", "web.server:app", "--host", "0.0.0.0", "--port", "8000"]
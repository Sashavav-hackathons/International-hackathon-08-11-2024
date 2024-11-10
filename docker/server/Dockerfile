FROM python:3.10

WORKDIR /app
# Копируем файлы сервера в контейнер
COPY . /app

ENV PYTHONDONTWRITEBYTECODE 1

RUN pip install poetry
RUN pip install fastapi uvicorn
RUN pip install redis openai
RUN poetry update

EXPOSE 8000

CMD ["uvicorn", "web.server:app", "--host", "0.0.0.0", "--port", "8000"]
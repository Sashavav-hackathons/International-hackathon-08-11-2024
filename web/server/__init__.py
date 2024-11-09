from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from web.server.requester import request_router
from fastapi.staticfiles import StaticFiles

# Инициализация веб-приложения
app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # разрешить все источники; можно настроить для безопасности
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Настройка загрузки файлов
UPLOAD_FOLDER = '../../TEST_DATA'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Роутер запросов
app.include_router(request_router)

# Добавление статических файлов
app.mount("/static", StaticFiles(directory="web/server/static"), name='static')

# Запуск приложения через Uvicorn
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
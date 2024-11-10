from fastapi import APIRouter, Request, UploadFile, File, Response, HTTPException
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from web.server.database.redis_tools import RedisDB
from web.server.utils import remove_redundant_newlines
from rag.rag import Rag  

# Инициализация модели и роутера
model = Rag()
request_router = APIRouter()

redis_client = RedisDB()

# Указание папки с шаблонами
templates = Jinja2Templates(directory="web/server/templates")

# Модель данных для запроса
class QueryRequest(BaseModel):
    message: str
    id: str

class IdRequest(BaseModel):
    id: str

@request_router.get("/", response_class=HTMLResponse)
def create_session(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Создание сессии
@request_router.get("/wayback")
def create_session(session_id: str):
    session_data = redis_client.get_pair(session_id)
    if not session_data:
        raise HTTPException(status_code=404, detail="Session not found")
    return RedirectResponse(url=f"/c/{session_id}")

# Стандартная страница
@request_router.get("/c/", response_class=HTMLResponse)
async def print_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Загрузка страницы
@request_router.get("/c/{session_id}")
async def session_page(session_id: str, request: Request):
    # Извлечение данных сессии из Redis
    session_data = redis_client.get_pair(session_id)
    if not session_data:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Логика обработки данных сессии и возврат нужной страницы
    return templates.TemplateResponse("index.html", {"request": request})

# Загрузка истории 
@request_router.get("/history/{session_id}")
async def session_page(session_id: str):
    # Извлечение данных сессии из Redis
    session_data = redis_client.get_pair(session_id)
    # Логика обработки данных сессии и возврат нужной страницы
    return session_data

# Получение запроса от пользователя
@request_router.post("/api/query")
async def query(data: QueryRequest):
    user_message = data.message
    user_message = remove_redundant_newlines(user_message)

    user_id = data.id
    session_data = redis_client.get_pair(user_id)
    if not session_data:
        redis_client.set_pair(user_id, "")

    ai_response = model.query(user_message)
    
    # Сохранение данных в Redis
    redis_client.set_pair(user_id, str(redis_client.get_pair(user_id).decode() + "\n\n\n\n\n" + user_message + "\n\n\n\n\n" + ai_response))
    return {"response": ai_response}

# Загрузка файла
@request_router.post("/api/load_file")
async def load_file(file: UploadFile = File(...)):
    file_content = await file.read()  # обработка файла
    return {"message": "File received", "filename": file.filename}

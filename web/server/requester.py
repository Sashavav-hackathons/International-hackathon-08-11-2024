from fastapi import APIRouter, Request, UploadFile, File, Response, HTTPException
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from web.server.database.redis_tools import RedisDB
from web.server.utils import remove_redundant_newlines
from rag.rag import Rag  
from rag.chunker.chunker import Chunker
import os
import tempfile


# Инициализация чанкера
chuncker = Chunker()
token = "t1.9euelZqSiYuSx42LlpmJjp6bx5CSnO3rnpWanJLMlMeXnZGcmc7KypSVis_l8_cVQz9G-e9cBm0__t3z91VxPEb571wGbT_-zef1656VmpiRypnHmpyXyJOSj5rNz46K7_zF656VmpiRypnHmpyXyJOSj5rNz46K.IHY3Rxlb7gdBdpeWe_MgwpGS_p4JHs_UZEMLF03e2fCylv8K--iutVT2OSg0rnyGoN06kJsj6Br7q0_EHg1LAg"


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
    if not redis_client.is_exists(session_id):
         redis_client.set_pair(session_id, "")
         redis_client.set_pair("history_" + session_id, "")
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
    if not redis_client.is_exists(session_id):
         redis_client.set_pair(session_id, "")
         redis_client.set_pair("history_" + session_id, "")
    
    # Логика обработки данных сессии и возврат нужной страницы
    return templates.TemplateResponse("index.html", {"request": request})

# Загрузка истории 
@request_router.get("/history/{session_id}")
async def session_page(session_id: str):
    # Извлечение данных сессии из Redis
    session_data = redis_client.get_pair(session_id)
    if not redis_client.is_exists(session_id):
         redis_client.set_pair(session_id, "")
         redis_client.set_pair("history_" + session_id, "")
    return session_data

# Получение запроса от пользователя
@request_router.post("/api/query")
async def query(data: QueryRequest):
    user_message = data.message
    user_message = remove_redundant_newlines(user_message)

    user_id = data.id
    if not redis_client.is_exists(user_id) or not redis_client.is_exists("history_" + user_id):
        redis_client.set_pair(user_id, "")
        redis_client.set_pair("history_" + user_id, "")

    ai_response = model.static_query(q=user_message, token=token, chunker=chuncker,
                                     history=redis_client.get_pair("history_" + user_id).decode())
    
    # Сохранение данных в Redis
    redis_client.set_pair(user_id, str(redis_client.get_pair(user_id).decode() + "\n\n\n\n\n" + user_message + "\n\n\n\n\n" + ai_response["answer"]))
    return {"response": ai_response["answer"]}

# Загрузка файла
@request_router.post("/api/load_file")
async def load_file(file: UploadFile = File(...)):
    file_content = await file.read()
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        temp_file_path = tmp_file.name
        file_content = await file.read()
        tmp_file.write(file_content)
    Rag.push_new_files_to_db(temp_file_path)
    os.remove(temp_file_path)
    return {"message": "File received", "filename": file.filename}

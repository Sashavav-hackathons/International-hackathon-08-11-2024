from fastapi import APIRouter, Request, UploadFile, File, Response, HTTPException
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from database.redis_tools import RedisDB
from uuid import uuid4

import sys
import os

# Настройка путей для импорта rag
rag_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../rag'))
sys.path.append(rag_path)

from rag import Rag  

# Инициализация модели и роутера
model = Rag()
request_router = APIRouter()

redis_client = RedisDB()

# Указание папки с шаблонами
templates = Jinja2Templates(directory="web/server/templates")

# Модель данных для запроса
class QueryRequest(BaseModel):
    message: str

@request_router.get("/create_session")
def create_session(response: Response):
    session_id = str(uuid4())
    
    redis_client.set_pair(session_id, " ")
    response.set_cookie(key="session_id", value=session_id)
    
    return RedirectResponse(url=f"/c/{session_id}")

@request_router.get("/c/", response_class=HTMLResponse)
async def print_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@request_router.get("/c/{session_id}")
def session_page(session_id: str):
    # Извлечение данных сессии из Redis
    session_data = redis_client.get_pair(session_id)
    if not session_data:
        raise HTTPException(status_code=404, detail="Session not found")
    # Логика обработки данных сессии и возврат нужной страницы
    return {"message": f"Welcome to session {session_id}", "session_data": session_data}

@request_router.post("/api/query")
async def query(data: QueryRequest):

    user_message = data.message
    ai_response = model.query(user_message)
    return {"response": ai_response}

# @request_router.post("/api/load_file")
# async def load_file(file: UploadFile = File(...)):
#     file_content = await file.read()  # обработка файла
#     return {"message": "File received", "filename": file.filename}

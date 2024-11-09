from fastapi import APIRouter, Request, UploadFile, File
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

import sys
import os

# Настройка путей для импорта rag
rag_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../rag'))
sys.path.append(rag_path)

from rag import Rag  

# Инициализация модели и роутера
model = Rag()
request_router = APIRouter()

# Указание папки с шаблонами
templates = Jinja2Templates(directory="web/server/templates")

# Модель данных для запроса
class QueryRequest(BaseModel):
    message: str

@request_router.get("/c", response_class=HTMLResponse)
async def print_index(request: Request):
    print("Current working directory:", os.getcwd())
    return templates.TemplateResponse("index.html", {"request": request})

@request_router.post("/api/query")
async def query(data: QueryRequest):
    user_message = data.message
    ai_response = model.query(user_message)
    return {"response": ai_response}

# @request_router.post("/api/load_file")
# async def load_file(file: UploadFile = File(...)):
#     file_content = await file.read()  # обработка файла
#     return {"message": "File received", "filename": file.filename}

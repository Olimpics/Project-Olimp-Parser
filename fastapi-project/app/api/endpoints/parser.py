from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Dict, Any, List
import os
from app.services.parser_service import ParserService
from app.utils.file_handler import save_upload_file_temporarily

router = APIRouter()
parser_service = ParserService()

@router.post("/parse-students", response_model=Dict[str, Any])
async def parse_students(file: UploadFile = File(...)):
    """Парсинг файлу зі студентами"""
    # Перевірка розширення файлу
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension != '.xlsx':
        raise HTTPException(status_code=400, detail="Для парсингу студентів підтримуються тільки файли Excel (.xlsx)")
    
    try:
        # Зберігаємо файл тимчасово
        temp_file = await save_upload_file_temporarily(file)
        
        # Парсимо дані студентів
        students = await parser_service.parse_students(temp_file, file_extension)
        
        return {"students": students}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Помилка парсингу файлу: {str(e)}")

@router.post("/parse-disciplines", response_model=Dict[str, Any])
async def parse_disciplines(file: UploadFile = File(...)):
    """Парсинг файлу з виборчими дисциплінами"""
    # Перевірка розширення файлу
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension not in ['.xlsx', '.pdf', '.docx']:
        raise HTTPException(
            status_code=400, 
            detail="Для парсингу дисциплін підтримуються файли Excel (.xlsx), PDF (.pdf) та Word (.docx)"
        )
    
    try:
        # Зберігаємо файл тимчасово
        temp_file = await save_upload_file_temporarily(file)
        
        # Парсимо дані дисциплін
        disciplines = await parser_service.parse_disciplines(temp_file, file_extension)
        
        return {"disciplines": disciplines}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Помилка парсингу файлу: {str(e)}")

@router.post("/parse-educational-programs", response_model=Dict[str, Any])
async def parse_educational_programs(file: UploadFile = File(...)):
    """Парсинг файлу з освітніми програмами"""
    # Перевірка розширення файлу
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension not in ['.pdf', '.docx']:
        raise HTTPException(
            status_code=400, 
            detail="Для парсингу освітніх програм підтримуються файли PDF (.pdf) та Word (.docx)"
        )
    
    try:
        # Зберігаємо файл тимчасово
        temp_file = await save_upload_file_temporarily(file)
        
        # Парсимо дані освітніх програм
        result = await parser_service.parse_educational_programs(temp_file, file_extension)
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Помилка парсингу файлу: {str(e)}")
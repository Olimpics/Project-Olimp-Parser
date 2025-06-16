from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Dict, Any, List, Optional
import os
from app.services.parser_service import ParserService
from app.core.config import settings

router = APIRouter()
parser_service = ParserService()

@router.get("/parse-students/{filename}", response_model=Dict[str, Any])
async def parse_students(filename: str, limit: int = Query(5, description="Максимальна кількість рядків для обробки")):
    file_extension = os.path.splitext(filename)[1].lower()
    
    if file_extension != '.xlsx':
        raise HTTPException(status_code=400, detail="Для парсингу студентів підтримуються тільки файли Excel (.xlsx)")
    
    file_path = os.path.join(settings.FILES_DIRECTORY, filename)
    
    debug_info = {
        "requested_file": filename,
        "file_extension": file_extension,
        "settings_files_directory": settings.FILES_DIRECTORY,
        "full_file_path": file_path,
        "file_exists": os.path.exists(file_path),
        "directory_exists": os.path.exists(settings.FILES_DIRECTORY),
        "directory_contents": os.listdir(settings.FILES_DIRECTORY) if os.path.exists(settings.FILES_DIRECTORY) else [],
        "processing_limit": limit
    }
    
    if not os.path.exists(file_path):
        return JSONResponse(
            status_code=404,
            content={
                "detail": f"Файл {filename} не знайдено в директорії {settings.FILES_DIRECTORY}",
                "debug_info": debug_info
            }
        )
    
    try:
        students = await parser_service.parse_students(file_path, file_extension, limit)
        
        return {
            "students": students,
            "total_processed": len(students),
            "limit_applied": limit
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Помилка парсингу файлу: {str(e)}")

@router.get("/parse-disciplines/{filename}", response_model=Dict[str, Any])
async def parse_disciplines(filename: str, limit: int = Query(5, description="Максимальна кількість рядків для обробки")):
    file_extension = os.path.splitext(filename)[1].lower()
    
    if file_extension not in ['.xlsx', '.pdf', '.docx']:
        raise HTTPException(
            status_code=400, 
            detail="Для парсингу дисциплін підтримуються файли Excel (.xlsx), PDF (.pdf) та Word (.docx)"
        )
    
    file_path = os.path.join(settings.FILES_DIRECTORY, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Файл {filename} не знайдено в директорії {settings.FILES_DIRECTORY}")
    
    try:
        disciplines = await parser_service.parse_disciplines(file_path, file_extension, limit)
        
        return {
            "disciplines": disciplines,
            "total_processed": len(disciplines),
            "limit_applied": limit
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Помилка парсингу файлу: {str(e)}")

@router.get("/parse-educational-programs/{filename}", response_model=Dict[str, Any])
async def parse_educational_programs(filename: str):
    """Парсинг файлу з освітніми програмами за назвою файлу (без обмежень)"""
    file_extension = os.path.splitext(filename)[1].lower()
    
    if file_extension not in ['.pdf', '.docx']:
        raise HTTPException(
            status_code=400, 
            detail="Для парсингу освітніх програм підтримуються файли PDF (.pdf) та Word (.docx)"
        )
    
    file_path = os.path.join(settings.FILES_DIRECTORY, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Файл {filename} не знайдено в директорії {settings.FILES_DIRECTORY}")
    
    try:
        result = await parser_service.parse_educational_programs(file_path, file_extension)
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Помилка парсингу файлу: {str(e)}")
from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import JSONResponse
from typing import Dict, Any, List, Optional
import os
from app.services.parser_service import ParserService
from app.core.config import settings
from pathlib import Path
from pydantic import BaseModel


router = APIRouter()
parser_service = ParserService()

class ParseStudentsRequest(BaseModel):
    filename: str
    limit: int = 5

class ParseDisciplinesRequest(BaseModel):
    filename: str
    limit: int = 5

class ParseEducationalProgramsRequest(BaseModel):
    filename: str

@router.post("/parse-students", response_model=Dict[str, Any])
async def parse_students(request_data: ParseStudentsRequest):
    filename = request_data.filename
    limit = request_data.limit
    
    if not filename:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "detail": "Не вказано ім'я файлу. Необхідно вказати параметр filename.",
                "required_params": {
                    "filename": "Назва файлу для парсингу (обов'язковий параметр)",
                    "limit": "Максимальна кількість рядків для обробки (опціональний параметр, за замовчуванням: 5)"
                },
                "received_params": {
                    "filename": filename,
                    "limit": limit
                }
            }
        )
    
    file_extension = os.path.splitext(filename)[1].lower()
    if file_extension != '.xlsx':
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "detail": f"Непідтримуваний формат файлу: {file_extension}. Для парсингу студентів підтримуються тільки файли Excel (.xlsx)",
                "supported_formats": [".xlsx"],
                "received_format": file_extension
            }
        )
    
    file_path = os.path.join(settings.FILES_DIRECTORY, filename)
    
    debug_info = {
        "request_info": {
            "requested_file": filename,
            "file_extension": file_extension,
            "processing_limit": limit
        },
        "system_info": {
            "settings_files_directory": settings.FILES_DIRECTORY,
            "full_file_path": file_path,
            "file_exists": os.path.exists(file_path),
            "directory_exists": os.path.exists(settings.FILES_DIRECTORY),
        }
    }
    
    if os.path.exists(settings.FILES_DIRECTORY):
        debug_info["system_info"]["directory_contents"] = os.listdir(settings.FILES_DIRECTORY)
        
        xlsx_files = [f for f in os.listdir(settings.FILES_DIRECTORY) if f.endswith('.xlsx')]
        debug_info["system_info"]["available_xlsx_files"] = xlsx_files
    else:
        debug_info["system_info"]["error"] = f"Директорія {settings.FILES_DIRECTORY} не існує"
    
    if not os.path.exists(file_path):
        suggestions = []
        
        if os.path.exists(settings.FILES_DIRECTORY):
            all_files = os.listdir(settings.FILES_DIRECTORY)
            
            xlsx_files = [f for f in all_files if f.endswith('.xlsx')]
            
            if xlsx_files:
                suggestions.append(f"Доступні Excel файли: {', '.join(xlsx_files)}")
            else:
                suggestions.append("Не знайдено жодного Excel файлу (.xlsx) в директорії")
                
                if all_files:
                    other_files = [f for f in all_files if os.path.isfile(os.path.join(settings.FILES_DIRECTORY, f))]
                    if other_files:
                        suggestions.append(f"Знайдено інші файли в директорії: {', '.join(other_files[:5])}" + 
                                          (f" та ще {len(other_files) - 5}" if len(other_files) > 5 else ""))
                else:
                    suggestions.append("Директорія порожня")
        else:
            suggestions.append(f"Директорія {settings.FILES_DIRECTORY} не існує")
        
        return JSONResponse(
            status_code=404,
            content={
                "status": "error",
                "detail": f"Файл {filename} не знайдено в директорії {settings.FILES_DIRECTORY}",
                "suggestions": suggestions,
                "debug_info": debug_info
            }
        )
    
    try:
        students = await parser_service.parse_students(file_path, file_extension, int(limit))
        
        return {
            "status": "success",
            "students": students,
            "total_processed": len(students),
            "limit_applied": limit
        }
    
    except Exception as e:
        error_message = str(e)
        suggestions = ["Переконайтеся, що файл має правильний формат Excel для списку студентів"]
        
        if "Invalid file" in error_message or "No such file" in error_message:
            suggestions.append("Файл може бути пошкоджений або мати неправильний формат")
        elif "Sheet" in error_message and "not found" in error_message:
            suggestions.append("Перевірте, чи є в Excel файлі потрібний аркуш")
        elif "column" in error_message.lower() or "row" in error_message.lower():
            suggestions.append("Структура таблиці може не відповідати очікуваному формату")
        
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "detail": f"Помилка парсингу файлу: {error_message}",
                "suggestions": suggestions,
                "debug_info": debug_info
            }
        )

@router.post("/parse-disciplines", response_model=Dict[str, Any])
async def parse_disciplines(request_data: ParseDisciplinesRequest):
    filename = request_data.filename
    limit = request_data.limit
    
    file_extension = os.path.splitext(filename)[1].lower()
    
    debug_info = {
        "request_info": {
            "requested_file": filename,
            "file_extension": file_extension,
            "processing_limit": limit
        },
        "system_info": {
            "settings_files_directory": settings.FILES_DIRECTORY,
            "full_file_path": os.path.join(settings.FILES_DIRECTORY, filename),
            "file_exists": os.path.exists(os.path.join(settings.FILES_DIRECTORY, filename)),
            "directory_exists": os.path.exists(settings.FILES_DIRECTORY),
        }
    }
    
    if file_extension not in ['.xlsx', '.pdf', '.docx']:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "detail": "Для парсингу дисциплін підтримуються файли Excel (.xlsx), PDF (.pdf) та Word (.docx)",
                "supported_formats": [".xlsx", ".pdf", ".docx"],
                "received_format": file_extension,
                "debug_info": debug_info
            }
        )
    
    file_path = os.path.join(settings.FILES_DIRECTORY, filename)
    
    if not os.path.exists(file_path):
        suggestions = []
        
        if os.path.exists(settings.FILES_DIRECTORY):
            all_files = os.listdir(settings.FILES_DIRECTORY)
            valid_files = [f for f in all_files if f.endswith(('.xlsx', '.pdf', '.docx'))]
            
            if valid_files:
                suggestions.append(f"Доступні файли для парсингу дисциплін: {', '.join(valid_files)}")
            else:
                suggestions.append("Не знайдено відповідних файлів в директорії")
        
        return JSONResponse(
            status_code=404,
            content={
                "status": "error",
                "detail": f"Файл {filename} не знайдено в директорії {settings.FILES_DIRECTORY}",
                "suggestions": suggestions,
                "debug_info": debug_info
            }
        )
    
    try:
        disciplines = await parser_service.parse_disciplines(file_path, file_extension, limit)
        
        return {
            "status": "success",
            "disciplines": disciplines,
            "total_processed": len(disciplines),
            "limit_applied": limit
        }
    
    except Exception as e:
        error_message = str(e)
        
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "detail": f"Помилка парсингу файлу: {error_message}",
                "debug_info": debug_info
            }
        )

@router.post("/parse-educational-programs", response_model=Dict[str, Any])
async def parse_educational_programs(request_data: ParseEducationalProgramsRequest):
    """Парсинг файлу з освітніми програмами за назвою файлу (без обмежень)"""
    filename = request_data.filename
    file_extension = os.path.splitext(filename)[1].lower()
    
    debug_info = {
        "request_info": {
            "requested_file": filename,
            "file_extension": file_extension
        },
        "system_info": {
            "settings_files_directory": settings.FILES_DIRECTORY,
            "full_file_path": os.path.join(settings.FILES_DIRECTORY, filename),
            "file_exists": os.path.exists(os.path.join(settings.FILES_DIRECTORY, filename)),
            "directory_exists": os.path.exists(settings.FILES_DIRECTORY),
        }
    }
    
    if file_extension not in ['.pdf', '.docx']:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "detail": "Для парсингу освітніх програм підтримуються файли PDF (.pdf) та Word (.docx)",
                "supported_formats": [".pdf", ".docx"],
                "received_format": file_extension,
                "debug_info": debug_info
            }
        )
    
    file_path = os.path.join(settings.FILES_DIRECTORY, filename)
    
    if not os.path.exists(file_path):
        suggestions = []
        
        if os.path.exists(settings.FILES_DIRECTORY):
            all_files = os.listdir(settings.FILES_DIRECTORY)
            valid_files = [f for f in all_files if f.endswith(('.pdf', '.docx'))]
            
            if valid_files:
                suggestions.append(f"Доступні файли для парсингу освітніх програм: {', '.join(valid_files)}")
            else:
                suggestions.append("Не знайдено відповідних файлів в директорії")
                
        return JSONResponse(
            status_code=404,
            content={
                "status": "error",
                "detail": f"Файл {filename} не знайдено в директорії {settings.FILES_DIRECTORY}",
                "suggestions": suggestions,
                "debug_info": debug_info
            }
        )
    
    try:
        result = await parser_service.parse_educational_programs(file_path, file_extension)
        
        return {
            "status": "success",
            **result
        }
    
    except Exception as e:
        error_message = str(e)
        
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "detail": f"Помилка парсингу файлу: {error_message}",
                "debug_info": debug_info
            }
        )
    
@router.get("/debug/files")
async def list_files():
    files = []
    for file in os.listdir(settings.FILES_DIRECTORY):
        file_path = os.path.join(settings.FILES_DIRECTORY, file)
        files.append({
            "filename": file,
            "size": os.path.getsize(file_path) if os.path.isfile(file_path) else "directory",
            "is_file": os.path.isfile(file_path),
            "absolute_path": os.path.abspath(file_path)
        })
    return {
        "files_directory": settings.FILES_DIRECTORY,
        "files": files,
        "cwd": os.getcwd(),
        "base_dir": str(Path(__file__).resolve().parent.parent.parent)
    }
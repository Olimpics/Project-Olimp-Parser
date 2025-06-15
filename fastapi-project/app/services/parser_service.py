from typing import Dict, Any, List, Optional
from app.parsers import excel_parser, pdf_parser, word_parser
from app.utils.file_handler import remove_temp_file

class ParserService:
    async def parse_students(self, file_path: str, file_extension: str) -> List[Dict[str, Any]]:
        """Парсинг файлу зі студентами"""
        try:
            # Excel файл (.xlsx)
            if file_extension == '.xlsx':
                students = await excel_parser.parse_students(file_path)
                return students
            else:
                raise ValueError(f"Непідтримуваний формат файлу для парсингу студентів: {file_extension}")
        finally:
            # Видаляємо тимчасовий файл після парсингу
            await remove_temp_file(file_path)
    
    async def parse_disciplines(self, file_path: str, file_extension: str) -> List[Dict[str, Any]]:
        """Парсинг файлу з виборчими дисциплінами"""
        try:
            # Excel файл (.xlsx)
            if file_extension == '.xlsx':
                disciplines = await excel_parser.parse_disciplines(file_path)
                return disciplines
            
            # PDF файл (.pdf)
            elif file_extension == '.pdf':
                disciplines = await pdf_parser.parse_disciplines(file_path)
                return disciplines
            
            # Word файл (.docx)
            elif file_extension == '.docx':
                disciplines = await word_parser.parse_disciplines(file_path)
                return disciplines
                
            else:
                raise ValueError(f"Непідтримуваний формат файлу для парсингу дисциплін: {file_extension}")
        finally:
            # Видаляємо тимчасовий файл після парсингу
            await remove_temp_file(file_path)
    
    async def parse_educational_programs(self, file_path: str, file_extension: str) -> Dict[str, Any]:
        """Парсинг файлу з освітніми програмами"""
        try:
            # PDF файл (.pdf)
            if file_extension == '.pdf':
                program_data = await pdf_parser.parse_educational_programs(file_path)
                return program_data
            
            # Word файл (.docx)
            elif file_extension == '.docx':
                program_data = await word_parser.parse_educational_programs(file_path)
                return program_data
                
            else:
                raise ValueError(f"Непідтримуваний формат файлу для парсингу освітніх програм: {file_extension}")
        finally:
            # Видаляємо тимчасовий файл після парсингу
            await remove_temp_file(file_path)
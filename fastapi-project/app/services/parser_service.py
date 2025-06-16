from typing import Dict, Any, List, Optional
from app.parsers import excel_parser, pdf_parser, word_parser

class ParserService:
    async def parse_students(self, file_path: str, file_extension: str, limit: int = 5) -> List[Dict[str, Any]]:
        if file_extension == '.xlsx':
            students = await excel_parser.parse_students(file_path, limit)
            return students
        else:
            raise ValueError(f"Непідтримуваний формат файлу для парсингу студентів: {file_extension}")
    
    async def parse_disciplines(self, file_path: str, file_extension: str, limit: int = 5) -> List[Dict[str, Any]]:
        if file_extension == '.xlsx':
            disciplines = await excel_parser.parse_disciplines(file_path, limit)
            return disciplines
        
        elif file_extension == '.pdf':
            disciplines = await pdf_parser.parse_disciplines(file_path, limit)
            return disciplines
        
        elif file_extension == '.docx':
            disciplines = await word_parser.parse_disciplines(file_path, limit)
            return disciplines
            
        else:
            raise ValueError(f"Непідтримуваний формат файлу для парсингу дисциплін: {file_extension}")
    
    async def parse_educational_programs(self, file_path: str, file_extension: str) -> Dict[str, Any]:

        if file_extension == '.pdf':
            program_data = await pdf_parser.parse_educational_programs(file_path)
            return program_data
        
        elif file_extension == '.docx':
            program_data = await word_parser.parse_educational_programs(file_path)
            return program_data
            
        else:
            raise ValueError(f"Непідтримуваний формат файлу для парсингу освітніх програм: {file_extension}")
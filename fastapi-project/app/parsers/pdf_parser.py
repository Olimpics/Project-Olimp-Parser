from typing import Dict, Any, List
import PyPDF2
import re

async def parse_disciplines(file_path: str, limit: int = 5) -> List[Dict[str, Any]]:
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            
            for page in reader.pages:
                text += page.extract_text()
        
        disciplines = []
        
        discipline_blocks = re.split(r'\n\s*\n', text)
        
        for block in discipline_blocks:
            if re.search(r'назва дисципліни|код дисципліни', block, re.IGNORECASE):
                name_match = re.search(r'назва(?:\s+дисципліни)?[:\s]+([^\n]+)', block, re.IGNORECASE)
                name = name_match.group(1).strip() if name_match else ""
                
                code_match = re.search(r'код(?:\s+дисципліни)?[:\s]+([^\n]+)', block, re.IGNORECASE)
                code = code_match.group(1).strip() if code_match else ""
                
                faculty_match = re.search(r'факультет[:\s]+([^\n]+)', block, re.IGNORECASE)
                faculty = faculty_match.group(1).strip() if faculty_match else ""
                
                min_count_match = re.search(r'мін(?:імальна)?(?:\s+кількість)?[:\s]+(\d+)', block, re.IGNORECASE)
                min_count = int(min_count_match.group(1)) if min_count_match else 0
                
                max_count_match = re.search(r'макс(?:имальна)?(?:\s+кількість)?[:\s]+(\d+)', block, re.IGNORECASE)
                max_count = int(max_count_match.group(1)) if max_count_match else 0
                
                details = {
                    "departmentId": 0,
                    "teacher": "",
                    "recomend": "",
                    "prerequisites": "",
                    "language": "",
                    "determination": "",
                    "whyInterestingDetermination": "",
                    "resultEducation": "",
                    "usingIrl": "",
                    "additionaLiterature": "",
                    "typesOfTraining": "",
                    "typeOfControll": ""
                }
                
                teacher_match = re.search(r'викладач[:\s]+([^\n]+)', block, re.IGNORECASE)
                if teacher_match:
                    details["teacher"] = teacher_match.group(1).strip()
                
                discipline = {
                    "nameAddDisciplines": name,
                    "codeAddDisciplines": code,
                    "faculty": faculty,
                    "minCountPeople": min_count,
                    "maxCountPeople": max_count,
                    "minCourse": 0,
                    "maxCourse": 0,
                    "addSemestr": "",
                    "degreeLevel": "",
                    "details": details,
                    "idAddDisciplines": 0
                }
                disciplines.append(discipline)
                
                if len(disciplines) >= limit:
                    break
        
        return disciplines[:limit]
    
    except Exception as e:
        print(f"Помилка при парсингу PDF файлу дисциплін: {str(e)}")
        raise ValueError(f"Не вдалося розібрати PDF файл дисциплін: {str(e)}")

async def parse_educational_programs(file_path: str) -> Dict[str, Any]:
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            
            for i, page in enumerate(reader.pages):
                text += page.extract_text()
                if i >= 2:
                    break
        
        name_match = re.search(r'(?:назва|найменування)(?:\s+освітньої)?(?:\s+програми)?[:\s]+([^\n]+)', text, re.IGNORECASE)
        name = name_match.group(1).strip() if name_match else ""
        
        degree_match = re.search(r'ступінь[:\s]+([^\n]+)', text, re.IGNORECASE)
        degree = degree_match.group(1).strip() if degree_match else ""
        
        speciality_match = re.search(r'спеціальність[:\s]+([^\n]+)', text, re.IGNORECASE)
        speciality = speciality_match.group(1).strip() if speciality_match else ""
        
        educational_program = {
            "idEducationalProgram": 0,
            "nameEducationalProgram": name,
            "countAddSemestr3": 0,
            "countAddSemestr4": 0,
            "countAddSemestr5": 0,
            "countAddSemestr6": 0,
            "countAddSemestr7": 0,
            "countAddSemestr8": 0,
            "degree": degree,
            "speciality": speciality,
            "accreditation": 0,
            "accreditationType": "",
            "studentsAmount": 0,
            "studentsCount": 0,
            "disciplinesCount": 0
        }
        
        main_disciplines = []
        
        discipline_blocks = re.finditer(
            r'(?:код|шифр)[:\s]+([^\n]+).*?(?:кредити|ЄКТС)[:\s]+(\d+).*?(?:форма контролю)[:\s]+([^\n]+).*?(?:семестр)[:\s]+(\d+)', 
            text, 
            re.IGNORECASE | re.DOTALL
        )
        
        count = 0
        for match in discipline_blocks:
            discipline = {
                "idBindMainDisciplines": 0,
                "codeMainDisciplines": match.group(1).strip() if match.group(1) else "",
                "loans": int(match.group(2)) if match.group(2) else 0,
                "formControll": match.group(3).strip() if match.group(3) else "",
                "semestr": int(match.group(4)) if match.group(4) else 0,
                "educationalProgramName": name
            }
            main_disciplines.append(discipline)
            
            count += 1
            if count >= 5: 
                break
        
        return {
            "educationalProgram": educational_program,
            "mainDisciplines": main_disciplines
        }
    
    except Exception as e:
        print(f"Помилка при парсингу PDF файлу освітньої програми: {str(e)}")
        raise ValueError(f"Не вдалося розібрати PDF файл освітньої програми: {str(e)}")
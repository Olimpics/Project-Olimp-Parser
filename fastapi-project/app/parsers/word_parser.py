from typing import Dict, Any, List
import docx
import re

async def parse_disciplines(file_path: str, limit: int = 5) -> List[Dict[str, Any]]:
    try:
        doc = docx.Document(file_path)
        
        paragraphs = doc.paragraphs[:min(100, len(doc.paragraphs))]
        text = "\n".join([paragraph.text for paragraph in paragraphs])
        
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
        print(f"Помилка при парсингу Word файлу дисциплін: {str(e)}")
        raise ValueError(f"Не вдалося розібрати Word файл дисциплін: {str(e)}")

async def parse_educational_programs(file_path: str) -> Dict[str, Any]:
    try:
        doc = docx.Document(file_path)
        
        paragraphs = doc.paragraphs[:min(100, len(doc.paragraphs))]
        text = "\n".join([paragraph.text for paragraph in paragraphs])
        
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
        
        table_limit = min(5, len(doc.tables))
        for table in doc.tables[:table_limit]:
            row_limit = min(6, len(table.rows)) 
            for row_idx in range(1, row_limit):
                row = table.rows[row_idx]
                
                cells = [cell.text.strip() for cell in row.cells]
                
                if len(cells) >= 4:
                    code = cells[0] if len(cells) > 0 else ""
                    loans = int(cells[1]) if len(cells) > 1 and cells[1].isdigit() else 0
                    form_controll = cells[2] if len(cells) > 2 else ""
                    semestr = int(cells[3]) if len(cells) > 3 and cells[3].isdigit() else 0
                    
                    discipline = {
                        "idBindMainDisciplines": 0,
                        "codeMainDisciplines": code,
                        "loans": loans,
                        "formControll": form_controll,
                        "semestr": semestr,
                        "educationalProgramName": name
                    }
                    main_disciplines.append(discipline)
        
        return {
            "educationalProgram": educational_program,
            "mainDisciplines": main_disciplines[:5]
        }
    
    except Exception as e:
        print(f"Помилка при парсингу Word файлу освітньої програми: {str(e)}")
        raise ValueError(f"Не вдалося розібрати Word файл освітньої програми: {str(e)}")
from typing import Dict, Any, List
import pandas as pd
import httpx
import os
import json
from pathlib import Path
from app.core.config import settings


async def get_faculty_map() -> Dict[str, int]:
    url = "https://localhost:7011/api/Faculty"
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(url, headers={"accept": "text/plain"})
        response.raise_for_status()
        faculties = response.json()
        return {f["nameFaculty"]: f["idFaculty"] for f in faculties}

async def get_degree_map() -> Dict[str, int]:
    url = "https://localhost:7011/api/EducationalDegree"
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(url, headers={"accept": "text/plain"})
        response.raise_for_status()
        degrees = response.json()
        return {d["nameEducationalDegreec"]: d["idEducationalDegree"] for d in degrees}

async def get_study_form_map() -> Dict[str, int]:
    url = "https://localhost:7011/api/StudyForm"
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(url, headers={"accept": "text/plain"})
        response.raise_for_status()
        forms = response.json()
        return {f["nameStudyForm"]: f["idStudyForm"] for f in forms}

async def get_group_map() -> Dict[str, Dict[str, int]]:
    url = "https://localhost:7011/api/Group?sortOrder=0"
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(url, headers={"accept": "text/plain"})
        response.raise_for_status()
        groups = response.json()
        return {g["code"].strip().upper(): {"groupId": g["id"], "departmentId": g["departmentId"]} for g in groups}

def save_to_json(data: List[Dict[str, Any]], output_file: str) -> str:
    """
    Зберігає дані у JSON-файл і повертає шлях до збереженого файлу.
    
    Args:
        data: Дані для збереження
        output_file: Шлях до вихідного файлу
    
    Returns:
        Повний шлях до збереженого файлу
    """
    from app.core.config import settings
    
    # Якщо вказано тільки ім'я файлу без шляху, зберігаємо в директорію output_json_files
    if os.path.dirname(output_file) == "":
        output_path = os.path.join(settings.OUTPUT_JSON_FOLDER, output_file)
    else:
        output_path = output_file
    
    # Переконуємося, що директорія існує
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Зберігаємо JSON-файл
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return output_path

async def parse_students(file_path: str, limit: int = 5, output_file: str = None) -> List[Dict[str, Any]]:
    try:
        faculty_name_to_id = await get_faculty_map()
        degree_name_to_id = await get_degree_map()
        study_form_name_to_id = await get_study_form_map()
        group_code_to_ids = await get_group_map()

        df = pd.read_excel(file_path, header=None)
        
        df = df.iloc[1:]
        
        if len(df) > limit:
            df = df.iloc[:limit]
        
        students = []
        for _, row in df.iterrows():
            status_col = 1  # B: Статус
            id_col = 2  # C: ID ФО
            name_col = 3    # D: Здобувач
            start_date_col = 5  # F: Початок навчання
            end_date_col = 6    # G: Завершення навчання
            faculty_col = 7  # H: Структурний підрозділ (факультет)
            degree_col = 9  # J: Освітній ступінь
            study_form_col = 10  # K: Форма навчання
            is_short_col = 11  # L: Чи скорочений термін
            edu_prog_col = 14  # O: ID ОП
            course_col = 17  # R: Курс
            group_col = 18  # S: Група

            faculty_name = str(row[faculty_col]) if pd.notna(row[faculty_col]) else None
            faculty_id = faculty_name_to_id.get(faculty_name) if faculty_name else None

            degree_name = str(row[degree_col]) if pd.notna(row[degree_col]) else None
            educational_degree_id = degree_name_to_id.get(degree_name) if degree_name else None

            study_form_name = str(row[study_form_col]) if pd.notna(row[study_form_col]) else None
            study_form_id = study_form_name_to_id.get(study_form_name) if study_form_name else None

            group_code = str(row[group_col]).strip().upper() if pd.notna(row[group_col]) else None
            
            if group_code:
                found = group_code in group_code_to_ids
                print(f"Шукаю групу: '{group_code}', Знайдено: {found}")
                if not found:
                    similar_codes = [code for code in group_code_to_ids.keys() 
                                   if code.replace("-", "").lower() == group_code.replace("-", "").lower()]
                    if similar_codes:
                        print(f"Знайдено схожі коди: {similar_codes}")
            
            group_info = group_code_to_ids.get(group_code) if group_code else None
            group_id = group_info["groupId"] if group_info else None
            department_id = group_info["departmentId"] if group_info else None

            education_start = None
            if pd.notna(row[start_date_col]):
                try:
                    start_date = pd.to_datetime(row[start_date_col])
                    education_start = {
                        "year": int(start_date.year),
                        "month": int(start_date.month),
                        "day": int(start_date.day),
                        "dayOfWeek": int(start_date.dayofweek)
                    }
                except Exception as e:
                    print(f"Помилка при обробці дати початку навчання: {str(e)}")
            
            education_end = None
            if pd.notna(row[end_date_col]):
                try:
                    end_date = pd.to_datetime(row[end_date_col])
                    education_end = {
                        "year": int(end_date.year),
                        "month": int(end_date.month),
                        "day": int(end_date.day),
                        "dayOfWeek": int(end_date.dayofweek)
                    }
                except Exception as e:
                    print(f"Помилка при обробці дати завершення навчання: {str(e)}")
            
            is_short = "0"
            if pd.notna(row[is_short_col]):
                is_short_val = str(row[is_short_col]).strip().lower()
                if is_short_val == "так":
                    is_short = "1"
            
            student = {
                "IDstudent": int(row[id_col]) if pd.notna(row[id_col]) else None,
                "nameStudent": str(row[name_col]) if pd.notna(row[name_col]) else None,
                # "statusId": str(row[status_col]) if pd.notna(row[status_col]) else None,
                "educationStart": education_start,
                "educationEnd": education_end,
                "course": int(row[course_col]) if pd.notna(row[course_col]) else None,
                "facultyId": faculty_id,
                "educationalDegreeId": educational_degree_id,
                "studyFormId": study_form_id,
                "isShort": int(is_short),
                "educationalProgramId": int(row[edu_prog_col]) if pd.notna(row[edu_prog_col]) else None,
                "departmentId": department_id,
                "groupId": group_id
            }
            students.append(student)
        
        # Зберігаємо результат у JSON-файл, якщо вказано шлях
        if output_file:
            if os.path.dirname(output_file) == "":
                output_path = os.path.join(settings.OUTPUT_JSON_FOLDER, output_file)
            else:
                output_path = output_file
                
            # Переконуємося, що директорія існує
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Зберігаємо JSON-файл
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(students, f, ensure_ascii=False, indent=2)
                
            print(f"Результати збережено у файл: {output_path}")
            
            # Повертаємо повний шлях до збереженого файлу
            return students, output_path
        
        return students
    
    except Exception as e:
        print(f"Помилка при парсингу Excel файлу студентів: {str(e)}")
        raise ValueError(f"Не вдалося розібрати файл студентів: {str(e)}")
    
async def parse_disciplines(file_path: str, limit: int = 5, output_file: str = None) -> List[Dict[str, Any]]:
    try:
        df = pd.read_excel(file_path)
        
        df = df.head(limit)
        
        disciplines = []
        for _, row in df.iterrows():
            details = {
                "departmentId": int(row.get("Кафедра ID", 0)),
                "teacher": row.get("Викладач", ""),
                "recomend": row.get("Рекомендації", ""),
                "prerequisites": row.get("Пререквізити", ""),
                "language": row.get("Мова викладання", ""),
                "determination": row.get("Визначення", ""),
                "whyInterestingDetermination": row.get("Чому цікаво", ""),
                "resultEducation": row.get("Результати навчання", ""),
                "usingIrl": row.get("Використання в реальному житті", ""),
                "additionaLiterature": row.get("Додаткова література", ""),
                "typesOfTraining": row.get("Види навчальних занять", ""),
                "typeOfControll": row.get("Вид контролю", "")
            }
            
            discipline = {
                "nameAddDisciplines": row.get("Назва дисципліни", ""),
                "codeAddDisciplines": row.get("Код дисципліни", ""),
                "faculty": row.get("Факультет", ""),
                "minCountPeople": int(row.get("Мін. кількість", 0)),
                "maxCountPeople": int(row.get("Макс. кількість", 0)),
                "minCourse": int(row.get("Мін. курс", 0)),
                "maxCourse": int(row.get("Макс. курс", 0)),
                "addSemestr": row.get("Семестр", ""),
                "degreeLevel": row.get("Освітній ступінь", ""),
                "details": details,
                "idAddDisciplines": int(row.get("ID", 0))
            }
            disciplines.append(discipline)
        
        # Зберігаємо результат у JSON-файл, якщо вказано шлях
        if output_file:
            saved_path = save_to_json(disciplines, output_file)
            print(f"Результати збережено у файл: {saved_path}")
        
        return disciplines
    
    except Exception as e:
        print(f"Помилка при парсингу Excel файлу дисциплін: {str(e)}")
        raise ValueError(f"Не вдалося розібрати файл дисциплін: {str(e)}")
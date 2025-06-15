from typing import Dict, Any, List
import pandas as pd
import os

async def parse_students(file_path: str) -> List[Dict[str, Any]]:
    """
    Парсинг студентів з Excel файлу
    """
    try:
        # Завантаження файлу Excel
        df = pd.read_excel(file_path)
        
        students = []
        for _, row in df.iterrows():
            # Перетворення дат в необхідний формат
            education_start = None
            if "Дата початку навчання" in row and pd.notna(row["Дата початку навчання"]):
                start_date = pd.to_datetime(row["Дата початку навчання"])
                education_start = {
                    "year": start_date.year,
                    "month": start_date.month,
                    "day": start_date.day,
                    "dayOfWeek": start_date.dayofweek
                }
            
            education_end = None
            if "Дата закінчення навчання" in row and pd.notna(row["Дата закінчення навчання"]):
                end_date = pd.to_datetime(row["Дата закінчення навчання"])
                education_end = {
                    "year": end_date.year,
                    "month": end_date.month,
                    "day": end_date.day,
                    "dayOfWeek": end_date.dayofweek
                }
            
            # Формування об'єкту студента
            student = {
                "nameStudent": row.get("ПІБ", ""),
                "statusId": int(row.get("Статус", 0)),
                "educationStart": education_start,
                "educationEnd": education_end,
                "course": int(row.get("Курс", 0)),
                "facultyId": int(row.get("Факультет ID", 0)),
                "educationalDegreeId": int(row.get("Освітній ступінь ID", 0)),
                "studyFormId": int(row.get("Форма навчання ID", 0)),
                "isShort": int(row.get("Скорочений", 0)),
                "educationalProgramId": int(row.get("Освітня програма ID", 0)),
                "departmentId": int(row.get("Кафедра ID", 0)),
                "groupId": int(row.get("Група ID", 0))
            }
            students.append(student)
        
        return students
    
    except Exception as e:
        print(f"Помилка при парсингу Excel файлу студентів: {str(e)}")
        raise ValueError(f"Не вдалося розібрати файл студентів: {str(e)}")

async def parse_disciplines(file_path: str) -> List[Dict[str, Any]]:
    """
    Парсинг виборчих дисциплін з Excel файлу
    """
    try:
        # Завантаження файлу Excel
        df = pd.read_excel(file_path)
        
        disciplines = []
        for _, row in df.iterrows():
            # Формування об'єкту дисципліни
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
        
        return disciplines
    
    except Exception as e:
        print(f"Помилка при парсингу Excel файлу дисциплін: {str(e)}")
        raise ValueError(f"Не вдалося розібрати файл дисциплін: {str(e)}")
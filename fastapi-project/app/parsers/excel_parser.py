from typing import Dict, Any, List
import pandas as pd
import os

async def parse_students(file_path: str, limit: int = 5) -> List[Dict[str, Any]]:
    try:
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
                "studentID": int(row[id_col]) if pd.notna(row[id_col]) else 0,
                "nameStudent": str(row[name_col]) if pd.notna(row[name_col]) else "",
                "statusId": str(row[status_col]) if pd.notna(row[status_col]) else "0",
                "educationStart": education_start,
                "educationEnd": education_end,
                "course": str(row[course_col]) if pd.notna(row[course_col]) else "0",
                "facultyId": str(row[faculty_col]) if pd.notna(row[faculty_col]) else "0",
                "educationalDegreeId": str(row[degree_col]) if pd.notna(row[degree_col]) else "0",
                "studyFormId": str(row[study_form_col]) if pd.notna(row[study_form_col]) else "0",
                "isShort": is_short,
                "educationalProgramId": str(row[edu_prog_col]) if pd.notna(row[edu_prog_col]) else "0",
                "departmentId": "0",  # За замовчуванням
                "groupId": str(row[group_col]) if pd.notna(row[group_col]) else "0"
            }
            students.append(student)
        
        return students
    
    except Exception as e:
        print(f"Помилка при парсингу Excel файлу студентів: {str(e)}")
        raise ValueError(f"Не вдалося розібрати файл студентів: {str(e)}")

async def parse_disciplines(file_path: str, limit: int = 5) -> List[Dict[str, Any]]:
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
        
        return disciplines
    
    except Exception as e:
        print(f"Помилка при парсингу Excel файлу дисциплін: {str(e)}")
        raise ValueError(f"Не вдалося розібрати файл дисциплін: {str(e)}")
from typing import Dict, Any, List
import PyPDF2
import re
import os

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
            
            for page in reader.pages:
                text += page.extract_text()
        
        program_name = "" 
        degree = ""
        accreditation_type = ""
        credits = 0
        speciality = ""
        
        semester_counts = {3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}
        
        ukr_match = re.search(r'(?:Освітньо-професійна програма|Освітня програма)\s*[«"]([^»"]+)[»"]', text, re.IGNORECASE)
        if ukr_match:
            name_content = ukr_match.group(1).strip()
            name_content = re.sub(r'Освітньо\s*-?професійна\s+програма\s*[«"]?\s*', '', name_content, flags=re.IGNORECASE)
            name_content = name_content.strip()
            name_content = re.sub(r'[»"]\s*$', '', name_content)
            program_name = f"Освітньо-професійна програма «{name_content}»"
            print(f"Found Ukrainian program name: {program_name}")
        else:
            alt_match = re.search(r'(?:Офіційна|Повна)\s+назва\s+освітньої\s+програми\s*[:\n\s]+([^\n]+)', text, re.IGNORECASE)
            if alt_match:
                name_content = alt_match.group(1).strip()
                name_content = re.sub(r'Освітньо\s*-?професійна\s+програма\s*[«"]?\s*', '', name_content, flags=re.IGNORECASE)
                name_content = name_content.strip()
                name_content = re.sub(r'[»"]\s*$', '', name_content)
                program_name = f"Освітньо-професійна програма «{name_content}»"
                print(f"Found alternative Ukrainian program name: {program_name}")
        
        degree_match = re.search(r'(?:ступінь|рівень)\s+(?:вищої\s+освіти)[:\s]+([^\n]+)', text, re.IGNORECASE)
        if degree_match:
            degree_text = degree_match.group(1).strip().lower()
            if 'бакалавр' in degree_text:
                degree = 'бакалавр'
            elif 'магістр' in degree_text:
                degree = 'магістр'
            elif 'доктор філософії' in degree_text:
                degree = 'доктор філософії'
        else:
            alt_degree = re.search(r'(?:перший|другий)[\s(]+(?:бакалаврський|магістерський)[)\s]', text, re.IGNORECASE)
            if alt_degree:
                if 'бакалавр' in alt_degree.group(0).lower():
                    degree = 'бакалавр'
                elif 'магістр' in alt_degree.group(0).lower():
                    degree = 'магістр'
        
        if not degree:
            degree = 'бакалавр'
        
        speciality_match = re.search(r'спеціальність[:\s]+(\d+)[^\n,;]*', text, re.IGNORECASE)
        if speciality_match:
            spec_num = speciality_match.group(1).strip()
            spec_name_match = re.search(f"{spec_num}[^\n,;]*", text)
            if spec_name_match:
                speciality = spec_name_match.group(0).strip()
            else:
                speciality = spec_num
        
        # Extract credits
        credits_match = re.search(r'(\d+)\s*кредит', text, re.IGNORECASE)
        if credits_match:
            credits = int(credits_match.group(1))
        else:
            credits = 240 if degree == 'бакалавр' else 120
        
        accreditation_match = re.search(r'(?:Наявність\s+акредитації|акредитація)[:\s]+((?:[^\n]+\n?){1,6})', text, re.IGNORECASE)
        if accreditation_match:
            accreditation_type = accreditation_match.group(1).strip()
            accreditation_type = re.sub(r'\s{2,}', ' ', accreditation_type)
        
        educational_program = {
            "idEducationalProgram": 0,
            "nameEducationalProgram": program_name,
            "countAddSemestr3": semester_counts[3],
            "countAddSemestr4": semester_counts[4],
            "countAddSemestr5": semester_counts[5],
            "countAddSemestr6": semester_counts[6],
            "countAddSemestr7": semester_counts[7],
            "countAddSemestr8": semester_counts[8],
            "degree": degree,
            "speciality": speciality,
            "accreditation": credits,
            "accreditationType": accreditation_type,
            "studentsAmount": 0,
            "studentsCount": 0,
            "disciplinesCount": 0
        }
        
        main_disciplines = []
        
        match = re.search(r'І Цикл загальної підготовки(.*?)Вибіркові компоненти', text, re.DOTALL | re.IGNORECASE)
        if match:
            disciplines_text = match.group(1)
            
            discipline_matches = re.finditer(
                r'(ОК\s*\d+(?:\.\d+)?)\s+([^\n]+?)\s+(\d+(?:[.,]\d+)?)\s+(екзамен|залік|іспит|диф\.\s*залік|атестаційний іспит)(?:,\s*(?:екзамен|залік|іспит|диф\.\s*залік|атестаційний іспит))*\s+(\d+(?:,\d+)?)',
                disciplines_text,
                re.IGNORECASE
            )
            
            for match in discipline_matches:
                code = match.group(1).strip()
                name_discipline = match.group(2).strip()
                loans_text = match.group(3).replace(',', '.')
                form_control = match.group(4).strip()
                
                full_control_text = re.search(
                    f"{re.escape(form_control)}((?:,\\s*(?:екзамен|залік|іспит|диф\\.\\s*залік|атестаційний іспит))*)",
                    match.group(0), 
                    re.IGNORECASE
                )
                
                if full_control_text and full_control_text.group(1):
                    form_control += full_control_text.group(1)
                
                semestr_text = match.group(5)
                
                try:
                    loans = float(loans_text)
                except ValueError:
                    loans = 0
                    
                try:
                    if ',' in semestr_text:
                        semestr = int(semestr_text.split(',')[0])
                    else:
                        semestr = int(semestr_text)
                except ValueError:
                    semestr = 0
                
                discipline = {
                    "idBindMainDisciplines": 0,
                    "codeMainDisciplines": code,
                    "disciplineName": name_discipline,
                    "loans": loans,
                    "formControll": form_control,
                    "semestr": semestr,
                    "educationalProgramName": program_name
                }
                main_disciplines.append(discipline)
            
            if len(main_disciplines) < 5:
                ok_matches = re.finditer(r'(ОК\s*\d+(?:\.\d+)?)\s+([^\n]+)', disciplines_text)
                
                for match in ok_matches:
                    code = match.group(1).strip()
                    rest_of_line = match.group(2).strip()
                    
                    if any(d["codeMainDisciplines"] == code for d in main_disciplines):
                        continue
                    
                    parts = re.split(r'\s{2,}', rest_of_line)
                    
                    name_discipline = parts[0] if parts else ""
                    loans = 0
                    form_control = ""
                    semestr = 0
                    
                    for part in parts:
                        if re.match(r'^\d+(?:[.,]\d+)?$', part.strip()):
                            try:
                                loans = float(part.replace(',', '.'))
                                break
                            except ValueError:
                                pass
                    
                    control_pattern = r'(екзамен|залік|іспит|диф\.\s*залік|атестаційний іспит)'
                    for part in parts:
                        if re.search(control_pattern, part, re.IGNORECASE):
                            form_control = part.strip()
                            break
                    
                    for part in reversed(parts):
                        if re.match(r'^\d+$', part.strip()):
                            try:
                                semestr = int(part)
                                break
                            except ValueError:
                                pass
                    
                    discipline = {
                        "idBindMainDisciplines": 0,
                        "codeMainDisciplines": code,
                        "disciplineName": name_discipline,
                        "loans": loans,
                        "formControll": form_control,
                        "semestr": semestr,
                        "educationalProgramName": program_name
                    }
                    main_disciplines.append(discipline)
        
        if len(main_disciplines) < 5:
            ok_patterns = re.finditer(r'(ОК\s*\d+(?:\.\d+)?)\s+([^\n]+?)\s+(\d+(?:[.,]\d+)?)\s+(?:екзамен|залік|іспит|диф\.\s*залік|атестаційний іспит)', text, re.IGNORECASE)
            
            for match in ok_patterns:
                code = match.group(1).strip()
                
                if any(d["codeMainDisciplines"] == code for d in main_disciplines):
                    continue
                
                name_discipline = match.group(2).strip()
                loans_text = match.group(3).replace(',', '.')
                
                form_control_match = re.search(r'(екзамен|залік|іспит|диф\.\s*залік|атестаційний іспит)(?:,\s*(?:екзамен|залік|іспит|диф\.\s*залік|атестаційний іспит))*', match.group(0), re.IGNORECASE)
                form_control = form_control_match.group(0) if form_control_match else ""
                
                semester_match = re.search(r'(?:семестр|сем\.?)[:\s]*(\d+)', match.group(0) + text[match.end():match.end()+50], re.IGNORECASE)
                semestr = int(semester_match.group(1)) if semester_match else 0
                
                try:
                    loans = float(loans_text)
                except ValueError:
                    loans = 0
                
                discipline = {
                    "idBindMainDisciplines": 0,
                    "codeMainDisciplines": code,
                    "disciplineName": name_discipline,
                    "loans": loans,
                    "formControll": form_control,
                    "semestr": semestr,
                    "educationalProgramName": program_name
                }
                main_disciplines.append(discipline)
        
        elective_section_match = re.search(r'Вибіркові компоненти(.*?)(?:Атестація|ІІІ Цикл|Всього за|Загальний обсяг)', text, re.DOTALL | re.IGNORECASE)
        if elective_section_match:
            electives_text = elective_section_match.group(1)
            
            vk_matches = re.finditer(r'(ВК\s*\d+(?:\.\d+)?)[^\d]*(\d+(?:[.,]\d+)?)[^\d]*(екзамен|залік|іспит|диф\.\s*залік)[^\d]*(\d+)', electives_text, re.IGNORECASE)
            
            for match in vk_matches:
                try:
                    semester = int(match.group(4))
                    if 3 <= semester <= 8:
                        semester_counts[semester] += 1
                except (ValueError, IndexError):
                    pass
            
            if all(count == 0 for count in semester_counts.values()):
                vk_entries = re.finditer(r'(ВК\s*\d+(?:\.\d+)?)\s+([^\n]+)', electives_text, re.IGNORECASE)
                
                for match in vk_entries:
                    line = match.group(2)
                    semester_match = re.search(r'(\d+)\s*$', line)
                    
                    if semester_match:
                        try:
                            semester = int(semester_match.group(1))
                            if 3 <= semester <= 8:
                                semester_counts[semester] += 1
                        except ValueError:
                            pass
            
            educational_program["countAddSemestr3"] = semester_counts[3]
            educational_program["countAddSemestr4"] = semester_counts[4]
            educational_program["countAddSemestr5"] = semester_counts[5]
            educational_program["countAddSemestr6"] = semester_counts[6]
            educational_program["countAddSemestr7"] = semester_counts[7]
            educational_program["countAddSemestr8"] = semester_counts[8]
        
        # Sort disciplines by code
        main_disciplines.sort(key=lambda d: d["codeMainDisciplines"])
        
        return {
            "educationalProgram": educational_program,
            "mainDisciplines": main_disciplines
        }
    
    except Exception as e:
        print(f"Помилка при парсингу PDF файлу освітньої програми: {str(e)}")
        raise ValueError(f"Не вдалося розібрати PDF файл освітньої програми: {str(e)}")
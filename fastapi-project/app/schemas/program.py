from pydantic import BaseModel
from typing import Optional, List

class EducationalProgram(BaseModel):
    idEducationalProgram: int = 0
    nameEducationalProgram: str
    countAddSemestr3: int = 0
    countAddSemestr4: int = 0
    countAddSemestr5: int = 0
    countAddSemestr6: int = 0
    countAddSemestr7: int = 0
    countAddSemestr8: int = 0
    degree: Optional[str] = None
    speciality: Optional[str] = None
    accreditation: int = 0
    accreditationType: Optional[str] = None
    studentsAmount: int = 0
    studentsCount: int = 0
    disciplinesCount: int = 0

class MainDiscipline(BaseModel):
    idBindMainDisciplines: int = 0
    codeMainDisciplines: Optional[str] = None
    loans: int = 0
    formControll: Optional[str] = None
    semestr: int = 0
    educationalProgramName: Optional[str] = None
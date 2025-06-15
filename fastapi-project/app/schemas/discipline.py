from pydantic import BaseModel
from typing import Optional

class DisciplineDetails(BaseModel):
    departmentId: int = 0
    teacher: Optional[str] = None
    recomend: Optional[str] = None
    prerequisites: Optional[str] = None
    language: Optional[str] = None
    determination: Optional[str] = None
    whyInterestingDetermination: Optional[str] = None
    resultEducation: Optional[str] = None
    usingIrl: Optional[str] = None
    additionaLiterature: Optional[str] = None
    typesOfTraining: Optional[str] = None
    typeOfControll: Optional[str] = None

class Discipline(BaseModel):
    nameAddDisciplines: str
    codeAddDisciplines: Optional[str] = None
    faculty: Optional[str] = None
    minCountPeople: int = 0
    maxCountPeople: int = 0
    minCourse: int = 0
    maxCourse: int = 0
    addSemestr: Optional[str] = None
    degreeLevel: Optional[str] = None
    details: DisciplineDetails
    idAddDisciplines: int = 0
from pydantic import BaseModel
from typing import Optional
from datetime import date

class EducationDate(BaseModel):
    year: int
    month: int
    day: int
    dayOfWeek: int

class Student(BaseModel):
    nameStudent: str
    statusId: int = 0
    educationStart: Optional[EducationDate] = None
    educationEnd: Optional[EducationDate] = None
    course: int = 0
    facultyId: int = 0
    educationalDegreeId: int = 0
    studyFormId: int = 0
    isShort: int = 0
    educationalProgramId: int = 0
    departmentId: int = 0
    groupId: int = 0
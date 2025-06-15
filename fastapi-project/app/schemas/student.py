from pydantic import BaseModel
from typing import Optional, Union

class EducationDate(BaseModel):
    year: int
    month: int
    day: int
    dayOfWeek: int

class Student(BaseModel):
    studentID: int = 0
    nameStudent: str = ""
    statusId: str = "0"
    educationStart: Optional[EducationDate] = None
    educationEnd: Optional[EducationDate] = None
    course: str = "0"
    facultyId: str = "0"
    educationalDegreeId: str = "0"
    studyFormId: str = "0"
    isShort: str = "0"
    educationalProgramId: str = "0"
    departmentId: str = "0"
    groupId: str = "0"
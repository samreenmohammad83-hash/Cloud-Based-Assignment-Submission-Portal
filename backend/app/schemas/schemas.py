from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class RegisterIn(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    role: str = Field(pattern="^(student|teacher)$")

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

class AssignmentIn(BaseModel):
    course_id: int
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=3, max_length=5000)
    deadline: datetime
    max_marks: int = Field(gt=0, le=1000)
    allowed_file_types: str = "pdf,docx"
    max_file_size_mb: int = Field(gt=0, le=100)

class AssignmentOut(AssignmentIn):
    assignment_id: int
    created_by: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class GradeIn(BaseModel):
    marks: int = Field(ge=0)
    feedback: str = Field(default="", max_length=5000)

class CourseIn(BaseModel):
    course_name: str = Field(min_length=2, max_length=150)

class CourseOut(CourseIn):
    course_id: int
    teacher_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

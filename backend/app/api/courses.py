from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.db import get_db
from ..models import Course
from ..schemas.schemas import CourseIn
from .deps import current_user, require_role
router=APIRouter(prefix="/api/courses",tags=["courses"])

@router.post("", dependencies=[Depends(require_role("teacher"))])
def create_course(data:CourseIn, db:Session=Depends(get_db), user=Depends(current_user)):
    c=Course(course_name=data.course_name,teacher_id=user.user_id); db.add(c); db.commit(); db.refresh(c); return c

@router.get("")
def list_courses(db:Session=Depends(get_db), user=Depends(current_user)):
    return db.query(Course).all()

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.db import get_db
from ..models import Assignment, Course
from ..schemas.schemas import AssignmentIn
from .deps import current_user, require_role
router=APIRouter(prefix="/api/assignments",tags=["assignments"])

@router.post("")
def create(data:AssignmentIn, db:Session=Depends(get_db), user=Depends(require_role("teacher"))):
    course=db.get(Course,data.course_id)
    if not course or course.teacher_id!=user.user_id: raise HTTPException(403,"Course not owned by teacher")
    a=Assignment(**data.model_dump(),created_by=user.user_id); db.add(a); db.commit(); db.refresh(a); return a

@router.get("")
def list_all(db:Session=Depends(get_db), user=Depends(current_user)):
    return db.query(Assignment).all()

@router.get("/{assignment_id}")
def get_one(assignment_id:int,db:Session=Depends(get_db),user=Depends(current_user)):
    a=db.get(Assignment,assignment_id)
    if not a: raise HTTPException(404,"Assignment not found")
    return a

@router.put("/{assignment_id}")
def update(assignment_id:int,data:AssignmentIn,db:Session=Depends(get_db),user=Depends(require_role("teacher"))):
    a=db.get(Assignment,assignment_id)
    if not a or a.created_by!=user.user_id: raise HTTPException(404,"Assignment not found")
    for k,v in data.model_dump().items(): setattr(a,k,v)
    db.commit(); db.refresh(a); return a

@router.delete("/{assignment_id}")
def delete(assignment_id:int,db:Session=Depends(get_db),user=Depends(require_role("teacher"))):
    a=db.get(Assignment,assignment_id)
    if not a or a.created_by!=user.user_id: raise HTTPException(404,"Assignment not found")
    db.delete(a); db.commit(); return {"message":"Assignment deleted"}

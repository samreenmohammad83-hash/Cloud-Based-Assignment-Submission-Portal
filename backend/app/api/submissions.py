from datetime import datetime, timezone
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
from ..core.db import get_db
from ..core.config import settings
from ..models import Submission, Assignment, Course
from ..services.storage import save_upload, read_file
from .deps import current_user, require_role
from ..schemas.schemas import GradeIn
router=APIRouter(prefix="/api",tags=["submissions"])

@router.post("/assignments/{assignment_id}/submit")
async def submit(assignment_id:int,file:UploadFile=File(...),db:Session=Depends(get_db),user=Depends(require_role("student"))):
    a=db.get(Assignment,assignment_id)
    if not a: raise HTTPException(404,"Assignment not found")
    now=datetime.now(timezone.utc)
    deadline=a.deadline if a.deadline.tzinfo else a.deadline.replace(tzinfo=timezone.utc)
    late=now>deadline
    if late and not settings.ALLOW_LATE_SUBMISSIONS: raise HTTPException(400,"Deadline passed")
    path,url=await save_upload(file,assignment_id,user.user_id,a.max_file_size_mb)
    status="LATE" if late else "SUBMITTED"
    s=Submission(assignment_id=assignment_id,student_id=user.user_id,file_name=file.filename or "file",file_url=url,storage_path=path,submitted_at=now,submission_status=status)
    db.add(s); db.commit(); db.refresh(s); return s

@router.get("/submissions/me")
def mine(db:Session=Depends(get_db),user=Depends(require_role("student"))): return db.query(Submission).filter(Submission.student_id==user.user_id).all()

@router.get("/assignments/{assignment_id}/submissions")
def assignment_submissions(assignment_id:int,db:Session=Depends(get_db),user=Depends(require_role("teacher"))):
    a=db.get(Assignment,assignment_id)
    if not a or a.created_by!=user.user_id: raise HTTPException(403,"Not permitted")
    return db.query(Submission).filter(Submission.assignment_id==assignment_id).all()

@router.get("/submissions/{submission_id}")
def get_submission(submission_id:int,db:Session=Depends(get_db),user=Depends(current_user)):
    s=db.get(Submission,submission_id)
    if not s: raise HTTPException(404,"Submission not found")
    if user.role=="student" and s.student_id!=user.user_id: raise HTTPException(403,"Private submission")
    if user.role=="teacher":
        a=db.get(Assignment,s.assignment_id)
        if not a or a.created_by!=user.user_id: raise HTTPException(403,"Private submission")
    return s

@router.get("/submissions/{submission_id}/download")
def download(submission_id:int,db:Session=Depends(get_db),user=Depends(current_user)):
    s=db.get(Submission,submission_id)
    if not s: raise HTTPException(404,"Submission not found")
    if user.role=="student" and s.student_id!=user.user_id: raise HTTPException(403,"Forbidden")
    if user.role=="teacher":
        a=db.get(Assignment,s.assignment_id)
        if not a or a.created_by!=user.user_id: raise HTTPException(403,"Forbidden")
    data=read_file(s.storage_path)
    return Response(content=data,media_type="application/octet-stream",headers={"Content-Disposition":f'attachment; filename="{s.file_name}"'})

@router.post("/submissions/{submission_id}/grade")
def grade(submission_id:int,data:GradeIn,db:Session=Depends(get_db),user=Depends(require_role("teacher"))):
    s=db.get(Submission,submission_id)
    if not s: raise HTTPException(404,"Submission not found")
    a=db.get(Assignment,s.assignment_id)
    if not a or a.created_by!=user.user_id: raise HTTPException(403,"Not permitted")
    if data.marks>a.max_marks: raise HTTPException(400,"Marks exceed maximum")
    s.marks=data.marks; s.feedback=data.feedback; s.graded_at=datetime.now(timezone.utc); s.submission_status="GRADED"
    db.commit(); db.refresh(s); return s

@router.get("/submissions/{submission_id}/feedback")
def feedback(submission_id:int,db:Session=Depends(get_db),user=Depends(current_user)):
    s=db.get(Submission,submission_id)
    if not s or (user.role=="student" and s.student_id!=user.user_id): raise HTTPException(403,"Forbidden")
    return {"marks":s.marks,"feedback":s.feedback,"graded_at":s.graded_at,"status":s.submission_status}

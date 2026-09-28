from pathlib import Path
from fastapi import UploadFile, HTTPException
from ..core.config import settings

ALLOWED = {"pdf","docx","doc","zip","png","jpg","jpeg"}

def safe_extension(name):
    ext = Path(name).suffix.lower().lstrip(".")
    if ext not in ALLOWED: raise HTTPException(400, f"File type .{ext} is not allowed")
    return ext

async def save_upload(file: UploadFile, assignment_id: int, student_id: int, max_mb: int):
    ext=safe_extension(file.filename or "")
    content=await file.read()
    if len(content)>max_mb*1024*1024: raise HTTPException(413, f"File exceeds {max_mb} MB")
    if not content: raise HTTPException(400,"Empty file")
    if settings.STORAGE_PROVIDER=="local":
        folder=Path(settings.LOCAL_STORAGE_DIR)/f"assignment_{assignment_id}"/f"student_{student_id}"
        folder.mkdir(parents=True,exist_ok=True)
        target=folder/(f"submission_{student_id}_{Path(file.filename).stem}.{ext}")
        target.write_bytes(content)
        return str(target), None
    from supabase import create_client
    sb=create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)
    path=f"assignment_{assignment_id}/student_{student_id}/submission_{student_id}_{Path(file.filename).stem}.{ext}"
    sb.storage.from_(settings.SUPABASE_STORAGE_BUCKET).upload(path, content, {"upsert":"true","content-type":file.content_type or "application/octet-stream"})
    return path, None

def read_file(path):
    if settings.STORAGE_PROVIDER=="local":
        p=Path(path)
        if not p.exists(): raise HTTPException(404,"File not found")
        return p.read_bytes()
    from supabase import create_client
    sb=create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)
    return sb.storage.from_(settings.SUPABASE_STORAGE_BUCKET).download(path)

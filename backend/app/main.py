from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .core.db import Base, engine
from .api import auth,courses,assignments,submissions

Path(settings.LOCAL_STORAGE_DIR).mkdir(parents=True,exist_ok=True)
Base.metadata.create_all(bind=engine)
app=FastAPI(title=settings.APP_NAME,version="1.0.0",description="Cloud-oriented assignment submission and feedback portal")
app.add_middleware(CORSMiddleware,allow_origins=settings.CORS_ORIGINS,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.include_router(auth.router); app.include_router(courses.router); app.include_router(assignments.router); app.include_router(submissions.router)

@app.get("/health")
def health(): return {"status":"ok","environment":settings.ENVIRONMENT,"storage":settings.STORAGE_PROVIDER,"database":settings.DATABASE_URL.split(":")[0]}

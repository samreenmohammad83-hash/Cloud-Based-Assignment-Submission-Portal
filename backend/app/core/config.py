import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME = os.getenv("APP_NAME", "Cloud Assignment Portal")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "local")
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./portal.db")
    CORS_ORIGINS = [x.strip() for x in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",") if x.strip()]
    AUTH_PROVIDER = os.getenv("AUTH_PROVIDER", "local")
    STORAGE_PROVIDER = os.getenv("STORAGE_PROVIDER", "local")
    LOCAL_STORAGE_DIR = os.getenv("LOCAL_STORAGE_DIR", "./uploads")
    MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "10"))
    ALLOW_LATE_SUBMISSIONS = os.getenv("ALLOW_LATE_SUBMISSIONS", "true").lower() == "true"
    SUPABASE_URL = os.getenv("SUPABASE_URL", "")
    SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")
    SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET", "")
    SUPABASE_STORAGE_BUCKET = os.getenv("SUPABASE_STORAGE_BUCKET", "submissions")

settings = Settings()

from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext
from ..core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password): return pwd_context.hash(password)
def verify_password(password, hashed): return pwd_context.verify(password, hashed)

def create_token(user_id, role, email):
    payload={"sub":str(user_id),"role":role,"email":email,"exp":datetime.now(timezone.utc)+timedelta(hours=8)}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

def decode_token(token): return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from ..core.db import get_db
from ..services.auth import decode_token

def db(): return Depends(get_db)

def current_user(authorization: str = Header(None), session: Session = Depends(get_db)):
    if not authorization or not authorization.lower().startswith("bearer "): raise HTTPException(401,"Missing bearer token")
    try: payload=decode_token(authorization.split(" ",1)[1])
    except Exception: raise HTTPException(401,"Invalid or expired token")
    from ..models import User
    user=session.get(User,int(payload["sub"]))
    if not user: raise HTTPException(401,"User not found")
    return user

def require_role(role):
    def checker(user=Depends(current_user)):
        if user.role!=role: raise HTTPException(403,"Insufficient permissions")
        return user
    return checker

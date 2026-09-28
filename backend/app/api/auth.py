from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.db import get_db
from ..models import User
from ..schemas.schemas import RegisterIn, LoginIn, TokenOut
from ..services.auth import hash_password, verify_password, create_token

router=APIRouter(prefix="/api", tags=["auth"])

@router.post("/register", response_model=TokenOut)
def register(data:RegisterIn, db:Session=Depends(get_db)):
    if db.query(User).filter(User.email==data.email).first(): raise HTTPException(409,"Email already registered")
    user=User(name=data.name,email=data.email,role=data.role,password_hash=hash_password(data.password))
    db.add(user); db.commit(); db.refresh(user)
    return {"access_token":create_token(user.user_id,user.role,user.email),"user":{"user_id":user.user_id,"name":user.name,"email":user.email,"role":user.role}}

@router.post("/login", response_model=TokenOut)
def login(data:LoginIn, db:Session=Depends(get_db)):
    user=db.query(User).filter(User.email==data.email).first()
    if not user or not verify_password(data.password,user.password_hash): raise HTTPException(401,"Invalid email or password")
    return {"access_token":create_token(user.user_id,user.role,user.email),"user":{"user_id":user.user_id,"name":user.name,"email":user.email,"role":user.role}}

@router.post("/logout")
def logout(): return {"message":"Logout is client-side token removal for the demo API"}

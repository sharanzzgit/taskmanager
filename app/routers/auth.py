from fastapi import APIRouter, Depends, HTTPException, status, Body, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.core.security import hash_password, verify_password, create_access_token, refresh_token, verify_access_token
from app.models.user import Users
from sqlalchemy import or_
from jose import JWTError
from app.core.limiter import limiter

router = APIRouter(prefix="/auth",tags=["auth"])

@router.post("/register", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_mail = db.query(Users).filter(Users.email==user.email).first()

    if existing_mail:
        raise HTTPException(
            status_code=400,
            detail="Email id already exists"
        )
    
    password = hash_password(user.password)
    new_user = Users(username = user.username, email=user.email, hashed_password = password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
@limiter.limit("5/minute")
def login(request:Request,form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Users).filter(or_(Users.email == form_data.username,Users.username == form_data.username)).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": str(user.id)})
    refresh = refresh_token({"sub":str(user.id)})
    return {"access_token": token, "refresh_token": refresh, "token_type": "bearer"}

@router.post("/refresh")
def refresh(token: str = Body(..., embed=True)):
    try:
        payload = verify_access_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        new_token = create_access_token({"sub": user_id})
        return {"access_token": new_token, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
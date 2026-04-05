from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from jose import JWTError
from sqlalchemy.orm import Session
from app.core.security import verify_access_token
from app.models.user import Users
from app.core.database import get_db

def get_current_user(token:str = Depends(OAuth2PasswordBearer(tokenUrl="auth/login")), db: Session=Depends(get_db)):
    try:
        payload = verify_access_token(token)
        user_id = payload.get("sub")
        user = db.query(Users).filter(Users.id==user_id).first()
        if not user: raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

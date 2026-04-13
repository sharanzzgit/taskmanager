from app.config import settings
from passlib.context import CryptContext
from jose import jwt 
from datetime import datetime, timedelta

pwd = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password):
    hashed = pwd.hash(password)
    return hashed 

def verify_password(plain, hashed):
    is_valid = pwd.verify(plain,hashed)
    return is_valid

def create_access_token(data):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode,settings.SECRET_KEY,algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_access_token(token):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    return payload

def refresh_token(data):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode,settings.SECRET_KEY,algorithm=settings.ALGORITHM)
    return encoded_jwt
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str 
    email: EmailStr 

class UserCreate(UserBase):
    password: str = Field(min_length=8)

class UserResponse(UserBase):
    id: int
    is_active: bool 
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(UserBase):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
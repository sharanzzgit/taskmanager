from fastapi import Depends,HTTPException,APIRouter
from sqlalchemy.orm import Session
from app.models.user import Users
from app.schemas.user import UserUpdate,UserResponse
from app.core.database import get_db
from app.dependencies import get_current_user

router = APIRouter(prefix='/users',tags=['users'])

@router.get('/me', response_model=UserResponse)
def user_profile(user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    return user

@router.put('/me', response_model=UserResponse)
def update_profile(user_update: UserUpdate, user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    
    for key,value in user_update.model_dump(exclude_unset=True).items():
        setattr(user,key,value)
    
    db.commit()
    db.refresh(user)
    return user

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.core.security import hash_password, verify_password, create_access_token
from app.models.task import Tasks
from app.models.user import Users
from app.dependencies import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    user: Users = Depends(get_current_user),
):
    new_task = Tasks(
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        owner_id=user.id,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.get("/", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db), user: Users = Depends(get_current_user)):
    tasks = list(db.query(Tasks).filter(Tasks.owner_id == user.id))
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int, db: Session = Depends(get_db), user: Users = Depends(get_current_user)
):
    task = (
        db.query(Tasks).filter(Tasks.owner_id == user.id, Tasks.id == task_id).first()
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    user: Users = Depends(get_current_user),
):
    task = (
        db.query(Tasks).filter(Tasks.owner_id == user.id, Tasks.id == task_id).first()
    )

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task_update.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}")
def delete_task(
    task_id: int, db: Session = Depends(get_db), user: Users = Depends(get_current_user)
):
    task = (
        db.query(Tasks).filter(Tasks.owner_id == user.id, Tasks.id == task_id).first()
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"Message": "Task Deleted successfully"}

from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.core.security import hash_password, verify_password, create_access_token
from app.models.task import Tasks
from app.models.user import Users
from app.dependencies import get_current_user
from sqlalchemy import or_, func
from app.core.email import send_task_email
from app.core.cache import get_cache,set_cache
from app.core.limiter import limiter

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse)
@limiter.limit("10/minute")
def create_task(
    request: Request,
    task: TaskCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    user: Users = Depends(get_current_user),
):
    new_task = Tasks(
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        owner_id=user.id,
        due_date=task.due_date,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    background_tasks.add_task(send_task_email, user.email, new_task.title)
    return new_task


@router.get("/", response_model=list[TaskResponse])
def get_tasks(
    db: Session = Depends(get_db),
    user: Users = Depends(get_current_user),
    skip: int = 0,
    limit: int = 10,
    status: str | None = None,
    priority: str | None = None,
    search: str | None = None,
    due_today: bool = False,
    overdue: bool = False,
):
    cache_key = f"tasks:{user.id}:{skip}:{limit}:{status}:{priority}:{search}:{due_today}:{overdue}"
    
    cached = get_cache(cache_key)
    if cached:
        return cached
    
    query = db.query(Tasks).filter(Tasks.owner_id == user.id, Tasks.is_deleted == False)

    if status:
        query = query.filter(Tasks.status == status)
    if priority:
        query = query.filter(Tasks.priority == priority)
    if search:
        query = query.filter(
            or_(Tasks.title.ilike(f"%{search}%"), Tasks.description.ilike(f"%{search}"))
        )
    if due_today:
        query = query.filter(func.date(Tasks.due_date) == date.today())
    if overdue:
        query = query.filter(func.date(Tasks.due_date) < date.today())
    tasks = query.offset(skip).limit(limit).all()
    # Correct - Pydantic handles serialization properly
    set_cache(cache_key, [TaskResponse.model_validate(task).model_dump(mode="json") for task in tasks])
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int, db: Session = Depends(get_db), user: Users = Depends(get_current_user)
):
    task = (
        db.query(Tasks)
        .filter(
            Tasks.owner_id == user.id, Tasks.id == task_id, Tasks.is_deleted == False
        )
        .first()
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
    task.is_deleted = True
    db.commit()
    return {"Message": "Task Deleted successfully"}

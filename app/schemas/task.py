from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from enum import Enum
from typing import Optional

class Status(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

class Priority(str, Enum):
    low = "low"
    med = "medium"
    high = "high"

class TaskBase(BaseModel):
    title: str
    description: Optional[str]=None
    status: Status = Status.pending
    priority: Priority = Priority.low
    due_date: Optional[datetime]=None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str]=None
    status: Optional[Status] = None
    priority: Optional[Priority] = None
    due_date: Optional[datetime]=None

class TaskResponse(TaskBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
from app.core.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
import datetime

class Tasks(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(
        Enum("pending","in_progress","completed", name="task_status"),
        nullable=False,
        default="pending")
    
    priority = Column(
        Enum("low","medium","high", name="task_priority"),
        nullable=False,
        default="low"
    )
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'))
    author = relationship('Users', back_populates='tasks')

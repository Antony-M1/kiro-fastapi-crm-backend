from sqlalchemy import Column, Integer, String, Enum, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base
import enum

class TaskType(str, enum.Enum):
    CALL = "Call"
    EMAIL = "Email"
    MEETING = "Meeting"
    FOLLOW_UP = "Follow-up"

class TaskStatus(str, enum.Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class Task(Base):
    __tablename__ = "tasks"
    
    task_id = Column(Integer, primary_key=True, index=True)
    reference_doctype = Column(String, nullable=False)
    reference_id = Column(Integer, nullable=False)
    task_type = Column(Enum(TaskType), nullable=False)
    due_date = Column(Date, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
    assigned_to = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

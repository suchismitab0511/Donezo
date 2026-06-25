from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    firebase_uid: str = Field(unique=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    active_hours: Optional[str] = Field(default="09:00-21:00")
    coins: int = Field(default=0)
    current_streak: int = Field(default=0)
    longest_streak: int = Field(default=0)
    last_completed_at: Optional[datetime] = Field(default=None)

class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    title: str
    deadline: datetime
    status: str = Field(default="pending")
    risk_score: Optional[float] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Subtask(SQLModel, table=True):
    __tablename__ = "subtasks"
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="tasks.id")
    title: str
    est_minutes: int
    status: str = Field(default="pending")
    order: int
    completed_at: Optional[datetime] = Field(default=None)

class Schedule(SQLModel, table=True):
    __tablename__ = "schedules"
    id: Optional[int] = Field(default=None, primary_key=True)
    subtask_id: int = Field(foreign_key="subtasks.id")
    start_time: datetime
    end_time: datetime
    gcal_event_id: Optional[str] = Field(default=None)
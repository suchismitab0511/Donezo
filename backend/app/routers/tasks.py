from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from datetime import datetime
from app.database import get_session
from app.firebase import verify_firebase_token
from app.models.models import User, Task
from pydantic import BaseModel

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

class TaskCreate(BaseModel):
    title: str
    deadline: datetime

def get_current_user(
    session: Session = Depends(get_session),
    token_data: dict = Depends(verify_firebase_token)
) -> User:
    user = session.exec(
        select(User).where(User.firebase_uid == token_data["uid"])
    ).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found. Login first.")
    return user

@router.post("/")
def create_task(
    task_data: TaskCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    task = Task(
        user_id=current_user.id,
        title=task_data.title,
        deadline=task_data.deadline
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.get("/")
def get_tasks(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    tasks = session.exec(
        select(Task).where(Task.user_id == current_user.id)
    ).all()
    return tasks
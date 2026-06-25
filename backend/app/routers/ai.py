from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from datetime import datetime
from app.database import get_session
from app.firebase import verify_firebase_token
from app.models.models import User, Task, Subtask
from app.gemini import decompose_task, calculate_risk_score

router = APIRouter(prefix="/api/ai", tags=["ai"])

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

@router.post("/decompose/{task_id}")
def decompose(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Get task
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your task")

    # Call Gemini to decompose
    deadline_str = task.deadline.strftime("%Y-%m-%d %H:%M")
    subtasks_data = decompose_task(task.title, deadline_str)

    # Save subtasks to DB
    subtasks = []
    total_minutes = 0
    for item in subtasks_data:
        subtask = Subtask(
            task_id=task.id,
            title=item["title"],
            est_minutes=item["est_minutes"],
            order=item["order"]
        )
        session.add(subtask)
        subtasks.append(subtask)
        total_minutes += item["est_minutes"]

    # Calculate risk score
    risk_score = calculate_risk_score(task.title, deadline_str, total_minutes)
    task.risk_score = risk_score

    session.add(task)
    session.commit()

    return {
        "task_id": task.id,
        "risk_score": risk_score,
        "total_minutes": total_minutes,
        "subtasks": subtasks_data
    }
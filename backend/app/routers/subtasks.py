from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from datetime import datetime
from app.database import get_session
from app.firebase import verify_firebase_token
from app.models.models import User, Task, Subtask

router = APIRouter(prefix="/api/subtasks", tags=["subtasks"])

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

@router.patch("/{subtask_id}")
def complete_subtask(
    subtask_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Get subtask
    subtask = session.get(Subtask, subtask_id)
    if not subtask:
        raise HTTPException(status_code=404, detail="Subtask not found")

    # Verify ownership via task
    task = session.get(Task, subtask.task_id)
    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your subtask")

    if subtask.status == "completed":
        raise HTTPException(status_code=400, detail="Subtask already completed")

    # Mark complete
    now = datetime.utcnow()
    subtask.status = "completed"
    subtask.completed_at = now

    # Coins logic
    coins_earned = 10
    if task.deadline and now <= task.deadline:
        coins_earned += 25  # on-time bonus

    current_user.coins += coins_earned

    # Streak logic
    if current_user.last_completed_at:
        diff = (now.date() - current_user.last_completed_at.date()).days
        if diff == 1:
            current_user.current_streak += 1
        elif diff > 1:
            current_user.current_streak = 1
        # diff == 0 means same day, streak stays
    else:
        current_user.current_streak = 1

    if current_user.current_streak > current_user.longest_streak:
        current_user.longest_streak = current_user.current_streak

    current_user.last_completed_at = now

    session.add(subtask)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return {
        "message": "Subtask completed",
        "coins_earned": coins_earned,
        "total_coins": current_user.coins,
        "current_streak": current_user.current_streak,
        "longest_streak": current_user.longest_streak
    }
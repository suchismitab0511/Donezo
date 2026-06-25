from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.firebase import verify_firebase_token
from app.models.models import User

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/login")
def login(
    session: Session = Depends(get_session),
    token_data: dict = Depends(verify_firebase_token)
):
    firebase_uid = token_data["uid"]
    email = token_data.get("email", "")

    # Check if user already exists
    user = session.exec(select(User).where(User.firebase_uid == firebase_uid)).first()

    if not user:
        # First time login → create user in our DB
        user = User(email=email, firebase_uid=firebase_uid)
        session.add(user)
        session.commit()
        session.refresh(user)

    return {
        "id": user.id,
        "email": user.email,
        "coins": user.coins,
        "current_streak": user.current_streak,
        "longest_streak": user.longest_streak
    }
from fastapi import APIRouter
from sqlmodel import Session, select, func
from models import User, UserAchievement
from database import engine

router = APIRouter()

@router.get("/leaderboard")
def get_leaderboard():
    with Session(engine) as session:
        users = session.exec(select(User).order_by(User.xp.desc())).all()

        result = []
        for rank, user in enumerate(users, 1):
            badge_count = session.exec(
                select(func.count()).select_from(UserAchievement).where(
                    UserAchievement.user_id == user.id
                )
            ).one()
            result.append({
                "rank": rank,
                "id": user.id,
                "username": user.username,
                "avatar": user.avatar,
                "xp": user.xp,
                "level": user.level,
                "current_streak": user.current_streak,
                "total_completed": user.total_completed,
                "badge_count": badge_count,
            })

        return result

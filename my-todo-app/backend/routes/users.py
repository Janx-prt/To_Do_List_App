from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from models import User, UserUpdate, Todo, UserAchievement
from database import engine
from gamification import ACHIEVEMENTS, LEVEL_THRESHOLDS, calc_level

router = APIRouter()

# GET /users — retrieve all users from the database and return them as a list
@router.get("/users")
def list_users():
    with Session(engine) as session:
        return session.exec(select(User)).all()
    
@router.post("/users")
def create_user(user: User):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    
@router.get("/users/{user_id}")
def get_user(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if user:
            return user
        raise HTTPException(status_code=404, detail="User not found")

@router.patch("/users/{user_id}")
def update_user(user_id: int, user_update: UserUpdate):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user_update.avatar is not None:
            user.avatar = user_update.avatar
        session.commit()
        session.refresh(user)
        return user

@router.get("/users/{user_id}/todos")
def get_user_todos(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return session.exec(select(Todo).where(Todo.user_id == user_id)).all()

@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if user:
            todos = session.exec(select(Todo).where(Todo.user_id == user_id)).all()
            for todo in todos:
                todo.user_id = None  # Unassign todos from the user instead of deleting them
            session.delete(user)
            session.commit()
            return {"ok": True}
        raise HTTPException(status_code=404, detail="User not found")

@router.get("/users/{user_id}/stats")
def get_user_stats(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Calculate level progress
        current_threshold = LEVEL_THRESHOLDS[user.level - 1] if user.level - 1 < len(LEVEL_THRESHOLDS) else LEVEL_THRESHOLDS[-1]
        next_threshold = LEVEL_THRESHOLDS[user.level] if user.level < len(LEVEL_THRESHOLDS) else LEVEL_THRESHOLDS[-1]
        xp_in_level = user.xp - current_threshold
        xp_for_level = next_threshold - current_threshold if next_threshold > current_threshold else 1

        # Get user achievements
        user_achievements = session.exec(
            select(UserAchievement).where(UserAchievement.user_id == user_id)
        ).all()
        unlocked_keys = {ua.achievement_key: ua.unlocked_at.isoformat() for ua in user_achievements}

        achievements = []
        for key, info in ACHIEVEMENTS.items():
            achievements.append({
                "key": key,
                **info,
                "unlocked": key in unlocked_keys,
                "unlocked_at": unlocked_keys.get(key),
            })

        return {
            "xp": user.xp,
            "level": user.level,
            "xp_in_level": xp_in_level,
            "xp_for_level": xp_for_level,
            "current_streak": user.current_streak,
            "max_streak": user.max_streak,
            "total_completed": user.total_completed,
            "achievements": achievements,
        }

@router.get("/achievements")
def get_achievements():
    return [{"key": key, **info} for key, info in ACHIEVEMENTS.items()]
    

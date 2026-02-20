from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from models import User, UserUpdate, Todo
from main import engine

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
            session.delete(user)
            session.commit()
            return {"ok": True}
        raise HTTPException(status_code=404, detail="User not found")
    

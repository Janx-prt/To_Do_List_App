from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select, func
from pydantic import BaseModel
from typing import List
from models import Todo, TodoUpdate
from main import engine

router = APIRouter()

class ReorderItem(BaseModel):
    id: int
    position: int

# Health-check endpoint — returns a simple message to confirm the API is running
@router.get("/")
def read_root():
    return {"message": "Todo API is running!"}

# GET /todos — retrieve all todos from the database and return them as a list
@router.get("/todos")
def list_todos():
    with Session(engine) as session:
        return session.exec(select(Todo)).all()

# POST /todos — create a new todo, save it to the database, and return the created record
@router.post("/todos")
def create_todo(todo: Todo):
    with Session(engine) as session:
        count = session.exec(select(func.count()).select_from(Todo)).one()
        todo.position = count 
        session.add(todo)
        session.commit()
        session.refresh(todo)  # refresh to get the auto-generated id and defaults
        return todo

@router.put("/todos/reorder")
def reorder_todos(items: List[ReorderItem]):
    with Session(engine) as session:
        for item in items:
            todo = session.get(Todo, item.id)
            if todo:
                todo.position = item.position
        session.commit()
        return {"ok": True}

# PATCH /todos/{todo_id} — partially update an existing todo's fields (title, category, completed)
@router.patch("/todos/{todo_id}")
def update_todo(todo_id: int, todo_update: TodoUpdate):
    with Session(engine) as session:
        todo = session.get(Todo, todo_id)
        if todo:
            # Only overwrite fields that were actually provided in the request
            todo.completed = todo_update.completed if todo_update.completed is not None else todo.completed
            todo.title = todo_update.title if todo_update.title is not None else todo.title
            todo.category = todo_update.category if todo_update.category is not None else todo.category
            todo.priority = todo_update.priority if todo_update.priority is not None else todo.priority
            todo.due_date = todo_update.due_date if todo_update.due_date is not None else todo.due_date
            if todo_update.user_id is not None:
                todo.user_id = todo_update.user_id
            session.commit()
            session.refresh(todo)
            return todo
        raise HTTPException(status_code=404, detail="Todo not found")

# DELETE /todos/{todo_id} — remove a todo from the database by its id
@router.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    with Session(engine) as session:
        todo = session.get(Todo, todo_id)
        if todo:
            session.delete(todo)
            session.commit()
            return {"ok": True}
        raise HTTPException(status_code=404, detail="Todo not found")
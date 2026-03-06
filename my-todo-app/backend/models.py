from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    avatar: str = "⚔️"
    xp: int = 0
    level: int = 1
    current_streak: int = 0
    max_streak: int = 0
    last_completion_date: Optional[str] = None
    total_completed: int = 0

class UserUpdate(SQLModel):
    avatar: Optional[str] = Field(default=None)

class UserAchievement(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    achievement_key: str
    unlocked_at: datetime = Field(default_factory=datetime.utcnow)

# Todo — the main database table model representing a single todo item
class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # Auto-incremented primary key
    title: str                                                  # The todo's text content
    category: str = "Personal"                                  # Category label: Work, Personal, or Urgent
    completed: bool = False                                     # Whether the todo is done
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")  # Reference to the user who created the todo
    priority: str = "Low"  # Priority level: Low, Medium, or High
    due_date: Optional[datetime] = None  # Optional due date for the todo item
    position: int = 0  # Position for ordering todos within a category
    completed_at: Optional[datetime] = None

# TodoUpdate — a schema for PATCH requests; all fields are optional so only provided fields get updated
class TodoUpdate(SQLModel):
    title: Optional[str] = Field(default=None)
    category: Optional[str] = Field(default=None)
    completed: Optional[bool] = Field(default=None)
    user_id: Optional[int] = Field(default=None)
    priority: Optional[str] = Field(default=None)
    due_date: Optional[datetime] = Field(default=None)
    position: Optional[int] = Field(default=None)

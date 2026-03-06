from sqlmodel import create_engine
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/todos")
engine = create_engine(DATABASE_URL)

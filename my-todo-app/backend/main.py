from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from database import engine
from routes.todos import router as todos_router
from routes.users import router as users_router
from routes.leaderboard import router as leaderboard_router

# Create the FastAPI application instance
app = FastAPI()

# Configure CORS to allow the Vite frontend (port 5174) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# On app startup, create all tables defined by SQLModel classes if they don't exist yet
@app.on_event("startup")
def create_tables():
    SQLModel.metadata.create_all(engine)

# Connect route files
app.include_router(todos_router)
app.include_router(users_router)
app.include_router(leaderboard_router)

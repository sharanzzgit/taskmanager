from fastapi import FastAPI
from app.core.database import Base, engine
from app.models import *
from app.routers import auth, tasks, users
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(users.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

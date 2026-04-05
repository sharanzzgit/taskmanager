from fastapi import FastAPI
from app.core.database import Base,engine
from app.models import *
from app.routers import auth
from fastapi import FastAPI

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
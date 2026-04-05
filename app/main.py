from app.core.database import Base,engine
from app.models import *
from fastapi import FastAPI

app = FastAPI()
Base.metadata.create_all(bind=engine)
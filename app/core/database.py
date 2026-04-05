from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import datetime 
Base = declarative_base()
engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(bind=engine,autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

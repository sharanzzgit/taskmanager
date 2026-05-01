from app.models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import get_db, Base
from app.main import app
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def auth_token(client):
    
    client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@test.com",
        "password": "test1234"
    })
    
    response = client.post("/auth/login", data={
        "username": "test@test.com",
        "password": "test1234"
    })
    return response.json()["access_token"]

@pytest.fixture(autouse=True)
def mock_email():
    with patch("app.core.email.send_task_email", new_callable=AsyncMock) as mock:
        yield mock
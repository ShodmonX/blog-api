# tests/conftest.py
import pytest
import os
import sys
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
import app.dependencies
from app import models, utils, database
import uuid

# Direktoriya yo‘lini qo‘shish
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Test ma'lumotlar bazasi
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# app.models ni aniq import qilish
import app.models  # Bu User va Post modellari Base ga ro‘yxatdan o‘tishini ta'minlaydi

# get_db override
def override_get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

from app.main import app

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def db_session():
    # Har bir test uchun jadvallarni tozalash va qayta yaratish
    Base.metadata.drop_all(bind=database.engine)
    Base.metadata.create_all(bind=database.engine)
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(db_session):
    print("Created tables:", Base.metadata.tables.keys())  # Debug uchun
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function")
def test_user(db_session):
    user = models.User(
        email=f"test_{uuid.uuid4().hex}@example.com",
        username=f"user_{uuid.uuid4().hex[:5]}",
        hashed_password=utils.hash_password("test123")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

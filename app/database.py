from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()

class Base(DeclarativeBase):
    pass

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./blog.db")
engine = create_engine(url=str(SQLALCHEMY_DATABASE_URL))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
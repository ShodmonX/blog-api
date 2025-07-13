from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from .database import Base, engine, get_db
from .routers import users, auth, posts
import os

app = FastAPI(title="Blog REST API", version="0.1.0")

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(posts.router)

if os.getenv("ENV") != "test":
    Base.metadata.create_all(bind=engine)

@app.get("/", tags=["Health"])
async def root():
    return {"status": "API is running"}

@app.get("/db-check", tags=["Health"])
async def db_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"db": "ok"}
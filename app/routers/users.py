from fastapi import APIRouter, Depends
from typing import Annotated

from app.auth.dependencies import get_current_user


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/")
async def get_users():
    return {"message": "Users"}

@router.get("/me/")
async def get_me(user: Annotated[dict, Depends(get_current_user)]):
    return {"message": "Me", "user": user}
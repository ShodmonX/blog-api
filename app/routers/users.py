from fastapi import APIRouter, Depends
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.schemas.user import UserOut, UserUpdate
from app.models.user import User
from app.db.session import get_db
from app.crud.user import update_user


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/")
async def get_users():
    return {"message": "Users"}

@router.get("/me", response_model=UserOut)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserOut)
async def update_me(
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await update_user(db=db, user_db=current_user, user_in=user_in)
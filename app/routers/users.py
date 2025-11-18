from fastapi import APIRouter, Depends
from typing import Annotated

from app.auth.dependencies import get_current_user
from app.schemas.user import UserOut
from app.models.user import User


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/")
async def get_users():
    return {"message": "Users"}

@router.get("/me", response_model=UserOut)
def read_users_me(current_user: User = Depends(get_current_user)):
    response = UserOut(id=current_user.id, email=current_user.email, username=current_user.username)
    return response
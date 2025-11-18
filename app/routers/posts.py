from fastapi import APIRouter, Depends, Query, status, Body
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Annotated

from app.db.session import get_db
from app.crud.post import get_posts, create_post
from app.schemas.post import PostOut, PostCreate
from app.models.user import User
from app.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=list[PostOut])
async def get_all_posts(
    db: AsyncSession = Depends(get_db),
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=0)] = 100
):
    return await get_posts(db=db, skip=skip, limit=limit)

@router.post("/", response_model=PostOut, status_code=status.HTTP_201_CREATED)
async def add_new_post(
    post: Annotated[PostCreate, Body()],
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db)
):
    return await create_post(db=db, post=post, owner_id=current_user.id)

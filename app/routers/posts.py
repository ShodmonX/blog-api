from fastapi import APIRouter, Depends, Query, status, Body, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Annotated

from app.db.session import get_db
from app.crud.post import get_posts, create_post, get_post, update_post, delete_post
from app.schemas.post import PostOut, PostCreate, PostUpdate
from app.models.user import User
from app.models.post import Post
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

@router.get("/{post_id}", response_model=PostOut)
async def get_post_by_id(post_id: int, db: AsyncSession = Depends(get_db)):
    post = await get_post(db=db, post_id=post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    return post

@router.put("/{post_id}", response_model=PostOut)
async def update_post_by_id(
    post_id: int,
    post_in: PostUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = await get_post(db=db, post_id=post_id)
    if not post:
        raise HTTPException(404, "Post not found")
    if post.owner_id != current_user.id:
        raise HTTPException(403, "Not authorized")
    return await update_post(db=db, post_db=post, post_in=post_in)

@router.delete("/{post_id}", status_code=204)
async def delete_post_by_id(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = await get_post(db=db, post_id=post_id)
    if not post:
        raise HTTPException(404, "Post not found")
    if post.owner_id != current_user.id:
        raise HTTPException(403, "Not authorized")
    await delete_post(db=db, post_db=post)
    return {"message": "Post deleted"}

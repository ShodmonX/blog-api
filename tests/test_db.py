from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from httpx import AsyncClient
from fastapi import HTTPException
import pytest

from app.crud.user import get_user, get_user_with_username, create_user, update_user
from app.crud.post import get_post, get_posts, create_post, update_post, delete_post
from app.schemas.user import UserUpdate
from app.schemas.post import PostCreate, PostUpdate

async def test_db_session(test_db: AsyncSession):
    assert test_db
    assert isinstance(test_db, AsyncSession)

async def test_create_success(client: AsyncClient, test_db: AsyncSession):
    user = await create_user(
        db=test_db,
        username="test_user",
        email="test_email",
        hashed_password="test_hashed_password"
    )
    assert user
    assert user.username == "test_user"
    assert user.email == "test_email"
    assert user.hashed_password == "test_hashed_password"

    user_db = await get_user(test_db, "test_email")
    assert user_db
    assert user_db.username == "test_user"
    assert user_db.email == "test_email"
    assert user_db.hashed_password == "test_hashed_password"

    user_db = await get_user_with_username(test_db, "test_user")
    assert user_db
    assert user_db.username == "test_user"
    assert user_db.email == "test_email"
    assert user_db.hashed_password == "test_hashed_password"

    updated_user = await update_user(test_db, user, UserUpdate(username="test_user_updated"))
    assert updated_user
    assert updated_user.username == "test_user_updated"

    post = await create_post(
        db=test_db,
        post=PostCreate(title="test_title", content="test_content"),
        owner_id=user.id
    )
    assert post
    assert post.title == "test_title"
    assert post.content == "test_content"
    assert post.owner_id == user.id

    post_db = await get_post(test_db, post.id)
    assert post_db
    assert post_db.title == "test_title"
    assert post_db.content == "test_content"
    assert post_db.owner_id == user.id

    posts = await get_posts(test_db)
    assert posts
    assert len(posts) == 1

    updated_post = await update_post(
        db=test_db,
        post_db=post,
        post_in=PostUpdate(title="test_title_updated")
    )
    assert updated_post
    assert updated_post.title == "test_title_updated"

    await delete_post(test_db, post)
    posts = await get_posts(test_db)
    assert posts == []
    assert len(posts) == 0

async def test_create_fail(client: AsyncClient, test_db: AsyncSession):
    user1 = await create_user(
        db=test_db,
        username="test_user",
        email="test_email",
        hashed_password="test_hashed_password"
    )
    user2 = await create_user(
        db=test_db,
        username="test_user2",
        email="test_email2",
        hashed_password="test_hashed_password"
    )

    with pytest.raises(IntegrityError):
        await create_user(
            db=test_db,
            username="test_user",
            email="test_email2",
            hashed_password="test_hashed_password"
        )

    with pytest.raises(IntegrityError):
        await create_user(
            db=test_db,
            username="test_user2",
            email="test_email",
            hashed_password="test_hashed_password"
        )

    user_db = await get_user(test_db, "test_email_none")
    assert user_db is None

    user_db = await get_user_with_username(test_db, "test_user_none")
    assert user_db is None


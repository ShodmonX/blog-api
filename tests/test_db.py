from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from httpx import AsyncClient
import pytest

from app.crud.user import get_user, get_user_with_username, create_user

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
    await test_db.commit()
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

async def test_create_fail(client: AsyncClient, test_db: AsyncSession):
    user = await create_user(
        db=test_db,
        username="test_user",
        email="test_email",
        hashed_password="test_hashed_password"
    )
    await test_db.commit()

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

    user_db = await get_user(test_db, "test_email2")
    assert user_db is None

    user_db = await get_user_with_username(test_db, "test_user2")
    assert user_db is None

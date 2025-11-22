from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException

from app.models.user import User
from app.schemas.user import UserUpdate


async def get_user(db: AsyncSession, email: str):
    try:
        stm = select(User).where(User.email == email)

        result = await db.execute(stm)
        return result.scalar_one_or_none()
    except Exception as e:
        await db.rollback()
        raise e

async def get_user_with_username(db: AsyncSession, username: str):
    stm = select(User).where(User.username == username)

    result = await db.execute(stm)
    return result.scalars().first()

async def create_user(db: AsyncSession, username: str, email: str, hashed_password: str):
    user = User(
        username=username,
        email=email,
        hashed_password=hashed_password
    )
    db.add(user)
    try:
        await db.commit()
        await db.refresh(user)
        return user
    except Exception as e:
        await db.rollback()
        raise e
    
async def update_user(db: AsyncSession, user_db: User, user_in: UserUpdate):
    update_data = user_in.model_dump(exclude_unset=True)
    if "username" in update_data:
        user_by_username = await get_user_with_username(db, update_data["username"])
        if user_by_username and user_by_username.id != user_db.id:
            raise HTTPException(400, "User already exists with this username")
    for key, value in update_data.items():
        setattr(user_db, key, value)
    try:
        await db.commit()
        await db.refresh(user_db)
        return user_db
    except Exception as e:
        await db.rollback()
        raise e
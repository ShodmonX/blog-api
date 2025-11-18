from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


async def get_user(db: AsyncSession, email: str):
    stm = select(User).where(User.email == email)

    result = await db.execute(stm)
    return result.scalars().first()

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
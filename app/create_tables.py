from .db.base import Base, engine
from .models.user import User
from .models.post import Post


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(
            User.__table__.insert(),
            [
                {
                    "username": "ShodmonX",
                    "email": "0VHfU@example.com",
                    "hashed_password": "123456"
                }
            ]
        )
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.post import Post
from app.schemas.post import PostCreate


async def get_posts(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Post).offset(skip).limit(limit))
    return result.scalars().all()

async def create_post(db: AsyncSession, post: PostCreate, owner_id: int):
    db_post = Post(**post.model_dump(), owner_id=owner_id)
    db.add(db_post)
    try:
        await db.commit()
        await db.refresh(db_post)
        return db_post
    except Exception as e:
        await db.rollback()
        raise e
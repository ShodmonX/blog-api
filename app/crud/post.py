from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate


async def get_posts(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Post).offset(skip).limit(limit))
    return result.scalars().all()

async def get_post(db: AsyncSession, post_id: int):
    result = await db.execute(select(Post).where(Post.id == post_id))
    return result.scalars().first()

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
    
async def update_post(db: AsyncSession, post_db: Post, post_in: PostUpdate):
    update_data = post_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(post_db, key, value)
    try:
        await db.commit()
        await db.refresh(post_db)
        return post_db
    except Exception as e:
        await db.rollback()
        raise e

async def delete_post(db: AsyncSession, post_db: Post):
    try:
        await db.delete(post_db)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e
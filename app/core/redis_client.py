from typing import AsyncIterator, Optional
from redis.asyncio import Redis
from app.core.config import settings

redis: Redis = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=getattr(settings, "REDIS_DB", 0),
    decode_responses=True,
)

async def save_refresh_token(user_id: int, token: str, expires_seconds: int) -> None:
    await redis.set(token, user_id, ex=expires_seconds)

async def get_user_email_by_refresh_token(token: str) -> Optional[str]:
    return await redis.get(token)

async def delete_refresh_token(token: str) -> int:
    return await redis.delete(token)

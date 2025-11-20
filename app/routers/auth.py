from fastapi import APIRouter, Depends, HTTPException, Response, Cookie

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserCreate, UserLogin, UserOut
from app.crud.user import get_user, create_user, get_user_with_username
from app.db.session import get_db
from app.auth.utils import get_password_hash, verify_password, create_access_token, create_refresh_token
from app.core.redis_client import get_user_email_by_refresh_token, save_refresh_token, delete_refresh_token
from app.core.config import settings


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    user_db_email = await get_user(db, user.email)
    user_db_username = await get_user_with_username(db, user.username)

    if user_db_email:
        raise HTTPException(400, "User already exists with this email")
    
    if user_db_username:
        raise HTTPException(400, "User already exists with this username")

    user = await create_user(db, user.username, user.email, get_password_hash(user.password))
    return {"msg": "User created", "user": UserOut(id=user.id, username=user.username, email=user.email)}

@router.post("/login")
async def login(user: UserLogin, response: Response, db: AsyncSession = Depends(get_db)):
    db_user = await get_user(db, user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(401, "Invalid credentials")

    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email})

    await save_refresh_token(refresh_token, db_user.email, settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=not settings.DEBUG,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/refresh")
async def refresh(response: Response, refresh_token: str = Cookie(None)):
    if not refresh_token:
        raise HTTPException(401, "Refresh token not provided")
    email = await get_user_email_by_refresh_token(refresh_token)
    if not email:
        raise HTTPException(401, "Invalid or expired refresh token")

    await delete_refresh_token(refresh_token)

    new_access = create_access_token({"sub": email})
    new_refresh = create_refresh_token({"sub": email})
    
    await save_refresh_token(new_refresh, email)

    response.set_cookie(
        key="refresh_token",
        value=new_refresh,
        httponly=True,
        secure=not settings.DEBUG,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    return {"access_token": new_access, "token_type": "bearer"}

@router.post("/logout")
async def logout(response: Response, refresh_token: str = Cookie(None)):
    if not refresh_token:
        raise HTTPException(401, "Refresh token not provided")
    
    email = await get_user_email_by_refresh_token(refresh_token)
    if email:
        await delete_refresh_token(refresh_token)
    response.delete_cookie("refresh_token", samesite="lax")
    return {"msg": "Muvaffaqiyatli chiqildi"}

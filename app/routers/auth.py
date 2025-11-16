from fastapi import APIRouter

from app.schemas.user import UserCrate, UserLogin, UserOut


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.get("/")
async def get_auth():
    return {"message": "Auth"}

@router.post("/register-test/")
async def register_test(user: UserCrate):
    return {"message": "Validation successful", "user": user}

@router.post("/login-test/")
async def login_test(user: UserLogin):
    return {"message": "Validation successful", "user": user}


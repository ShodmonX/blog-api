from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from .. import models, schemas, database, utils, auth

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user or not utils.verify_password(user_credentials.password, str(user.hashed_password)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )

    access_token = auth.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}


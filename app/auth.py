from datetime import datetime, timedelta
from jose import JWTError, jwt

import os
from dotenv import load_dotenv

load_dotenv()

# Maxfiy kalit (real loyihada .env fayldan olasiz)
SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_ME_PLEASE")  # .env dan olingan bo'lishi kerak
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        return user_id
    except JWTError:
        raise credentials_exception
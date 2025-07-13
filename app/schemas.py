from pydantic import BaseModel, EmailStr, ConfigDict

# users
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str

    model_config = ConfigDict(from_attributes=True)

# tokens
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: int | None = None

# posts
class PostBase(BaseModel):
    title: str
    content: str

class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None

class PostCreate(PostBase):
    pass

class PostOut(PostBase):
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)
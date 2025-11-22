from pydantic import BaseModel, Field, EmailStr, field_validator


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

    @field_validator("email", mode="before")
    def validate_email(cls, value):
        if value is None:
            return value
        return value.strip().lower()

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)

    @field_validator("email", mode="before")
    def validate_email(cls, value):
        if value is None:
            return value
        return value.strip().lower()

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    profile_pic: str | None = None
    bio: str | None = None

class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=50)
    profile_pic: str | None = None
    bio: str | None = None
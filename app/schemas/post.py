from pydantic import BaseModel, ConfigDict


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostOut(PostBase):
    id: int
    owner_id: int
    
    model_config = ConfigDict(from_attributes=True)

class PostUpdate(PostBase):
    title: str | None = None
    content: str | None = None

    model_config = ConfigDict(from_attributes=True)
from pydantic import BaseModel

class UserBase(BaseModel):
    telegram_id: int
    username: str
    first_name: str
    last_name: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

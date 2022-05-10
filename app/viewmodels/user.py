from pydantic import BaseModel, Field, EmailStr


class UserModel(BaseModel):
    user_id: str = Field(...)
    username: str = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: EmailStr = Field(...)

from pydantic import BaseModel, Field, EmailStr


class UserDocument(BaseModel):
    user_id: str | None = None
    username: str = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

from pydantic import BaseModel, EmailStr, Field
from app.regex import password_regex
from app.config import settings


class SUserAuth(BaseModel):
    email: EmailStr
    password: str = Field('password', regex=password_regex)


class SUserLogin(BaseModel):
    email: EmailStr
    password: str

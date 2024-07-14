from pydantic import BaseModel, EmailStr, Field
from typing import List
from datetime import datetime


class UserSchema(BaseModel):
    id: int
    first_name: str | None = Field(None, max_length=40)
    last_name: str | None = Field(None, max_length=40)
    email: EmailStr
    city: str | None = Field(None, max_length=70)
    phone: str | None = Field(None, max_length=30)
    avatar: str | None = Field(None, max_length=255)
    is_superuser: bool = False
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class SignInRequest(BaseModel):
    email: EmailStr
    password: str


class SignUpRequest(BaseModel):
    first_name: str | None = Field(None, max_length=40)
    last_name: str | None = Field(None, max_length=40)
    email: EmailStr
    password1: str
    password2: str
    city: str | None = Field(None, max_length=70)
    phone: str | None = Field(None, max_length=30)
    avatar: str | None = Field(None, max_length=255)


class UserUpdateRequest(BaseModel):
    first_name: str | None = Field(None, max_length=40)
    last_name: str | None = Field(None, max_length=40)
    city: str | None = Field(None, max_length=70)
    phone: str | None = Field(None, max_length=30)
    avatar: str | None = Field(None, max_length=255)
    # is_superuser: bool | None = None
    # is_active: bool | None = None


class UsersListResponse(BaseModel):
    users: List[UserSchema]


class UserDetailResponse(BaseModel):
    user: UserSchema
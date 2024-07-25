from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.core.security import hash_password, is_password_strong_enough
from app.core.config import settings
from app.db.models import User
from app.schemas.user_schema import UserUpdateRequest, SignUpRequest, UserSchema
from app.db.postgres_session import get_session


async def user_by_id(user_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"user": UserSchema.model_validate(user)}


async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Users do not exist")
    users_for_return = [UserSchema.model_validate(user) for user in users]
    return {"users": users_for_return}


async def create_user(session: AsyncSession, user: SignUpRequest) -> User:
    
    if user.password1 != user.password2:
        raise HTTPException(status_code=400, detail="The password don't match")
    
    user_exist = await session.execute(select(User).filter(User.email == user.email))

    if user_exist.scalars().first():
        raise HTTPException(status_code=400, detail="Email is already exists.")

    if not await is_password_strong_enough(user.password1):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is not strong enough",
        )
    hashed_password = hash_password(user.password1)
    user_data = User()
    user_data.email = user.email
    user_data.hashed_password = hashed_password
    user_data.first_name = user.first_name
    user_data.last_name = user.last_name
    user_data.city = user.city
    user_data.phone = user.phone
    user_data.avatar = user.avatar
    session.add(user_data)
    await session.commit()
    await session.refresh(user_data)
    return {"user": UserSchema.model_validate(user_data)}


async def update_user(user_id: int, user_update: UserUpdateRequest, session: AsyncSession):
    result = await session.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    
    await session.commit()
    await session.refresh(user)
    return {"user": UserSchema.model_validate(user)}

    

async def delete_user(user_id: int, session: AsyncSession):
    result = await session.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    await session.delete(user)
    await session.commit()
    return "User deleted"
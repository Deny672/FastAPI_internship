from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.core.security import hash_password, is_password_strong_enough
from app.core.config import settings
from app.db.models import User
from app.schemas.user_schema import UserDetailResponse, UsersListResponse, UserUpdateRequest, SignUpRequest, SignInRequest, UserSchema
from app.db.postgres_session import get_session


async def user_by_id(user_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
    return users


async def create_user(session: AsyncSession, user: SignUpRequest) -> User:
    user_exist = session.execute(select(User).filter(User.email == user.email).first())
    if user_exist:
        raise HTTPException(status_code=400, detail="Email is already exists.")

    if not await is_password_strong_enough(user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is not strong enough",
        )

    hashed_password = await hash_password(user.password)
    user_data = user.model_dump()
    user_data['password'] = hashed_password
    db_user = User(**user_data)
    session.add(db_user)
    session.commit()
    return db_user


async def update_user(session: AsyncSession, id: int, user: UserUpdateRequest) -> User:
    db_user = await user_by_id(session, id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    for k, v in user.model_dump(exclude_unset=True).items():
        setattr(db_user, k, v)

    try:
        await session.commit()
        await session.refresh(db_user)
        return db_user
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="Updated user collides with other users",
        )
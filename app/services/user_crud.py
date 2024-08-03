from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.core.security import hash_password, is_password_strong_enough
from app.db.models import User
from app.schemas.user_schema import UserUpdateRequest, SignUpRequest, UserDetailResponse


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

file_handler = logging.FileHandler('app_logs.log')
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


async def user_by_id(user_id: int, session: AsyncSession):
    logger.info(f"Fetching user by id: {user_id}")
    result = await session.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if user is None:
        logger.warning(f"User not found: {user_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    logger.info(f"User fetched successfully: {user_id}")
    return UserDetailResponse.model_validate(user)


async def get_users(limit: int, offset: int, session: AsyncSession):
    offset *=limit
    logger.info(f"Fetching users with limit: {limit}, offset: {offset}")
    result = await session.execute(select(User).order_by(User.id).offset(offset).limit(limit))
    users = result.scalars().all()
    if not users:
        logger.warning("Users not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Users do not exist")
    users_for_return = [UserDetailResponse.model_validate(user) for user in users]
    logger.info("Users fetched successfully")
    return users_for_return


async def create_user(session: AsyncSession, user: SignUpRequest) -> User:
    logger.info(f"Creating user: {user.email}")
    if user.password1 != user.password2:
        logger.warning("Password mismatch")
        raise HTTPException(status_code=400, detail="The password don't match")
    
    user_exist = await session.execute(select(User).filter(User.email == user.email))

    if user_exist.scalars().first():
        logger.warning("Email already exists")
        raise HTTPException(status_code=400, detail="Email is already exists.")

    if not await is_password_strong_enough(user.password1):
        logger.warning("Password not strong enough")
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
    logger.info(f"User created successfully: {user_data.email}")
    return UserDetailResponse.model_validate(user_data)


async def update_user(user_id: int, user_update: UserUpdateRequest, session: AsyncSession):
    logger.info(f"Updating user: {user_id}")
    result = await session.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    
    if user is None:
        logger.warning(f"User not found: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    
    await session.commit()
    await session.refresh(user)
    logger.info(f"User updated successfully: {user_id}")
    return UserDetailResponse.model_validate(user)


async def delete_user(user_id: int, session: AsyncSession):
    logger.info(f"Deleting user: {user_id}")
    result = await session.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    
    if user is None:
        logger.warning(f"User not found: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    
    await session.delete(user)
    await session.commit()
    logger.info(f"User deleted successfully: {user_id}")
    return user
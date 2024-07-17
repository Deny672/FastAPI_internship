
from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.db.models import User

from app.services.user_crud import user_by_id, create_user, get_users, update_user
from app.schemas.user_schema import UserDetailResponse, UsersListResponse, UserUpdateRequest, SignUpRequest, SignInRequest, UserSchema
from app.db.postgres_session import get_session


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}/", response_model=UserDetailResponse, status_code = status.HTTP_200_OK)
async def user_by_id_route(user_id: int, session: AsyncSession = Depends(get_session)):
    return await user_by_id(user_id=user_id, session=session)


@router.get("/all", response_model=UsersListResponse)
async def get_all_users_route(session: AsyncSession = Depends(get_session)):
    return await get_users(session = session)


@router.post("/", response_model=UserDetailResponse)
async def create_user_route(user_create: SignUpRequest, session: AsyncSession = Depends(get_session)):
    return await create_user(session=session, user=user_create)


@router.patch("/{id}", response_model=UserDetailResponse)
async def update_user_route(
    id: int, data: UserUpdateRequest, session: AsyncSession = Depends(get_session)):
    return await update_user(session=session, id=id, user=data)
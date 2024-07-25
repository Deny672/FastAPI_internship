
from fastapi import FastAPI, HTTPException, Depends, status, APIRouter, Query
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.db.models import User

from app.services.user_crud import user_by_id, create_user, get_users, update_user, delete_user
from app.schemas.user_schema import UserDetailResponse, UsersListResponse, UserUpdateRequest, SignUpRequest, SignInRequest, UserSchema
from app.db.postgres_session import get_session


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}/", response_model=UserDetailResponse, status_code = status.HTTP_200_OK)
async def user_by_id_route(user_id: int, session: AsyncSession = Depends(get_session)):
    return await user_by_id(user_id=user_id, session=session)


@router.get("/all", response_model=UsersListResponse)
async def get_all_users_route(
    limit: int = Query(default=3, ge=1),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_session)):
    return await get_users(limit=limit, offset=offset, session = session)


@router.post("/", response_model=UserDetailResponse)
async def create_user_route(user_create: SignUpRequest, session: AsyncSession = Depends(get_session)):
    return await create_user(session=session, user=user_create)


@router.put("/{user_id}", response_model=UserDetailResponse)
async def update_user_route(user_id: int, new_data: UserUpdateRequest, session: AsyncSession = Depends(get_session)):
    return await update_user(user_id, session=session, user_update=new_data)


@router.delete("/{user_id}")
async def delete_user_route(user_id: int, session: AsyncSession = Depends(get_session)):
    return await delete_user(user_id, session)
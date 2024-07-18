from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import redis.asyncio as aioredis

from app.db.postgres_session import get_session
from app.db.redis_session import get_redis


router = APIRouter(prefix="/healthcheck", tags=["healthcheck"])


@router.get("/")
async def health_check():
    output = {
        "status_code": 200,
        "detail": "ok",
        "result": "working"
    }
    return output

@router.get("/postgres")
async def postgres_health_check(session: AsyncSession = Depends(get_session)):
    await session.execute(select(1))
    return {
        "status_code": 200,
        "detail": "ok",
        "result": "postgres working"
    }

@router.get("/redis")
async def healthcheck_redis(redis_client: aioredis.Redis = Depends(get_redis)):
    await redis_client.ping()
    return {
        "status_code": 200,
        "detail": "ok",
        "result": "redis working"
    }
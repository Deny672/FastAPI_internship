from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
import redis.asyncio as aioredis
from redis.exceptions import ConnectionError


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
async def redis_health_check(redis_pool: aioredis.Redis = Depends(get_redis)):
    redis = await get_redis().__anext__()
    try:
        await redis_pool.ping()
        output = {
            "status_code": 200,
            "detail": "ok",
            "result": "Redis working"
        }
        return output
    except ConnectionError:
        return {"status_code": 500,
            "detail": "None",
            "result": "Connection to redis was not succsessfull"}
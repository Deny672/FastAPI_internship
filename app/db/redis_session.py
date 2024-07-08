import redis.asyncio as redis
from fastapi import Depends
from app.core.config import settings


async def get_redis():
    redis_client = redis.from_url(settings.REDIS_URL)
    try:
        yield redis_client
    finally:
        await redis_client.aclose()
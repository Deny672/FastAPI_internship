import redis.asyncio as redis
from fastapi import Depends
from app.core.config import settings

REDIS_URL = f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}'

async def get_redis():
    redis_client = redis.from_url(REDIS_URL)
    try:
        yield redis_client
    finally:
        await redis_client.aclose()
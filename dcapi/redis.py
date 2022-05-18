# -*- coding: utf-8 -*-
from aioredis import ConnectionPool, Redis
from typing import Union
from .settings import settings


def get_redis_pool() -> Union[ConnectionPool, Redis]:
    pool = ConnectionPool.from_url(
        f'redis://:{settings.redis_pass}@{settings.redis_host}:',
        encoding="utf-8", decode_responses=True
    )

    redis = Redis(connection_pool=pool)

    return pool, redis

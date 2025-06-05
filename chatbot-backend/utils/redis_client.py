import redis.asyncio as redis
from core.config import settings

redis_client = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    db=settings.redis_db,
    password=settings.redis_password,
    decode_responses=True, # redis는 기본적으로 바이트로 데이터를 주고받기 때문에 문자열로 디코딩 해줌
)
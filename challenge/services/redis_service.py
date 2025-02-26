import hashlib
import json

from challenge.redis.redis_client import get_redis_connection
from challenge.schemas.templates import RequestTemplate
from challenge.settings import Settings

settings = Settings()

redis_client = get_redis_connection(redis_host=settings.REDIS_HOST, redis_port=settings.REDIS_PORT)


def generate_request_key(data: RequestTemplate):
    request_dicts = [item.dict() for item in data]
    request_str = json.dumps(request_dicts, sort_keys=True)
    return hashlib.md5(request_str.encode()).hexdigest()


def get_cached_prediction(key: str):
    cached_result = redis_client.get(key)
    return json.loads(cached_result) if cached_result else None


def cache_prediction(key: str, result):
    redis_client.set(key, json.dumps(result))

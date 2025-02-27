import redis


def get_redis_connection(redis_host: str, redis_port: int, db=0):
    return redis.Redis(host=redis_host, port=redis_port, db=db, decode_responses=True)

import redis 
import json 
from app.config import settings

r = redis.from_url(settings.REDIS_URL)

def get_cache(key:str):
    data = r.get(key)
    if data:
        return json.loads(data)
    return None

def set_cache(key:str,value,ttl: int=60):
    r.setex(key,ttl,json.dumps(value))

def invalidate_user_tasks_cache(user_id: int):
    pattern = f"tasks:{user_id}:*"
    cursor = 0
    while True:
        cursor, keys = r.scan(cursor, match=pattern, count=100)
        if keys:
            r.delete(*keys)
        if cursor == 0:
            break
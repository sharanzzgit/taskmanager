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
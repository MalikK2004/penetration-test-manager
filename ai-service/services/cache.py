import os
import json
import redis
import hashlib

class CacheService:
    def __init__(self):
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        try:
            self.redis_client = redis.from_url(redis_url)
            self.enabled = True
        except Exception:
            self.enabled = False

    def get_cache_key(self, endpoint, payload):
        payload_str = json.dumps(payload, sort_keys=True)
        return f"{endpoint}:{hashlib.sha256(payload_str.encode()).hexdigest()}"

    def get(self, key):
        if not self.enabled: return None
        try:
            cached = self.redis_client.get(key)
            return json.loads(cached) if cached else None
        except Exception:
            return None

    def set(self, key, value, ttl=3600):
        if not self.enabled: return
        try:
            self.redis_client.setex(key, ttl, json.dumps(value))
        except Exception:
            pass

cache_service = CacheService()

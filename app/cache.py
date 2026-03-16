import redis
import os
import hashlib
import json

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

_redis_client = None

def get_redis_client():
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
    return _redis_client

def make_cache_key(question: str, context: list = None) -> str:
    # Use question and context (if any) to make a unique key
    base = question
    if context:
        base += json.dumps(context, sort_keys=True)
    return "qa:" + hashlib.sha256(base.encode()).hexdigest()

def get_cached_answer(question: str, context: list = None):
    client = get_redis_client()
    key = make_cache_key(question, context)
    return client.get(key)

def set_cached_answer(question: str, answer: str, context: list = None, expire_seconds: int = 86400):
    client = get_redis_client()
    key = make_cache_key(question, context)
    client.set(key, answer, ex=expire_seconds)


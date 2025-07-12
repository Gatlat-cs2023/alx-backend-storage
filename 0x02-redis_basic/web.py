#!/usr/bin/env python3
import redis
import requests
from functools import wraps

cache = redis.Redis()

def count_calls(method):
    @wraps(method)
    def wrapper(url):
        key = f"count:{url}"
        cache.incr(key)
        return method(url)
    return wrapper

def cache_page(expire=10):
    def decorator(method):
        @wraps(method)
        def wrapper(url):
            cached = cache.get(url)
            if cached:
                return cached.decode('utf-8')
            result = method(url)
            cache.setex(url, expire, result)
            return result
        return wrapper
    return decorator

@count_calls
@cache_page(expire=10)
def get_page(url: str) -> str:
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://example.com"
    print(get_page(url))  # First time fetches and caches
    print(get_page(url))  # Second time returns cached instantly
    print(f"Access count: {cache.get(f'count:{url}').decode('utf-8')}")

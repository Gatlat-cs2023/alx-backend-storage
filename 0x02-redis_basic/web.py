#!/usr/bin/env python3
"""
Implements a web cache with expiration and access tracking
"""

import redis
import requests
from functools import wraps

# Create Redis client instance (localhost, default port)
redis_client = redis.Redis()

def count_access(method):
    """
    Decorator to count how many times a URL is accessed
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        count_key = f"count:{url}"
        redis_client.incr(count_key)
        return method(url)
    return wrapper

def cache_page(method):
    """
    Decorator to cache page content with 10 second expiration
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        cache_key = f"cache:{url}"
        cached = redis_client.get(cache_key)
        if cached:
            return cached.decode("utf-8")
        page = method(url)
        redis_client.setex(cache_key, 10, page)
        return page
    return wrapper

@count_access
@cache_page
def get_page(url: str) -> str:
    """
    Fetches HTML content of a URL and returns as string
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.text


if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://example.com"
    print(get_page(url))   # first time: slow, caches result
    print(get_page(url))   # second time within 10s: fast, from cache

#!/usr/bin/env python3
"""
Defines a Cache class for storing and retrieving typed data from Redis
"""
import redis
import uuid
from typing import Union, Callable, Optional


class Cache:
    def __init__(self):
        """Initialize Redis connection and flush the database"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis with a random UUID key
        Args:
            data: The data to store (can be str, bytes, int, float)
        Returns:
            The key as a string
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[bytes, str, int, float, None]:
        """
        Retrieve data from Redis and optionally apply a conversion function
        Args:
            key: The Redis key to fetch
            fn: Optional function to apply to the returned data
        Returns:
            The retrieved and possibly transformed data
        """
        data = self._redis.get(key)
        if data is None:
            return None
        return fn(data) if fn else data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve string data from Redis
        Args:
            key: Redis key
        Returns:
            Decoded string value or None
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve integer data from Redis
        Args:
            key: Redis key
        Returns:
            Integer value or None
        """
        return self.get(key, fn=int)

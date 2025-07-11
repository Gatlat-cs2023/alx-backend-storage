#!/usr/bin/env python3
"""
Defines a Cache class for storing data in Redis
"""
import redis
import uuid
from typing import Union


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

#!/usr/bin/env python3
"""
Defines a Cache class with a count_calls decorator to count method calls using Redis
"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps
from typing import Callable

def call_history(method: Callable) -> Callable:
    """
    Decorator to store history of inputs and outputs for a method
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"

        # Store the input arguments as a string
        self._redis.rpush(input_key, str(args))

        # Execute the original method and get the output
        output = method(self, *args, **kwargs)

        # Store the output
        self._redis.rpush(output_key, output)

        return output

    return wrapper

def count_calls(method: Callable) -> Callable:
    """
    Decorator to count how many times a method is called using Redis INCR
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    def __init__(self):
        """Initialize Redis connection and flush the database"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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

def replay(method: Callable):
    """
    Display the history of calls of a particular method.
    """
    redis_client = method.__self__._redis  # access Redis from instance (self)
    qualname = method.__qualname__

    input_key = f"{qualname}:inputs"
    output_key = f"{qualname}:outputs"

    # Get the number of calls
    calls = redis_client.get(qualname)
    calls = int(calls) if calls else 0

    print(f"{qualname} was called {calls} times:")

    # Get all inputs and outputs lists
    inputs = redis_client.lrange(input_key, 0, -1)
    outputs = redis_client.lrange(output_key, 0, -1)

    for inp, outp in zip(inputs, outputs):
        print(f"{qualname}(*{inp.decode('utf-8')}) -> {outp.decode('utf-8')}")

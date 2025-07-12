#!/usr/bin/env python3
"""
Test file for Task 2: count_calls decorator
"""
Cache = __import__('exercise').Cache

cache = Cache()

cache.store(b"first")
print(cache.get(cache.store.__qualname__))  # Expect b'1'

cache.store(b"second")
cache.store(b"third")
print(cache.get(cache.store.__qualname__))  # Expect b'3'

#!/usr/bin/env python3
"""
Main file to test Cache and replay function
"""

Cache = __import__('exercise').Cache
replay = __import__('exercise').replay

cache = Cache()

# Store some values
key1 = cache.store("foo")
print(key1)

key2 = cache.store("bar")
print(key2)

key3 = cache.store(42)
print(key3)

# Replay history of calls to cache.store
replay(cache.store)

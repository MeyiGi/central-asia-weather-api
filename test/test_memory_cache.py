from app.infrastructure.cache.in_memory_cache import InMemoryLRUCache
from pytest import fixture

@fixture
def cache():
    return InMemoryLRUCache()

def test_cache_with_value(cache):
    cache.set("my_key", b"hello")
    assert cache.get("my_key") == b"hello"

def test_cache_not_exist(cache):
    assert cache.get("non_existing_value") is None

def test_clear(cache):
    cache.set("key", "value")
    cache.clear()
    assert cache.get("key") is None

def test_remove_old():
    cache = InMemoryLRUCache(max_size=2)
    cache.set("a", 1)
    cache.set("b", 2)
    cache.set("c", 3)
    assert cache.get("a") is None
    assert cache.get("c") == 3
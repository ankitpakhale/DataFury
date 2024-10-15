from typing import Any
import diskcache as dc


class CacheManager:
    """
    CacheManager handles caching operations using a dictionary for now.
    """

    # diskcache configurations
    cache_store = dc.Cache("mycache")

    @staticmethod
    def get(key: str) -> Any:
        """
        get value from cache by key
        """
        return CacheManager.cache_store.get(key)

    @staticmethod
    def set(key: str, value: Any) -> None:
        """
        set value in cache by key
        """
        CacheManager.cache_store[key] = value

    @staticmethod
    def has(key: str) -> bool:
        """
        check if key exists in cache
        """
        return key in CacheManager.cache_store


# object of cache_manager
cache_manager = CacheManager()

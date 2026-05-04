import time
from collections import OrderedDict
from typing import Callable, Any


def make_key(args: tuple, kwargs: dict) -> str:
    return str(args) + str(sorted(kwargs.items()))


class LRUCache:
    def __init__(self, max_size: int):
        self.max_size = max_size
        self._cache: OrderedDict[str, Any] = OrderedDict()

    def get(self, key: str) -> tuple[bool, Any]:
        if key not in self._cache:
            return False, None
        self._cache.move_to_end(key)
        return True, self._cache[key]

    def set(self, key: str, value: Any) -> None:
        if key in self._cache:
            self._cache.move_to_end(key)
        else:
            if len(self._cache) >= self.max_size:
                self._cache.popitem(last=False)
            self._cache[key] = value

    def __len__(self) -> int:
        return len(self._cache)
class LFUCache:
    def __init__(self, max_size: int):
        self.max_size = max_size
        self._cache: dict[str, Any] = {}
        self._freq: dict[str, int] = {}

    def get(self, key: str) -> tuple[bool, Any]:
        if key not in self._cache:
            return False, None
        self._freq[key] += 1
        return True, self._cache[key]

    def set(self, key: str, value: Any) -> None:
        if key in self._cache:
            self._freq[key] += 1
        else:
            if len(self._cache) >= self.max_size:
                lfu_key = min(self._freq, key=lambda k: self._freq[k])
                del self._cache[lfu_key]
                del self._freq[lfu_key]
            self._cache[key] = value
            self._freq[key] = 1

    def __len__(self) -> int:
        return len(self._cache)


class TTLCache:
    def __init__(self, ttl_seconds: float):
        self.ttl = ttl_seconds
        self._cache: dict[str, Any] = {}
        self._timestamps: dict[str, float] = {}

    def get(self, key: str) -> tuple[bool, Any]:
        if key not in self._cache:
            return False, None
        if time.monotonic() - self._timestamps[key] > self.ttl:
            del self._cache[key]
            del self._timestamps[key]
            return False, None
        return True, self._cache[key]

    def set(self, key: str, value: Any) -> None:
        self._cache[key] = value
        self._timestamps[key] = time.monotonic()

    def __len__(self) -> int:
        return len(self._cache)
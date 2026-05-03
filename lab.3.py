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

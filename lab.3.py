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
def memoize(
    fn: Callable,
    max_size: int | None = None,
    policy: str = "lru",
    ttl: float | None = None,
    custom_evict: Callable | None = None,
) -> Callable:
    if custom_evict is not None:
        cache: dict[str, Any] = {}

        def wrapper(*args, **kwargs):
            key = make_key(args, kwargs)
            if key in cache:
                return cache[key]
            result = fn(*args, **kwargs)
            if len(cache) >= (max_size or float("inf")):
                evict_key = custom_evict(cache)
                if evict_key is not None:
                    del cache[evict_key]
            cache[key] = result
            return result

        return wrapper

    if ttl is not None:
        store = TTLCache(ttl_seconds=ttl)
    elif max_size is not None and policy == "lfu":
        store = LFUCache(max_size=max_size)
    else:
        store = LRUCache(max_size=max_size or float("inf"))

    def wrapper(*args, **kwargs):
        key = make_key(args, kwargs)
        hit, value = store.get(key)
        if hit:
            return value
        result = fn(*args, **kwargs)
        store.set(key, result)
        return result

    return wrapper
def demo_lru():
    call_count = 0

    def slow_square(n: int) -> int:
        nonlocal call_count
        call_count += 1
        return n * n

    memoized = memoize(slow_square, max_size=3, policy="lru")

    print("--- LRU demo ---")
    for n in [2, 3, 4, 2, 3, 5, 2]:
        print(f"square({n}) = {memoized(n)}")
    print(f"Actual calls to slow_square: {call_count}")


def demo_lfu():
    call_count = 0

    def slow_double(n: int) -> int:
        nonlocal call_count
        call_count += 1
        return n * 2

    memoized = memoize(slow_double, max_size=2, policy="lfu")

    print("\n--- LFU demo ---")
    for n in [1, 2, 1, 3, 2, 1]:
        print(f"double({n}) = {memoized(n)}")
    print(f"Actual calls to slow_double: {call_count}")


def demo_ttl():
    call_count = 0

    def slow_add(a: int, b: int) -> int:
        nonlocal call_count
        call_count += 1
        return a + b

    memoized = memoize(slow_add, ttl=0.5)

    print("\n--- TTL demo ---")
    print(f"add(1, 2) = {memoized(1, 2)}")
    print(f"add(1, 2) = {memoized(1, 2)} (cached)")
    time.sleep(0.6)
    print(f"add(1, 2) = {memoized(1, 2)} (expired, recomputed)")
    print(f"Actual calls to slow_add: {call_count}")


def demo_custom():
    call_count = 0

    def slow_mod(n: int) -> int:
        nonlocal call_count
        call_count += 1
        return n % 7

    def evict_first(cache: dict) -> str:
        return next(iter(cache))

    memoized = memoize(slow_mod, max_size=2, custom_evict=evict_first)

    print("\n--- Custom eviction demo ---")
    for n in [10, 20, 10, 30, 20]:
        print(f"mod({n}) = {memoized(n)}")
    print(f"Actual calls to slow_mod: {call_count}")


if __name__ == "__main__":
    demo_lru()
    demo_lfu()
    demo_ttl()
    demo_custom()
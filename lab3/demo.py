import time
import runpy

_module = runpy.run_path("lab3.py")

memoize = _module["memoize"]


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
import random
import time


def random_number_generator():
    while True:
        yield random.randint(1, 100)


def timeout_iterator(iterator, duration: float) -> None:
    start = time.time()
    total = 0
    count = 0

    while time.time() - start < duration:
        num = next(iterator)
        count += 1
        total += num
        avg = total / count
        print(f"Value: {num}, Total: {total}, Avg: {avg:.2f}")
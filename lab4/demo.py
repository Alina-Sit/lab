import runpy

_module = runpy.run_path("lab.4.py")
BiDirectionalPriorityQueue = _module["BiDirectionalPriorityQueue"]


def demo_priority():
    q = BiDirectionalPriorityQueue()
    q.enqueue("low task", 1)
    q.enqueue("high task", 10)
    q.enqueue("mid task", 5)

    print(" Priority demo ")
    print("peek highest:", q.peek("highest"))
    print("dequeue highest:", q.dequeue("highest"))
    print("peek lowest:", q.peek("lowest"))
    print("dequeue lowest:", q.dequeue("lowest"))


def demo_insertion_order():
    q = BiDirectionalPriorityQueue()
    q.enqueue("first", 3)
    q.enqueue("second", 3)
    q.enqueue("third", 3)

    print("\n--- Insertion order demo ---")
    print("peek oldest:", q.peek("oldest"))
    print("peek newest:", q.peek("newest"))
    print("dequeue oldest (FIFO):", q.dequeue("oldest"))
    print("dequeue newest (LIFO):", q.dequeue("newest"))


def demo_monotonic_counter():
    q = BiDirectionalPriorityQueue()
    for i in range(5):
        q.enqueue(f"item-{i}", priority=1)

    print("\n--- Monotonic counter (stable FIFO) ---")
    while not q.is_empty():
        print("dequeue oldest:", q.dequeue("oldest"))


if __name__ == "__main__":
    demo_priority()
    demo_insertion_order()
    demo_monotonic_counter()
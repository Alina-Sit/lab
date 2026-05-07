class BiDirectionalPriorityQueue:
    def __init__(self):
        self._items: list[dict] = []
        self._counter: int = 0

    def enqueue(self, item, priority: int | float) -> None:
        self._items.append({
            "item": item,
            "priority": priority,
            "index": self._counter,
        })
        self._counter += 1

    def __len__(self) -> int:
        return len(self._items)

    def is_empty(self) -> bool:
        return len(self._items) == 0
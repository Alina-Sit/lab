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

    def peek(self, mode: str = "highest"):
        if self.is_empty():
            return None
        if mode == "highest":
            return max(self._items, key=lambda x: x["priority"])["item"]
        if mode == "lowest":
            return min(self._items, key=lambda x: x["priority"])["item"]
        if mode == "oldest":
            return self._items[0]["item"]
        if mode == "newest":
            return self._items[-1]["item"]
        raise ValueError(f"Unknown mode: {mode}")

    def dequeue(self, mode: str = "highest"):
        if self.is_empty():
            return None
        if mode == "highest":
            idx = max(range(len(self._items)), key=lambda i: self._items[i]["priority"])
            return self._items.pop(idx)["item"]
        if mode == "lowest":
            idx = min(range(len(self._items)), key=lambda i: self._items[i]["priority"])
            return self._items.pop(idx)["item"]
        if mode == "oldest":
            return self._items.pop(0)["item"]
        if mode == "newest":
            return self._items.pop()["item"]
        raise ValueError(f"Unknown mode: {mode}")

    def __len__(self) -> int:
        return len(self._items)

    def is_empty(self) -> bool:
        return len(self._items) == 0
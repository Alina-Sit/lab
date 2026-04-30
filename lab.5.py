import asyncio
import threading
import time
from typing import TypeVar, Callable, Any

T = TypeVar("T")
R = TypeVar("R")


def async_map_callback(
    array: list[T],
    async_fn: Callable[[T, Callable[[Exception | None, R | None], None]], None],
    callback: Callable[[Exception | None, list[R] | None], None],
    cancel_event: threading.Event | None = None,
) -> None:
    if not array:
        return callback(None, [])
    if cancel_event and cancel_event.is_set():
        return callback(Exception("Cancelled"), None)

    results: list[Any] = [None] * len(array)
    lock = threading.Lock()
    state = {"completed": 0, "done": False}

    def done(index: int, err: Exception | None, result: R | None) -> None:
        with lock:
            if state["done"]:
                return
            if cancel_event and cancel_event.is_set():
                state["done"] = True
                callback(Exception("Cancelled"), None)
                return
            if err:
                state["done"] = True
                callback(err, None)
                return
            results[index] = result
            state["completed"] += 1
            if state["completed"] == len(array):
                state["done"] = True
                callback(None, results)

    def run(index: int, item: T) -> None:
        if cancel_event and cancel_event.is_set():
            done(index, Exception("Cancelled"), None)
            return
        async_fn(item, lambda err, res: done(index, err, res))

    for i, item in enumerate(array):
        threading.Thread(target=run, args=(i, item), daemon=True).start()


async def async_map_promise(
    array: list[T],
    async_fn: Callable[[T], "asyncio.Future[R]"],
    cancel_event: asyncio.Event | None = None,
) -> list[R]:
    if cancel_event and cancel_event.is_set():
        raise asyncio.CancelledError("Cancelled")

    async def guarded(item: T) -> R:
        task = asyncio.ensure_future(async_fn(item))
        if cancel_event is None:
            return await task
        cancel_task = asyncio.ensure_future(cancel_event.wait())
        done, pending = await asyncio.wait(
            [task, cancel_task], return_when=asyncio.FIRST_COMPLETED
        )
        for p in pending:
            p.cancel()
        if cancel_task in done:
            raise asyncio.CancelledError("Cancelled")
        return task.result()

    return await asyncio.gather(*[guarded(item) for item in array])


async def async_map_await(
    array: list[T],
    async_fn: Callable[[T], "asyncio.Future[R]"],
    cancel_event: asyncio.Event | None = None,
) -> list[R]:
    if cancel_event and cancel_event.is_set():
        raise asyncio.CancelledError("Cancelled")

    results: list[R] = []
    for item in array:
        if cancel_event and cancel_event.is_set():
            raise asyncio.CancelledError("Cancelled")
        results.append(await async_fn(item))
    return results


def fake_api_callback(item: int, done) -> None:
    def work():
        time.sleep(0.1)
        done(None, item * 2)
    threading.Thread(target=work, daemon=True).start()


async def fake_api(item: int) -> int:
    await asyncio.sleep(0.1)
    return item * 2


INPUT = [1, 2, 3, 4, 5]


def demo_callback() -> None:
    finished = threading.Event()

    def on_result(err, res):
        if err:
            print("Callback error:", err)
        else:
            print("Callback result:", res)
        finished.set()

    async_map_callback(INPUT, fake_api_callback, on_result)
    finished.wait()


async def demo_await() -> None:
    result = await async_map_await(INPUT, fake_api)
    print("Await result:", result)


async def demo_await_cancel() -> None:
    cancel = asyncio.Event()
    asyncio.get_event_loop().call_later(0.25, cancel.set)
    try:
        result = await async_map_await(INPUT, fake_api, cancel)
        print("Await result:", result)
    except asyncio.CancelledError as e:
        print("Await cancelled:", e)


async def demo_promise() -> None:
    result = await async_map_promise(INPUT, fake_api)
    print("Promise result:", result)


async def demo_promise_cancel() -> None:
    cancel = asyncio.Event()
    asyncio.get_event_loop().call_later(0.15, cancel.set)
    try:
        result = await async_map_promise(INPUT, fake_api, cancel)
        print("Promise result:", result)
    except asyncio.CancelledError as e:
        print("Promise cancelled:", e)


if __name__ == "__main__":
    demo_callback()
    asyncio.run(demo_await())
    asyncio.run(demo_await_cancel())
    asyncio.run(demo_promise())
    asyncio.run(demo_promise_cancel())
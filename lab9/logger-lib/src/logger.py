import time
import json
import asyncio
import datetime


LEVELS = {"DEBUG": 0, "INFO": 1, "ERROR": 2}


def _format_text(level, func_name, args, kwargs, result=None, error=None, duration=None):
    ts = datetime.datetime.now().isoformat()
    msg = f"[{ts}] [{level}] {func_name} | args={args} kwargs={kwargs}"
    if duration is not None:
        msg += f" | time={duration:.4f}s"
    if error:
        msg += f" | error={error}"
    else:
        msg += f" | result={result}"
    return msg


def _format_json(level, func_name, args, kwargs, result=None, error=None, duration=None):
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "level": level,
        "function": func_name,
        "args": str(args),
        "kwargs": str(kwargs),
        "duration": duration,
    }
    if error:
        entry["error"] = str(error)
    else:
        entry["result"] = str(result)
    return json.dumps(entry)


def _write(output, message):
    if output == "console":
        print(message)
    elif isinstance(output, str):
        with open(output, "a") as f:
            f.write(message + "\n")


def log(level="INFO", output="console", min_level="DEBUG", fmt="text"):
    def decorator(func):
        if asyncio.iscoroutinefunction(func):
            async def async_wrapper(*args, **kwargs):
                if LEVELS.get(level, 0) < LEVELS.get(min_level, 0):
                    return await func(*args, **kwargs)
                start = time.time()
                try:
                    result = await func(*args, **kwargs)
                    duration = time.time() - start
                    if fmt == "json":
                        msg = _format_json(level, func.__name__, args, kwargs, result=result, duration=duration)
                    else:
                        msg = _format_text(level, func.__name__, args, kwargs, result=result, duration=duration)
                    _write(output, msg)
                    return result
                except Exception as e:
                    duration = time.time() - start
                    if fmt == "json":
                        msg = _format_json("ERROR", func.__name__, args, kwargs, error=e, duration=duration)
                    else:
                        msg = _format_text("ERROR", func.__name__, args, kwargs, error=e, duration=duration)
                    _write(output, msg)
                    raise
            return async_wrapper
        else:
            def sync_wrapper(*args, **kwargs):
                if LEVELS.get(level, 0) < LEVELS.get(min_level, 0):
                    return func(*args, **kwargs)
                start = time.time()
                try:
                    result = func(*args, **kwargs)
                    duration = time.time() - start
                    if fmt == "json":
                        msg = _format_json(level, func.__name__, args, kwargs, result=result, duration=duration)
                    else:
                        msg = _format_text(level, func.__name__, args, kwargs, result=result, duration=duration)
                    _write(output, msg)
                    return result
                except Exception as e:
                    duration = time.time() - start
                    if fmt == "json":
                        msg = _format_json("ERROR", func.__name__, args, kwargs, error=e, duration=duration)
                    else:
                        msg = _format_text("ERROR", func.__name__, args, kwargs, error=e, duration=duration)
                    _write(output, msg)
                    raise
            return sync_wrapper
    return decorator
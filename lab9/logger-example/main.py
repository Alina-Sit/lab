import sys
import asyncio
sys.path.append("../logger-lib")

from src.logger import log

# INFO в консоль
@log(level="INFO")
def add(a, b):
    return a + b

# DEBUG в файл
@log(level="DEBUG", output="debug.log", fmt="text")
def multiply(a, b):
    return a * b

# ERROR — логує тільки коли виняток
@log(level="ERROR")
def divide(a, b):
    return a / b

# JSON формат
@log(level="INFO", fmt="json")
def subtract(a, b):
    return a - b

# async функція
@log(level="INFO")
async def fetch_data(url):
    await asyncio.sleep(0.1)
    return f"data from {url}"


print(add(3, 4))
print(multiply(5, 6))

try:
    divide(10, 0)
except ZeroDivisionError:
    pass

print(subtract(10, 3))
asyncio.run(fetch_data("https://example.com"))
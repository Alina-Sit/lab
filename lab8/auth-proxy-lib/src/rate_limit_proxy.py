import time

class RateLimitProxy:
    def __init__(self, client, max_calls, period):
        self.client = client
        self.max_calls = max_calls
        self.period = period
        self.calls = []

    def request(self, method, url, headers=None, body=None):
        now = time.time()
        self.calls = [t for t in self.calls if now - t < self.period]

        if len(self.calls) >= self.max_calls:
            wait = self.period - (now - self.calls[0])
            print(f"Rate limit reached, waiting {wait:.1f}s")
            time.sleep(wait)

        self.calls.append(time.time())
        return self.client.request(method, url, headers, body)
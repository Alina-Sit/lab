import datetime

class LoggingProxy:
    def __init__(self, client):
        self.client = client

    def request(self, method, url, headers=None, body=None):
        print(f"[{datetime.datetime.now()}] {method} {url}")
        response = self.client.request(method, url, headers, body)
        print(f"[{datetime.datetime.now()}] status: {response['status']}")
        return response
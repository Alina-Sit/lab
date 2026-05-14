import time

class ApiKeyAuth:
    def __init__(self, client, api_key):
        self.client = client
        self.api_key = api_key

    def request(self, method, url, headers=None, body=None):
        headers = headers or {}
        headers["X-API-Key"] = self.api_key
        return self.client.request(method, url, headers, body)


class JWTAuth:
    def __init__(self, client, token):
        self.client = client
        self.token = token

    def request(self, method, url, headers=None, body=None):
        headers = headers or {}
        headers["Authorization"] = f"Bearer {self.token}"
        response = self.client.request(method, url, headers, body)

        if response["status"] == 401:
            self.token = self._refresh()
            headers["Authorization"] = f"Bearer {self.token}"
            return self.client.request(method, url, headers, body)

        return response

    def _refresh(self):
        # в реальному проекті тут був би запит на refresh endpoint
        return self.token


class OAuthProxy:
    def __init__(self, client, token):
        self.client = client
        self.token = token

    def request(self, method, url, headers=None, body=None):
        headers = headers or {}
        headers["Authorization"] = f"OAuth {self.token}"
        return self.client.request(method, url, headers, body)
import urllib.request
import json

class BaseClient:
    def request(self, method, url, headers=None, body=None):
        headers = headers or {}
        data = json.dumps(body).encode() if body else None
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req) as resp:
                return {
                    "status": resp.status,
                    "body": resp.read().decode()
                }
        except urllib.error.HTTPError as e:
            return {
                "status": e.code,
                "body": e.read().decode()
            }
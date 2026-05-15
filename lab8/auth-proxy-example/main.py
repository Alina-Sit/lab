import sys
import os
sys.path.append("../auth-proxy-lib")

from src.base_client import BaseClient
from src.auth_proxy import ApiKeyAuth, JWTAuth, OAuthProxy
from src.logging_proxy import LoggingProxy
from src.rate_limit_proxy import RateLimitProxy

api_key = os.getenv("API_KEY", "test-key-123")
jwt_token = os.getenv("JWT_TOKEN", "test-token-abc")

base = BaseClient()

# API Key + logging
client = LoggingProxy(ApiKeyAuth(base, api_key))
response = client.request("GET", "https://httpbin.org/get")
print(response["status"])

# JWT + rate limit + logging
client2 = LoggingProxy(RateLimitProxy(JWTAuth(base, jwt_token), max_calls=3, period=10))
response2 = client2.request("GET", "https://httpbin.org/bearer")
print(response2["status"])

# OAuth
client3 = OAuthProxy(base, "oauth-token-xyz")
response3 = client3.request("GET", "https://httpbin.org/get")
print(response3["status"])
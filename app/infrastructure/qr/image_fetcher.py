import requests
from typing import Tuple


class ImageHTTPFetcher:
    def __init__(self, timeout: float = 5.0):
        self.timeout = timeout

    def fetch(self, url: str) -> Tuple[bytes, str]:
        r = requests.get(url, timeout=self.timeout, stream=True)
        r.raise_for_status()
        content_type = r.headers.get("Content-Type", "application/octet-stream")
        data = r.content
        return data, content_type

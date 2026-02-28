import requests
import logging
import time
from typing import Dict, Any, Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from core.exceptions import APIError, APITimeoutError, APIConnectionError

logger = logging.getLogger(__name__)


class APIClient:
    """
    A unified API client to interact with the backend services.
    It wraps the standard requests library with logging, default headers,
    configurable timeouts, and automatic retry logic for transient failures.
    """
    def __init__(self, base_url: str, timeout: int = 10, max_retries: int = 3):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()

        # Ensure we ask for JSON responses
        self.session.headers.update({"Accept": "application/json"})

        # Configure retry strategy for transient failures (5xx, connection errors)
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        logger.info(f"API Request: {method} {url}")

        if 'params' in kwargs and kwargs['params']:
            logger.info(f"Query params: {kwargs['params']}")
        if 'json' in kwargs and kwargs['json']:
            logger.info(f"JSON body: {kwargs['json']}")

        # Apply default timeout if not explicitly provided by the caller
        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout

        start_time = time.time()

        try:
            response = self.session.request(method, url, **kwargs)
        except requests.exceptions.Timeout as exc:
            raise APITimeoutError(
                f"Request timed out after {self.timeout}s: {method} {url}"
            ) from exc
        except requests.exceptions.ConnectionError as exc:
            raise APIConnectionError(
                f"Failed to connect: {method} {url}"
            ) from exc

        elapsed_ms = (time.time() - start_time) * 1000
        logger.info(f"API Response Status: {response.status_code} ({elapsed_ms:.0f}ms)")

        try:
            logger.info(f"API Response Body: {response.json()}")
        except ValueError:
            logger.debug(f"API Response is not JSON. Text: {response.text}")

        return response

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        return self.request("GET", endpoint, params=params, **kwargs)

    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        return self.request("POST", endpoint, data=data, json=json, **kwargs)

    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        return self.request("PUT", endpoint, data=data, json=json, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request("DELETE", endpoint, **kwargs)

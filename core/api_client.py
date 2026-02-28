import requests
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class APIClient:
    """
    A unified API client to interact with the backend services. 
    It wraps the standard requests library with logging and default headers.
    """
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        # Ensure we ask for JSON responses
        self.session.headers.update({"Accept": "application/json"})

    def request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        logger.info(f"API Request: {method} {url}")
        
        if 'params' in kwargs and kwargs['params']:
            logger.info(f"Query params: {kwargs['params']}")
        if 'json' in kwargs and kwargs['json']:
            logger.info(f"JSON body: {kwargs['json']}")

        response = self.session.request(method, url, **kwargs)
        
        logger.info(f"API Response Status: {response.status_code}")
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

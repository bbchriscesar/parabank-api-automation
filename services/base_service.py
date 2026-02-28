"""
Base service class providing common functionality for all API service objects.
Implements the DRY principle by centralizing shared initialization logic.
"""
from core.api_client import APIClient


class BaseService:
    """
    Abstract base for all Service Objects (API Object Model pattern).
    Subclasses should set `endpoint` to their primary resource path.
    """
    endpoint: str = ""

    def __init__(self, api_client: APIClient):
        self.api_client = api_client

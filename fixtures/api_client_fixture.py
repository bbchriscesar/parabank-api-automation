import pytest
from core.api_client import APIClient
from config.settings import settings


@pytest.fixture(scope="session")
def api_client():
    """
    Session-scoped fixture to provide a configured API client.
    Passes TIMEOUT from settings for consistent request timeout enforcement.
    """
    client = APIClient(base_url=settings.BASE_URL, timeout=settings.TIMEOUT)
    yield client
    # Teardown logic
    client.session.close()
